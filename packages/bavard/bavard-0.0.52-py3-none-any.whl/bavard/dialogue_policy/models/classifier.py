import typing as t

import tensorflow as tf
from bavard_ml_common.mlops.serialization import Serializer
from tensorflow.keras.layers import Dense, TimeDistributed
import kerastuner as kt

from bavard.common.layers.attention_pooling import GlobalAttentionPooling1D
from bavard.common.serialization import KerasSerializer
from bavard.dialogue_policy.data.agent import Agent
from bavard.dialogue_policy.data.preprocessed_data import PreprocessedTrainingData
from bavard.dialogue_policy.data.conversations.conversation import Conversation
from bavard.dialogue_policy.models.base import BaseDPModel
from bavard.common.layers import TextEmbedder, model_bodies
from bavard.common.pydantics import StrPredWithConf
from bavard.dialogue_policy.constants import MAX_UTTERANCE_LEN


class Classifier(BaseDPModel):
    """Standard multinomial classifier predicting the next dialogue actions to take.
    """

    serializer = Serializer(KerasSerializer())

    def __init__(
        self,
        *,
        units: int = 512,
        num_blocks: int = 2,
        body: str = "encoder",
        l2: float = 0.0,
        epochs: int = 100,
        learning_rate: float = 1e-4,
        fine_tune_nlu_embedder: bool = False,
        batch_size: float = 32,
        dropout: float = 0.0,
        use_utterances: bool = False,
        predict_single: bool = True,  # also performs class balancing
        callbacks: list = None,
    ) -> None:
        # Control parameters
        self._fitted = False
        self._preprocessor = None
        self._model = None
        self._action_names = None
        self.callbacks = callbacks if callbacks else []

        # Tuning parameters
        self.units = units
        self.num_blocks = num_blocks
        assert body in model_bodies
        self.body = body
        self.l2 = l2
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.fine_tune_nlu_embedder = fine_tune_nlu_embedder
        self.batch_size = batch_size
        self.dropout = dropout
        self.use_utterances = use_utterances
        self.predict_single = predict_single

    @staticmethod
    def get_hp_spec(hp: kt.HyperParameters) -> t.Dict[str, kt.engine.hyperparameters.HyperParameter]:
        return {
            "units": hp.Int("units", 32, 512, default=512),
            "num_blocks": hp.Int("num_blocks", 1, 4),
            "body": hp.Choice("body", list(model_bodies.keys())),
            "l2": hp.Float("l2", 1e-12, 0.1, sampling="log"),
            "epochs": hp.Int("epochs", 5, 200, step=5, default=100),
            "learning_rate": hp.Float("learning_rate", 1e-3, 0.1, sampling="log", default=5e-5),
            "fine_tune_nlu_embedder": hp.Boolean("fine_tune_nlu_embedder", default=False),
            "batch_size": hp.Choice("batch_size", [8, 16]),  # @TODO: Add larger sizes once memory issues are resolved.
            "dropout": hp.Float("dropout", 0.0, 0.6, default=0.1),
            "use_utterances": hp.Boolean("use_utterances", default=False),
            "predict_single": hp.Boolean("predict_single", default=False),
        }

    def fit(self, agent: Agent) -> None:
        """Fits the model on `agent`'s training conversations..
        """
        # Preprocess the data.
        self._preprocessor = PreprocessedTrainingData(agent, predict_single=self.predict_single)
        self._action_names = self._preprocessor.enc_context.inverse_transform(
            "action_index", list(range(self._preprocessor.num_actions))
        )  # we'll use these when we're decoding predictions.

        # Define the model.
        feature_vec = tf.keras.Input((self._preprocessor.max_len, self._preprocessor.input_dim), name="feature_vec")
        utterance_ids = tf.keras.Input((self._preprocessor.max_len, MAX_UTTERANCE_LEN),
                                       name="utterance_ids", dtype=tf.int32)
        utterance_mask = tf.keras.Input((self._preprocessor.max_len, MAX_UTTERANCE_LEN),
                                        name="utterance_mask", dtype=tf.int32)
        conversation_mask = tf.keras.Input((self._preprocessor.max_len, 1), name="conversation_mask", dtype=tf.float32)

        # Embed utterances and concatenate to feature_vec.
        if self.use_utterances:
            utterance_emb = TextEmbedder(self.fine_tune_nlu_embedder)([utterance_ids, utterance_mask])
            all_features = tf.concat([feature_vec, utterance_emb], axis=-1)
        else:
            all_features = feature_vec

        outputs = model_bodies[self.body](
            num_blocks=self.num_blocks,
            units=self.units,
            dropout=self.dropout,
            l2=self.l2,
        )(all_features, True)  # (batch_size, seq_len, hidden_size)

        if self.predict_single:
            outputs = GlobalAttentionPooling1D(self.units)(outputs)  # (batch_size, hidden_size)
            outputs = Dense(self._preprocessor.num_actions, activation="softmax")(outputs)  # (batch_size, num_actions)
        else:
            outputs = TimeDistributed(
                Dense(self._preprocessor.num_actions, activation="softmax")
            )(outputs)  # (batch_size, seq_len, num_actions)

        self._model = tf.keras.Model(
            inputs=[feature_vec, utterance_ids, utterance_mask, conversation_mask], outputs=outputs
        )

        # Build the model.
        self._model.compile(
            loss='sparse_categorical_crossentropy',
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
            metrics="accuracy",
        )

        # Fit the model.
        self._model.fit(self._preprocessor.to_classifier_dataset().batch(self.batch_size),
                        epochs=self.epochs,
                        callbacks=self.callbacks + [self.get_tensorboard_cb()])

        self._fitted = True

    def predict(self, conversations: t.List[Conversation]) -> t.List[t.List[StrPredWithConf]]:
        """Predict a distribution over the next action to take on each conversation in `conversations`.

        Parameters
        ----------
        conversations : list of Conversations
            A list of conversations. Each is the current state of a JSON chatbot conversation.
        """
        assert self._fitted
        X = self._preprocessor.encode_conversations(conversations)

        softmaxes = self._model.predict(X, self.batch_size)
        if not self.predict_single:
            softmaxes = softmaxes[:, -1, :]

        outputs = []
        for confs in softmaxes:
            # `confs` is the softmax distribution over actions for a single conversation.
            conv_outputs = [
                StrPredWithConf(value=action, confidence=conf) for action, conf in zip(self._action_names, confs)
            ]
            # Sort so the highest confidence predictions are first.
            outputs.append(sorted(conv_outputs, key=lambda pred: pred.confidence, reverse=True))

        return outputs

import typing as t

import spacy
from bavard_ml_common.mlops.serialization import Persistent, Serializer
from bavard_ml_common.mlops.web_service import WebService, endpoint

from bavard.common.pydantics import TagValue
from bavard.common.serialization import KerasSerializer, SpacyLanguageSerializer
from bavard.dialogue_policy.data.agent import Agent
from bavard.dialogue_policy.models.classifier import Classifier
from bavard.mlops.pydantics import ChatbotPipelinePredictions, ChatbotPipelinePrediction, ChatbotPipelineInputs
from bavard.nlu.model import NLUModel


class ChatbotPipeline(WebService, Persistent):
    """
    A machine learning pipeline for chatbots that handles NLU parsing
    and dialogue policy prediction.
    """
    serializer = Serializer(SpacyLanguageSerializer(), KerasSerializer())

    def __init__(self, config: t.Optional[dict] = None):
        if config is None:
            config = {}
        self._fitted = False
        self._do_dp = False
        self._nlu_model = NLUModel(**config.get("nlu", {}))
        self._dp_model = Classifier(**config.get("dp", {}))
        self._use_ner_presets: bool = config.get('use_ner_presets', True)
        self.language = 'en'  # To be read from the agent config, but defaults to english.

        # TODO: Load spaCy models for multiple languages. Then detect the language at prediction time and apply
        #       the appropriate model.
        self.spacy_en = spacy.load('en_core_web_md')

    def fit(self, agent: Agent):
        # Set the language field.
        self.language = agent.config.language

        # Train the ML models.
        self._nlu_model.train(agent.nluData)
        if len(agent.trainingConversations) > 0:
            self._dp_model.fit(agent)
            self._do_dp = True
        else:
            self._do_dp = False
        self._fitted = True

    @endpoint(methods=["POST"])
    def predict(self, inputs: ChatbotPipelineInputs) -> ChatbotPipelinePredictions:
        """
        Takes `instances` (a list of conversations) and parses the intent of the final user
        utterance on each of them. Also, predicts the next agent action to take for
        each one. If the agent the pipeline was trained on had no training conversations, the pipeline will
        not use a dialogue policy model and its dialogue policy prediction will be `None`. If the final turn
        in any of the conversations is not a user turn and doesn't have an utterance, no NLU prediction will
        be made for that conversation and its NLU prediction will be `None`.
        """
        assert self._fitted
        convs = inputs.instances

        predictions = [ChatbotPipelinePrediction(nlu=None, dp=None)] * len(convs)

        # Parse the user utterances.
        utterances = [conv.get_final_user_utterance() for conv in convs]
        nlu_preds = self._nlu_model.predict(utterances).predictions
        for conv, utterance, pred, nlu_pred in zip(convs, utterances, predictions, nlu_preds):
            # If there is no utterance then the prediction for it won't make sense.
            if utterance:

                # Supplement NLU prediction with spaCy NER.
                if self._use_ner_presets:
                    # TODO: Handle more languages.
                    if self.language == 'en':
                        tags = nlu_pred.tags
                        doc = self.spacy_en(utterance)
                        for entity in doc.ents:
                            tags.append(TagValue(tagType=entity.label_, value=entity.text))

                pred.nlu = nlu_pred
                # The DP model will need to have the NLU intent prediction to make its own
                # action prediction.
                conv.turns[-1].userAction.intent = nlu_pred.intent.value

        if self._do_dp:
            # Predict the next agent action to take.
            dp_preds = self._dp_model.predict(convs)
            for pred, dp_pred in zip(predictions, dp_preds):
                pred.dp = dp_pred

        return ChatbotPipelinePredictions(predictions=predictions)

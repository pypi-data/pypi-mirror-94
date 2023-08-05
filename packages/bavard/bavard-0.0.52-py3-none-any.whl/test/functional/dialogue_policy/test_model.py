from unittest import TestCase
import typing as t

from bavard.dialogue_policy.data.agent import Agent
from bavard.dialogue_policy.models import Classifier
from bavard.dialogue_policy.data.conversations.conversation import Conversation


class TestModel(TestCase):

    def setUp(self) -> None:
        self.agent = Agent.parse_file("test/data/agents/bavard.json")

    def test_can_fit_and_predict(self) -> None:
        convs, _ = self.agent.make_validation_pairs()
        convs = [Conversation.parse_obj(c) for c in convs]

        # Should be able to fit
        model = Classifier(epochs=1, predict_single=False)
        model.fit(self.agent)
        # Predicted actions should be valid actions
        self._assert_can_predict(model, convs)

        # Should be able to fit in predict single mode
        model.set_params(predict_single=True)
        model.fit(self.agent)
        self._assert_can_predict(model, convs)

        # Model should be able to be serialized and deserialized and still work.
        model.to_dir("temp-model")
        loaded_model = Classifier.from_dir("temp-model", True)
        self._assert_can_predict(loaded_model, convs)

        # Model should be able to predict on a conversation of length 0.
        self._assert_can_predict(loaded_model, [Conversation(turns=[])])

    def _assert_can_predict(self, model: Classifier, convs: t.List[Conversation]):
        preds = model.predict(convs)
        self.assertEqual(len(preds), len(convs))
        for conv_preds in preds:
            # One prediction for each action.
            self.assertEqual(len(conv_preds), model._preprocessor.enc_context.get_size("action_index"))
            # Predicted actions should be valid actions
            for pred in conv_preds:
                self.assertIn(pred.value, model._preprocessor.enc_context.classes_("action_index"))

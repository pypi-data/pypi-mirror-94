from unittest import TestCase
from copy import deepcopy

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

from bavard.mlops.pipeline import ChatbotPipeline
from bavard.mlops.pydantics import ChatbotPipelinePredictions, ChatbotPipelineInputs
from bavard.dialogue_policy.data.conversations.conversation import Conversation
from bavard.dialogue_policy.data.agent import Agent


class TestChatbotPipeline(TestCase):
    def setUp(self) -> None:
        self.agent_with_convs = Agent.parse_file("test/data/agents/bavard.json")
        self.agent_no_convs = deepcopy(self.agent_with_convs)
        self.agent_no_convs.trainingConversations = []
        self.save_path = "test-model"
        self.test_conv = Conversation.parse_obj({
            "turns": [
                {
                    "actor": "USER",
                    "state": {
                        "slotValues": []
                    },
                    "userAction": {
                        "type": "UTTERANCE_ACTION",
                        "utterance": "Bon matin, David.",
                        "translatedUtterance": "Good morning, David.",
                        "intent": ""
                    }
                }
            ]
        })
        self.pipeline_inputs = ChatbotPipelineInputs(instances=[self.test_conv])

    def test_can_fit_predict(self):
        pipe = ChatbotPipeline({
            "nlu": {"epochs": 1},
            "dp": {"epochs": 1},
            "use_ner_presets": True
        })
        pipe.fit(self.agent_with_convs)

        # Predictions should be valid values.
        preds = pipe.predict(self.pipeline_inputs)
        self._assert_predictions_are_valid(self.agent_with_convs, pipe, preds, True)

        # Model should be able to be persisted, loaded, and still work.
        pipe.to_dir(self.save_path)
        loaded_pipe = ChatbotPipeline.from_dir(self.save_path, delete=True)
        preds = loaded_pipe.predict(self.pipeline_inputs)
        self._assert_predictions_are_valid(self.agent_with_convs, pipe, preds, True)

        # Model should be able to work as a web service.
        app = loaded_pipe.to_app()
        client = TestClient(app)

        res = client.get("/")
        self.assertEqual(res.status_code, 200)

        res = client.post("/predict", json=jsonable_encoder(self.pipeline_inputs))  # should work on raw JSON too
        self.assertEqual(res.status_code, 200)
        predictions = res.json()
        print(predictions)

        # The Spacy NER model should have detected two tags.
        self.assertDictEqual(predictions['predictions'][0]['nlu']['tags'][0], {
            'tagType': 'TIME',
            'value': 'morning'
        })
        self.assertDictEqual(predictions['predictions'][0]['nlu']['tags'][1], {
            'tagType': 'PERSON',
            'value': 'David'
        })
        self._assert_predictions_are_valid(
            self.agent_with_convs,
            pipe,
            ChatbotPipelinePredictions.parse_obj(predictions),
            True
        )

    def test_can_fit_predict_no_convs(self):
        pipe = ChatbotPipeline({"nlu": {"epochs": 1}, "dp": {"epochs": 1}})
        pipe.fit(self.agent_no_convs)

        # Predictions should be valid values.
        preds = pipe.predict(self.pipeline_inputs)
        self._assert_predictions_are_valid(self.agent_no_convs, pipe, preds, False)

    def _assert_predictions_are_valid(
            self, agent: Agent, pipe: ChatbotPipeline, preds: ChatbotPipelinePredictions, has_dp: bool
    ):
        intents = agent.nluData.intents
        actions = {action.name for action in agent.config.actions}
        for pred in preds.predictions:
            self.assertIn(pred.nlu.intent.value, intents)
            if has_dp:
                self.assertEqual(len(pred.dp), pipe._dp_model._preprocessor.enc_context.get_size("action_index"))
                for action_pred in pred.dp:
                    self.assertIn(action_pred.value, actions)
            else:
                self.assertIsNone(pred.dp)

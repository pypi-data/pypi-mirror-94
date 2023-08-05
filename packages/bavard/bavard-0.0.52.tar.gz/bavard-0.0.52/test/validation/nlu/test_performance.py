from unittest import TestCase

from bavard.dialogue_policy.data.agent import Agent
from bavard.nlu.model import NLUModel


class TestPerformance(TestCase):
    def setUp(self):
        self.nlu_data = Agent.parse_file("test/data/agents/bavard.json").nluData

    def test_model_performance(self):
        # A model fully trained on a dataset representative of what
        # we might see in production should give good generalizeable
        # predictive performance.
        model = NLUModel(auto=True)
        train_performance, test_performance = model.evaluate(self.nlu_data, nfolds=3)
        print("train_performance:", train_performance)
        print("test_performance:", test_performance)
        self.assertGreaterEqual(train_performance["intent_acc"], .9)
        self.assertGreaterEqual(test_performance["intent_acc"], .70)

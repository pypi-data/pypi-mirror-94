from unittest import TestCase

from bavard.dialogue_policy.models import Classifier
from bavard.dialogue_policy.data.agent import Agent


class TestPerformance(TestCase):
    def setUp(self):
        self.agent = Agent.parse_file("test/data/agents/bavard.json")

    def test_model_performance(self):
        # The DP model should be able to at *least* memorize and recreate a small
        # set of training conversations when in predict/inference mode.
        model = Classifier()  # default hyperparams, which is what our docker containers use
        model.fit(self.agent)
        train_performance = model.score(self.agent)
        print("train_performance:", train_performance)
        self.assertGreaterEqual(train_performance["f1_macro"], .95)

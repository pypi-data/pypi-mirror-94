from unittest import TestCase

from bavard.dialogue_policy.data.agent import Agent
from bavard.nlu.data.nlu_data import NLUTrainingData


class TestNLUTrainingData(TestCase):
    def setUp(self) -> None:
        self.nlu_data = Agent.parse_file("test/data/agents/bavard.json").nluData

    def test_balance_by_intent(self) -> None:

        intent_distribution = self.nlu_data.get_intent_distribution()
        majority_class_n = intent_distribution.most_common(1)[0][1]

        balanced = self.nlu_data.balance_by_intent()
        balanced_intents = NLUTrainingData.get_intents(balanced.examples)

        # The intents should still be the same
        self.assertSetEqual(set(self.nlu_data.intents), set(balanced_intents))
        # Each intent's examples should have been upsampled.
        balanced_intent_distribution = balanced.get_intent_distribution()
        for intent in self.nlu_data.intents:
            self.assertEqual(balanced_intent_distribution[intent], majority_class_n)

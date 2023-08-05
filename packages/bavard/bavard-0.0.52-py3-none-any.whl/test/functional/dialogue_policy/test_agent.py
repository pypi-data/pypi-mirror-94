import json
from unittest import TestCase

from fastapi.encoders import jsonable_encoder

from bavard.dialogue_policy.data.agent import Agent
from bavard.dialogue_policy.data.conversations.conversation import Conversation, TrainingConversation
from bavard.dialogue_policy.data.conversations.dialogue_turns import UserDialogueTurn
from bavard.dialogue_policy.data.conversations.actions import UserAction


class TestAgent(TestCase):
    def test_filters_bad_training_conversations(self):
        agent = Agent.parse_file("test/data/agents/test-agent.json")

        # Empty conversations should be filtered out.
        num_convs = len(agent.trainingConversations)
        agent.trainingConversations.append(TrainingConversation(conversation=Conversation(turns=[])))
        self.assertEqual(len(agent.trainingConversations), num_convs + 1)
        agent = Agent.parse_obj(jsonable_encoder(agent))
        # The added conversation should be filtered out.
        self.assertEqual(len(agent.trainingConversations), num_convs)

        # Conversations with no agent actions should be filtered out.
        agent.trainingConversations.append(
            TrainingConversation(
                conversation=Conversation(turns=[UserDialogueTurn(userAction=UserAction(type="UTTERANCE_ACTION"))])
            )
        )
        self.assertEqual(len(agent.trainingConversations), num_convs + 1)
        agent = Agent.parse_obj(jsonable_encoder(agent))
        # The added conversation should be filtered out.
        self.assertEqual(len(agent.trainingConversations), num_convs)

    def test_adds_nlu_examples_from_training_conversations(self):
        with open("test/data/agents/bavard.json") as f:
            raw_agent = json.load(f)

        n_nlu_examples = len(raw_agent["nluData"]["examples"])
        # When parsed, the `Agent` object should have more nlu examples than `n_nlu_examples`.
        self.assertGreater(len(Agent.parse_obj(raw_agent).nluData.examples), n_nlu_examples)

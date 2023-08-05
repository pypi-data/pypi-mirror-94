from unittest import TestCase

import numpy as np
from fastapi.encoders import jsonable_encoder

from bavard.dialogue_policy.data.conversations.actions import Actor
from bavard.dialogue_policy.data.conversations.dialogue_turns import UserDialogueTurn, AgentDialogueTurn
from bavard.dialogue_policy.data.conversations.conversation import Conversation
from test.functional.dialogue_policy.utils import (
    DummyContext,
    check_user_dialogue_turn_feature_vec,
    check_agent_action_feature_vec
)
from test.utils import load_json_file


class TestConversation(TestCase):
    def setUp(self):
        self.raw_conv = load_json_file("test/data/conversations/last-turn-user.json")
        self.raw_conv_short = load_json_file("test/data/conversations/length-one.json")
        self.raw_conv_dummy = load_json_file("test/data/conversations/dummy.json")
        self.raw_conv_with_human_agent = load_json_file("test/data/conversations/with-human-agent.json")
        self.ctx = DummyContext()

    def test_serialization(self):
        conv = Conversation.parse_obj(self.raw_conv)
        re_raw = jsonable_encoder(conv)
        # The object should be fully reconstructable.
        self.assertEqual(conv, Conversation.parse_obj(re_raw))

    def test_encoding(self):
        conv = Conversation.parse_obj(self.raw_conv_dummy)
        encoding = conv.encode(self.ctx.enc_context)
        expected_conv_rows = 2

        # Shape should be correct

        self.assertEqual(
            encoding["feature_vec"].shape,
            (
                expected_conv_rows,
                len(self.ctx.intents) + len(self.ctx.tag_types) + len(self.ctx.actions) + len(self.ctx.slots)
            )
        )
        self.assertEqual(encoding["action"].shape, (expected_conv_rows,))

        # Content should be correct

        user_turn_dim = UserDialogueTurn.get_encoding_shape(self.ctx.enc_context)["feature_vec"][1]
        agent_turn_dim = AgentDialogueTurn.get_encoding_shape(self.ctx.enc_context)[1]
        self.assertTrue(
            (self.ctx.enc_context.inverse_transform("action_index", encoding["action"]) == ["action1", "action2"]).all()
        )
        row1, row2 = np.split(encoding["feature_vec"], 2)
        row1_user = row1[:, :user_turn_dim]
        check_user_dialogue_turn_feature_vec(row1_user, self.ctx, slots=("slot1",), intent="intent1", tag_types=())

        row1_agent = row1[:, -agent_turn_dim:]
        # The agent turn in row one of the feature matrix should
        # be all zeros, because at that point in the conversation,
        # no agent turn had taken place yet.
        self.assertEqual(np.count_nonzero(row1_agent), 0)

        row2_user = row2[:, :user_turn_dim]
        check_user_dialogue_turn_feature_vec(
            row2_user, self.ctx, slots=("slot1", "slot3"), intent="intent2", tag_types=("tagtype1",)
        )

        row2_agent = row2[:, -agent_turn_dim:]
        check_agent_action_feature_vec(row2_agent, self.ctx, action="action1")

    def test_make_validation_pairs(self):
        convs, next_actions = Conversation.parse_obj(self.raw_conv).make_validation_pairs()
        self.assertEqual(len(convs), len(next_actions))

        # Each validation conversation should end with a user action
        for conv in convs:
            self.assertEqual(conv.turns[-1].actor, Actor.USER)

    def test_can_handle_human_agent_data(self):
        encoding = Conversation.parse_obj(self.raw_conv_dummy).encode(self.ctx.enc_context)
        # Human to human interactions should be skipped when encoding
        encoding_with_human_agent = Conversation.parse_obj(self.raw_conv_with_human_agent).encode(self.ctx.enc_context)

        for key in ["feature_vec", "utterance_ids", "utterance_mask", "action"]:
            self.assertTrue(np.array_equal(encoding[key], encoding_with_human_agent[key]))

    def test_can_handle_unseen_action(self):
        conv = Conversation.parse_obj(self.raw_conv_dummy)
        conv.turns[1].agentAction.name = "unseen_action"
        encoding = conv.encode(self.ctx.enc_context)
        # Encoding with unseen action should filter down from two encoded turns to just one.
        self.assertEqual(encoding["feature_vec"].shape[0], 1)

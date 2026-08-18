"""B4 canonical Conversation lifecycle tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "conversation" / "python" / "src"))

from ai_workforce_conversation.control import (
    ConversationError,
    ConversationService,
    Message,
)


class ConversationServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ConversationService()
        self.conversation = self.service.open("tenant-a", "session-a", "conversation-a")

    def test_messages_are_correlated_ordered_and_idempotent(self) -> None:
        first = Message("event-1", 1, "correlation-1")
        self.assertEqual(self.service.append_message(self.conversation, first), "accepted")
        self.assertEqual(self.service.append_message(self.conversation, first), "duplicate")
        with self.assertRaises(ConversationError):
            self.service.append_message(self.conversation, Message("event-3", 3, "correlation-3"))

    def test_turn_ownership_blocks_competing_turns_and_tracks_uncertainty(self) -> None:
        self.assertEqual(self.service.begin_turn(self.conversation, "turn-1"), "started")
        self.assertEqual(self.service.begin_turn(self.conversation, "turn-1"), "duplicate")
        with self.assertRaises(ConversationError):
            self.service.begin_turn(self.conversation, "turn-2")
        self.service.finish_turn(self.conversation, "turn-1", "uncertain")
        self.assertEqual(self.conversation.turn_outcomes["turn-1"], "uncertain")
        self.assertEqual(self.service.begin_turn(self.conversation, "turn-2"), "started")

    def test_scope_conflict_and_wrong_turn_completion_fail_closed(self) -> None:
        with self.assertRaises(ConversationError):
            self.service.open("tenant-b", "session-a", "conversation-a")
        self.service.begin_turn(self.conversation, "turn-1")
        with self.assertRaises(ConversationError):
            self.service.finish_turn(self.conversation, "turn-2", "failed")

    def test_event_ids_are_idempotent_only_within_one_conversation(self) -> None:
        other = self.service.open("tenant-b", "session-b", "conversation-b")
        self.assertEqual(
            self.service.append_message(self.conversation, Message("event-1", 1, "correlation-a")),
            "accepted",
        )
        self.assertEqual(
            self.service.append_message(other, Message("event-1", 1, "correlation-b")),
            "accepted",
        )

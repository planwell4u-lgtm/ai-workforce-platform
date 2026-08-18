"""Tests for database-backed canonical conversation transitions."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "conversation" / "python" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "data" / "python" / "src"))

from ai_workforce_backend.persistent_conversation import PersistentConversationService
from ai_workforce_conversation.control import ConversationError, Message
from ai_workforce_data.sqlite_store import SqliteTenantStore, TenantScope


class PersistentConversationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = SqliteTenantStore(Path(":memory:"))
        self.store.apply_migrations()
        self.correlation = 0

    def service(self) -> PersistentConversationService:
        def next_correlation() -> str:
            self.correlation += 1
            return f"correlation-{self.correlation}"

        return PersistentConversationService(self.store, "test", next_correlation)

    def tearDown(self) -> None:
        self.store.close()

    def test_state_survives_service_restart_and_keeps_message_rules(self) -> None:
        first = self.service()
        conversation = first.open("tenant-a", "session-a", "conversation-a")
        self.assertEqual(first.append_message(conversation, Message("event-1", 1, "corr-1")), "accepted")
        first.begin_turn(conversation, "turn:event-1")
        first.finish_turn(conversation, "turn:event-1", "succeeded")

        restarted = self.service()
        restored = restarted.open("tenant-a", "session-a", "conversation-a")
        self.assertEqual(restarted.append_message(restored, Message("event-1", 1, "corr-2")), "duplicate")
        self.assertEqual(restarted.append_message(restored, Message("event-2", 2, "corr-2")), "accepted")
        with self.assertRaisesRegex(ConversationError, "out_of_order_message"):
            restarted.append_message(restored, Message("event-4", 4, "corr-4"))

        record = self.store.get(TenantScope("tenant-a", "test", "read"), "conversation", "conversation-a")
        self.assertIsNotNone(record)
        self.assertEqual(record.payload["state_version"], 4)


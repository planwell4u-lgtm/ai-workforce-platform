"""B5 Web Chat authentication, canonical-input, and delivery tests."""

from __future__ import annotations

import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "conversation" / "python" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "digital_channel" / "python" / "src"))

from ai_workforce_conversation.control import ConversationService
from ai_workforce_digital_channel.web_chat import (
    ChannelCredential,
    ChannelDenied,
    DeliveryIntent,
    LocalWebChatAdapter,
)


class WebChatAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conversations = ConversationService()
        self.conversation = self.conversations.open("tenant-a", "session-a", "conversation-a")
        self.adapter = LocalWebChatAdapter(self.conversations)
        self.credential = ChannelCredential("tenant-a", "participant-a", int(time.time()) + 60)

    def test_authenticated_input_uses_canonical_conversation_and_is_idempotent(self) -> None:
        self.assertEqual(
            self.adapter.receive(self.credential, self.conversation, "event-1", 1, "corr-1"),
            "accepted",
        )
        self.assertEqual(
            self.adapter.receive(self.credential, self.conversation, "event-1", 1, "corr-1"),
            "duplicate",
        )

    def test_expired_or_wrong_tenant_credential_is_rejected(self) -> None:
        with self.assertRaises(ChannelDenied):
            self.adapter.receive(
                ChannelCredential("tenant-a", "p", 0), self.conversation, "event-1", 1, "corr"
            )
        with self.assertRaises(ChannelDenied):
            self.adapter.receive(
                ChannelCredential("tenant-b", "p", int(time.time()) + 60),
                self.conversation,
                "event-1",
                1,
                "corr",
            )

    def test_delivery_is_idempotent_and_honors_opt_out(self) -> None:
        intent = DeliveryIntent("tenant-a", "conversation-a", "delivery-1", "Hello")
        self.assertEqual(self.adapter.deliver(intent).disposition, "accepted")
        self.assertEqual(self.adapter.deliver(intent).disposition, "duplicate")
        suppressed = DeliveryIntent(
            "tenant-a", "conversation-a", "delivery-2", "Hello", opted_out=True
        )
        self.assertEqual(self.adapter.deliver(suppressed).disposition, "suppressed")

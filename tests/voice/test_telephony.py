from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "conversation" / "python" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "voice" / "python" / "src"))

from ai_workforce_conversation.control import ConversationError, ConversationService
from ai_workforce_voice.telephony import InboundTelephoneAdapter, InboundTelephoneCall


class InboundTelephoneAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conversations = ConversationService()
        self.adapter = InboundTelephoneAdapter(
            self.conversations, {"+12402251204": "staging-demo"}
        )

    def test_admits_configured_number_without_putting_number_in_session_scope(self) -> None:
        interaction = self.adapter.admit(
            InboundTelephoneCall("call-a", "+12402251204", "phone-support-private-a")
        )

        self.assertEqual(interaction.conversation.tenant_ref, "staging-demo")
        self.assertEqual(interaction.conversation.session_ref, "telephone-session-call-a")
        self.assertEqual(interaction.conversation.conversation_ref, "telephone-conversation-call-a")
        self.assertNotIn("+12402251204", interaction.conversation.session_ref)

    def test_unknown_called_number_fails_closed_before_opening_conversation(self) -> None:
        with self.assertRaisesRegex(ConversationError, "telephone_route_unavailable"):
            self.adapter.admit(InboundTelephoneCall("call-b", "+19995550123", "room-b"))

        conversation = self.conversations.open(
            "staging-demo", "fresh-session", "telephone-conversation-call-b"
        )
        self.assertEqual(conversation.tenant_ref, "staging-demo")

    def test_disconnect_marks_active_turn_uncertain(self) -> None:
        interaction = self.adapter.admit(
            InboundTelephoneCall("call-c", "+12402251204", "phone-support-private-c")
        )
        self.adapter.begin_output(interaction, "turn-c")
        self.adapter.disconnect(interaction)

        self.assertEqual(interaction.conversation.turn_outcomes["turn-c"], "uncertain")
        self.assertEqual(interaction.voice.state, "disconnected")

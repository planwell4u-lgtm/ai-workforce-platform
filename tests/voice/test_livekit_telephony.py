from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "conversation" / "python" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "voice" / "python" / "src"))

from ai_workforce_conversation.control import ConversationError, ConversationService
from ai_workforce_voice.livekit_telephony import (
    LiveKitInboundCallEvent,
    LiveKitInboundTelephoneAdapter,
)
from ai_workforce_voice.telephony import InboundTelephoneAdapter


class LiveKitInboundTelephoneAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        telephone = InboundTelephoneAdapter(
            ConversationService(), {"+12402251204": "staging-demo"}
        )
        self.adapter = LiveKitInboundTelephoneAdapter(telephone)

    def test_admits_only_a_valid_sip_event_for_a_configured_number(self) -> None:
        interaction = self.adapter.admit(
            LiveKitInboundCallEvent(
                "call-a",
                "phone-support-private-a",
                "sip",
                {"sip.trunkPhoneNumber": "+12402251204", "sip.callFrom": "+15555550123"},
            )
        )

        self.assertEqual(interaction.conversation.tenant_ref, "staging-demo")
        self.assertNotIn("+15555550123", interaction.conversation.session_ref)

    def test_rejects_non_sip_participant(self) -> None:
        with self.assertRaisesRegex(ConversationError, "livekit_sip_participant_required"):
            self.adapter.admit(
                LiveKitInboundCallEvent(
                    "call-b", "room-b", "standard", {"sip.trunkPhoneNumber": "+12402251204"}
                )
            )

    def test_rejects_missing_or_malformed_called_number(self) -> None:
        for attributes in ({}, {"sip.trunkPhoneNumber": "12402251204"}):
            with self.subTest(attributes=attributes):
                with self.assertRaisesRegex(ConversationError, "livekit_called_number_required"):
                    self.adapter.admit(LiveKitInboundCallEvent("call-c", "room-c", "sip", attributes))

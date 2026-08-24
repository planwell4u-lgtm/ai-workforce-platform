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
    call_ref_from_sip_attributes,
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

    def test_admits_managed_number_only_with_an_exact_trusted_dispatch_route(self) -> None:
        routed_adapter = LiveKitInboundTelephoneAdapter(
            InboundTelephoneAdapter(
                ConversationService(), {"+12402251204": "staging-demo"}
            ),
            {"planwell-native-support-v1": "+12402251204"},
        )

        for attributes in ({"sip.callFrom": "+15555550123"}, {"sip.trunkPhoneNumber": ""}):
            with self.subTest(attributes=attributes):
                interaction = routed_adapter.admit(
                    LiveKitInboundCallEvent(
                        "call-managed",
                        "phone-support-private-managed",
                        "sip",
                        attributes,
                        "planwell-native-support-v1",
                    )
                )

                self.assertEqual(interaction.conversation.tenant_ref, "staging-demo")
                self.assertNotIn("+15555550123", interaction.conversation.session_ref)

    def test_rejects_unknown_dispatch_metadata_when_called_number_is_missing(self) -> None:
        routed_adapter = LiveKitInboundTelephoneAdapter(
            InboundTelephoneAdapter(
                ConversationService(), {"+12402251204": "staging-demo"}
            ),
            {"planwell-native-support-v1": "+12402251204"},
        )

        with self.assertRaisesRegex(ConversationError, "livekit_called_number_required"):
            routed_adapter.admit(
                LiveKitInboundCallEvent(
                    "call-untrusted",
                    "room-untrusted",
                    "sip",
                    {"sip.callFrom": "+15555550123"},
                    "other-route",
                )
            )

    def test_prefers_provider_global_call_reference_without_reading_caller_number(self) -> None:
        call_ref = call_ref_from_sip_attributes(
            {
                "sip.callID": "local-call-id",
                "sip.callIDFull": "provider-call-id",
                "sip.phoneNumber": "+15555550123",
            }
        )

        self.assertEqual(call_ref, "provider-call-id")

    def test_requires_a_sip_call_reference(self) -> None:
        with self.assertRaisesRegex(ConversationError, "livekit_call_reference_required"):
            call_ref_from_sip_attributes({"sip.phoneNumber": "+15555550123"})

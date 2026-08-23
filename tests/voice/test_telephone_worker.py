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
from ai_workforce_voice.telephone_worker import InboundTelephoneWorker
from ai_workforce_voice.telephony import InboundTelephoneAdapter


class InboundTelephoneWorkerTests(unittest.TestCase):
    def setUp(self) -> None:
        telephone = InboundTelephoneAdapter(
            ConversationService(), {"+12402251204": "staging-demo"}
        )
        self.worker = InboundTelephoneWorker(LiveKitInboundTelephoneAdapter(telephone))
        self.event = LiveKitInboundCallEvent(
            "call-a", "phone-support-private-a", "sip", {"sip.trunkPhoneNumber": "+12402251204"}
        )

    def test_admits_one_interaction_per_livekit_call(self) -> None:
        first = self.worker.participant_connected(self.event)
        second = self.worker.participant_connected(self.event)

        self.assertIs(first, second)
        self.assertEqual(self.worker.active_call_count(), 1)

    def test_rejects_duplicate_call_ref_in_another_room(self) -> None:
        self.worker.participant_connected(self.event)
        conflicting = LiveKitInboundCallEvent(
            "call-a", "other-room", "sip", {"sip.trunkPhoneNumber": "+12402251204"}
        )

        with self.assertRaisesRegex(ConversationError, "livekit_call_scope_conflict"):
            self.worker.participant_connected(conflicting)

    def test_disconnect_marks_active_output_uncertain_and_removes_call(self) -> None:
        interaction = self.worker.participant_connected(self.event)
        self.worker.begin_output("call-a", "turn-a")
        self.worker.participant_disconnected("call-a")

        self.assertEqual(interaction.conversation.turn_outcomes["turn-a"], "uncertain")
        self.assertEqual(self.worker.active_call_count(), 0)

    def test_unknown_disconnect_fails_closed(self) -> None:
        with self.assertRaisesRegex(ConversationError, "livekit_call_not_active"):
            self.worker.participant_disconnected("missing-call")

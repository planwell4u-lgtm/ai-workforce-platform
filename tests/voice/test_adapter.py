from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "conversation" / "python" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "voice" / "python" / "src"))

from ai_workforce_conversation.control import ConversationService
from ai_workforce_voice.adapter import LocalVoiceAdapter


class VoiceAdapterTests(unittest.TestCase):
    def test_interrupt_and_disconnect_preserve_uncertain_turn_state(self) -> None:
        conversations = ConversationService()
        conversation = conversations.open("tenant-a", "session-a", "conversation-a")
        adapter = LocalVoiceAdapter(conversations)
        interaction = adapter.connect("voice-1", conversation)
        adapter.begin_output(interaction, conversation, "turn-1")
        adapter.interrupt(interaction, conversation)
        self.assertEqual(conversation.turn_outcomes["turn-1"], "uncertain")
        adapter.disconnect(interaction, conversation)
        self.assertEqual(interaction.state, "disconnected")

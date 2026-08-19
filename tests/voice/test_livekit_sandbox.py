from __future__ import annotations

import asyncio
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "conversation" / "python" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "voice" / "python" / "src"))

from ai_workforce_conversation.control import ConversationService
from ai_workforce_voice.livekit_sandbox import LiveKitSandboxAdapter, LiveKitSandboxConfiguration


@unittest.skipUnless(
    os.environ.get("LIVEKIT_SANDBOX_TEST") == "1",
    "requires the explicitly started local LiveKit sandbox",
)
class LiveKitSandboxTests(unittest.TestCase):
    def test_connect_and_disconnect_marks_active_turn_uncertain(self) -> None:
        async def exercise() -> None:
            conversations = ConversationService()
            conversation = conversations.open("tenant-a", "voice-session-a", "voice-conversation-a")
            configuration = LiveKitSandboxConfiguration(
                url=os.environ.get("LIVEKIT_URL", "ws://localhost:7880"),
                api_key=os.environ.get("LIVEKIT_API_KEY", "devkey"),
                api_secret=os.environ.get("LIVEKIT_API_SECRET", "secret"),
            )
            adapter = LiveKitSandboxAdapter(conversations, configuration)
            interaction = await adapter.connect(
                "livekit-interaction-a", conversation, "participant-a"
            )
            adapter.begin_output(interaction, conversation, "voice-turn-a")
            await adapter.disconnect(interaction, conversation)
            self.assertEqual(conversation.turn_outcomes["voice-turn-a"], "uncertain")
            self.assertEqual(interaction.voice.state, "disconnected")
            self.assertFalse(interaction.room.isconnected())

        asyncio.run(exercise())

"""Test-only LiveKit adapter for the local provider-evaluation sandbox."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workforce_conversation.control import Conversation, ConversationError, ConversationService
from livekit import api, rtc

from .adapter import LocalVoiceAdapter, VoiceInteraction


@dataclass(frozen=True)
class LiveKitSandboxConfiguration:
    url: str
    api_key: str
    api_secret: str

    def __post_init__(self) -> None:
        if not self.url.startswith(("ws://", "wss://")):
            raise ValueError("LiveKit sandbox URL must use ws:// or wss://")
        if not self.api_key or not self.api_secret:
            raise ValueError("LiveKit sandbox credentials are required")


@dataclass
class LiveKitVoiceInteraction:
    voice: VoiceInteraction
    room: rtc.Room


class LiveKitSandboxAdapter:
    """Connects only to a local evaluation server through Voice lifecycle rules."""

    def __init__(
        self,
        conversations: ConversationService,
        configuration: LiveKitSandboxConfiguration,
    ) -> None:
        self._lifecycle = LocalVoiceAdapter(conversations)
        self._configuration = configuration

    async def connect(
        self,
        interaction_ref: str,
        conversation: Conversation,
        participant_ref: str,
    ) -> LiveKitVoiceInteraction:
        if not participant_ref:
            raise ConversationError("participant_ref is required")
        voice = self._lifecycle.connect(interaction_ref, conversation)
        room = rtc.Room()
        token = (
            api.AccessToken(self._configuration.api_key, self._configuration.api_secret)
            .with_identity(participant_ref)
            .with_grants(api.VideoGrants(room_join=True, room=conversation.conversation_ref))
            .to_jwt()
        )
        try:
            await room.connect(self._configuration.url, token)
        except Exception:
            voice.state = "disconnected"
            raise
        return LiveKitVoiceInteraction(voice, room)

    def begin_output(
        self,
        interaction: LiveKitVoiceInteraction,
        conversation: Conversation,
        turn_ref: str,
    ) -> None:
        self._lifecycle.begin_output(interaction.voice, conversation, turn_ref)

    async def disconnect(
        self,
        interaction: LiveKitVoiceInteraction,
        conversation: Conversation,
    ) -> None:
        self._lifecycle.disconnect(interaction.voice, conversation)
        await interaction.room.disconnect()

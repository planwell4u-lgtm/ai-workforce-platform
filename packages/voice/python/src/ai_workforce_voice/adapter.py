"""B6 local Voice interaction lifecycle."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ai_workforce_conversation.control import Conversation, ConversationError, ConversationService

VoiceState = Literal["connected", "interrupted", "disconnected"]


@dataclass
class VoiceInteraction:
    interaction_ref: str
    conversation_ref: str
    state: VoiceState = "connected"
    active_turn_ref: str | None = None


class LocalVoiceAdapter:
    def __init__(self, conversations: ConversationService) -> None:
        self._conversations = conversations

    def connect(self, interaction_ref: str, conversation: Conversation) -> VoiceInteraction:
        if not interaction_ref:
            raise ConversationError("interaction_ref is required")
        return VoiceInteraction(interaction_ref, conversation.conversation_ref)

    def begin_output(
        self, interaction: VoiceInteraction, conversation: Conversation, turn_ref: str
    ) -> None:
        if (
            interaction.state != "connected"
            or interaction.conversation_ref != conversation.conversation_ref
        ):
            raise ConversationError("voice_interaction_unavailable")
        self._conversations.begin_turn(conversation, turn_ref)
        interaction.active_turn_ref = turn_ref

    def interrupt(self, interaction: VoiceInteraction, conversation: Conversation) -> None:
        if interaction.active_turn_ref is not None:
            self._conversations.finish_turn(conversation, interaction.active_turn_ref, "uncertain")
            interaction.active_turn_ref = None
        interaction.state = "interrupted"

    def disconnect(self, interaction: VoiceInteraction, conversation: Conversation) -> None:
        self.interrupt(interaction, conversation)
        interaction.state = "disconnected"

"""Provider-neutral inbound telephone admission for canonical Conversations.

This module deliberately contains no SIP, LiveKit, model, transcription, or
knowledge access.  A provider worker supplies trusted call facts after it has
validated the carrier event.  The called number is used only to resolve the
configured tenant route and is never placed in the canonical session reference.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ai_workforce_conversation.control import Conversation, ConversationError, ConversationService

from .adapter import LocalVoiceAdapter, VoiceInteraction


@dataclass(frozen=True)
class InboundTelephoneCall:
    """Trusted, minimized facts provided by the telephony worker."""

    call_ref: str
    called_number: str
    room_ref: str


@dataclass
class InboundTelephoneInteraction:
    """Canonical state for one admitted inbound telephone call."""

    call_ref: str
    room_ref: str
    conversation: Conversation
    voice: VoiceInteraction


class InboundTelephoneAdapter:
    """Maps one configured inbound number to one tenant and Voice lifecycle.

    The mapping is deployment configuration, not caller input.  Unknown,
    missing, or malformed routes fail closed before a Conversation is opened.
    """

    def __init__(
        self,
        conversations: ConversationService,
        tenant_by_called_number: Mapping[str, str],
    ) -> None:
        self._conversations = conversations
        self._lifecycle = LocalVoiceAdapter(conversations)
        self._tenant_by_called_number = dict(tenant_by_called_number)

    def admit(self, call: InboundTelephoneCall) -> InboundTelephoneInteraction:
        if not all((call.call_ref, call.called_number, call.room_ref)):
            raise ConversationError("telephone_call_facts_required")
        tenant_ref = self._tenant_by_called_number.get(call.called_number)
        if not tenant_ref:
            raise ConversationError("telephone_route_unavailable")
        conversation = self._conversations.open(
            tenant_ref,
            f"telephone-session-{call.call_ref}",
            f"telephone-conversation-{call.call_ref}",
        )
        voice = self._lifecycle.connect(f"telephone-interaction-{call.call_ref}", conversation)
        return InboundTelephoneInteraction(call.call_ref, call.room_ref, conversation, voice)

    def begin_output(self, interaction: InboundTelephoneInteraction, turn_ref: str) -> None:
        self._lifecycle.begin_output(interaction.voice, interaction.conversation, turn_ref)

    def disconnect(self, interaction: InboundTelephoneInteraction) -> None:
        self._lifecycle.disconnect(interaction.voice, interaction.conversation)

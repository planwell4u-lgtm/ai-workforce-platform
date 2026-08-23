"""Local worker harness for validated inbound LiveKit telephone events.

The runtime adapter intentionally owns no media, model, transcription, or
knowledge behavior. A LiveKit Agents process will later call this harness from
its SIP participant callbacks after the provider runtime is installed.
"""

from __future__ import annotations

from ai_workforce_conversation.control import ConversationError

from .livekit_telephony import LiveKitInboundCallEvent, LiveKitInboundTelephoneAdapter
from .telephony import InboundTelephoneInteraction


class InboundTelephoneWorker:
    """Keeps one canonical interaction per active trusted LiveKit call."""

    def __init__(self, admission: LiveKitInboundTelephoneAdapter) -> None:
        self._admission = admission
        self._active: dict[str, InboundTelephoneInteraction] = {}

    def participant_connected(self, event: LiveKitInboundCallEvent) -> InboundTelephoneInteraction:
        existing = self._active.get(event.call_ref)
        if existing is not None:
            if existing.room_ref != event.room_ref:
                raise ConversationError("livekit_call_scope_conflict")
            return existing
        interaction = self._admission.admit(event)
        self._active[event.call_ref] = interaction
        return interaction

    def participant_disconnected(self, call_ref: str) -> None:
        interaction = self._active.pop(call_ref, None)
        if interaction is None:
            raise ConversationError("livekit_call_not_active")
        self._admission.disconnect(interaction)

    def begin_output(self, call_ref: str, turn_ref: str) -> None:
        interaction = self._active.get(call_ref)
        if interaction is None:
            raise ConversationError("livekit_call_not_active")
        self._admission.begin_output(interaction, turn_ref)

    def active_call_count(self) -> int:
        return len(self._active)

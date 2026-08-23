"""LiveKit-specific validation before provider-neutral telephone admission.

The worker must obtain these facts from a validated LiveKit SIP participant
event. This adapter intentionally does not connect to LiveKit, start an agent,
or process media; it makes the provider event contract testable locally.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping

from ai_workforce_conversation.control import ConversationError

from .telephony import InboundTelephoneAdapter, InboundTelephoneInteraction, InboundTelephoneCall

_E164 = re.compile(r"^\+[1-9][0-9]{7,14}$")
_CALLED_NUMBER_ATTRIBUTE = "sip.trunkPhoneNumber"


@dataclass(frozen=True)
class LiveKitInboundCallEvent:
    """Minimal facts from one validated LiveKit SIP participant event."""

    call_ref: str
    room_ref: str
    participant_kind: str
    attributes: Mapping[str, str]


class LiveKitInboundTelephoneAdapter:
    """Accept only SIP participants with a valid called-number attribute."""

    def __init__(self, telephone: InboundTelephoneAdapter) -> None:
        self._telephone = telephone

    def admit(self, event: LiveKitInboundCallEvent) -> InboundTelephoneInteraction:
        if event.participant_kind.lower() != "sip":
            raise ConversationError("livekit_sip_participant_required")
        called_number = event.attributes.get(_CALLED_NUMBER_ATTRIBUTE)
        if not isinstance(called_number, str) or not _E164.fullmatch(called_number):
            raise ConversationError("livekit_called_number_required")
        return self._telephone.admit(
            InboundTelephoneCall(event.call_ref, called_number, event.room_ref)
        )

"""B5 local Web Chat adapter with authenticated ingress and idempotent delivery."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Literal

from ai_workforce_conversation.control import Conversation, ConversationService, Message


class ChannelDenied(PermissionError):
    """Web Chat input or delivery is ineligible for the current channel context."""


@dataclass(frozen=True)
class ChannelCredential:
    tenant_ref: str
    participant_ref: str
    expires_at: int
    revoked: bool = False


@dataclass(frozen=True)
class DeliveryIntent:
    tenant_ref: str
    conversation_ref: str
    idempotency_ref: str
    content: str
    opted_out: bool = False


@dataclass(frozen=True)
class DeliveryEvidence:
    disposition: Literal["accepted", "duplicate", "suppressed"]
    idempotency_ref: str


class LocalWebChatAdapter:
    """Normalizes authenticated input; it never creates canonical conversations."""

    def __init__(self, conversation_service: ConversationService) -> None:
        self._conversation_service = conversation_service
        self._deliveries: dict[str, DeliveryEvidence] = {}

    def receive(
        self,
        credential: ChannelCredential,
        conversation: Conversation,
        event_ref: str,
        sequence: int,
        correlation_ref: str,
    ) -> Literal["accepted", "duplicate"]:
        if credential.revoked or credential.expires_at <= int(time.time()):
            raise ChannelDenied("credential_unavailable")
        if credential.tenant_ref != conversation.tenant_ref:
            raise ChannelDenied("tenant_mismatch")
        return self._conversation_service.append_message(
            conversation, Message(event_ref, sequence, correlation_ref)
        )

    def deliver(self, intent: DeliveryIntent) -> DeliveryEvidence:
        previous = self._deliveries.get(intent.idempotency_ref)
        if previous is not None:
            return DeliveryEvidence("duplicate", intent.idempotency_ref)
        if not intent.content or intent.opted_out:
            evidence = DeliveryEvidence("suppressed", intent.idempotency_ref)
        else:
            evidence = DeliveryEvidence("accepted", intent.idempotency_ref)
        self._deliveries[intent.idempotency_ref] = evidence
        return evidence

"""B4 canonical Conversation and turn-control state machine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

TurnOutcome = Literal["pending", "succeeded", "failed", "uncertain"]


class ConversationError(ValueError):
    """A message or turn violates canonical Conversation ownership rules."""


@dataclass(frozen=True)
class Message:
    event_ref: str
    sequence: int
    correlation_ref: str


@dataclass(frozen=True)
class TranscriptEntry:
    sender: Literal["support", "you"]
    text: str


@dataclass
class Conversation:
    conversation_ref: str
    tenant_ref: str
    session_ref: str
    messages: list[Message] = field(default_factory=list)
    active_turn_ref: str | None = None
    turn_outcomes: dict[str, TurnOutcome] = field(default_factory=dict)
    transcript: list[TranscriptEntry] = field(default_factory=list)


class ConversationService:
    """Owns one canonical session path and fails closed on scope/order conflicts."""

    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}

    def open(self, tenant_ref: str, session_ref: str, conversation_ref: str) -> Conversation:
        if not all((tenant_ref, session_ref, conversation_ref)):
            raise ConversationError("trusted tenant, session, and conversation are required")
        existing = self._conversations.get(conversation_ref)
        if existing is not None:
            if existing.tenant_ref != tenant_ref or existing.session_ref != session_ref:
                raise ConversationError("conversation_scope_conflict")
            return existing
        conversation = Conversation(conversation_ref, tenant_ref, session_ref)
        self._conversations[conversation_ref] = conversation
        return conversation

    def append_message(
        self, conversation: Conversation, message: Message
    ) -> Literal["accepted", "duplicate"]:
        if not all((message.event_ref, message.correlation_ref)) or message.sequence < 1:
            raise ConversationError("invalid_message")
        if any(item.event_ref == message.event_ref for item in conversation.messages):
            return "duplicate"
        if conversation.messages and message.sequence != conversation.messages[-1].sequence + 1:
            raise ConversationError("out_of_order_message")
        conversation.messages.append(message)
        return "accepted"

    def begin_turn(
        self, conversation: Conversation, turn_ref: str
    ) -> Literal["started", "duplicate"]:
        if not turn_ref:
            raise ConversationError("turn_ref is required")
        if turn_ref in conversation.turn_outcomes:
            return "duplicate"
        if conversation.active_turn_ref is not None:
            raise ConversationError("competing_turn")
        conversation.active_turn_ref = turn_ref
        conversation.turn_outcomes[turn_ref] = "pending"
        return "started"

    def finish_turn(self, conversation: Conversation, turn_ref: str, outcome: TurnOutcome) -> None:
        if conversation.active_turn_ref != turn_ref:
            raise ConversationError("turn_not_owned")
        if outcome == "pending":
            raise ConversationError("terminal_outcome_required")
        conversation.turn_outcomes[turn_ref] = outcome
        conversation.active_turn_ref = None

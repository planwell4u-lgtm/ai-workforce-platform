"""Durable canonical conversation state backed by the tenant record store."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from ai_workforce_conversation.control import (
    Conversation,
    ConversationError,
    Message,
    TranscriptEntry,
    TurnOutcome,
)
from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord


class ConversationRecordStore(Protocol):
    def get(self, scope: TenantScope, kind: str, record_ref: str) -> VersionedRecord | None: ...

    def compare_and_swap(
        self,
        scope: TenantScope,
        kind: str,
        record: VersionedRecord,
        expected_state_version: int,
    ) -> bool: ...


class PersistentConversationService:
    """Reloads and atomically persists each canonical conversation transition."""

    def __init__(
        self,
        store: ConversationRecordStore,
        environment_ref: str,
        correlation_factory: Callable[[], str],
    ) -> None:
        self._store = store
        self._environment_ref = environment_ref
        self._correlation_factory = correlation_factory

    def open(self, tenant_ref: str, session_ref: str, conversation_ref: str) -> Conversation:
        if not all((tenant_ref, session_ref, conversation_ref)):
            raise ConversationError("trusted tenant, session, and conversation are required")
        record = self._store.get(self._scope(tenant_ref), "conversation", conversation_ref)
        if record is None:
            return Conversation(conversation_ref, tenant_ref, session_ref)
        return self._decode(record, tenant_ref, session_ref)

    def append_message(self, conversation: Conversation, message: Message) -> str:
        if not all((message.event_ref, message.correlation_ref)) or message.sequence < 1:
            raise ConversationError("invalid_message")
        current, version = self._current(conversation)
        if any(item.event_ref == message.event_ref for item in current.messages):
            return "duplicate"
        if current.messages and message.sequence != current.messages[-1].sequence + 1:
            raise ConversationError("out_of_order_message")
        current.messages.append(message)
        if not self._save(current, version, message.correlation_ref):
            raise ConversationError("conversation_write_conflict")
        self._replace(conversation, current)
        return "accepted"

    def begin_turn(self, conversation: Conversation, turn_ref: str) -> str:
        if not turn_ref:
            raise ConversationError("turn_ref is required")
        current, version = self._current(conversation)
        if turn_ref in current.turn_outcomes:
            return "duplicate"
        if current.active_turn_ref is not None:
            raise ConversationError("competing_turn")
        current.active_turn_ref = turn_ref
        current.turn_outcomes[turn_ref] = "pending"
        if not self._save(current, version):
            raise ConversationError("conversation_write_conflict")
        self._replace(conversation, current)
        return "started"

    def finish_turn(self, conversation: Conversation, turn_ref: str, outcome: TurnOutcome) -> None:
        current, version = self._current(conversation)
        if current.active_turn_ref != turn_ref:
            raise ConversationError("turn_not_owned")
        if outcome == "pending":
            raise ConversationError("terminal_outcome_required")
        current.turn_outcomes[turn_ref] = outcome
        current.active_turn_ref = None
        if not self._save(current, version):
            raise ConversationError("conversation_write_conflict")
        self._replace(conversation, current)

    def add_transcript_entry(self, conversation: Conversation, sender: str, text: str) -> None:
        if sender not in {"support", "you"} or not text:
            raise ConversationError("invalid_transcript_entry")
        current, version = self._current(conversation)
        current.transcript.append(TranscriptEntry(sender, text))
        if not self._save(current, version):
            raise ConversationError("conversation_write_conflict")
        self._replace(conversation, current)

    def transcript(self, conversation: Conversation) -> list[TranscriptEntry]:
        current, _ = self._current(conversation)
        return list(current.transcript)

    def _current(self, conversation: Conversation) -> tuple[Conversation, int]:
        record = self._store.get(
            self._scope(conversation.tenant_ref), "conversation", conversation.conversation_ref
        )
        if record is None:
            return Conversation(
                conversation.conversation_ref, conversation.tenant_ref, conversation.session_ref
            ), 0
        payload = record.payload
        version = payload.get("state_version")
        if not isinstance(version, int) or version < 1:
            raise ConversationError("invalid_conversation_record")
        return self._decode(record, conversation.tenant_ref, conversation.session_ref), version

    def _save(
        self, conversation: Conversation, expected_version: int, correlation_ref: str | None = None
    ) -> bool:
        next_version = expected_version + 1
        record = VersionedRecord(
            conversation.conversation_ref,
            "v1",
            {
                "state_version": next_version,
                "session_ref": conversation.session_ref,
                "messages": [
                    {
                        "event_ref": item.event_ref,
                        "sequence": item.sequence,
                        "correlation_ref": item.correlation_ref,
                    }
                    for item in conversation.messages
                ],
                "active_turn_ref": conversation.active_turn_ref,
                "turn_outcomes": dict(conversation.turn_outcomes),
                "transcript": [
                    {"sender": entry.sender, "text": entry.text}
                    for entry in conversation.transcript
                ],
            },
        )
        return self._store.compare_and_swap(
            TenantScope(
                conversation.tenant_ref,
                self._environment_ref,
                correlation_ref or self._correlation_factory(),
            ),
            "conversation",
            record,
            expected_version,
        )

    def _scope(self, tenant_ref: str) -> TenantScope:
        return TenantScope(tenant_ref, self._environment_ref, self._correlation_factory())

    @staticmethod
    def _decode(record: VersionedRecord, tenant_ref: str, session_ref: str) -> Conversation:
        payload = record.payload
        stored_session = payload.get("session_ref")
        messages = payload.get("messages")
        outcomes = payload.get("turn_outcomes")
        transcript = payload.get("transcript", [])
        active_turn = payload.get("active_turn_ref")
        if (
            stored_session != session_ref
            or not isinstance(messages, list)
            or not isinstance(outcomes, dict)
            or not isinstance(transcript, list)
        ):
            raise ConversationError("conversation_scope_conflict")
        parsed_messages: list[Message] = []
        for item in messages:
            if not isinstance(item, dict):
                raise ConversationError("invalid_conversation_record")
            event_ref, sequence, correlation_ref = (
                item.get("event_ref"),
                item.get("sequence"),
                item.get("correlation_ref"),
            )
            if (
                not isinstance(event_ref, str)
                or not isinstance(sequence, int)
                or not isinstance(correlation_ref, str)
            ):
                raise ConversationError("invalid_conversation_record")
            parsed_messages.append(Message(event_ref, sequence, correlation_ref))
        if active_turn is not None and not isinstance(active_turn, str):
            raise ConversationError("invalid_conversation_record")
        if not all(
            isinstance(key, str) and value in {"pending", "succeeded", "failed", "uncertain"}
            for key, value in outcomes.items()
        ):
            raise ConversationError("invalid_conversation_record")
        parsed_transcript: list[TranscriptEntry] = []
        for entry in transcript:
            if (
                not isinstance(entry, dict)
                or entry.get("sender") not in {"support", "you"}
                or not isinstance(entry.get("text"), str)
            ):
                raise ConversationError("invalid_conversation_record")
            parsed_transcript.append(TranscriptEntry(entry["sender"], entry["text"]))
        return Conversation(
            record.record_ref,
            tenant_ref,
            session_ref,
            parsed_messages,
            active_turn,
            dict(outcomes),
            parsed_transcript,
        )

    @staticmethod
    def _replace(destination: Conversation, source: Conversation) -> None:
        destination.messages = source.messages
        destination.active_turn_ref = source.active_turn_ref
        destination.turn_outcomes = source.turn_outcomes
        destination.transcript = source.transcript

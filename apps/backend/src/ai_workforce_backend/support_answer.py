"""Protected deterministic support-answer API."""

from __future__ import annotations

import hashlib
import json
import uuid
from collections.abc import Callable, Mapping
from typing import cast
from urllib.parse import parse_qs

from ai_workforce_agent.support import FaqSupportAgent
from ai_workforce_conversation.control import ConversationError, Message

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)
from .persistent_conversation import PersistentConversationService


class SupportAnswerApi:
    route_ref = "agent.support-answer.v1"
    required_permission = "agent.context.read"

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        audit_sink: AuditSink,
        agent: FaqSupportAgent,
        conversations: PersistentConversationService,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._audit_sink = audit_sink
        self._agent = agent
        self._conversations = conversations
        self._correlation_factory = correlation_factory

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        if environ.get("PATH_INFO") != "/v1/support-answers":
            return self._respond(start_response, "404 Not Found", headers, {"error": "not_found"})
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if (
                self.required_permission not in membership.permissions
                or self.required_permission not in identity.granted_permissions
            ):
                raise AuthorizationError("insufficient_permission")
            if environ.get("REQUEST_METHOD") == "GET":
                session_ref = self._parse_session_ref(environ)
                conversation = self._conversations.open(
                    membership.tenant_ref,
                    session_ref,
                    self._conversation_ref(membership.tenant_ref, session_ref),
                )
                return self._respond(
                    start_response,
                    "200 OK",
                    headers,
                    {
                        "conversation_ref": conversation.conversation_ref,
                        "messages": [
                            {"sender": entry.sender, "text": entry.text}
                            for entry in self._conversations.transcript(conversation)
                        ],
                        "correlation_ref": correlation_ref,
                    },
                )
            if environ.get("REQUEST_METHOD") != "POST":
                return self._respond(
                    start_response,
                    "405 Method Not Allowed",
                    headers,
                    {"error": "method_not_allowed"},
                )
            payload = self._parse_request(environ)
            conversation_ref = self._conversation_ref(membership.tenant_ref, payload["session_ref"])
            conversation = self._conversations.open(
                membership.tenant_ref, payload["session_ref"], conversation_ref
            )
            disposition = self._conversations.append_message(
                conversation,
                Message(payload["event_ref"], payload["sequence"], correlation_ref),
            )
            if disposition == "duplicate":
                self._audit_sink.record(
                    AuditEvent(
                        "allowed",
                        "duplicate_event",
                        correlation_ref,
                        self.route_ref,
                        identity.principal_ref,
                        membership.tenant_ref,
                    )
                )
                return self._respond(
                    start_response,
                    "202 Accepted",
                    headers,
                    {"disposition": "duplicate", "correlation_ref": correlation_ref},
                )
            self._conversations.add_transcript_entry(conversation, "you", payload["question"])
            turn_ref = f"turn:{payload['event_ref']}"
            self._conversations.begin_turn(conversation, turn_ref)
            result = self._agent.answer(
                tenant_ref=membership.tenant_ref,
                agent_ref=payload["agent_ref"],
                subject_ref=identity.principal_ref,
                session_ref=payload["session_ref"],
                question=payload["question"],
                permissions=membership.permissions,
            )
            self._conversations.finish_turn(conversation, turn_ref, "succeeded")
            self._conversations.add_transcript_entry(conversation, "support", result.answer)
        except AuthenticationError as error:
            self._audit_sink.record(
                AuditEvent("denied", str(error), correlation_ref, self.route_ref)
            )
            return self._respond(
                start_response, "401 Unauthorized", headers, {"error": "unauthorized"}
            )
        except (AuthorizationError, ConversationError, TypeError, ValueError) as error:
            self._audit_sink.record(
                AuditEvent("denied", str(error), correlation_ref, self.route_ref)
            )
            return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})
        self._audit_sink.record(
            AuditEvent(
                "allowed",
                "answered",
                correlation_ref,
                self.route_ref,
                identity.principal_ref,
                membership.tenant_ref,
            )
        )
        return self._respond(
            start_response,
            "200 OK",
            headers,
            {
                "answer": result.answer,
                "source_ref": result.source_ref,
                "ticket_recommended": result.ticket_recommended,
                "conversation_ref": conversation.conversation_ref,
                "correlation_ref": correlation_ref,
            },
        )

    @staticmethod
    def _parse_request(environ: Mapping[str, object]) -> dict[str, str]:
        content_length = int(cast(str, environ.get("CONTENT_LENGTH", "0")))
        raw = cast(object, environ.get("wsgi.input"))
        if not hasattr(raw, "read"):
            raise TypeError("invalid_request")
        payload = json.loads(raw.read(content_length).decode("utf-8"))
        if not isinstance(payload, dict):
            raise TypeError("invalid_request")
        values = {
            name: payload.get(name)
            for name in ("agent_ref", "session_ref", "question", "event_ref")
        }
        sequence = payload.get("sequence")
        if not all(isinstance(value, str) and value for value in values.values()) or not isinstance(
            sequence, int
        ):
            raise ValueError("invalid_request")
        parsed = cast(dict[str, str], values)
        parsed["sequence"] = sequence
        return cast(dict[str, str], parsed)

    @staticmethod
    def _parse_session_ref(environ: Mapping[str, object]) -> str:
        values = parse_qs(cast(str, environ.get("QUERY_STRING", ""))).get("session_ref", [])
        if len(values) != 1 or not values[0]:
            raise ValueError("invalid_request")
        return values[0]

    @staticmethod
    def _conversation_ref(tenant_ref: str, session_ref: str) -> str:
        return hashlib.sha256(f"{tenant_ref}:{session_ref}".encode()).hexdigest()

    @staticmethod
    def _respond(
        start_response: Callable[..., object],
        status: str,
        headers: list[tuple[str, str]],
        body: object,
    ) -> list[bytes]:
        encoded = json.dumps(body, separators=(",", ":")).encode("utf-8")
        start_response(status, [*headers, ("Content-Length", str(len(encoded)))])
        return [encoded]

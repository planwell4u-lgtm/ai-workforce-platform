"""Protected test-only deterministic sales-answer API."""

from __future__ import annotations

import json
import uuid
import hashlib
from collections.abc import Callable, Mapping
from typing import cast

from ai_workforce_agent.sales import CatalogSalesAgent

from .b1 import AuditEvent, AuditSink, AuthenticationError, AuthorizationError, IdentityVerifier, MembershipDirectory
from .persistent_conversation import PersistentConversationService


class SalesAnswerApi:
    path = "/v1/sales-answers"
    route_ref = "agent.sales-answer.v1"
    required_permission = "agent.context.read"

    def __init__(self, verifier: IdentityVerifier, memberships: MembershipDirectory, audit_sink: AuditSink, agent: CatalogSalesAgent, conversations: PersistentConversationService) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._audit_sink = audit_sink
        self._agent = agent
        self._conversations = conversations

    def __call__(self, environ: Mapping[str, object], start_response: Callable[..., object]) -> list[bytes]:
        correlation_ref = str(uuid.uuid4())
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        try:
            if environ.get("REQUEST_METHOD") != "POST" or environ.get("PATH_INFO") != self.path:
                return self._respond(start_response, "404 Not Found", headers, {"error": "not_found"})
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if self.required_permission not in membership.permissions or self.required_permission not in identity.granted_permissions:
                raise AuthorizationError("insufficient_permission")
            request = self._request(environ)
            conversation = self._conversations.open(
                membership.tenant_ref,
                request["session_ref"],
                self._conversation_ref(membership.tenant_ref, request["session_ref"]),
            )
            turn_ref = f"sales:{correlation_ref}"
            self._conversations.begin_turn(conversation, turn_ref)
            result = self._agent.answer(
                tenant_ref=membership.tenant_ref, agent_ref=request["agent_ref"], subject_ref=identity.principal_ref,
                session_ref=request["session_ref"], question=request["question"], permissions=membership.permissions,
            )
            self._conversations.finish_turn(conversation, turn_ref, "succeeded")
        except AuthenticationError as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return self._respond(start_response, "401 Unauthorized", headers, {"error": "unauthorized"})
        except (AuthorizationError, TypeError, ValueError) as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})
        self._audit_sink.record(AuditEvent("allowed", "answered", correlation_ref, self.route_ref, identity.principal_ref, membership.tenant_ref))
        return self._respond(start_response, "200 OK", headers, {
            "answer": result.answer, "source_ref": result.source_ref,
            "human_sales_recommended": result.human_sales_recommended, "correlation_ref": correlation_ref,
            "conversation_ref": conversation.conversation_ref,
        })

    @staticmethod
    def _conversation_ref(tenant_ref: str, session_ref: str) -> str:
        return hashlib.sha256(f"sales:{tenant_ref}:{session_ref}".encode()).hexdigest()

    @staticmethod
    def _request(environ: Mapping[str, object]) -> dict[str, str]:
        raw = cast(object, environ.get("wsgi.input"))
        length = int(cast(str, environ.get("CONTENT_LENGTH", "0")))
        if not hasattr(raw, "read") or length < 2:
            raise TypeError("invalid_request")
        value = json.loads(raw.read(length).decode("utf-8"))
        if not isinstance(value, dict) or set(value) != {"agent_ref", "session_ref", "question"}:
            raise ValueError("invalid_request")
        if not all(isinstance(value.get(name), str) and value[name] for name in value):
            raise ValueError("invalid_request")
        return cast(dict[str, str], value)

    @staticmethod
    def _respond(start_response: Callable[..., object], status: str, headers: list[tuple[str, str]], body: object) -> list[bytes]:
        encoded = json.dumps(body, separators=(",", ":")).encode("utf-8")
        start_response(status, [*headers, ("Content-Length", str(len(encoded)))])
        return [encoded]

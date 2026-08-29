"""Authorized tenant-scoped support conversation history."""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable, Mapping
from typing import Protocol, cast

from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)


class ConversationHistoryStore(Protocol):
    def list(self, scope: TenantScope, kind: str, limit: int = 25) -> list[VersionedRecord]: ...


class AdminConversationsApi:
    route_ref = "operator.conversation-history.v1"
    required_permission = "operator.status.read"

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        audit_sink: AuditSink,
        store: ConversationHistoryStore,
        environment_ref: str,
    ) -> None:
        self._verifier, self._memberships, self._audit_sink = verifier, memberships, audit_sink
        self._store, self._environment_ref = store, environment_ref

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = str(uuid.uuid4())
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        try:
            if (
                environ.get("REQUEST_METHOD") != "GET"
                or environ.get("PATH_INFO") != "/v1/admin/conversations"
            ):
                return self._respond(
                    start_response, "404 Not Found", headers, {"error": "not_found"}
                )
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if (
                self.required_permission not in membership.permissions
                or self.required_permission not in identity.granted_permissions
            ):
                raise AuthorizationError("insufficient_permission")
            scope = TenantScope(membership.tenant_ref, self._environment_ref, correlation_ref)
            records = self._store.list(scope, "conversation")
            actions = {
                record.record_ref: record.payload for record in self._store.list(scope, "action")
            }
            conversations = [
                {
                    "conversation_ref": record.record_ref,
                    "messages": record.payload.get("transcript", []),
                    "status": self._status(record.payload.get("turn_outcomes", {})),
                    # An escalation uses the canonical conversation reference as its
                    # idempotency reference.  Expose only the saved result for this
                    # tenant; the UI must not infer ticket state from local memory.
                    "ticket_ref": self._ticket_ref(actions.get(record.record_ref)),
                    "ticket_outcome": self._ticket_outcome(actions.get(record.record_ref)),
                    "ticket_reason": self._ticket_reason(actions.get(record.record_ref)),
                }
                for record in records
            ]
            self._audit_sink.record(
                AuditEvent(
                    "allowed",
                    "history_viewed",
                    correlation_ref,
                    self.route_ref,
                    identity.principal_ref,
                    membership.tenant_ref,
                )
            )
            return self._respond(
                start_response, "200 OK", headers, {"conversations": conversations}
            )
        except AuthenticationError:
            return self._respond(
                start_response, "401 Unauthorized", headers, {"error": "unauthorized"}
            )
        except AuthorizationError:
            return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})

    @staticmethod
    def _status(outcomes: object) -> str:
        if not isinstance(outcomes, dict):
            return "needs attention"
        values = set(outcomes.values())
        if values & {"pending", "failed", "uncertain"}:
            return "needs attention"
        return "resolved" if values else "new"

    @staticmethod
    def _ticket_ref(action: object) -> str | None:
        if not isinstance(action, dict):
            return None
        ticket_ref = action.get("ticket_ref")
        return ticket_ref if isinstance(ticket_ref, str) and ticket_ref else None

    @staticmethod
    def _ticket_outcome(action: object) -> str | None:
        if not isinstance(action, dict):
            return None
        outcome = action.get("outcome")
        return outcome if outcome in {"succeeded", "failed", "uncertain"} else None

    @staticmethod
    def _ticket_reason(action: object) -> str | None:
        if not isinstance(action, dict):
            return None
        reason = action.get("reason")
        return reason if isinstance(reason, str) and reason.startswith("jira_") else None

    @staticmethod
    def _respond(
        start_response: Callable[..., object],
        status: str,
        headers: list[tuple[str, str]],
        body: object,
    ) -> list[bytes]:
        encoded = json.dumps(body, separators=(",", ":")).encode()
        start_response(status, [*headers, ("Content-Length", str(len(encoded)))])
        return [encoded]

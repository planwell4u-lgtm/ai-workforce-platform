"""B8 tenant-scoped operator status view and escalation request."""

from __future__ import annotations

from dataclasses import dataclass


class OperatorDenied(PermissionError):
    pass


@dataclass(frozen=True)
class OperatorView:
    tenant_ref: str
    agent_version_ref: str
    conversation_ref: str
    ticket_outcome: str


@dataclass(frozen=True)
class EscalationRequest:
    tenant_ref: str
    conversation_ref: str
    ticket_idempotency_ref: str
    reason: str


class OperatorJourney:
    view_permission = "operator.status.read"
    escalate_permission = "operator.support-ticket.escalate"

    def view(
        self, view: OperatorView, tenant_ref: str, permissions: frozenset[str]
    ) -> OperatorView:
        if self.view_permission not in permissions or view.tenant_ref != tenant_ref:
            raise OperatorDenied("operator_view_not_authorized")
        return view

    def request_escalation(
        self, request: EscalationRequest, tenant_ref: str, permissions: frozenset[str]
    ) -> str:
        if (
            self.escalate_permission not in permissions
            or request.tenant_ref != tenant_ref
            or not request.reason
        ):
            raise OperatorDenied("operator_escalation_not_authorized")
        return "requested"

"""Authorized, idempotent Jira Service Management support-ticket action."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Literal
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ActionOutcome = Literal["pending", "succeeded", "failed", "uncertain"]


class ActionDenied(PermissionError):
    pass


class JiraRequestRejected(RuntimeError):
    """Jira definitively refused a request, so a ticket was not created."""


class JiraRequestUncertain(RuntimeError):
    """Jira did not provide enough evidence to determine the ticket outcome."""


@dataclass(frozen=True)
class SupportTicketRequest:
    tenant_ref: str
    conversation_ref: str
    idempotency_ref: str
    summary: str


@dataclass(frozen=True)
class SupportTicketResult:
    outcome: ActionOutcome
    idempotency_ref: str
    ticket_ref: str | None = None


@dataclass(frozen=True)
class JiraServiceManagementSettings:
    site_url: str
    cloud_id: str
    service_desk_id: str
    request_type_id: str
    api_token: str

    @classmethod
    def from_environment(cls, environment: Mapping[str, str]) -> JiraServiceManagementSettings:
        required = (
            "JIRA_SITE_URL",
            "JIRA_CLOUD_ID",
            "JIRA_SERVICE_DESK_ID",
            "JIRA_REQUEST_TYPE_ID",
            "JIRA_API_TOKEN",
        )
        missing = [name for name in required if not environment.get(name)]
        if missing:
            raise ValueError(f"missing Jira configuration: {', '.join(missing)}")
        site_url = environment["JIRA_SITE_URL"].rstrip("/")
        if not site_url.startswith("https://") or not site_url.endswith(".atlassian.net"):
            raise ValueError("JIRA_SITE_URL must be an Atlassian Cloud HTTPS site URL")
        return cls(
            site_url,
            environment["JIRA_CLOUD_ID"],
            environment["JIRA_SERVICE_DESK_ID"],
            environment["JIRA_REQUEST_TYPE_ID"],
            environment["JIRA_API_TOKEN"],
        )


HttpRequest = Callable[[Request, float], object]


class JiraServiceManagementClient:
    """Small client for Jira's create-customer-request endpoint."""

    def __init__(
        self, settings: JiraServiceManagementSettings, request: HttpRequest = urlopen
    ) -> None:
        self._settings = settings
        self._request = request

    def create_request(self, request: SupportTicketRequest) -> str:
        payload = json.dumps(
            {
                "serviceDeskId": self._settings.service_desk_id,
                "requestTypeId": self._settings.request_type_id,
                "requestFieldValues": {
                    "summary": request.summary,
                    "description": (
                        f"Tenant: {request.tenant_ref}\n"
                        f"Conversation: {request.conversation_ref}\n"
                        f"Idempotency reference: {request.idempotency_ref}"
                    ),
                },
            }
        ).encode("utf-8")
        http_request = Request(
            "https://api.atlassian.com/ex/jira/"
            f"{self._settings.cloud_id}/rest/servicedeskapi/request",
            data=payload,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self._settings.api_token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with self._request(http_request, timeout=10.0) as response:
                body = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            raise JiraRequestRejected(f"jira_rejected_{error.code}") from error
        except (TimeoutError, URLError, OSError, ValueError, json.JSONDecodeError) as error:
            raise JiraRequestUncertain("jira_request_outcome_unknown") from error
        ticket_ref = body.get("issueKey")
        if not isinstance(ticket_ref, str) or not ticket_ref:
            raise JiraRequestUncertain("jira_response_missing_issue_key")
        return ticket_ref


class JiraSupportTicketAction:
    """Create a Jira customer request only after authorization and validation."""

    required_permission = "integration.support-ticket.create"

    def __init__(self, client: JiraServiceManagementClient) -> None:
        self._client = client
        self._results: dict[str, SupportTicketResult] = {}

    def request(
        self, request: SupportTicketRequest, permissions: frozenset[str]
    ) -> SupportTicketResult:
        if self.required_permission not in permissions:
            raise ActionDenied("support_ticket_not_authorized")
        if not all(
            (request.tenant_ref, request.conversation_ref, request.idempotency_ref, request.summary)
        ):
            return SupportTicketResult("failed", request.idempotency_ref)
        existing = self._results.get(request.idempotency_ref)
        if existing is not None:
            return existing
        try:
            result = SupportTicketResult(
                "succeeded", request.idempotency_ref, self._client.create_request(request)
            )
        except JiraRequestRejected:
            result = SupportTicketResult("failed", request.idempotency_ref)
        except JiraRequestUncertain:
            result = SupportTicketResult("uncertain", request.idempotency_ref)
        self._results[request.idempotency_ref] = result
        return result


def create_jira_support_ticket_action(
    environment: Mapping[str, str],
) -> JiraSupportTicketAction:
    """Create the configured staging Jira action without exposing its credential."""
    return JiraSupportTicketAction(
        JiraServiceManagementClient(JiraServiceManagementSettings.from_environment(environment))
    )


class LocalSupportTicketAction:
    required_permission = "integration.support-ticket.create"

    def __init__(self) -> None:
        self._results: dict[str, SupportTicketResult] = {}

    def request(
        self, request: SupportTicketRequest, permissions: frozenset[str]
    ) -> SupportTicketResult:
        if self.required_permission not in permissions:
            raise ActionDenied("support_ticket_not_authorized")
        if not all(
            (request.tenant_ref, request.conversation_ref, request.idempotency_ref, request.summary)
        ):
            return SupportTicketResult("failed", request.idempotency_ref)
        existing = self._results.get(request.idempotency_ref)
        if existing is not None:
            return existing
        result = SupportTicketResult("pending", request.idempotency_ref)
        self._results[request.idempotency_ref] = result
        return result

    def reconcile(
        self, idempotency_ref: str, provider_outcome: Literal["accepted", "failed", "timeout"]
    ) -> SupportTicketResult:
        current = self._results[idempotency_ref]
        if current.outcome != "pending":
            return current
        if provider_outcome == "accepted":
            result = SupportTicketResult("succeeded", idempotency_ref, f"ticket:{idempotency_ref}")
        elif provider_outcome == "failed":
            result = SupportTicketResult("failed", idempotency_ref)
        else:
            result = SupportTicketResult("uncertain", idempotency_ref)
        self._results[idempotency_ref] = result
        return result

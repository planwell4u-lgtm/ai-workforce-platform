"""Jira Service Management support-ticket action tests."""

from __future__ import annotations

import json
import sys
import unittest
from io import BytesIO
from pathlib import Path
from typing import Self
from unittest.mock import Mock
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "integration" / "python" / "src"))

from ai_workforce_integration.support_ticket import (
    ActionDenied,
    JiraServiceManagementClient,
    JiraServiceManagementSettings,
    JiraSupportTicketAction,
    SupportTicketRequest,
)

SETTINGS = JiraServiceManagementSettings(
    "https://example.atlassian.net", "cloud-123", "67", "69", "secret"
)
REQUEST = SupportTicketRequest("tenant-a", "conversation-a", "request-1", "Need support")
PERMISSION = frozenset({"integration.support-ticket.create"})


class Response:
    def __init__(self, body: dict[str, object]) -> None:
        self._body = json.dumps(body).encode("utf-8")

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self._body


class JiraSupportTicketActionTests(unittest.TestCase):
    def test_success_creates_a_customer_request_once_and_returns_the_issue_key(self) -> None:
        sender = Mock(return_value=Response({"issueKey": "CS-3"}))
        action = JiraSupportTicketAction(JiraServiceManagementClient(SETTINGS, sender))
        result = action.request(REQUEST, PERMISSION)
        self.assertEqual(result.ticket_ref, "CS-3")
        self.assertEqual(result.outcome, "succeeded")
        self.assertEqual(action.request(REQUEST, PERMISSION), result)
        sender.assert_called_once()
        sent_request = sender.call_args.args[0]
        self.assertEqual(
            sent_request.full_url,
            "https://api.atlassian.com/ex/jira/cloud-123/rest/servicedeskapi/request",
        )
        self.assertEqual(
            json.loads(sent_request.data),
            {
                "serviceDeskId": "67",
                "requestTypeId": "69",
                "requestFieldValues": {
                    "summary": "Need support",
                    "description": (
                        "Tenant: tenant-a\nConversation: conversation-a\nIdempotency reference: request-1"
                    ),
                },
            },
        )

    def test_authorization_rejection_and_ambiguous_delivery_are_safe(self) -> None:
        action = JiraSupportTicketAction(JiraServiceManagementClient(SETTINGS, Mock()))
        with self.assertRaises(ActionDenied):
            action.request(REQUEST, frozenset())
        rejected_sender = Mock(side_effect=HTTPError("url", 400, "bad request", {}, BytesIO()))
        rejected = JiraSupportTicketAction(JiraServiceManagementClient(SETTINGS, rejected_sender))
        rejected_result = rejected.request(REQUEST, PERMISSION)
        self.assertEqual((rejected_result.outcome, rejected_result.reason), ("failed", "jira_rejected_400"))
        uncertain_sender = Mock(side_effect=URLError("unavailable"))
        uncertain = JiraSupportTicketAction(JiraServiceManagementClient(SETTINGS, uncertain_sender))
        uncertain_result = uncertain.request(REQUEST, PERMISSION)
        self.assertEqual((uncertain_result.outcome, uncertain_result.reason), ("uncertain", "jira_request_outcome_unknown"))

    def test_settings_require_an_atlassian_cloud_secret_configuration(self) -> None:
        with self.assertRaises(ValueError):
            JiraServiceManagementSettings.from_environment({})
        with self.assertRaises(ValueError):
            JiraServiceManagementSettings.from_environment(
                {
                    "JIRA_SITE_URL": "http://not-atlassian.example",
                    "JIRA_CLOUD_ID": "cloud-123",
                    "JIRA_SERVICE_DESK_ID": "67",
                    "JIRA_REQUEST_TYPE_ID": "69",
                    "JIRA_API_TOKEN": "secret",
                }
            )

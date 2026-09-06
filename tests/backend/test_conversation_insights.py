"""Unit tests for ConversationInsightsGenerator and ConversationInsightsApi."""

import io
import json
import unittest
from typing import Any
from unittest.mock import MagicMock

from ai_workforce_backend.conversation_insights import (
    ConversationInsightsApi,
    ConversationInsightsGenerator,
)


class TestConversationInsightsGenerator(unittest.TestCase):
    def test_analyze_billing_positive(self) -> None:
        messages = [
            {"role": "user", "content": "How do I download my payment invoice for the subscription?"},
            {"role": "assistant", "content": "Thank you! Your invoice was generated and fixed perfectly."},
        ]
        insight = ConversationInsightsGenerator.analyze(
            tenant_ref="tenant-123",
            conversation_ref="conv-001",
            messages=messages,
            channel="web",
        )
        self.assertEqual(insight.tenant_ref, "tenant-123")
        self.assertEqual(insight.conversation_ref, "conv-001")
        self.assertEqual(insight.intent, "Billing & Subscription")
        self.assertEqual(insight.sentiment, "positive")
        self.assertGreater(insight.sentiment_score, 0)
        self.assertEqual(insight.resolution_status, "resolved")
        self.assertIn("Verify customer billing status", insight.action_items[0])

    def test_analyze_support_negative(self) -> None:
        messages = [
            {"role": "user", "content": "There is a terrible error and bug in the system! I need a human agent now."},
            {"role": "assistant", "content": "I apologize for the bad experience."},
        ]
        insight = ConversationInsightsGenerator.analyze(
            tenant_ref="tenant-123",
            conversation_ref="conv-002",
            messages=messages,
            channel="whatsapp",
        )
        self.assertEqual(insight.intent, "Technical Support")
        self.assertEqual(insight.sentiment, "negative")
        self.assertEqual(insight.resolution_status, "needs_followup")
        self.assertIn("Escalate to tier-2 human agent", insight.action_items[0])


class TestConversationInsightsApi(unittest.TestCase):
    def setUp(self) -> None:
        self.verifier = MagicMock()
        self.memberships = MagicMock()
        self.store = MagicMock()
        self.audit_sink = MagicMock()

        principal = MagicMock()
        principal.principal_ref = "auth0|user1"
        self.verifier.verify.return_value = principal

        membership = MagicMock()
        membership.tenant_ref = "staging-demo"
        membership.permissions = frozenset({"platform.owner", "platform.front-desk.configure"})
        self.memberships.resolve.return_value = membership

        self.api = ConversationInsightsApi(
            self.verifier,
            self.memberships,
            self.store,
            self.audit_sink,
        )

    def _call(self, method: str, path: str, body: dict | None = None) -> tuple[int, Any]:
        body_bytes = json.dumps(body).encode("utf-8") if body else b""
        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "HTTP_AUTHORIZATION": "Bearer token",
            "CONTENT_LENGTH": str(len(body_bytes)),
            "wsgi.input": io.BytesIO(body_bytes),
        }
        captured_status = []
        captured_headers = []

        def start_response(status: str, headers: list[tuple[str, str]]) -> None:
            captured_status.append(int(status.split()[0]))
            captured_headers.append(headers)

        response = self.api(environ, start_response)
        data = json.loads(response[0].decode("utf-8")) if response and response[0] else {}
        return captured_status[0], data

    def test_list_insights(self) -> None:
        self.store.list_conversation_insights.return_value = []
        status, data = self._call("GET", "/v1/owner/insights")
        self.assertEqual(status, 200)
        self.assertIn("insights", data)
        self.assertGreater(len(data["insights"]), 0)

    def test_generate_insight(self) -> None:
        payload = {
            "conversation_ref": "conv-test-99",
            "channel": "sms",
            "messages": [
                {"role": "user", "content": "Can I integrate webhooks?"},
                {"role": "assistant", "content": "Yes, configure channel webhooks under setup."},
            ],
        }
        status, data = self._call("POST", "/v1/owner/insights/generate", body=payload)
        self.assertEqual(status, 201)
        self.assertEqual(data["insight"]["intent"], "Integration & Setup")
        self.assertEqual(data["insight"]["channel"], "sms")


if __name__ == "__main__":
    unittest.main()

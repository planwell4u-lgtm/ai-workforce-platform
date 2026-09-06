"""Unit tests for OmnichannelApi endpoints (SMS, WhatsApp, Channel Status & Simulation)."""

import io
import json
import unittest
from typing import Any
from unittest.mock import MagicMock

from ai_workforce_backend.omnichannel_management import OmnichannelApi


class TestOmnichannelApi(unittest.TestCase):
    def setUp(self) -> None:
        self.verifier = MagicMock()
        self.memberships = MagicMock()
        self.store = MagicMock()
        self.audit_sink = MagicMock()
        self.agent = MagicMock()

        # Mock auth identity
        identity = MagicMock()
        identity.principal_ref = "auth0|owner"
        self.verifier.verify.return_value = identity

        # Mock membership
        membership = MagicMock()
        membership.tenant_ref = "staging-demo"
        membership.permissions = frozenset({"platform.owner", "platform.front-desk.configure"})
        self.memberships.resolve.return_value = membership

        # Mock agent decision
        decision = MagicMock()
        decision.answer_text = "Standard delivery takes 3-5 business days."
        self.agent.decide.return_value = decision

        self.api = OmnichannelApi(
            self.verifier,
            self.memberships,
            self.store,
            self.audit_sink,
            self.agent,
            whatsapp_verify_token="test-wa-token",
        )

    def _call(self, method: str, path: str, body: dict | None = None, query: str = "", auth: str = "Bearer test") -> tuple[str, list, Any]:
        body_bytes = json.dumps(body).encode("utf-8") if body else b""
        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "QUERY_STRING": query,
            "HTTP_AUTHORIZATION": auth,
            "CONTENT_LENGTH": str(len(body_bytes)),
            "wsgi.input": io.BytesIO(body_bytes),
        }
        captured_status = ""
        captured_headers = []

        def start_response(status, headers):
            nonlocal captured_status, captured_headers
            captured_status = status
            captured_headers = headers

        res_list = self.api(environ, start_response)
        raw_res = b"".join(res_list).decode("utf-8")
        parsed_res = json.loads(raw_res) if raw_res.startswith("{") or raw_res.startswith("[") else raw_res
        return captured_status, captured_headers, parsed_res

    def test_whatsapp_verification_challenge(self):
        status, _, challenge = self._call("GET", "/v1/channels/whatsapp/webhook", query="hub.mode=subscribe&hub.verify_token=test-wa-token&hub.challenge=998877")
        self.assertEqual(status, "200 OK")
        self.assertEqual(challenge, "998877")

    def test_sms_webhook_ingestion(self):
        form_payload = b"From=%2B15550192834&To=%2B18005550199&Body=What+is+delivery+timeframe%3F"
        environ = {
            "REQUEST_METHOD": "POST",
            "PATH_INFO": "/v1/channels/sms/webhook",
            "CONTENT_LENGTH": str(len(form_payload)),
            "wsgi.input": io.BytesIO(form_payload),
        }
        captured_status = ""
        def start_response(status, headers):
            nonlocal captured_status
            captured_status = status

        res = b"".join(self.api(environ, start_response)).decode("utf-8")
        self.assertEqual(captured_status, "200 OK")
        self.assertIn("<Response><Message>Standard delivery takes 3-5 business days.</Message></Response>", res)

    def test_channel_status_endpoint(self):
        self.store.list_knowledge_articles.return_value = [MagicMock()]
        status, _, data = self._call("GET", "/v1/owner/channels/status")
        self.assertEqual(status, "200 OK")
        self.assertEqual(data["tenant_ref"], "staging-demo")
        self.assertEqual(len(data["channels"]), 4)

    def test_channel_test_simulation(self):
        status, _, data = self._call("POST", "/v1/owner/channels/test-simulate", body={"channel": "sms", "sender": "+15550192834", "message": "What is delivery timeframe?"})
        self.assertEqual(status, "200 OK")
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["agent_answer"], "Standard delivery takes 3-5 business days.")
        self.assertIn("twiml_xml", data["formatted_outbound"])

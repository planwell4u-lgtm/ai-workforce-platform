"""Unit tests for TwilioVoiceAdapter and VoiceManagementApi."""

import io
import json
import unittest
from unittest.mock import MagicMock

from ai_workforce_backend.voice_management import VoiceManagementApi
from ai_workforce_digital_channel.voice_adapter import TwilioVoiceAdapter


class TestVoiceManagement(unittest.TestCase):
    def setUp(self) -> None:
        self.verifier = MagicMock()
        self.memberships = MagicMock()
        self.store = MagicMock()
        self.audit_sink = MagicMock()

        # Mock auth identity
        identity = MagicMock()
        identity.principal_ref = "auth0|owner"
        self.verifier.verify.return_value = identity

        # Mock membership
        membership = MagicMock()
        membership.tenant_ref = "staging-demo"
        membership.permissions = frozenset({"platform.owner", "platform.front-desk.configure"})
        self.memberships.resolve.return_value = membership

        self.api = VoiceManagementApi(
            self.verifier,
            self.memberships,
            self.store,
            self.audit_sink,
            stream_url="wss://voice.planwell.online",
        )

    def test_parse_incoming_call_and_twiml_generation(self) -> None:
        form = {
            "From": ["+15005550006"],
            "To": ["+18005550199"],
            "CallSid": ["CA123456789"],
            "CallStatus": ["ringing"],
            "CallDuration": ["125"],
        }
        parsed = TwilioVoiceAdapter.parse_incoming_call(form)
        self.assertEqual(parsed["from"], "+15005550006")
        self.assertEqual(parsed["to"], "+18005550199")
        self.assertEqual(parsed["duration_seconds"], "125")

        billable = TwilioVoiceAdapter.calculate_billable_minutes(125)
        self.assertEqual(billable, 3)

        twiml = TwilioVoiceAdapter.build_twiml_response(
            stream_url="wss://voice.planwell.online"
        )
        self.assertIn("Response", twiml)
        self.assertIn("Stream", twiml)
        self.assertIn("wss://voice.planwell.online", twiml)

    def test_voice_management_api_incoming_call(self) -> None:
        form_payload = b"From=%2B15005550006&To=%2B18005550199&CallSid=CA999&CallDuration=45"
        environ = {
            "PATH_INFO": "/v1/channels/voice/incoming",
            "REQUEST_METHOD": "POST",
            "CONTENT_LENGTH": str(len(form_payload)),
            "wsgi.input": io.BytesIO(form_payload),
        }

        captured_status = ""
        def start_response(status, headers):
            nonlocal captured_status
            captured_status = status

        body = b"".join(self.api(environ, start_response)).decode("utf-8")
        self.assertEqual(captured_status, "200 OK")
        self.assertIn("<Response>", body)
        self.assertIn("Planwell AI Voice Support", body)

    def test_voice_management_api_get_phone_numbers(self) -> None:
        phone_mock = MagicMock()
        phone_mock.phone_ref = "phone_123"
        phone_mock.phone_number = "+1 (800) 555-0199"
        phone_mock.friendly_name = "Primary Voice Support Line"
        phone_mock.status = "active"
        phone_mock.twiml_url = "https://planwell.online/api/v1/channels/voice/incoming"
        phone_mock.created_at = "2026-09-06T12:00:00Z"

        self.store.list_tenant_phone_numbers.return_value = [phone_mock]
        self.store.list_tenant_voice_call_logs.return_value = []

        environ = {
            "PATH_INFO": "/v1/owner/phone-numbers",
            "REQUEST_METHOD": "GET",
            "HTTP_AUTHORIZATION": "Bearer valid_token",
        }

        captured_status = ""
        def start_response(status, headers):
            nonlocal captured_status
            captured_status = status

        res = b"".join(self.api(environ, start_response)).decode("utf-8")
        self.assertEqual(captured_status, "200 OK")
        data = json.loads(res)
        self.assertEqual(len(data["phone_numbers"]), 1)
        self.assertEqual(data["phone_numbers"][0]["phone_number"], "+1 (800) 555-0199")

    def test_voice_management_api_unauthorized_get(self) -> None:
        self.verifier.verify.side_effect = Exception("unauthorized")
        environ = {
            "PATH_INFO": "/v1/owner/phone-numbers",
            "REQUEST_METHOD": "GET",
        }

        captured_status = ""
        def start_response(status, headers):
            nonlocal captured_status
            captured_status = status

        body = b"".join(self.api(environ, start_response)).decode("utf-8")
        self.assertEqual(captured_status, "401 Unauthorized")
        self.assertIn("unauthorized", body)

    def test_voice_management_api_outbound_dial(self) -> None:
        log_mock = MagicMock()
        log_mock.call_ref = "call_outbound_999"
        self.store.log_tenant_voice_call.return_value = log_mock

        payload = json.dumps({
            "to_number": "+1 (555) 234-5678",
            "from_number": "+1 (800) 555-0199",
            "greeting": "Hello from Planwell Outbound Support",
        }).encode("utf-8")

        environ = {
            "PATH_INFO": "/v1/owner/phone-numbers/outbound-dial",
            "REQUEST_METHOD": "POST",
            "HTTP_AUTHORIZATION": "Bearer valid_token",
            "CONTENT_LENGTH": str(len(payload)),
            "wsgi.input": io.BytesIO(payload),
        }

        captured_status = ""
        def start_response(status, headers):
            nonlocal captured_status
            captured_status = status

        res = b"".join(self.api(environ, start_response)).decode("utf-8")
        self.assertEqual(captured_status, "200 OK")
        data = json.loads(res)
        self.assertEqual(data["status"], "outbound_call_initiated")
        self.assertEqual(data["to_number"], "+1 (555) 234-5678")
        outbound_payload = TwilioVoiceAdapter.build_outbound_call_payload("+1555", "+1800")
        self.assertEqual(outbound_payload["To"], "+1555")
        self.assertEqual(outbound_payload["From"], "+1800")

    def test_voice_management_api_voice_respond(self) -> None:
        agent_mock = MagicMock()
        answer_mock = MagicMock()
        answer_mock.answer = "Our operating hours are Monday through Friday 9 AM to 6 PM."
        agent_mock.answer.return_value = answer_mock
        self.api._agent = agent_mock

        form_payload = b"SpeechResult=What+are+your+operating+hours%3F"
        environ = {
            "PATH_INFO": "/v1/channels/voice/respond",
            "REQUEST_METHOD": "POST",
            "CONTENT_LENGTH": str(len(form_payload)),
            "wsgi.input": io.BytesIO(form_payload),
        }

        captured_status = ""
        def start_response(status, headers):
            nonlocal captured_status
            captured_status = status

        body = b"".join(self.api(environ, start_response)).decode("utf-8")
        self.assertEqual(captured_status, "200 OK")
        self.assertIn("<Gather", body)
        self.assertIn("Our operating hours are Monday through Friday", body)


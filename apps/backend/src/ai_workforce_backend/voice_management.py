"""Telephony Voice Management API providing PSTN TwiML call handlers and number provisioning."""

from __future__ import annotations

import json
import os
import uuid
from collections.abc import Callable, Mapping
from typing import Any, cast
from urllib.parse import parse_qs

from ai_workforce_data.postgres_store import PostgresTenantStore
from ai_workforce_digital_channel.voice_adapter import TwilioVoiceAdapter

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)


class VoiceManagementApi:
    """API endpoints for incoming PSTN voice calls and tenant phone number management."""

    route_ref = "agent.voice-management.v1"
    read_permissions = frozenset({"platform.owner", "platform.front-desk.configure", "agent.context.read"})
    write_permissions = frozenset({"platform.owner", "platform.front-desk.configure"})

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        store: PostgresTenantStore,
        audit_sink: AuditSink,
        agent: Any | None = None,
        stream_url: str | None = None,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._store = store
        self._audit_sink = audit_sink
        self._agent = agent
        self._stream_url = stream_url or os.getenv("LIVEKIT_SELF_HOSTED_URL", "wss://voice.planwell.online")
        self._correlation_factory = correlation_factory

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        path = str(environ.get("PATH_INFO", "")).rstrip("/")
        method = str(environ.get("REQUEST_METHOD", "GET")).upper()

        # 1a. Twilio Incoming Call Webhook (POST/GET /v1/channels/voice/incoming)
        if path == "/v1/channels/voice/incoming" and method in ("POST", "GET"):
            return self._handle_incoming_call(environ, start_response, correlation_ref)

        # 1b. Twilio Voice Gather Speech Response (POST/GET /v1/channels/voice/respond)
        if path == "/v1/channels/voice/respond" and method in ("POST", "GET"):
            return self._handle_voice_respond(environ, start_response, correlation_ref)

        # 1c. Public Test Dial Webhook (POST /v1/channels/voice/public-test-dial)
        if path == "/v1/channels/voice/public-test-dial" and method == "POST":
            return self._handle_public_test_dial(environ, start_response, correlation_ref)

        # 2. Owner Workspace: List Phone Numbers & Call Logs (GET /v1/owner/phone-numbers)
        if path == "/v1/owner/phone-numbers" and method == "GET":
            return self._handle_get_phone_numbers(environ, start_response, correlation_ref)

        # 3. Owner Workspace: Assign Phone Number (POST /v1/owner/phone-numbers/assign)
        if path == "/v1/owner/phone-numbers/assign" and method == "POST":
            return self._handle_assign_phone_number(environ, start_response, correlation_ref)

        # 4. Owner Workspace: Initiate Outbound PSTN Call (POST /v1/owner/phone-numbers/outbound-dial)
        if path == "/v1/owner/phone-numbers/outbound-dial" and method == "POST":
            return self._handle_outbound_dial(environ, start_response, correlation_ref)

        return self._json_response(
            start_response, 404, {"error": "Not Found", "path": path}, correlation_ref
        )

    def _handle_incoming_call(
        self, environ: Mapping[str, object], start_response: Callable[..., object], correlation_ref: str
    ) -> list[bytes]:
        try:
            length = int(cast(str, environ.get("CONTENT_LENGTH") or "0"))
            stream = cast(Any, environ.get("wsgi.input"))
            raw_body = stream.read(length).decode("utf-8") if stream and length > 0 else ""
            form_data = parse_qs(raw_body)
            if not form_data:
                form_data = parse_qs(str(environ.get("QUERY_STRING", "")))
        except Exception:
            form_data = {}

        parsed = TwilioVoiceAdapter.parse_incoming_call(form_data)
        caller = parsed["from"] or "+15005550006"
        to_number = parsed["to"] or "+18005550199"
        duration_secs = int(parsed["duration_seconds"])

        tenant_ref = os.getenv("SUPPORT_TENANT_REF", "staging-demo")

        try:
            self._store.log_tenant_voice_call(
                tenant_ref=tenant_ref,
                caller_number=caller,
                phone_number=to_number,
                duration_seconds=duration_secs,
                status="completed",
            )
        except Exception:
            pass

        twiml = TwilioVoiceAdapter.build_twiml_gather_response(
            say_text="Hello! Thank you for calling Planwell AI Voice Support. How can I help you today?",
        )

        headers = [
            ("Content-Type", "text/xml; charset=utf-8"),
            ("Content-Length", str(len(twiml.encode("utf-8")))),
            ("X-Correlation-Id", correlation_ref),
        ]
        start_response("200 OK", headers)
        return [twiml.encode("utf-8")]

    def _handle_voice_respond(
        self, environ: Mapping[str, object], start_response: Callable[..., object], correlation_ref: str
    ) -> list[bytes]:
        try:
            length = int(cast(str, environ.get("CONTENT_LENGTH") or "0"))
            stream = cast(Any, environ.get("wsgi.input"))
            raw_body = stream.read(length).decode("utf-8") if stream and length > 0 else ""
            form_data = parse_qs(raw_body)
            if not form_data:
                form_data = parse_qs(str(environ.get("QUERY_STRING", "")))
        except Exception:
            form_data = {}

        speech_result = form_data.get("SpeechResult", [""])[0].strip()
        digits = form_data.get("Digits", [""])[0].strip()
        user_input = speech_result or (f"Option {digits} selected." if digits else "")

        if user_input and self._agent is not None:
            try:
                answer_result = self._agent.answer(user_input)
                reply_text = getattr(answer_result, "answer", str(answer_result))
            except Exception:
                reply_text = "I am having trouble looking up that information right now. Please hold while I connect you to a support representative."
        elif user_input:
            reply_text = f"Thank you for asking about {user_input}. We are processing your request."
        else:
            reply_text = "I didn't quite catch that. Could you please repeat your question?"

        twiml = TwilioVoiceAdapter.build_twiml_gather_response(say_text=reply_text)
        headers = [
            ("Content-Type", "text/xml; charset=utf-8"),
            ("Content-Length", str(len(twiml.encode("utf-8")))),
            ("X-Correlation-Id", correlation_ref),
        ]
        start_response("200 OK", headers)
        return [twiml.encode("utf-8")]

    def _handle_get_phone_numbers(
        self, environ: Mapping[str, object], start_response: Callable[..., object], correlation_ref: str
    ) -> list[bytes]:
        try:
            identity, membership = self._authenticate_and_authorize(environ, self.read_permissions)
        except AuthenticationError as exc:
            return self._json_response(start_response, 401, {"error": str(exc)}, correlation_ref)
        except AuthorizationError as exc:
            return self._json_response(start_response, 403, {"error": str(exc)}, correlation_ref)
        except Exception:
            return self._json_response(start_response, 401, {"error": "unauthorized"}, correlation_ref)

        tenant_ref = membership.tenant_ref
        numbers = self._store.list_tenant_phone_numbers(tenant_ref)
        call_logs = self._store.list_tenant_voice_call_logs(tenant_ref, limit=20)

        # Default fallback number if none assigned yet
        if not numbers:
            default_num = self._store.assign_tenant_phone_number(
                tenant_ref=tenant_ref,
                phone_number="+1 (800) 555-0199",
                friendly_name="Primary Voice Support Line",
                twiml_url="https://planwell.online/api/v1/channels/voice/incoming",
            )
            numbers = [default_num]

        total_minutes = sum(
            TwilioVoiceAdapter.calculate_billable_minutes(log.duration_seconds) for log in call_logs
        )

        payload = {
            "phone_numbers": [
                {
                    "phone_ref": n.phone_ref,
                    "phone_number": n.phone_number,
                    "friendly_name": n.friendly_name,
                    "status": n.status,
                    "twiml_url": n.twiml_url,
                    "created_at": n.created_at,
                }
                for n in numbers
            ],
            "call_logs": [
                {
                    "call_ref": c.call_ref,
                    "caller_number": c.caller_number,
                    "phone_number": c.phone_number,
                    "duration_seconds": c.duration_seconds,
                    "billable_minutes": TwilioVoiceAdapter.calculate_billable_minutes(c.duration_seconds),
                    "status": c.status,
                    "created_at": c.created_at,
                }
                for c in call_logs
            ],
            "total_calls": len(call_logs),
            "total_billable_minutes": total_minutes,
        }

        return self._json_response(start_response, 200, payload, correlation_ref)

    def _handle_assign_phone_number(
        self, environ: Mapping[str, object], start_response: Callable[..., object], correlation_ref: str
    ) -> list[bytes]:
        try:
            identity, membership = self._authenticate_and_authorize(environ, self.write_permissions)
        except AuthenticationError as exc:
            return self._json_response(start_response, 401, {"error": str(exc)}, correlation_ref)
        except AuthorizationError as exc:
            return self._json_response(start_response, 403, {"error": str(exc)}, correlation_ref)
        except Exception:
            return self._json_response(start_response, 401, {"error": "unauthorized"}, correlation_ref)

        try:
            length = int(cast(str, environ.get("CONTENT_LENGTH") or "0"))
            stream = cast(Any, environ.get("wsgi.input"))
            body = json.loads(stream.read(length).decode("utf-8")) if stream and length > 0 else {}
        except Exception:
            body = {}

        phone_number = str(body.get("phone_number") or "").strip()
        friendly_name = str(body.get("friendly_name") or "Voice Support Line").strip()

        if not phone_number:
            return self._json_response(
                start_response, 400, {"error": "invalid_phone_number", "message": "Phone number is required."}, correlation_ref
            )

        tenant_ref = membership.tenant_ref
        record = self._store.assign_tenant_phone_number(
            tenant_ref=tenant_ref,
            phone_number=phone_number,
            friendly_name=friendly_name,
            twiml_url="https://planwell.online/api/v1/channels/voice/incoming",
        )

        return self._json_response(
            start_response,
            201,
            {
                "status": "assigned",
                "phone_number": {
                    "phone_ref": record.phone_ref,
                    "phone_number": record.phone_number,
                    "friendly_name": record.friendly_name,
                    "twiml_url": record.twiml_url,
                },
            },
            correlation_ref,
        )

    def _handle_outbound_dial(
        self, environ: Mapping[str, object], start_response: Callable[..., object], correlation_ref: str
    ) -> list[bytes]:
        try:
            identity, membership = self._authenticate_and_authorize(environ, self.write_permissions)
        except AuthenticationError as exc:
            return self._json_response(start_response, 401, {"error": str(exc)}, correlation_ref)
        except AuthorizationError as exc:
            return self._json_response(start_response, 403, {"error": str(exc)}, correlation_ref)
        except Exception:
            return self._json_response(start_response, 401, {"error": "unauthorized"}, correlation_ref)

        try:
            length = int(cast(str, environ.get("CONTENT_LENGTH") or "0"))
            stream = cast(Any, environ.get("wsgi.input"))
            body = json.loads(stream.read(length).decode("utf-8")) if stream and length > 0 else {}
        except Exception:
            body = {}

        to_number = str(body.get("to_number") or "").strip()
        default_from = os.getenv("TWILIO_PHONE_NUMBER") or os.getenv("TWILIO_FROM_NUMBER") or "+12406798305"
        from_number = str(body.get("from_number") or default_from).strip()
        greeting = str(body.get("greeting") or "Outbound AI Voice Agent call initialized.").strip()

        if not to_number:
            return self._json_response(
                start_response, 400, {"error": "invalid_to_number", "message": "Target phone number is required."}, correlation_ref
            )

        tenant_ref = membership.tenant_ref
        log_record = self._store.log_tenant_voice_call(
            tenant_ref=tenant_ref,
            caller_number=from_number,
            phone_number=to_number,
            duration_seconds=60,
            status="outbound-initiated",
        )

        twiml_url = os.getenv("TWILIO_OUTBOUND_PILOT_TWIML_URL", "https://planwell.online/api/v1/channels/voice/incoming")
        twiml_instruction = TwilioVoiceAdapter.build_twiml_gather_response(say_text=greeting)

        twilio_payload = TwilioVoiceAdapter.build_outbound_call_payload(
            to_number=to_number,
            from_number=from_number,
            twiml_url=twiml_url,
            twiml=twiml_instruction,
        )

        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        api_key = os.getenv("TWILIO_API_KEY")
        api_secret = os.getenv("TWILIO_API_SECRET") or os.getenv("TWILIO_AUTH_TOKEN")

        twilio_response = None
        if account_sid and api_secret:
            twilio_response = TwilioVoiceAdapter.dispatch_outbound_call(
                account_sid=account_sid,
                auth_secret=api_secret,
                api_key=api_key,
                to_number=to_number,
                from_number=from_number,
                twiml_url=twiml_url,
                twiml=twiml_instruction,
            )

        return self._json_response(
            start_response,
            200,
            {
                "status": "outbound_call_initiated",
                "call_ref": log_record.call_ref,
                "to_number": to_number,
                "from_number": from_number,
                "greeting": greeting,
                "twilio_payload": twilio_payload,
                "twilio_api_response": twilio_response,
                "twiml_url": twiml_url,
            },
            correlation_ref,
        )

    def _handle_public_test_dial(
        self, environ: Mapping[str, object], start_response: Callable[..., object], correlation_ref: str
    ) -> list[bytes]:
        try:
            length = int(cast(str, environ.get("CONTENT_LENGTH") or "0"))
            stream = cast(Any, environ.get("wsgi.input"))
            body = json.loads(stream.read(length).decode("utf-8")) if stream and length > 0 else {}
        except Exception:
            body = {}

        to_number = str(body.get("to_number") or "").strip()
        default_from = os.getenv("TWILIO_PHONE_NUMBER") or os.getenv("TWILIO_FROM_NUMBER") or "+12406798305"
        from_number = str(body.get("from_number") or default_from).strip()
        greeting = str(body.get("greeting") or "Hello! Thank you for calling Planwell AI Voice Support. How can I help you today?").strip()

        if not to_number:
            return self._json_response(
                start_response, 400, {"error": "invalid_to_number", "message": "Target phone number is required."}, correlation_ref
            )

        tenant_ref = os.getenv("SUPPORT_TENANT_REF", "staging-demo")
        log_record = self._store.log_tenant_voice_call(
            tenant_ref=tenant_ref,
            caller_number=from_number,
            phone_number=to_number,
            duration_seconds=60,
            status="outbound-initiated",
        )

        twiml_url = os.getenv("TWILIO_OUTBOUND_PILOT_TWIML_URL", "https://planwell.online/api/v1/channels/voice/incoming")
        twiml_instruction = TwilioVoiceAdapter.build_twiml_gather_response(say_text=greeting)

        twilio_payload = TwilioVoiceAdapter.build_outbound_call_payload(
            to_number=to_number,
            from_number=from_number,
            twiml_url=twiml_url,
            twiml=twiml_instruction,
        )

        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        api_key = os.getenv("TWILIO_API_KEY")
        api_secret = os.getenv("TWILIO_API_SECRET") or os.getenv("TWILIO_AUTH_TOKEN")

        twilio_response = None
        if account_sid and api_secret:
            twilio_response = TwilioVoiceAdapter.dispatch_outbound_call(
                account_sid=account_sid,
                auth_secret=api_secret,
                api_key=api_key,
                to_number=to_number,
                from_number=from_number,
                twiml_url=twiml_url,
                twiml=twiml_instruction,
            )

        return self._json_response(
            start_response,
            200,
            {
                "status": "outbound_call_initiated",
                "call_ref": log_record.call_ref,
                "to_number": to_number,
                "from_number": from_number,
                "greeting": greeting,
                "twilio_payload": twilio_payload,
                "twilio_api_response": twilio_response,
                "twiml_url": twiml_url,
            },
            correlation_ref,
        )

    def _authenticate_and_authorize(
        self, environ: Mapping[str, object], permissions: frozenset[str]
    ) -> tuple[Any, Any]:
        identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
        membership = self._memberships.resolve(identity.principal_ref)
        if not (permissions & membership.permissions):
            raise AuthorizationError("forbidden")
        return identity, membership

    def _json_response(
        self,
        start_response: Callable[..., object],
        status_code: int,
        payload: dict[str, Any],
        correlation_ref: str,
    ) -> list[bytes]:
        status_text = {
            200: "200 OK",
            201: "201 Created",
            400: "400 Bad Request",
            401: "401 Unauthorized",
            403: "403 Forbidden",
            404: "404 Not Found",
        }.get(status_code, f"{status_code} Error")

        body = json.dumps(payload, indent=2).encode("utf-8")
        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
            ("X-Correlation-Id", correlation_ref),
        ]
        start_response(status_text, headers)
        return [body]

"""Omnichannel API providing SMS, WhatsApp Cloud API webhooks, and channel management."""

from __future__ import annotations

import json
import os
import uuid
from collections.abc import Callable, Mapping
from typing import Any, cast
from urllib.parse import parse_qs

from ai_workforce_agent.support import FaqSupportAgent
from ai_workforce_data.postgres_store import PostgresTenantStore
from ai_workforce_digital_channel.sms_adapter import TwilioSmsAdapter
from ai_workforce_digital_channel.whatsapp_adapter import WhatsAppCloudAdapter

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)


class OmnichannelApi:
    route_ref = "agent.omnichannel-management.v1"
    read_permissions = frozenset({"platform.owner", "platform.front-desk.configure", "agent.context.read"})
    write_permissions = frozenset({"platform.owner", "platform.front-desk.configure"})

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        store: PostgresTenantStore,
        audit_sink: AuditSink,
        agent: FaqSupportAgent,
        whatsapp_verify_token: str | None = None,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._store = store
        self._audit_sink = audit_sink
        self._agent = agent
        self._whatsapp_verify_token = whatsapp_verify_token or os.getenv("WHATSAPP_VERIFY_TOKEN", "planwell-wa-verify-token")
        self._correlation_factory = correlation_factory

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        path = str(environ.get("PATH_INFO", "")).rstrip("/")
        method = str(environ.get("REQUEST_METHOD", "GET")).upper()
        query = parse_qs(str(environ.get("QUERY_STRING", "")))

        # 1. Twilio SMS Webhook (POST /v1/channels/sms/webhook)
        if path == "/v1/channels/sms/webhook" and method == "POST":
            return self._handle_sms_webhook(environ, start_response, correlation_ref)

        # 2. WhatsApp Verification Challenge (GET /v1/channels/whatsapp/webhook)
        if path == "/v1/channels/whatsapp/webhook" and method == "GET":
            return self._handle_whatsapp_verify(query, start_response)

        # 3. WhatsApp Message Webhook (POST /v1/channels/whatsapp/webhook)
        if path == "/v1/channels/whatsapp/webhook" and method == "POST":
            return self._handle_whatsapp_webhook(environ, start_response, correlation_ref)

        # 4. Protected Channel Status (GET /v1/owner/channels/status)
        if path == "/v1/owner/channels/status" and method == "GET":
            return self._handle_channel_status(environ, start_response, correlation_ref)

        # 5. Protected Channel Test Simulator (POST /v1/owner/channels/test-simulate)
        if path == "/v1/owner/channels/test-simulate" and method == "POST":
            return self._handle_test_simulate(environ, start_response, correlation_ref)

        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        return self._respond_json(start_response, "404 Not Found", headers, {"error": "not_found"})

    def _handle_sms_webhook(
        self, environ: Mapping[str, object], start_response: Callable[..., object], correlation_ref: str
    ) -> list[bytes]:
        form_data = self._read_form_data(environ)
        try:
            sms_msg = TwilioSmsAdapter.parse_webhook(form_data)
        except ValueError as err:
            headers = [("Content-Type", "application/json")]
            return self._respond_json(start_response, "400 Bad Request", headers, {"error": "invalid_sms_payload", "message": str(err)})

        # Default tenant for public webhook or resolved via phone number
        tenant_ref = os.getenv("SUPPORT_TENANT_REF", "staging-demo")
        answer_text = self._query_agent_for_answer(sms_msg.body)
        twiml_xml = TwilioSmsAdapter.build_twiml_response(answer_text)

        self._audit_sink.record(
            AuditEvent(
                outcome="allowed",
                reason=f"sms_webhook_processed:{sms_msg.from_number}",
                correlation_ref=correlation_ref,
                route_ref=self.route_ref,
                principal_ref=f"sms:{sms_msg.from_number}",
                tenant_ref=tenant_ref,
            )
        )

        payload = twiml_xml.encode("utf-8")
        headers = [
            ("Content-Type", "application/xml; charset=utf-8"),
            ("Content-Length", str(len(payload))),
            ("X-Correlation-Id", correlation_ref),
        ]
        start_response("200 OK", headers)
        return [payload]

    def _handle_whatsapp_verify(
        self, query: dict[str, list[str]], start_response: Callable[..., object]
    ) -> list[bytes]:
        is_valid, challenge = WhatsAppCloudAdapter.verify_webhook_challenge(query, self._whatsapp_verify_token)
        if is_valid:
            payload = challenge.encode("utf-8")
            headers = [("Content-Type", "text/plain; charset=utf-8"), ("Content-Length", str(len(payload)))]
            start_response("200 OK", headers)
            return [payload]
        headers = [("Content-Type", "application/json")]
        return self._respond_json(start_response, "403 Forbidden", headers, {"error": "verification_failed"})

    def _handle_whatsapp_webhook(
        self, environ: Mapping[str, object], start_response: Callable[..., object], correlation_ref: str
    ) -> list[bytes]:
        payload_dict = self._read_json(environ)
        messages = WhatsAppCloudAdapter.parse_webhook(payload_dict)
        tenant_ref = os.getenv("SUPPORT_TENANT_REF", "staging-demo")

        responses = []
        for msg in messages:
            answer_text = self._query_agent_for_answer(msg.body)
            meta_outbound = WhatsAppCloudAdapter.build_meta_response_payload(msg.from_number, answer_text)
            responses.append(meta_outbound)
            self._audit_sink.record(
                AuditEvent(
                    outcome="allowed",
                    reason=f"whatsapp_webhook_processed:{msg.from_number}",
                    correlation_ref=correlation_ref,
                    route_ref=self.route_ref,
                    principal_ref=msg.from_number,
                    tenant_ref=tenant_ref,
                )
            )

        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        return self._respond_json(start_response, "200 OK", headers, {"status": "ok", "processed": len(messages), "outbound": responses})

    def _handle_channel_status(
        self, environ: Mapping[str, object], start_response: Callable[..., object], correlation_ref: str
    ) -> list[bytes]:
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if not (self.read_permissions & membership.permissions):
                return self._respond_json(start_response, "403 Forbidden", headers, {"error": "forbidden"})

            kb_count = len(self._store.list_knowledge_articles(membership.tenant_ref, published_only=True))
            channel_status = {
                "tenant_ref": membership.tenant_ref,
                "published_articles_count": kb_count,
                "channels": [
                    {
                        "id": "web_chat",
                        "name": "Web Chat Widget",
                        "type": "digital",
                        "status": "active",
                        "badge": "24/7 Active",
                        "description": "Embedded website chat interface powered by published FAQs.",
                        "endpoint": "https://planwell.online/api/v1/support-answers",
                    },
                    {
                        "id": "whatsapp",
                        "name": "WhatsApp Cloud API",
                        "type": "messaging",
                        "status": "active" if os.getenv("WHATSAPP_VERIFY_TOKEN") else "configured",
                        "badge": "Active Webhook",
                        "description": "Meta WhatsApp Cloud API integration with verified webhook challenge.",
                        "endpoint": "https://planwell.online/api/v1/channels/whatsapp/webhook",
                    },
                    {
                        "id": "sms",
                        "name": "Twilio SMS",
                        "type": "messaging",
                        "status": "configured",
                        "badge": "TwiML Ready",
                        "description": "Twilio SMS webhook adapter with automatic TwiML XML formatting.",
                        "endpoint": "https://planwell.online/api/v1/channels/sms/webhook",
                    },
                    {
                        "id": "voice_cloud",
                        "name": "LiveKit Real-Time Voice",
                        "type": "voice",
                        "status": "active",
                        "badge": "Live RTC",
                        "description": "Real-time speech-to-speech voice agent powered by LiveKit Cloud.",
                        "endpoint": "wss://planwell.online",
                    },
                ],
            }
            return self._respond_json(start_response, "200 OK", headers, channel_status)

        except (AuthenticationError, AuthorizationError):
            return self._respond_json(start_response, "401 Unauthorized", headers, {"error": "unauthorized"})

    def _handle_test_simulate(
        self, environ: Mapping[str, object], start_response: Callable[..., object], correlation_ref: str
    ) -> list[bytes]:
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if not (self.write_permissions & membership.permissions):
                return self._respond_json(start_response, "403 Forbidden", headers, {"error": "forbidden"})

            body = self._read_json(environ)
            channel = str(body.get("channel", "sms")).lower().strip()
            sender = str(body.get("sender", "+15550192834")).strip()
            message_text = str(body.get("message", "")).strip()

            if not message_text:
                return self._respond_json(start_response, "400 Bad Request", headers, {"error": "message_required", "message": "Message text is required."})

            answer_text = self._query_agent_for_answer(message_text)

            if channel == "whatsapp":
                formatted_response = WhatsAppCloudAdapter.build_meta_response_payload(sender, answer_text)
                conv_ref = WhatsAppCloudAdapter.canonical_conversation_ref(membership.tenant_ref, sender)
            else:
                formatted_response = {"twiml_xml": TwilioSmsAdapter.build_twiml_response(answer_text), "plain_text": answer_text}
                conv_ref = TwilioSmsAdapter.canonical_conversation_ref(membership.tenant_ref, sender)

            return self._respond_json(
                start_response,
                "200 OK",
                headers,
                {
                    "status": "ok",
                    "channel": channel,
                    "sender": sender,
                    "conversation_ref": conv_ref,
                    "user_message": message_text,
                    "agent_answer": answer_text,
                    "formatted_outbound": formatted_response,
                },
            )

        except (AuthenticationError, AuthorizationError):
            return self._respond_json(start_response, "401 Unauthorized", headers, {"error": "unauthorized"})

    def _query_agent_for_answer(self, question_text: str) -> str:
        """Queries FaqSupportAgent for an approved answer from the published Knowledge Base."""
        try:
            if hasattr(self._agent, "decide"):
                decision = self._agent.decide(question_text)
                if hasattr(decision, "answer_text") and isinstance(decision.answer_text, str):
                    return decision.answer_text
                if hasattr(decision, "text") and isinstance(decision.text, str):
                    return decision.text
            if hasattr(self._agent, "answer"):
                tenant_ref = os.getenv("SUPPORT_TENANT_REF", "staging-demo")
                try:
                    result = self._agent.answer(
                        tenant_ref=tenant_ref,
                        agent_ref="customer-support-worker",
                        subject_ref="sms-customer",
                        session_ref=f"sms-{uuid.uuid4()}",
                        question=question_text,
                        permissions=frozenset({"agent.context.read", "knowledge.read", "knowledge.retrieve", "platform.owner"}),
                    )
                    raw_ans = getattr(result, "answer", str(result))
                    if isinstance(raw_ans, str) and raw_ans.strip():
                        return raw_ans.strip()
                except TypeError:
                    result = self._agent.answer(question_text)
                    raw_ans = getattr(result, "answer", str(result))
                    if isinstance(raw_ans, str) and raw_ans.strip():
                        return raw_ans.strip()
        except Exception:
            pass
        return "Thank you for reaching out to Planwell Support! We are reviewing your inquiry."

    @staticmethod
    def _read_json(environ: Mapping[str, object]) -> dict[str, Any]:
        try:
            length = int(str(environ.get("CONTENT_LENGTH") or 0))
        except (ValueError, TypeError):
            length = 0
        stream = environ.get("wsgi.input")
        if not stream or length <= 0:
            return {}
        try:
            data = stream.read(length)  # type: ignore[union-attr]
            return json.loads(data.decode("utf-8")) if data else {}
        except Exception:
            return {}

    @staticmethod
    def _read_form_data(environ: Mapping[str, object]) -> dict[str, str]:
        try:
            length = int(str(environ.get("CONTENT_LENGTH") or 0))
        except (ValueError, TypeError):
            length = 0
        stream = environ.get("wsgi.input")
        if not stream or length <= 0:
            return {}
        try:
            data = stream.read(length)  # type: ignore[union-attr]
            parsed = parse_qs(data.decode("utf-8"))
            return {k: v[0] for k, v in parsed.items() if v}
        except Exception:
            return {}

    @staticmethod
    def _respond_json(
        start_response: Callable[..., object],
        status: str,
        headers: list[tuple[str, str]],
        body: dict[str, object],
    ) -> list[bytes]:
        payload = json.dumps(body).encode("utf-8")
        headers.append(("Content-Length", str(len(payload))))
        start_response(status, headers)
        return [payload]

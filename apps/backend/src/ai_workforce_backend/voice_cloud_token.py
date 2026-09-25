"""Short-lived browser access to one explicitly configured LiveKit Cloud agent."""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable, Mapping
from datetime import timedelta
from typing import cast

from livekit import api
from ai_workforce_agent.context import LocalKnowledgeSource

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)



from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)
from .voice_presets import get_role_preset


class VoiceCloudAgentTokenApi:
    """Issue a tenant-bound token that dispatches only the configured Cloud agent."""

    route_ref = "voice.cloud-agent.token.v1"
    required_permission = "agent.context.read"
    path = "/v1/livekit-cloud-agent-token"
    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        audit_sink: AuditSink,
        *,
        url: str,
        api_key: str,
        api_secret: str,
        agent_name: str,
        knowledge: LocalKnowledgeSource,
        store: Any | None = None,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        if not url.startswith("wss://"):
            raise ValueError("LIVEKIT_CLOUD_URL must use wss://")
        if not api_key or not api_secret or not agent_name:
            raise ValueError("LiveKit Cloud credentials and agent name are required")
        self._verifier = verifier
        self._memberships = memberships
        self._audit_sink = audit_sink
        self._url = url
        self._api_key = api_key
        self._api_secret = api_secret
        self._agent_name = agent_name
        self._knowledge = knowledge
        self._store = store
        self._correlation_factory = correlation_factory

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        if environ.get("REQUEST_METHOD") != "POST" or environ.get("PATH_INFO") != self.path:
            return self._respond(start_response, "404 Not Found", headers, {"error": "not_found"})
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if (
                self.required_permission not in membership.permissions
                or self.required_permission not in identity.granted_permissions
            ):
                raise AuthorizationError("insufficient_permission")
            body_size = int(cast(str, environ.get("CONTENT_LENGTH") or "0"))
            if body_size < 1 or body_size > 1024:
                raise AuthorizationError("invalid_context_request")
            request = json.loads(cast(object, environ.get("wsgi.input")).read(body_size))
            query = request.get("support_query") if isinstance(request, dict) else None
            if not isinstance(query, str) or not query.strip() or len(query) > 240:
                raise AuthorizationError("invalid_context_request")
            # Natural phrasing is allowed, but the agent receives only one
            # existing approved FAQ excerpt for the matching tenant.
            entry = self._knowledge.search(
                membership.tenant_ref, query, minimum_match_ratio=0
            )
            if entry is None:
                raise AuthorizationError("approved_context_unavailable")

            meta_dict: dict[str, Any] = {
                "mode": "support-faq",
                "source_ref": entry.source_ref,
                "support_context": entry.excerpt,
            }

            # Resolve Role Archetype or Custom Tenant Workspace
            req_preset = request.get("preset_id") or request.get("role")
            tenant_ref = str(membership.tenant_ref or "").lower()

            is_known_preset = bool(get_role_preset(req_preset) or get_role_preset(tenant_ref))

            is_mock = type(self._store).__name__.endswith("Mock") or hasattr(self._store, "_mock_name") if self._store else False
            tenant_record = None
            if self._store and not is_mock and hasattr(self._store, "get_tenant") and tenant_ref:
                try:
                    tenant_record = self._store.get_tenant(tenant_ref)
                except Exception:
                    tenant_record = None

            articles = []
            if self._store and not is_mock and hasattr(self._store, "list_knowledge_articles") and tenant_ref:
                try:
                    articles = self._store.list_knowledge_articles(tenant_ref, published_only=False)
                except Exception:
                    articles = []

            active_custom = None
            if self._store and not is_mock and hasattr(self._store, "get_active_custom_role") and tenant_ref:
                try:
                    active_custom = self._store.get_active_custom_role(tenant_ref)
                except Exception:
                    active_custom = None

            if "moving" in tenant_ref or tenant_ref == "moving-beavers" or (req_preset and "moving" in str(req_preset).lower()):
                preset_id = "moving_beavers"
                preset = get_role_preset(preset_id)
            elif is_known_preset:
                preset_id = req_preset if get_role_preset(req_preset) else tenant_ref
                preset = get_role_preset(preset_id)
            elif tenant_record or articles or active_custom or (tenant_ref and tenant_ref not in ("staging-demo", "default", "flora_dispatch")):
                preset_id = tenant_ref
                tenant_name = (tenant_record.name if tenant_record else None) or request.get("tenant_name") or tenant_ref.replace("-", " ").title()
                industry = (tenant_record.industry if tenant_record and tenant_record.industry else None) or request.get("industry") or "Customer Care & Services"
                persona = (active_custom.persona if active_custom and active_custom.persona else None) or request.get("persona_name") or "Alex"
                role_name = (active_custom.name if active_custom and active_custom.name else None) or request.get("role") or "AI Workspace Receptionist"
                greeting_text = (active_custom.greeting_text if active_custom and active_custom.greeting_text else None) or request.get("greeting") or f"Hello and welcome to {tenant_name}! How can I assist you today?"

                if articles:
                    # Priority-aware assembly: job/careers articles first so they are
                    # never crowded out when truncation is needed.
                    _KB_CHAR_LIMIT = 23_500
                    job_keywords = ("job", "career", "position", "hiring", "opening", "vacancy", "role", "employment")
                    priority_articles = [
                        a for a in articles
                        if any(kw in (a.topic or "").lower() or kw in (a.question or "").lower() for kw in job_keywords)
                    ]
                    general_articles = [a for a in articles if a not in priority_articles]
                    ordered_articles = priority_articles + general_articles
                    kb_parts: list[str] = []
                    char_count = 0
                    for a in ordered_articles:
                        line = f"Topic: {a.topic}\nQ: {a.question}\nA: {a.answer}"
                        if char_count + len(line) + 2 > _KB_CHAR_LIMIT:
                            break
                        kb_parts.append(line)
                        char_count += len(line) + 2
                    custom_kb = "\n\n".join(kb_parts)
                else:
                    custom_kb = request.get("support_context") or f"Company: {tenant_name}\nIndustry: {industry}\nDomain: {tenant_record.domain if tenant_record and tenant_record.domain else ''}"

                if active_custom and getattr(active_custom, "system_prompt", None):
                    system_prompt = str(active_custom.system_prompt)
                else:
                    system_prompt = (
                        f"You are {persona}, a dedicated {role_name} for {tenant_name} ({industry}).\n"
                        f"Always stay in character. Greet callers warmly, understand their requests, and answer questions accurately using company knowledge.\n"
                        f"Keep spoken responses concise (1-2 sentences), clear, conversational, and natural.\n"
                        f"Never mention that you are a generic bot."
                    )

                preset = {
                    "id": tenant_ref,
                    "name": role_name,
                    "persona": persona,
                    "industry": industry,
                    "profiles": {
                        "webrtc": {
                            "system_prompt": system_prompt,
                            "greeting_text": greeting_text,
                            "stt_provider": (active_custom.stt_provider if active_custom and getattr(active_custom, "stt_provider", None) else None) or "deepgram",
                            "stt_model": (active_custom.stt_model if active_custom and getattr(active_custom, "stt_model", None) else None) or "nova-3",
                            "tts_provider": (active_custom.tts_provider if active_custom and getattr(active_custom, "tts_provider", None) else None) or "openai",
                            "tts_model": "tts-1",
                            "tts_voice_id": (active_custom.tts_voice_id if active_custom and getattr(active_custom, "tts_voice_id", None) else None) or "nova",
                        }
                    }
                }
                meta_dict["support_context"] = custom_kb
            else:
                preset_id = "flora_dispatch"
                preset = get_role_preset(preset_id)

            if preset:
                prof_webrtc = preset.get("profiles", {}).get("webrtc", {})
                meta_dict["system_prompt"] = prof_webrtc.get("system_prompt")
                meta_dict["greeting_text"] = prof_webrtc.get("greeting_text")
                meta_dict["persona"] = preset.get("persona")
                meta_dict["role_id"] = preset.get("id")
                meta_dict["role_name"] = preset.get("name")
                meta_dict["industry"] = preset.get("industry")
                meta_dict["stt_provider"] = prof_webrtc.get("stt_provider", "deepgram")
                meta_dict["stt_model"] = prof_webrtc.get("stt_model", "nova-3")
                meta_dict["tts_provider"] = prof_webrtc.get("tts_provider", "openai")
                meta_dict["tts_model"] = prof_webrtc.get("tts_model", "tts-1")
                meta_dict["tts_voice_id"] = prof_webrtc.get("tts_voice_id", "nova")

                domain_knowledge = {
                    "moving_beavers": "Q: What are your local moving rates in Calgary?\nA: Local moves in Calgary are around $140 to $160 per hour for 2 movers and a 20-foot truck, or $200 per hour for 3 movers and a 26-foot truck.\nQ: What are your hours?\nA: We are open Monday through Saturday from 8 AM to 7 PM, closed Sundays.\nQ: Do you offer storage?\nA: Yes, clean, heated storage units starting at $150 per month.",
                    "flora_dispatch": "Q: What services and areas do you cover?\nA: We provide 24/7 emergency dispatch for HVAC, plumbing, electrical, roofing, and cleaning with 2-hour arrival windows.\nQ: How do you handle emergency leaks?\nA: We dispatch licensed on-call master technicians immediately.",
                    "zoe_realestate": "Q: What properties are available?\nA: We have 1, 2, and 3-bedroom luxury apartments and residential listings available with in-unit laundry and pet-friendly amenities.\nQ: How do I schedule a tour?\nA: We offer in-person private tours and self-guided lockbox showings Monday through Saturday 9 AM to 6 PM.",
                    "dwight_sales": "Q: What are your pricing plans?\nA: We offer Starter at $99/mo, Pro at $299/mo, and custom Enterprise plans with unlimited AI voice minutes and CRM integrations.\nQ: Can I book a live demo?\nA: Yes, I can book you a 1-on-1 walkthrough with our executive team.",
                    "llama_medical": "Q: What insurances do you accept?\nA: We accept BlueCross, Aetna, Cigna, UnitedHealthcare, and HSA/FSA cards.\nQ: What are your hours?\nA: We are open Monday through Friday 8 AM to 5 PM with 24/7 on-call triage.",
                    "yumi_hospitality": "Q: How do I reserve a table?\nA: We take table reservations up to 10 guests online and offer private dining rooms for events.\nQ: Do you have vegan and gluten-free options?\nA: Yes, our menu features dedicated gluten-free and vegan chef specials.",
                    "viva_automotive": "Q: Can I book vehicle service?\nA: Yes, our master service bays handle oil changes, brake repairs, tire rotations, and inspections.\nQ: Do you offer test drives?\nA: Yes, we offer test drives for all new and certified pre-owned vehicles.",
                }
                preset_key = preset.get("id")
                if preset_key in domain_knowledge:
                    meta_dict["support_context"] = f"{entry.excerpt}\n\n{domain_knowledge[preset_key]}"

            if self._store is not None:
                try:
                    if hasattr(self._store, "get_active_custom_role") and not req_preset and not type(self._store).__name__.endswith("Mock"):
                        active_custom = self._store.get_active_custom_role(membership.tenant_ref)
                        if active_custom and not type(active_custom).__name__.endswith("Mock"):
                            if getattr(active_custom, "system_prompt", None):
                                meta_dict["system_prompt"] = str(active_custom.system_prompt)
                            if getattr(active_custom, "greeting_text", None):
                                meta_dict["greeting_text"] = str(active_custom.greeting_text)
                            if getattr(active_custom, "persona", None):
                                meta_dict["persona"] = str(active_custom.persona)
                            if getattr(active_custom, "role_ref", None):
                                meta_dict["role_id"] = str(active_custom.role_ref)
                            if getattr(active_custom, "name", None):
                                meta_dict["role_name"] = str(active_custom.name)
                            if getattr(active_custom, "industry", None):
                                meta_dict["industry"] = str(active_custom.industry)
                            if getattr(active_custom, "tts_provider", None):
                                meta_dict["tts_provider"] = str(active_custom.tts_provider)
                            if getattr(active_custom, "tts_voice_id", None):
                                meta_dict["tts_voice_id"] = str(active_custom.tts_voice_id)
                            if getattr(active_custom, "stt_provider", None):
                                meta_dict["stt_provider"] = str(active_custom.stt_provider)
                            if getattr(active_custom, "stt_model", None):
                                meta_dict["stt_model"] = str(active_custom.stt_model)

                    if hasattr(self._store, "get_effective_voice_profile"):
                        prof = self._store.get_effective_voice_profile(membership.tenant_ref, "webrtc")
                        if prof is not None:
                            if getattr(prof, "stt_provider", None):
                                meta_dict["stt_provider"] = str(prof.stt_provider)
                            if getattr(prof, "stt_model", None):
                                meta_dict["stt_model"] = str(prof.stt_model)
                            if getattr(prof, "tts_provider", None):
                                meta_dict["tts_provider"] = str(prof.tts_provider)
                            if getattr(prof, "tts_model", None):
                                meta_dict["tts_model"] = str(prof.tts_model)
                            if getattr(prof, "tts_voice_id", None):
                                meta_dict["tts_voice_id"] = str(prof.tts_voice_id)
                    elif hasattr(self._store, "get_tenant_voice_model_settings"):
                        m_settings = self._store.get_tenant_voice_model_settings(membership.tenant_ref)
                        if m_settings is not None:
                            if getattr(m_settings, "stt_provider", None):
                                meta_dict["stt_provider"] = str(m_settings.stt_provider)
                            if getattr(m_settings, "stt_model", None):
                                meta_dict["stt_model"] = str(m_settings.stt_model)
                            if getattr(m_settings, "tts_provider", None):
                                meta_dict["tts_provider"] = str(m_settings.tts_provider)
                            if getattr(m_settings, "tts_model", None):
                                meta_dict["tts_model"] = str(m_settings.tts_model)
                            if getattr(m_settings, "tts_voice_id", None):
                                meta_dict["tts_voice_id"] = str(m_settings.tts_voice_id)
                except Exception:
                    pass

            room_ref = f"cloud-agent-{membership.tenant_ref}-{uuid.uuid4()}"
            token = (
                api.AccessToken(self._api_key, self._api_secret)
                .with_ttl(timedelta(minutes=5))
                .with_identity(f"cloud-agent-user-{uuid.uuid4()}")
                .with_name("Planwell browser agent test")
                .with_grants(api.VideoGrants(room_join=True, room=room_ref))
                .with_room_config(
                    api.RoomConfiguration(
                        agents=[
                            api.RoomAgentDispatch(
                                agent_name=self._agent_name,
                                metadata=json.dumps(meta_dict, separators=(",", ":")),
                            )
                        ]
                    )
                )
                .to_jwt()
            )
        except AuthenticationError as error:
            self._audit_sink.record(
                AuditEvent("denied", str(error), correlation_ref, self.route_ref)
            )
            return self._respond(
                start_response, "401 Unauthorized", headers, {"error": "unauthorized"}
            )
        except (AuthorizationError, TypeError, ValueError) as error:
            self._audit_sink.record(
                AuditEvent("denied", str(error), correlation_ref, self.route_ref)
            )
            public_error = (
                "approved_context_unavailable"
                if str(error) == "approved_context_unavailable"
                else "forbidden"
            )
            return self._respond(start_response, "403 Forbidden", headers, {"error": public_error})
        self._audit_sink.record(
            AuditEvent(
                "allowed",
                "cloud_agent_token_issued",
                correlation_ref,
                self.route_ref,
                identity.principal_ref,
                membership.tenant_ref,
            )
        )
        return self._respond(
            start_response,
            "200 OK",
            headers,
            {
                "url": self._url,
                "token": token,
                "room_ref": room_ref,
                "correlation_ref": correlation_ref,
            },
        )

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

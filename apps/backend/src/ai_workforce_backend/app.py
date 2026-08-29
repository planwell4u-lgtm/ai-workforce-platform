"""Backend application composition."""

from __future__ import annotations

import os
import uuid
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import cast

from ai_workforce_agent.context import (
    AgentContextService,
    AgentVersion,
    LocalKnowledgeSource,
    SessionMemoryStore,
)
from ai_workforce_agent.support import FaqSupportAgent
from ai_workforce_agent.sales import CatalogSalesAgent
from ai_workforce_data.postgres_store import PostgresTenantStore
from ai_workforce_integration.support_ticket import create_jira_support_ticket_action
from ai_workforce_integration.hubspot_lead import HubSpotClient, HubSpotSettings

from .admin_conversations import AdminConversationsApi
from .auth0 import Auth0JwtVerifier
from .b1 import (
    ProtectedApi,
)
from .persistent_conversation import PersistentConversationService
from .front_desk_routing import ActiveDestinationRegistry, FrontDeskHumanSalesRequestsApi, FrontDeskRoutingApi
from .front_desk_destinations import FrontDeskDestinationsApi
from .runtime import (
    PostgresAuditSink,
    PostgresMembershipDirectory,
    TenantStore,
    create_tenant_store,
)
from .support_answer import SupportAnswerApi
from .sales_answer import SalesAnswerApi
from .sales_lead import SalesLeadApi
from .ticket_flow import SupportTicketApi
from .voice_cloud_token import VoiceCloudAgentTokenApi
from .voice_sandbox_token import VoiceSandboxTokenApi


class BackendApplication:
    """Application lifecycle owner for the protected API and tenant store."""

    def __init__(
        self,
        api: ProtectedApi,
        support_ticket_api: SupportTicketApi,
        support_answer_api: SupportAnswerApi,
        sales_answer_api: SalesAnswerApi | None,
        sales_lead_api: SalesLeadApi | None,
        admin_conversations_api: AdminConversationsApi,
        front_desk_routing_api: FrontDeskRoutingApi,
        front_desk_human_sales_requests_api: FrontDeskHumanSalesRequestsApi,
        front_desk_destinations_api: FrontDeskDestinationsApi,
        voice_sandbox_token_api: VoiceSandboxTokenApi | None,
        voice_cloud_agent_token_api: VoiceCloudAgentTokenApi | None,
        tenant_store: TenantStore,
        allowed_origin: str = "http://localhost:3000",
    ) -> None:
        self.api = api
        self.support_ticket_api = support_ticket_api
        self.support_answer_api = support_answer_api
        self.sales_answer_api = sales_answer_api
        self.sales_lead_api = sales_lead_api
        self.admin_conversations_api = admin_conversations_api
        self.front_desk_routing_api = front_desk_routing_api
        self.front_desk_human_sales_requests_api = front_desk_human_sales_requests_api
        self.front_desk_destinations_api = front_desk_destinations_api
        self.voice_sandbox_token_api = voice_sandbox_token_api
        self.voice_cloud_agent_token_api = voice_cloud_agent_token_api
        self.tenant_store = tenant_store
        self.allowed_origin = allowed_origin

    @property
    def route_ref(self) -> str:
        return self.api.route_ref

    def close(self) -> None:
        self.tenant_store.close()

    def __call__(
        self, environ: Mapping[str, str], start_response: Callable[..., object]
    ) -> list[bytes]:
        origin = environ.get("HTTP_ORIGIN")
        path_info = environ.get("PATH_INFO", "")
        protected_cors_paths = {
            "/v1/support-answers",
            "/v1/sales-answers",
            "/v1/sales-leads",
            "/v1/admin/conversations",
            "/v1/support-tickets",
            "/v1/voice-sandbox-token",
            "/v1/livekit-cloud-agent-token",
        }
        front_desk_cors_path = (
            path_info == "/v1/conversation-routing-requests"
            or path_info.startswith(FrontDeskHumanSalesRequestsApi.path)
            or path_info.startswith(FrontDeskDestinationsApi.path)
        )
        if environ.get("REQUEST_METHOD") == "OPTIONS" and (
            path_info in protected_cors_paths or front_desk_cors_path
        ):
            if origin != self.allowed_origin:
                start_response("403 Forbidden", [("Content-Length", "0")])
                return [b""]
            start_response(
                "204 No Content",
                [
                    ("Access-Control-Allow-Origin", origin),
                    ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
                    ("Access-Control-Allow-Headers", "Authorization, Content-Type"),
                    ("Content-Length", "0"),
                ],
            )
            return [b""]
        if environ.get("REQUEST_METHOD") == "GET" and environ.get("PATH_INFO") == "/healthz":
            body = b'{"status":"ok"}'
            start_response(
                "200 OK",
                [("Content-Type", "application/json"), ("Content-Length", str(len(body)))],
            )
            return [body]
        if (
            environ.get("REQUEST_METHOD") in {"GET", "POST"}
            and cast(str, environ.get("PATH_INFO", "")).startswith(FrontDeskDestinationsApi.path)
        ):

            def destinations_start(status: str, headers: list[tuple[str, str]]) -> object:
                if origin == self.allowed_origin:
                    headers = [*headers, ("Access-Control-Allow-Origin", origin)]
                return start_response(status, headers)

            return self.front_desk_destinations_api(environ, destinations_start)
        if (
            environ.get("REQUEST_METHOD") == "POST"
            and environ.get("PATH_INFO") == FrontDeskRoutingApi.path
        ):

            def routing_start(status: str, headers: list[tuple[str, str]]) -> object:
                if origin == self.allowed_origin:
                    headers = [*headers, ("Access-Control-Allow-Origin", origin)]
                return start_response(status, headers)

            return self.front_desk_routing_api(environ, routing_start)
        if (
            environ.get("REQUEST_METHOD") in {"GET", "POST"}
            and environ.get("PATH_INFO") == FrontDeskHumanSalesRequestsApi.path
            or environ.get("REQUEST_METHOD") == "POST"
            and environ.get("PATH_INFO", "").startswith(f"{FrontDeskHumanSalesRequestsApi.path}/")
        ):

            def human_sales_requests_start(status: str, headers: list[tuple[str, str]]) -> object:
                if origin == self.allowed_origin:
                    headers = [*headers, ("Access-Control-Allow-Origin", origin)]
                return start_response(status, headers)

            return self.front_desk_human_sales_requests_api(environ, human_sales_requests_start)
        if (
            environ.get("REQUEST_METHOD") == "POST"
            and environ.get("PATH_INFO") == "/v1/support-tickets"
        ):

            def ticket_start(status: str, headers: list[tuple[str, str]]) -> object:
                if origin == self.allowed_origin:
                    headers = [*headers, ("Access-Control-Allow-Origin", origin)]
                return start_response(status, headers)

            return self.support_ticket_api(environ, ticket_start)
        if (
            environ.get("REQUEST_METHOD") in {"GET", "POST"}
            and environ.get("PATH_INFO") == "/v1/support-answers"
        ):
            if origin is not None and origin != self.allowed_origin:
                body = b'{"error":"forbidden"}'
                start_response(
                    "403 Forbidden",
                    [("Content-Type", "application/json"), ("Content-Length", str(len(body)))],
                )
                return [body]

            def support_start(status: str, headers: list[tuple[str, str]]) -> object:
                if origin == self.allowed_origin:
                    headers = [*headers, ("Access-Control-Allow-Origin", origin)]
                return start_response(status, headers)

            return self.support_answer_api(environ, support_start)
        if (
            self.sales_answer_api is not None
            and environ.get("REQUEST_METHOD") == "POST"
            and environ.get("PATH_INFO") == SalesAnswerApi.path
        ):
            def sales_start(status: str, headers: list[tuple[str, str]]) -> object:
                if origin == self.allowed_origin:
                    headers = [*headers, ("Access-Control-Allow-Origin", origin)]
                return start_response(status, headers)
            return self.sales_answer_api(environ, sales_start)
        if (
            self.sales_lead_api is not None
            and environ.get("REQUEST_METHOD") == "POST"
            and environ.get("PATH_INFO") == SalesLeadApi.path
        ):
            def sales_lead_start(status: str, headers: list[tuple[str, str]]) -> object:
                if origin == self.allowed_origin:
                    headers = [*headers, ("Access-Control-Allow-Origin", origin)]
                return start_response(status, headers)
            return self.sales_lead_api(environ, sales_lead_start)
        if (
            environ.get("REQUEST_METHOD") == "GET"
            and environ.get("PATH_INFO") == "/v1/admin/conversations"
        ):

            def admin_start(status: str, headers: list[tuple[str, str]]) -> object:
                if origin == self.allowed_origin:
                    headers = [*headers, ("Access-Control-Allow-Origin", origin)]
                return start_response(status, headers)

            return self.admin_conversations_api(environ, admin_start)
        if (
            self.voice_sandbox_token_api is not None
            and environ.get("REQUEST_METHOD") == "POST"
            and environ.get("PATH_INFO") == "/v1/voice-sandbox-token"
        ):

            def voice_token_start(status: str, headers: list[tuple[str, str]]) -> object:
                if origin == self.allowed_origin:
                    headers = [*headers, ("Access-Control-Allow-Origin", origin)]
                return start_response(status, headers)

            return self.voice_sandbox_token_api(environ, voice_token_start)
        if (
            self.voice_cloud_agent_token_api is not None
            and environ.get("REQUEST_METHOD") == "POST"
            and environ.get("PATH_INFO") == VoiceCloudAgentTokenApi.path
        ):

            def cloud_agent_token_start(status: str, headers: list[tuple[str, str]]) -> object:
                if origin == self.allowed_origin:
                    headers = [*headers, ("Access-Control-Allow-Origin", origin)]
                return start_response(status, headers)

            return self.voice_cloud_agent_token_api(environ, cloud_agent_token_start)
        return self.api(environ, start_response)


def create_app() -> BackendApplication:
    """Create the protected API with Auth0 as its identity provider."""
    domain = os.environ.get("AUTH0_DOMAIN")
    audience = os.environ.get("AUTH0_AUDIENCE")
    environment_ref = os.environ.get("APP_ENV")
    faq_path = os.environ.get("SUPPORT_FAQ_PATH")
    sales_catalog_path = os.environ.get("SALES_CATALOG_PATH")
    hubspot_token = os.environ.get("HUBSPOT_PRIVATE_APP_TOKEN")
    support_tenant_ref = os.environ.get("SUPPORT_TENANT_REF")
    livekit_url = os.environ.get("LIVEKIT_SANDBOX_URL")
    livekit_api_key = os.environ.get("LIVEKIT_API_KEY")
    livekit_api_secret = os.environ.get("LIVEKIT_API_SECRET")
    livekit_cloud_url = os.environ.get("LIVEKIT_CLOUD_URL")
    livekit_cloud_api_key = os.environ.get("LIVEKIT_CLOUD_API_KEY")
    livekit_cloud_api_secret = os.environ.get("LIVEKIT_CLOUD_API_SECRET")
    livekit_cloud_agent_name = os.environ.get("LIVEKIT_CLOUD_AGENT_NAME")
    livekit_isolation_url = os.environ.get("LIVEKIT_ISOLATION_URL")
    livekit_isolation_api_key = os.environ.get("LIVEKIT_ISOLATION_API_KEY")
    livekit_isolation_api_secret = os.environ.get("LIVEKIT_ISOLATION_API_SECRET")
    livekit_isolation_agent_name = (
        os.environ.get("LIVEKIT_ISOLATION_AGENT_NAME") or "customer-support-realtime-v1"
    )
    missing = [
        name
        for name, value in (
            ("AUTH0_DOMAIN", domain),
            ("AUTH0_AUDIENCE", audience),
            ("APP_ENV", environment_ref),
            ("SUPPORT_FAQ_PATH", faq_path),
            ("SUPPORT_TENANT_REF", support_tenant_ref),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(f"missing required backend configuration: {', '.join(missing)}")
    livekit_values = (livekit_url, livekit_api_key, livekit_api_secret)
    if any(livekit_values) and not all(livekit_values):
        raise RuntimeError(
            "LIVEKIT_SANDBOX_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET must be set together"
        )
    isolation_values = (
        livekit_isolation_url,
        livekit_isolation_api_key,
        livekit_isolation_api_secret,
    )
    if any(isolation_values):
        livekit_cloud_values = (*isolation_values, livekit_isolation_agent_name)
    else:
        livekit_cloud_values = (
            livekit_cloud_url,
            livekit_cloud_api_key,
            livekit_cloud_api_secret,
            livekit_cloud_agent_name,
        )
    if any(livekit_cloud_values) and not all(livekit_cloud_values):
        raise RuntimeError(
            "the selected LiveKit Cloud profile must include URL, API key, API secret, and agent name"
        )
    tenant_store = create_tenant_store(environment_ref, os.environ)
    verifier = Auth0JwtVerifier(domain, audience, environment_ref)
    memberships = PostgresMembershipDirectory(cast(PostgresTenantStore, tenant_store))
    audit_sink = PostgresAuditSink(cast(PostgresTenantStore, tenant_store))
    knowledge = LocalKnowledgeSource.from_jsonl(
        Path(cast(str, faq_path)),
        tenant_ref=cast(str, support_tenant_ref),
        source_ref="support-faqs:v1",
    )
    support_agent = FaqSupportAgent(
        AgentContextService(
            (
                AgentVersion(
                    "customer-support-worker",
                    "customer-support-worker:faq-v1",
                    cast(str, support_tenant_ref),
                    "released",
                    frozenset({"knowledge.retrieve"}),
                ),
            ),
            knowledge,
            SessionMemoryStore(()),
        ),
        knowledge,
    )
    sales_agent = None
    if sales_catalog_path:
        sales_knowledge = LocalKnowledgeSource.from_jsonl(
            Path(sales_catalog_path),
            tenant_ref=cast(str, support_tenant_ref),
            source_ref="sales-catalog:v1",
        )
        sales_agent = CatalogSalesAgent(
            AgentContextService(
                (
                    AgentVersion(
                        "sales-worker", "sales-worker:catalog-v1", cast(str, support_tenant_ref),
                        "released", frozenset({"knowledge.retrieve"}),
                    ),
                ),
                sales_knowledge,
                SessionMemoryStore(()),
            ),
            sales_knowledge,
        )
    return BackendApplication(
        ProtectedApi(
            verifier,
            memberships,
            audit_sink,
        ),
        SupportTicketApi(
            verifier,
            memberships,
            audit_sink,
            tenant_store,
            create_jira_support_ticket_action(os.environ),
        ),
        SupportAnswerApi(
            verifier,
            memberships,
            audit_sink,
            support_agent,
            PersistentConversationService(
                cast(PostgresTenantStore, tenant_store),
                cast(str, environment_ref),
                correlation_factory=lambda: str(uuid.uuid4()),
            ),
        ),
        SalesAnswerApi(
            verifier, memberships, audit_sink, sales_agent,
            PersistentConversationService(cast(PostgresTenantStore, tenant_store), cast(str, environment_ref), correlation_factory=lambda: str(uuid.uuid4())),
        ) if sales_agent else None,
        SalesLeadApi(
            verifier, memberships, audit_sink, tenant_store,
            HubSpotClient(HubSpotSettings.from_environment(os.environ)),
            cast(str, environment_ref),
        ) if hubspot_token else None,
        AdminConversationsApi(
            verifier, memberships, audit_sink, tenant_store, cast(str, environment_ref)
        ),
        FrontDeskRoutingApi(
            verifier,
            memberships,
            audit_sink,
            tenant_store,
            ActiveDestinationRegistry(tenant_store),
        ),
        FrontDeskHumanSalesRequestsApi(verifier, memberships, audit_sink, tenant_store),
        FrontDeskDestinationsApi(verifier, memberships, audit_sink, tenant_store),
        VoiceSandboxTokenApi(
            verifier,
            memberships,
            audit_sink,
            url=cast(str, livekit_url),
            api_key=cast(str, livekit_api_key),
            api_secret=cast(str, livekit_api_secret),
        )
        if all(livekit_values)
        else None,
        VoiceCloudAgentTokenApi(
            verifier,
            memberships,
            audit_sink,
            url=cast(str, livekit_cloud_url),
            api_key=cast(str, livekit_cloud_api_key),
            api_secret=cast(str, livekit_cloud_api_secret),
            agent_name=cast(str, livekit_cloud_agent_name),
            knowledge=knowledge,
        )
        if all(livekit_cloud_values)
        else None,
        tenant_store,
        os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000"),
    )

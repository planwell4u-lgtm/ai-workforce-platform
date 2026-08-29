# 14_FRONTEND_DELIVERY_PLAN

**Version:** 0.2
**Status:** Planned — with a test-only Front Desk route-offer control implemented
**Owner:** Frontend Platform Owner
**Phase:** Post–First Vertical Slice Delivery Planning

---

# Purpose

This document turns the approved Frontend Platform architecture into an incremental product-delivery plan for the AI Workforce Platform. It does not change platform ownership, authorization, privacy, data, integration, or deployment boundaries.

The platform has one master delivery roadmap. This plan is a frontend delivery track within that roadmap and must stay aligned with the related backend, security, data, integration, operations, and testing work for each milestone.

# Product Model

The frontend is a multi-tenant B2B SaaS experience with three distinct surfaces:

1. **Customer-facing channels** — web chat, browser voice, telephone, and future digital channels.
2. **Client Workspace** — where one tenant configures and monitors its workers.
3. **Platform Admin** — where authorized internal staff manage tenant support, platform operations, and governed platform policy.

These surfaces must not share unrestricted data access or administrative authority.

# Roles

| Role | Primary frontend need |
|---|---|
| Customer or caller | Receive safe assistance and a clear human handoff when needed. |
| Client operator | Review conversations, respond to handoffs, and manage authorized tickets. |
| Client admin | Configure workers, approved knowledge, integrations, and tenant team access. |
| Client owner | Review service health, usage, and account status. |
| Platform support | Assist a tenant through purpose-limited, audited workflows. |
| Platform admin | Govern tenants, platform policies, providers, and operations. |

# Shared Frontend Foundation

Every frontend milestone builds on one shared application foundation:

- Authenticated, tenant-aware application shell and navigation.
- Role- and entitlement-aware presentation; backend authorization remains authoritative.
- Accessible, responsive design system with loading, empty, error, and permission-denied states.
- Notification center and safe user-preference controls.
- Audit-visible configuration and approval actions.
- Client privacy, consent, redaction, telemetry, and session-handling requirements from the approved Frontend and Security architecture.

# Delivery Sequence

## Implemented Test-only Front Desk Control

The signed-in support web chat receives its opaque conversation reference only
from the authenticated support API. After a conversation exists, it can ask the
backend to check Support availability and, only after an approved offer, record
a Support route request. The UI renders the approved outcome and explicitly
states that the chat is not transferred. It has no destination configuration,
provider details, human assignment, or external side effect.

The separate `/front-desk-admin` route provides the matching test-only
administrator screen. It lists destinations and allows a permitted admin to
create a Support draft, then validate, activate, suspend, or withdraw it using
the record's expected version. It requires the dedicated
`platform.front-desk.configure` permission. Until Auth0 exposes that permission
on the configured API and a tenant-admin role receives it, the screen reports
no access; it does not fall back to operator or customer permissions.

## F1 — Client Workspace MVP

**Goal:** Give one tenant a focused control center for the already-proven Support Worker journey.

| Area | Initial capability |
|---|---|
| Overview | Worker health, conversations, human handoffs, ticket status, and safe knowledge-gap signals. |
| Workers | View and configure the approved Support Worker within its permitted capability boundary. |
| Knowledge | Review approved FAQ sources, publication state, and version history through approved backend contracts. |
| Conversations and tickets | Review tenant-scoped conversations, handoffs, and Jira outcomes. |
| Team and access | Invite, role assignment, and revocation through Platform Foundation and Security contracts. |
| Settings | Tenant profile, notification preferences, and approved channel configuration. |

## F2 — Worker Lifecycle

**Goal:** Make workers a governed product object rather than a fixed application flow.

- Worker library for Support, Front Desk, and Sales worker templates.
- Create-worker and configuration journey.
- Test mode before activation.
- Approved knowledge, channel, capability, and handoff assignment.
- Version history, approval, rollback, and disable controls.

## F3 — Role-Specific Workers

**Goal:** Add focused experiences without creating separate products for each worker.

| Worker | Focused configuration |
|---|---|
| Front Desk | Routing, business hours, locations/services, and human handoff. |
| Sales | Qualification, consent-based lead capture, and approved CRM handoff. |
| Support | Knowledge coverage, ticket rules, escalation queue, and safe fallback. |

## F4 — Channels and Integrations

**Goal:** Allow a client to select desired outcomes without exposing provider complexity by default.

- Web chat and browser voice as the initial client-facing channels.
- Phone onboarding: managed number, existing-number connection, or approved enterprise provider connection.
- Approved CRM, helpdesk, calendar, webhook, and API-key configuration journeys.
- Integration health, least-privilege connection state, and failure history.
- Provider/model selection remains a governed Platform Admin policy; normal clients choose service level, channels, languages, and behavior rather than raw provider credentials or model identifiers.

## F5 — Analytics, Usage, and Billing

**Goal:** Give clients decision-ready reporting without exposing unrestricted data access.

- Conversation/channel volume, resolution, handoff, and knowledge-gap trends.
- Worker availability and quality signals.
- Tenant-scoped metering, plan, invoice, seat, and upgrade views.
- Curated exports and scheduled reports with permission, audit, retention, and tenant-scope controls.

## F6 — Platform Admin

**Goal:** Provide a separate, tightly governed internal surface.

```text
Tenants
Platform Health
Support Cases
Worker Templates and Policies
Providers and Integrations
Audit and Compliance
Billing Operations
```

Platform support access must be purpose-limited, tenant-scoped, and auditable. The Admin interface must not create unrestricted access to client conversations, data, configurations, or credentials.

# Navigation Model

```text
Client Workspace
├── Overview
├── Workers
├── Knowledge
├── Conversations and Tickets
├── Integrations
├── Analytics
├── Team and Access
└── Settings

Platform Admin
├── Tenants
├── Platform Health
├── Support Cases
├── Worker Templates and Policies
├── Providers and Integrations
├── Audit and Compliance
└── Billing Operations
```

# Delivery Rules

- Build client-facing, client-workspace, and Platform Admin routes separately.
- Deliver one worker journey at a time, with test and approval evidence before broadening its permissions or channels.
- Do not expose raw database access, provider credentials, unrestricted query workbenches, or client-side authorization decisions.
- Defer broad Data Studio capability until tenant isolation, permission, retention, audit, and export contracts are implemented and tested.
- Treat billing, production phone routing, customer-data access, recording, outbound calling, and new external effects as separately authorized scopes.

# Next Planning Artifact

Create a Client Workspace MVP sitemap and wireframes for Overview, Workers, Knowledge, Conversations and Tickets, Team and Access, and Settings. Validate this against the existing Frontend Platform architecture before implementation.

# Related Documents

- `README.md`
- `01_FRONTEND_PLATFORM_ARCHITECTURE.md`
- `02_USER_OPERATOR_AND_TENANT_EXPERIENCE.md`
- `08_FRONTEND_ADMINISTRATION_CONFIGURATION_AND_ENTITLEMENTS.md`
- `10_FRONTEND_PRIVACY_SAFETY_AND_DATA_HANDLING.md`
- `12_FRONTEND_TESTING_AND_QUALITY.md`
- `../20_ENGINEERING/09_SHARED_WORKER_BLUEPRINT.md`
- `../20_ENGINEERING/10_FRONT_DESK_WORKER_V1.md`
- `../20_ENGINEERING/11_FRONT_DESK_ROUTING_REQUEST_CONTRACT.md`
- `../20_ENGINEERING/12_FRONT_DESK_DESTINATION_REGISTRY.md`
- `../20_ENGINEERING/13_FRONT_DESK_ROUTING_API_CONTRACT.md`
- `../00_CONTROL/ROADMAP.md`
- `../00_CONTROL/02_PROJECT_ROADMAP.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 0.3 | 2026-08-27 | Added the permission-bound test-only Front Desk destination admin screen. |
| 0.2 | 2026-08-27 | Recorded the implemented test-only Front Desk route-offer control in web chat. |
| 0.1 | 2026-08-27 | Added the planned frontend delivery track for Client Workspace, worker lifecycle, channels, analytics, and Platform Admin. |

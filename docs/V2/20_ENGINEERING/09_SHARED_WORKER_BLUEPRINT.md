# Shared Worker Blueprint

**Version:** 0.1
**Status:** Planned
**Date:** 2026-08-27
**Purpose:** Define the reusable delivery contract for every AI worker before a
worker-specific charter, frontend configuration flow, integration, or runtime
implementation is created.

---

## Purpose

An AI worker is a narrowly scoped, tenant-bound business capability. This
blueprint gives Support, Front Desk, Sales, and future workers one consistent
way to define purpose, knowledge, permissions, channels, human handoff,
success measures, and safety limits.

It is an engineering planning artifact. It does not alter the approved Agent,
Conversation, Knowledge, Integration, Security, or Frontend Platform
architecture, and it does not authorize a new worker or external effect.

## Design Rules

1. Each worker has one clear business role and a versioned identity.
2. A worker receives only the approved knowledge, tools, data, and channels
   required for that role.
3. The worker must safely hand off when it cannot answer, lacks authority, or
   encounters protected information.
4. Tenant, identity, permission, configuration, and action authority come from
   trusted backend contracts, never the browser, caller, model output, or
   channel metadata.
5. A new channel, data class, tool, external action, model policy, or proactive
   contact path is a separately reviewed scope expansion.
6. Worker configuration is versioned, testable, observable, approvable, and
   reversible.

## Required Worker Definition

Every worker-specific charter must define the following fields before
implementation begins.

| Area | Required definition |
|---|---|
| Identity | Worker name, stable reference, version, owning tenant/template, and lifecycle state. |
| Business role | One-sentence purpose, target participants, and supported journeys. |
| Allowed outcomes | Answers, routing, drafts, handoffs, or actions the worker may produce. |
| Explicit exclusions | Data, claims, actions, channels, or promises the worker must not make. |
| Knowledge | Approved sources, retrieval rule, freshness/version requirement, and safe-unavailable behavior. |
| Data | Allowed data classes, purpose, retention, redaction, and prohibited classes. |
| Capabilities and tools | Named allowed capability contracts; no implicit or arbitrary tool access. |
| Channels | Supported channels, entry conditions, consent requirements, and channel-specific limits. |
| Human handoff | Trigger conditions, destination, state ownership, user notice, and uncertain/failure behavior. |
| Permissions | Required participant, operator, workload, and action permissions enforced by backend policy. |
| Safety | Refusal, escalation, abuse, privacy, failure, and degraded-mode behavior. |
| Success measures | Quality, completion, handoff, safety, latency, and business metrics. |
| Evidence | Test plan, negative cases, approvals, observability, rollout, rollback, and owner. |

## Standard Lifecycle

```text
Template or charter
        ↓
Tenant-bound draft configuration
        ↓
Validation and negative-path tests
        ↓
Named owner approval
        ↓
Limited test activation
        ↓
Monitored release
        ↓
Versioned update, suspend, or retire
```

A frontend screen may request a lifecycle transition, but the backend must
enforce current tenant scope, entitlement, permission, approval, and version
state.

## Worker Configuration Contract

The Client Workspace should eventually expose only safe, approved configuration
controls. It must not expose provider credentials, raw database access,
unrestricted prompt editing, or client-side authorization.

| Client-visible control | Backend-governed contract |
|---|---|
| Worker name, tone, business hours, and handoff contact | Versioned configuration with tenant scope and validation. |
| Approved knowledge selection | Knowledge publication, provenance, retrieval, and access policy. |
| Enabled channels | Channel entitlement, consent, routing, and provider configuration. |
| Allowed actions | Named capability and integration authorization. |
| Test/activate/disable | Lifecycle state, approval, audit, rollback, and operational readiness. |
| Quality and handoff signals | Tenant-scoped, privacy-aware observability and analytics. |

## Initial Worker Sequence

### 1. Customer Support Worker

**Status:** Implemented baseline.

The existing Customer Support Worker V1 is the reference implementation of this
blueprint: approved FAQ-only answers, safe fallback, tenant-scoped
conversation history, authorized Jira escalation, and controlled voice FAQ
rehearsal. It does not gain data access, payments, refunds, outbound contact,
or additional tools through this blueprint.

### 2. Front Desk Worker

**Status:** Next planned worker charter.

Initial intended role: greet a visitor, identify a general purpose or
destination, offer only approved basic information, and route to the correct
worker or human team.

Initial exclusions: customer/account lookup, appointment creation, payment,
outbound contact, unapproved personal-data collection, and unrestricted
integrations.

### 3. Sales Worker

**Status:** Planned after Front Desk approval and evidence.

Initial intended role: answer approved product questions, support discovery,
and offer an authorized lead handoff. CRM write access, contact capture,
follow-up, pricing promises, and outbound contact require separate consent,
integration, and action approval.

### 4. Specialized Workers

Billing, onboarding, account-service, and other role-specific workers require
their own charters. They must not inherit a broader worker's permissions merely
because they use the same frontend shell or channel.

## Worker Charter Template

Use this structure for every proposed worker:

```text
Worker name and version:
Business role:
Target participant and channel:
Permitted user journeys:
Approved knowledge sources:
Allowed data classes and purpose:
Allowed capabilities/actions:
Required permissions and approvals:
Human handoff conditions and destination:
Explicit exclusions:
Safe-unavailable and failure behavior:
Success measures:
Required tests and evidence:
Rollout, rollback, and owner:
```

## Minimum Acceptance Gate

Before a worker may be activated beyond a controlled test, evidence must show:

1. The worker can complete its allowed journey from approved sources only.
2. It refuses or hands off unsupported, protected, cross-tenant, and
   unauthorized requests safely.
3. Every allowed action has server-side permission, validation, audit,
   idempotency, and explicit outcome handling.
4. Tenant, identity, permission, version, and lifecycle inputs cannot be
   forged through the frontend, model, channel metadata, or provider callback.
5. Its channel-specific consent, failure, disconnect, retry, and recovery paths
   are tested.
6. Approved owners have accepted the scope, evidence, monitoring, and rollback
   path.

## Next Artifact

The Front Desk Worker V1 Charter now adopts the greeting, approved-information,
and safe-routing-only scope. Appointment requests, lead capture, and
integrations remain separately approved future scope.

## Related Documents

- `07_CUSTOMER_SUPPORT_WORKER_V1.md`
- `10_FRONT_DESK_WORKER_V1.md`
- `../02_AGENT_PLATFORM/04_AGENT_LIFECYCLE.md`
- `../02_AGENT_PLATFORM/06_AGENT_CONFIGURATION_MODEL.md`
- `../02_AGENT_PLATFORM/14_AGENT_CAPABILITY_MODEL.md`
- `../02_AGENT_PLATFORM/25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md`
- `../02_AGENT_PLATFORM/27_AGENT_VERSIONING_MODEL.md`
- `../10_FRONTEND_PLATFORM/14_FRONTEND_DELIVERY_PLAN.md`
- `../00_CONTROL/ROADMAP.md`

## Revision History

| Version | Date | Changes |
|---|---|---|
| 0.1 | 2026-08-27 | Created the planned reusable blueprint for worker-specific delivery charters. |

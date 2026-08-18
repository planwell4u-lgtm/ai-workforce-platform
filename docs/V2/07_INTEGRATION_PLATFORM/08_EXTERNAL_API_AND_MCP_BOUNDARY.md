# 08_EXTERNAL_API_AND_MCP_BOUNDARY

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines the public and cross-platform API, event, webhook-response, and MCP-compatible boundaries through which Integration capabilities are discovered, requested, observed, and administered.

The boundary exposes versioned, provider-neutral contracts. It does not expose provider SDKs, credentials, direct database access, unrestricted connector operations, or a bypass around action authorization and approval.

---

# Purpose

The API and MCP boundary lets approved agents, services, operators, and developer consumers use Integration safely while preserving tenant scope, least privilege, data minimization, compatibility, audit, and external-effect controls.

---

# Objectives

- Define versioned capability discovery, action request, outcome, approval, administration, and event contracts.
- Ensure every API/MCP operation resolves trusted caller, tenant/environment, purpose, entitlement, connector/capability, and representation scope.
- Separate discovery, request, approval, execution status, and protected evidence access.
- Contain MCP tools to the same registry, authorization, credential, execution, and audit rules as other Integration surfaces.
- Support compatibility, deprecation, rate limits, idempotency, error privacy, observability, and consumer migration.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| API gateway admission, organization/tenant context, shared version policy, and service discovery | 16_PLATFORM_FOUNDATION |
| Enterprise authentication, authorization, secrets, cryptography, compliance, and audit infrastructure | 09_SECURITY_PLATFORM |
| Agent reasoning, MCP client selection, prompt behavior, or business intent | 02_AGENT_PLATFORM |
| Connector registry, credential delegation, action approval, execution, or workflow mechanics | Integration documents 03–07 |
| Canonical Conversation state, routing, participant communication, or channel delivery | 03_CONVERSATION_PLATFORM, 04_VOICE_PLATFORM, and 17_DIGITAL_CHANNEL_PLATFORM |
| Incoming provider webhook validation | 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md |

---

# Boundary Principles

## One Action Path for Every Surface

REST, event, internal service, operator, and MCP requests all create the same bounded ActionRequest and traverse the same current guard, approval, credential, idempotency, execution, outcome, and audit path. No API or MCP tool has direct provider authority.

## MCP Tool Is a Capability View, Not a Privileged Runtime

An MCP tool maps to a registered Integration capability and an approved representation of its schema/result. The MCP server does not grant additional tenant, connector, credential, or action authority because a model can see or invoke a tool.

## Contracts Are Provider-Neutral and Versioned

Published schemas contain platform IDs, normalized outcomes, protected references, and declared compatibility. Provider method names, account IDs, raw payloads, tokens, error details, and SDK types remain inside adapters.

## Read Is Also Scoped

Capability discovery, action status, audit evidence, and outcome retrieval each require current purpose, tenant/environment, principal, representation, and access evaluation. A correlation ID or action ID is not a read credential.

---

# Surface Model

| Surface | Permitted purpose | Must not expose |
|---|---|---|
| Capability discovery API | List currently visible registered capability metadata. | Credentials, provider accounts, hidden capabilities, other tenant state. |
| Action request API | Submit one validated, idempotent bounded intended effect. | Direct dispatch, provider payload, implicit approval. |
| Approval API | Present/request/record approved confirmation or delegated approval. | Raw sensitive parameters beyond authorized representation. |
| Action status/outcome API | Return normalized bounded state and protected evidence references. | Canonical Conversation state, raw provider response, unscoped audit. |
| Administration API | Enable/configure a connector or profile under privileged governance. | Broad runtime credential access or ordinary business actions. |
| Event subscription | Deliver authorized normalized Integration facts. | Commands, secrets, raw external content, cross-tenant fan-out. |
| MCP server | Expose approved tool and resource representations to an authorized MCP client. | Arbitrary provider API, shell/database access, or policy bypass. |

---

# Core Contract Operations

| Operation | Required request controls | Result |
|---|---|---|
| `capabilities.list` | Trusted context, purpose, visibility scope, compatibility. | Minimal available/restricted capability metadata. |
| `actions.create` | Capability/schema, target/parameters, idempotency, current context, representation validation. | Action reference and authorization/approval state; not assumed execution. |
| `actions.get` | Current read authorization and action scope. | Normalized action/outcome state and allowed representation. |
| `approvals.submit` | Request fingerprint, authorized approver/confirmation, expiry, correlation. | Recorded decision or restriction. |
| `connectors.admin.*` | Privileged delegated authority, separation of duties, change/audit requirements. | Controlled configuration lifecycle outcome. |
| `events.subscribe` | Tenant, event type, purpose, representation, delivery authorization. | Versioned facts with replay/ordering contract. |
| `mcp.tools.list` / `mcp.tools.call` | Same discovery/action rules plus MCP client/workload identity and tool schema validation. | Registered capability view / standard ActionRequest result. |

Every mutation supports a documented idempotency key and returns a correlation reference. Read APIs never translate an unknown ID into target-existence disclosure.

---

# MCP-Specific Controls

MCP-compatible exposure is optional per capability/profile. Before a tool is listed or called, the MCP boundary validates client/workload identity, tenant/environment, allowed server, session/connection scope, purpose, tool/capability version, input schema, rate/cost limits, and current availability.

MCP resources expose only approved, read-scoped representations; they cannot become a general data browser. Tool output returns a normalized action/outcome representation, not a raw credential, provider response, or authorization policy explanation. An MCP server must not accept model-generated instructions as policy, activate a connector, alter grants, or execute an effect outside the ActionRequest path.

MCP protocol support does not make a connector capability public. Each server and tool is explicitly registered, tenant/profile-scoped, versioned, monitored, tested, and retired through the same Integration lifecycle.

---

# Versioning and Compatibility

Contracts use explicit semantic versions or an equivalent documented compatibility policy. Additive optional fields are preferred. Changes to effect class, required inputs, approval requirements, data classification, outcome semantics, idempotency, error behavior, or representation require a new compatible version or migration plan.

Each deprecated endpoint, event, MCP tool, or resource identifies replacement, support window, tenant/profile impact, consumer migration, rollout/rollback, telemetry, and retirement date. A provider SDK update cannot silently alter a public API/MCP contract.

---

# API Security, Privacy, and Tenant Isolation

All calls use Platform Foundation API-edge context and Security-managed identity/authorization. Integration validates trusted tenant/environment, subject/purpose, entitlement, connector/profile, action scope, and representation at the service boundary and again before effectful execution.

Requests and responses are schema-validated, size-limited, rate-limited, replay/idempotency-protected, classified, redacted/minimized, logged safely, and audited as required. URLs, headers, callback locations, provider IDs, error text, tokens, and client metadata are untrusted input. Detailed data requires a separate authorized evidence/artifact representation path.

---

# Platform Foundation and Channel Boundaries

Platform Foundation owns API-edge policy, tenant context, routing, and shared version/discovery contracts. Integration defines domain operations and validates its scope; it does not create a parallel gateway or tenant control plane.

Voice and Digital Channel Platforms may invoke an approved Integration action through these contracts but do not expose Integration provider APIs to participants. Integration does not choose a participant channel, send delivery, or treat a channel request as approval without the current action guard.

---

# Observability and Audit

Required signals include API/MCP operation/version, caller/workload category, tenant-safe scope, capability/profile, schema validation, authorization/approval outcome, idempotency, rate/cost limit, error category, action correlation, outcome certainty, and compatibility/deprecation usage.

Events and logs contain normalized categories and protected references. They exclude credentials, raw provider payloads, sensitive inputs, detailed policy rules, direct participant identity, and unrestricted target information.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Integration API/event schema catalog | Defines operations, schemas, versions, compatibility, errors, idempotency, and representation. | Integration with Platform Foundation, Security, and Testing owners |
| MCP server/tool/resource catalog | Defines registered MCP servers, tools, resources, profile scope, input/output contracts, and retirement. | Integration with Agent, Security, and Testing owners |
| Boundary security standard | Defines identity, tenant, purpose, validation, rate/replay, privacy, evidence, and audit. | Integration with Security and Platform Foundation owners |
| Consumer migration policy | Defines deprecation, support windows, telemetry, replacement, rollout, and rollback. | Integration with Operations and consumer owners |
| API/MCP conformance suite | Proves no provider bypass, cross-tenant disclosure, unsafe output, compatibility break, or direct effect. | Integration with Testing and Security owners |

---

# Anti-Patterns

## MCP Tool Calls Provider SDK Directly

Every MCP call creates a bounded ActionRequest and uses the same guard, credential, execution, and audit path as every other surface.

## Tool Listing Grants Permission

Discovery visibility is not permission to call a tool, access credentials, or execute a high-impact action.

## Action ID Is an Evidence Token

Action and correlation IDs require current read authorization; they cannot be guessed, replayed, or used across tenants.

## API Version Is Just a URL Label

Version changes include schema, semantics, privacy, idempotency, lifecycle, consumer compatibility, and migration review.

---

# Related Documents

| Document | Relationship |
|---|---|
| 03_TOOL_AND_CONNECTOR_REGISTRY.md | Defines registered capability and lifecycle metadata. |
| 05_ACTION_AUTHORIZATION_AND_APPROVAL.md | Defines the action guard and approval model. |
| 06_ACTION_EXECUTION_AND_IDEMPOTENCY.md | Defines dispatch and outcome handling. |
| 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md | Defines incoming external event boundary. |
| 10_INTEGRATION_ACCESS_AND_TENANT_ISOLATION.md | Defines access/scope isolation. |
| 16_INTEGRATION_TECHNOLOGY_REFERENCE_MAP.md | Will map API, webhook, MCP, workflow, and SDK technology choices. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created external API and MCP boundary covering versioned contracts, tool exposure, security, compatibility, and audit. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

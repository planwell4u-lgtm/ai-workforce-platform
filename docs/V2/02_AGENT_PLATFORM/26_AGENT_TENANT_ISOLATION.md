# 26_AGENT_TENANT_ISOLATION

**Version:** 2.0  
**Status:** Deprecated  
**Phase:** Agent Platform

**Replacement:** `26A_AGENT_TENANT_BOUNDARY_REWRITE_DRAFT.md` (Approved)  
**Deprecation Date:** 2026-08-07  
**Deprecation Note:** Retained for historical reference. Its previous tenant-ownership model is superseded by the approved Agent-to-Tenant boundary.

---

# Overview

This document defines how the Agent Platform preserves tenant boundaries while creating, configuring, executing, observing, and recovering AI agents. It ensures that one organization’s agents, instructions, capabilities, conversations, context, knowledge access, memory access, workflows, tools, events, and operational records cannot be accessed, influenced, or exposed by another tenant.

The document applies the project’s **Multi-Tenant First** principle to the Agent Platform. It defines the required tenant context, authorization behavior, propagation rules, validation points, and audit expectations. It does not replace the Security Platform’s identity and authorization controls or the Data Platform’s storage-isolation implementation.

---

# Purpose

The purpose of this model is to make tenant isolation an explicit, verifiable property of every Agent Platform operation rather than an assumption made by individual services or developers.

It provides a shared contract so that the Agent Runtime, Execution Engine, Context Model, Tool System, Workflow Integration, Event Integration, Multi-Channel Model, and Session Management model consistently preserve the same tenant boundary.

---

# Objectives

The Agent Tenant Isolation Model must:

- Require authoritative tenant context for every tenant-scoped operation.
- Prevent cross-tenant reads, writes, execution, configuration, events, and delivery.
- Bind agent identity, configuration, capability, model eligibility, and policy to a tenant.
- Propagate tenant context safely across synchronous, asynchronous, event-driven, and background work.
- Ensure tenant boundaries remain effective in caches, logs, traces, metrics, search, analytics, replay, support, and recovery.
- Fail closed when tenant context is missing, ambiguous, inconsistent, or unauthorized.
- Support controlled platform administration without implicitly granting tenant-data access.
- Provide testable contracts and evidence for implementation and operational review.

---

# Scope

This document defines:

- The tenant context contract for Agent Platform requests and events.
- Tenant-scoped ownership and lifecycle rules for agents and agent-related resources.
- Propagation and validation requirements across runtime, sessions, channels, workflows, tools, and events.
- Cross-tenant prevention rules for data access, caching, observability, operations, and recovery.
- Tenant-aware authorization, audit, testing, and implementation artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Tenant, organization, membership, configuration, and entitlement facts; enterprise identity and authorization policy | Platform Foundation owns the tenant/control-plane facts; Security Platform owns identity and authorization policy |
| Database partitioning, encryption keys, backup, residency, and storage implementation | Data Platform |
| Platform-wide multi-tenant infrastructure, network boundaries, and deployment controls | Deployment and Security Platforms |
| Detailed permission grants, roles, and policy evaluation | `25_AGENT_PERMISSION_MODEL.md` |
| Agent security principles, data classification, and incident response | `24_AGENT_SECURITY_MODEL.md` |
| Channel provider protocol mapping | `22_AGENT_MULTI_CHANNEL_MODEL.md` |
| Canonical conversation/session lifecycle | `23_AGENT_SESSION_MANAGEMENT.md` |
| Knowledge and memory ownership or retention policy | Knowledge Platform and Memory Platform |

---

# Tenant Isolation Principles

## Tenant Context Is Mandatory

Every tenant-scoped request, record, event, job, cache entry, audit record, and external action includes an authoritative `tenantId`. Missing tenant context never means “all tenants,” “default tenant,” or “platform access.” The operation is denied or quarantined.

## Tenant Is an Authorization Constraint

Tenant scope is evaluated before ordinary role, grant, ownership, or capability checks. A valid identity or broad platform role does not permit access to a tenant resource without an explicit tenant-scoped authorization decision.

## One Resource Has One Tenant Owner

Every tenant-owned agent resource has one immutable tenant owner for its lifetime. Resources include agents, agent versions, instructions, configurations, sessions, execution records, context snapshots, workflow references, tool connections, event subscriptions, and channel mappings.

Cross-tenant sharing is prohibited by default. Any future shared catalog, template, or marketplace capability must use an explicitly designed publication and copy/import model; it must not create a mutable shared tenant resource.

## Propagate, Do Not Infer

Services carry validated tenant context through approved contracts. They must not infer a tenant from a hostname, user-supplied identifier, email domain, phone number, cache key, provider account, or unvalidated payload.

## Partition Every Operational Surface

Tenant isolation applies beyond business data. Caches, queues, events, logs, traces, metrics, search indexes, analytics, dead-letter flows, backups, support tools, and operational dashboards must preserve tenant scope and access controls.

## Fail Closed and Make Ambiguity Visible

When tenant identity conflicts across a request, session, event, resource, delegation, or provider binding, the operation fails closed and produces a security-relevant audit signal. It is never silently reassigned to another tenant.

---

# Tenant Context Contract

Every Agent Platform boundary uses a versioned tenant-context contract.

```text
Tenant Context
|
+-- tenantId
+-- organizationId               (when applicable)
+-- environment
+-- region / residency scope     (when applicable)
+-- authenticated subject
+-- workload identity
+-- authorization decision reference
+-- purpose and classification
+-- correlationId / causationId / traceId
+-- issuedAt / expiresAt
```

## Authoritative Sources

`tenantId` is established only from an authenticated, trusted source: an approved identity claim, tenant-bound service credential, validated channel/provider configuration, or signed internal contract. User input, model output, external event payload, and tool result may carry a tenant hint but cannot establish or override tenant context.

## Validation Rules

Every Policy Enforcement Point validates that the tenant context:

- Exists and has an approved format.
- Matches the authenticated subject or workload binding.
- Matches the target resource’s immutable tenant owner.
- Matches the session, conversation, event, workflow, tool, and channel references when present.
- Is within the decision’s scope, environment, region, and expiry.
- Has not been altered or broadened during propagation.

## Context Lifetime

Tenant context is immutable for a request or execution session. A new request, event, or background job obtains a new validated context. Context propagation tokens are short-lived, scoped, integrity-protected, and not reusable as broad authorization credentials.

---

# Tenant-Scoped Agent Resources

## Agent Control Plane

An agent, its configuration, instructions, persona, capabilities, tool assignments, model eligibility, policies, and versions belong to exactly one tenant. Creating, cloning, importing, publishing, or changing them requires a tenant-scoped control-plane decision.

Platform-provided defaults are templates, not tenant-owned live configuration. A tenant must explicitly adopt or copy a template into its own governed configuration before it becomes executable.

## Agent Runtime and Execution

Each execution is bound to one tenant before context assembly or model invocation. A runtime worker may process work for multiple tenants over time, but a single execution, context snapshot, tool invocation, workflow action, and result record cannot span tenants.

Worker reuse must clear tenant-scoped in-memory state, request caches, model-session references, and temporary files between executions. The runtime must not retain prior tenant context as an implicit default.

## Context, Knowledge, and Memory Access

Context assembly retrieves only data authorized for the current tenant and purpose. A global search index, knowledge catalog, memory service, or analytics store does not permit cross-tenant discovery; the tenant filter is mandatory and enforced by the owning platform.

The Agent Platform records source references and tenant scope but does not duplicate another platform’s data or weaken its access policy.

---

# Propagation Across Platform Boundaries

## Channels and Sessions

Channel adapters bind each provider account, phone number, sender identity, web client, or API credential to an approved tenant configuration before an interaction is normalized. The Interaction Gateway validates that the resulting tenant context matches the target agent and session resolution result.

A cross-channel conversation association is permitted only within the same tenant. A shared contact detail across tenants is not grounds for linking conversations, users, memories, or customer records.

## Events and Background Work

Tenant-scoped events include tenant context in their envelope and are published only by an authorized tenant-bound producer. Consumers validate the envelope and subscription eligibility before handling the event.

Background jobs, schedules, retries, dead-letter processing, replay, and delayed workflows persist the tenant context with the durable work item and revalidate it before execution. Replays never run under an operator’s broad platform context by default.

## Workflows and Tools

Workflow instances and tool invocations receive tenant scope from the initiating authorized execution or a validated event. They validate it again against their target resource, integration connection, parameter constraints, and authorization decision.

An integration connection, external account, credential, webhook endpoint, or delivery target is tenant-bound. The platform must not use a connection configured by Tenant A while executing work for Tenant B.

---

# Isolation Controls by Surface

| Surface | Required control |
|---|---|
| APIs and service calls | Validated tenant context, tenant-scoped authorization, resource-owner check |
| Databases and storage | Data Platform-enforced partitioning, tenant keying, and controlled access paths |
| Caches | Tenant-prefixed keys, scoped eviction, no cross-tenant shared objects, bounded TTL |
| Queues and events | Tenant envelope, producer/consumer authorization, subscription filtering, replay validation |
| Search and retrieval | Mandatory tenant filter enforced by the owning service; no client-controlled bypass |
| Runtime workers | Per-execution context isolation and clearing of temporary tenant state |
| Tool and integration calls | Tenant-bound connection, parameter validation, decision scope, and audit |
| Channels and delivery | Tenant-bound provider configuration, recipient/consent validation, and delivery authorization |
| Logs, traces, metrics | Tenant tags with access-controlled query and redaction; no sensitive payload by default |
| Analytics and reporting | Tenant-filtered query paths, aggregation controls, and approved anonymization only |
| Operations and support | Scoped just-in-time access, tenant selection, purpose, audit, and expiration |
| Backup, replay, and recovery | Tenant-aware restore/replay scope, authorization, and verification before action |

---

# Platform Administration and Support

Platform administration is separate from tenant-data access. A platform operator may administer shared infrastructure or configuration without seeing tenant content. Access to a particular tenant’s protected records requires an additional scoped authorization, business purpose, expiry, and audit trail.

Support, incident response, migration, and recovery tools require an explicit tenant selector. Bulk or multi-tenant operations are permitted only through approved administrative workflows with a declared tenant set, purpose, safeguards, and enhanced audit. An empty selector never means every tenant.

---

# Tenant Lifecycle and Resource Lifecycle

## Tenant Activation

Before a tenant can activate agents, the platform establishes a tenant identity, allowed environment and region, administrative authority, security baseline, channel/integration bindings, and applicable policy configuration. Default agent templates are copied or adopted through controlled tenant-scoped operations.

## Suspension and Termination

Suspending a tenant blocks new agent executions, delivery, tool actions, and external integration activity unless an approved legal, recovery, or safety policy specifies otherwise. Tenant termination revokes active grants, credentials, delegations, sessions, subscriptions, scheduled work, and cached decisions according to the owning platform’s lifecycle controls.

Retention, deletion, anonymization, backup expiry, and legal hold are implemented by the Data and Security Platforms. The Agent Platform must stop producing new tenant data and preserve only the references required by approved policy.

## Migration and Region Change

Tenant migration, organization restructuring, and residency change are controlled operations. They require a migration plan, data and identity verification, authorization review, audit, rollback, and post-migration isolation tests. Resource ownership is not silently reassigned during ordinary execution.

---

# Failure Handling and Recovery

## Tenant Mismatch

When a tenant mismatch occurs, the platform denies or quarantines the operation, prevents side effects, records the involved references without exposing protected content, and emits a security-relevant signal. Automatic retries are allowed only after the source context is corrected and revalidated.

## Missing Context

Missing tenant context causes a fail-closed outcome for tenant-scoped work. The platform may route the item for authorized reconciliation or human review, but it must not assign a default tenant or process the work as platform-scoped.

## Replay and Restore

Replay, dead-letter handling, backup restore, and recovery use an explicit tenant scope and revalidate current authorization, lifecycle, consent, classification, idempotency, and external side-effect risk. An operator’s recovery identity does not replace the resource’s original tenant context.

---

# Observability and Audit

Tenant context is included in protected audit metadata for every material Agent Platform action. The platform records tenant identity, resource owner, subject/workload, decision reference, channel/session/event/workflow/tool correlation, outcome, and any isolation failure.

Tenant-facing observability is filtered to the requesting tenant. Platform-level metrics use approved aggregation and anonymization where required. Support and operational access to traces or logs is purpose-bound, tenant-scoped, time-limited, and auditable.

Key metrics include tenant-mismatch denials, missing-context rejections, cross-tenant retrieval attempts, scope-validation failures, tenant-scoped cache collision findings, unauthorized subscription attempts, recovery/replay rejections, and support-access review completion.

---

# Testing Strategy

## Contract Tests

Contract tests validate the tenant-context schema, propagation fields, immutable owner binding, event envelopes, authorization-scope matching, and failure responses for missing or conflicting context.

## Isolation Tests

Isolation tests create multiple representative tenants and verify that agents, configurations, sessions, context, knowledge references, memory references, workflows, tools, events, channels, caches, logs, and operational queries cannot cross boundaries.

## Resilience Tests

Tests simulate worker reuse, delayed jobs, duplicate events, replay, dead-letter handling, cache eviction, provider callback mismatch, migration failure, tenant suspension, and recovery. They verify that a fault cannot cause a request to inherit or leak a previous tenant context.

## Security Tests

Security tests verify forged tenant claims, manipulated event envelopes, cross-tenant identifier guessing, broad operator access, unauthorized provider binding, stale authorization, cache-key collision, and attempts to use Tenant A’s tool or channel connection for Tenant B.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Tenant-context schema | Versioned request, event, job, and audit context contract | Agent Platform with Security Platform review |
| Tenant resource-ownership registry | Defines tenant-owned Agent Platform resources and immutable owner fields | Agent Platform |
| Tenant propagation standard | Defines boundary validation, token lifetime, event/job propagation, cache requirements, and failure behavior | Agent Platform and platform engineering |
| Isolation control matrix | Maps every data and operational surface to required controls and tests | Agent, Data, Security, and Operations Platform owners |
| Tenant lifecycle runbook | Defines activation, suspension, termination, migration, recovery, and audit steps | Tenant, Security, Data, and Operations owners |
| Cross-tenant test suite | Automated isolation, regression, resilience, and security test scenarios | Engineering and Testing Platform owners |
| Support-access procedure | Defines just-in-time tenant access, approval, expiry, logging, and review | Security and Operations Platform owners |

---

# Anti-Patterns

## Default Tenant

Using a fallback tenant for a missing, malformed, or delayed request turns an integration error into a data-isolation incident. Tenant-scoped work must fail closed.

## Tenant Inference from User Content

Email domains, phone numbers, agent prompts, model output, and provider payload fields may be useful evidence but cannot establish tenant ownership without trusted binding and authorization.

## Shared Cache Without Tenant Keying

Storing context, permissions, responses, credentials, or lookup results in a shared cache without robust tenant scoping can leak data despite correct database controls.

## Platform Administrator Equals Tenant Reader

Infrastructure administration is not permission to inspect tenant content. Support and recovery access requires a separate, scoped, auditable decision.

## Cross-Tenant Template Mutation

Allowing a tenant to modify a shared template changes other tenants’ behavior and violates ownership. Publish templates as immutable shared artifacts and require controlled tenant adoption.

## Replay Under Operator Context

Replaying a tenant event under a broad operator identity can bypass original restrictions. Replay must retain and revalidate the tenant scope and current policy.

---

# Related Documents

| Document | Relationship |
|---|---|
| `00_CONTROL/03_ARCHITECTURE_PRINCIPLES.md` | Establishes Multi-Tenant First, modular ownership, and event-driven principles. |
| `00_CONTROL/04_SYSTEM_BOUNDARIES.md` | Defines Data and Security Platform ownership boundaries. |
| `00_CONTROL/05_MODULE_OWNERSHIP.md` | Defines the mission and responsibility of each platform module. |
| `07_AGENT_RUNTIME_ARCHITECTURE.md` | Applies tenant binding and isolation to runtime workers and executions. |
| `08_AGENT_EXECUTION_ENGINE.md` | Requires tenant-scoped reasoning context and execution records. |
| `11_AGENT_CONTEXT_MODEL.md` | Defines bounded, authorized context assembly. |
| `15_AGENT_TOOL_SYSTEM.md` | Requires tenant-bound tools, integrations, and actions. |
| `20_AGENT_WORKFLOW_INTEGRATION.md` | Requires tenant-safe workflow initiation and state transitions. |
| `21_AGENT_EVENT_INTEGRATION.md` | Defines tenant-scoped event contracts, subscriptions, and replay. |
| `22_AGENT_MULTI_CHANNEL_MODEL.md` | Binds channels, delivery, and cross-channel continuity to a tenant. |
| `23_AGENT_SESSION_MANAGEMENT.md` | Owns tenant-scoped conversation and session references. |
| `24_AGENT_SECURITY_MODEL.md` | Defines zero-trust security, data protection, and incident controls. |
| `25_AGENT_PERMISSION_MODEL.md` | Defines tenant-scoped authorization decisions, grants, and enforcement. |
| `08_DATA_PLATFORM` | Owns persistence, storage, backup, retention, and data-isolation implementation. |
| `09_SECURITY_PLATFORM` | Owns enterprise authentication, authorization, security policy, and compliance. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Agent Tenant Isolation architecture document. |

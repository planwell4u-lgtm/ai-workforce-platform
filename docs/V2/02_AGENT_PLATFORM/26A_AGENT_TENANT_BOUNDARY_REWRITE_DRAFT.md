# 26A_AGENT_TENANT_BOUNDARY_REWRITE_DRAFT

**Version:** 1.1  
**Status:** Approved  
**Owner:** Agent Platform Owner  
**Phase:** Agent Platform approval review  
**Supersedes:** `26_AGENT_TENANT_ISOLATION.md`  

**File-name note:** The working filename is retained to preserve review traceability; this approved document is the authoritative Agent-to-Tenant boundary.  

---

# Purpose

This draft defines how Agent Platform consumes Platform Foundation tenant-control-plane facts and applies them to Agent-owned resources and execution. Every Agent operation must use trusted tenant, organization, membership, configuration, and entitlement context and must fail safely when that context is missing, inconsistent, inactive, or unauthorized.

Platform Foundation owns tenant, organization, workspace, membership, configuration, entitlement, API-edge, and lifecycle facts. Security Platform owns identity, authorization, security policy, secrets, cryptography, and compliance controls. Data Platform owns physical partitioning, storage, deletion, recovery, and residency mechanisms. Agent Platform owns only the tenant-scoped behavior of Agent resources and execution within those controls.

---

# Boundary Model

| Concern | Authoritative owner | Agent Platform responsibility |
|---|---|---|
| Tenant, organization, workspace, membership, configuration, entitlement, and control-plane lifecycle facts | Platform Foundation | Consume current trusted facts; bind Agent resources and execution to them without redefining their lifecycle. |
| Identity, authorization, policy, workload trust, secrets, and security evidence | Security Platform | Obtain and enforce current decisions for Agent-owned resources/actions. |
| Database partitioning, storage, cache, vectors, backups, deletion, residency, and recovery | Data Platform | Require tenant scope in Agent contracts; never bypass Data mechanisms or access shared stores directly. |
| Canonical conversations, participants, sessions, routing, and handoff | Conversation Platform | Use approved tenant-scoped references and report outcomes through owned contracts. |
| Knowledge, Memory, Workflow, connector, and channel behavior | Their respective platforms | Consume only authorized tenant-scoped contracts. |
| Agent definitions, versions, instructions, capabilities, context assembly, execution records, and behavior evidence | Agent Platform | Maintain a single immutable tenant association for each Agent-owned resource and validate it at every boundary. |

---

# Required Tenant Context

Agent requests, events, work items, context snapshots, configuration reads, and outcome reports carry trusted references for tenant, organization/workspace where applicable, actor or workload, purpose, environment, correlation, and relevant configuration/entitlement version. These values are resolved or verified by approved server-side contracts, not accepted as authority from a client, prompt, channel identifier, provider callback, or model output.

An Agent resource has one immutable tenant owner. Cross-tenant sharing, cloning, migration, support access, analytics, recovery, or administrative work requires an explicit cross-platform policy and auditable authorization; it is never implied by a platform role or common provider account.

---

# Enforcement Rules

- Validate tenant context at ingress, configuration resolution, context assembly, capability selection, tool/workflow request, event consumption, asynchronous resume, delivery, replay, and recovery.
- Bind cache keys, idempotency keys, correlation references, logs, metrics, traces, exports, and search filters to the proper tenant scope and classification.
- Treat membership, entitlement, tenant state, configuration, and policy changes as invalidation events for affected Agent work and cached context.
- Deny, quarantine, defer, or terminate work when tenant scope is absent, ambiguous, inconsistent, suspended, terminated, or unauthorized.
- Do not use a broad operator, service, or provider identity to bypass the originating tenant scope during support, replay, reconciliation, or recovery.
- Pass tenant context only through approved contracts; downstream platform owners must independently validate and enforce their own scope.

---

# Tenant Lifecycle Behavior

When Platform Foundation changes a tenant's lifecycle, membership, entitlement, or configuration, Agent Platform re-resolves the relevant facts before continuing material work. Suspension blocks new Agent work and triggers safe restriction or cancellation of affected in-flight work according to the owning platform's rules. Termination, deletion, legal hold, retention, recovery, and residency execution remain governed by Platform Foundation, Data, Security, and domain owners; Agent Platform supplies its owned references and honors the returned disposition.

---

# Evidence and Validation

The boundary must prove that:

- a tenant mismatch, identifier substitution, stale membership, expired entitlement, or ambiguous scope cannot reach Agent behavior or external effects;
- configuration and entitlement changes invalidate cached Agent decisions and context;
- asynchronous events, retries, replays, support, analytics, and recovery retain and revalidate tenant scope;
- Agent telemetry and exports are tenant-scoped, minimized, and access-controlled;
- suspension, revocation, and termination cause safe restriction rather than cross-tenant fallback or fabricated completion;
- Agent contracts never require direct database/provider access to establish tenant truth.

---

# Authoritative References

- `16_PLATFORM_FOUNDATION/01_PLATFORM_FOUNDATION_ARCHITECTURE.md`
- `16_PLATFORM_FOUNDATION/02_TENANT_ORGANIZATION_AND_MEMBERSHIP_MODEL.md`
- `16_PLATFORM_FOUNDATION/03_CONFIGURATION_AND_ENTITLEMENT_MODEL.md`
- `16_PLATFORM_FOUNDATION/05_FOUNDATION_SECURITY_AND_TENANT_ISOLATION.md`
- `08_DATA_PLATFORM/09_DATA_ACCESS_AND_TENANT_ISOLATION.md`
- `08_DATA_PLATFORM/10_DATA_SECURITY_PRIVACY_AND_RESIDENCY.md`
- `09_SECURITY_PLATFORM/03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md`
- `09_SECURITY_PLATFORM/08_TENANT_ISOLATION_AND_DATA_PROTECTION.md`

---

# Approval Conditions

The Agent and Platform Foundation review confirmed that this document consumes, rather than redefines, tenant-control-plane facts and lifecycle authority. `26_AGENT_TENANT_ISOLATION.md` remains available as a deprecated historical artifact; this document is the authoritative replacement.

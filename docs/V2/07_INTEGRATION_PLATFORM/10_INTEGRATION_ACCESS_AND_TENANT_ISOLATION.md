# 10_INTEGRATION_ACCESS_AND_TENANT_ISOLATION

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how Integration Platform enforces tenant, environment, subject, purpose, connector, credential, external-resource, action, workflow, event, and evidence isolation.

Integration applies the enterprise tenant and access model to external-system operations. It does not own tenant lifecycle, identity, authorization policy, storage partitioning, or network controls.

---

# Purpose

The model prevents one tenant, subject, provider account, connector, callback, credential, queue message, cache entry, workflow, support session, or external-resource reference from discovering, accessing, changing, or affecting another tenant's integration scope.

---

# Objectives

- Bind every material Integration record and operation to one trusted tenant and environment.
- Require current subject, purpose, entitlement, connector/capability, credential-grant, target-resource, and representation scope where applicable.
- Prevent provider account, API key, OAuth subject, callback, URL, action ID, cache key, or client field from selecting or widening tenant scope.
- Enforce isolation across configuration, registry visibility, credentials, execution, callbacks, queues, caches, telemetry, audit, support, migration, and recovery.
- Fail closed on ambiguous, stale, mismatched, or revoked scope.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Tenant/organization/membership/entitlement/configuration lifecycle | 16_PLATFORM_FOUNDATION |
| Enterprise authentication, authorization engine, network, key, compliance, or incident controls | 09_SECURITY_PLATFORM |
| Data-store partitioning, backup, physical deletion, residency infrastructure, or analytics implementation | 08_DATA_PLATFORM |
| Capability registry, credential lifecycle, action authorization, execution, workflow, or webhook semantics | Integration documents 03–09 |
| Canonical participant/conversation/work state | 03_CONVERSATION_PLATFORM |

---

# Isolation Principles

## One Tenant and Environment per Integration Resource

Connectors, profiles, account bindings, grants, credential references, capability availability, actions, attempts, workflows, callbacks, external-operation mappings, audit records, queues, caches, metrics, and support references have one immutable trusted tenant/environment binding.

## Server-Resolved Scope

Tenant/environment and current access context come from authenticated server-side Platform Foundation/Security contracts. Client input, provider account, token claim, callback payload, URL, action ID, or external ID is evidence to validate—not an authority to choose scope.

## Correlation Is Not Access

Action, workflow, trace, provider, callback, or external-resource correlation links records only inside its existing scope. It cannot be used to query, join, export, replay, or authorize data/effects in another scope.

## Ambiguity Fails Closed

Mismatch, missing scope, stale mapping, replay, resource reassignment, grant revocation, or conflicting provider evidence produces deny, restrict, quarantine, or reconciliation—not a best-match tenant or fallback account.

---

# Required Access Context

Every material operation validates trusted references for tenant/environment; principal/workload; subject and purpose where relevant; entitlement/configuration; connector/capability/profile; provider account/resource; credential grant/lease; action/workflow/callback; target representation/classification/egress; lifecycle/approval/policy; idempotency/correlation; and audit/incident restriction.

All relevant bindings must match before effect. A prior action, cached record, active provider session, or support context cannot authorize a new operation.

---

# Isolation Boundaries

| Boundary | Required control |
|---|---|
| Connector/profile | Tenant/environment-scoped configuration, visibility, lifecycle, and provider account mapping. |
| Credential/grant | One approved account/resource/scope; least privilege, expiry, revocation, and no cross-tenant reuse. |
| Action/workflow | Immutable scope snapshot and revalidation before each effectful transition. |
| External resource | Protected mapping plus current target/purpose/access check; provider ID is not platform identity. |
| Queue/cache/job | Protected tenant/environment key, bounded expiry, scoped consumer, and no wildcard/unscoped replay. |
| Callback/event | Source, account/resource, tenant, action/workflow, freshness, replay, and ordering validation. |
| Telemetry/audit/support | Tenant-safe references, purpose-bound access, minimized representation, expiry, and audit. |
| Migration/recovery | Explicit source/destination scope, reauthorization, rollback, historical evidence, and no stale resurrection. |

---

# Access Guard

Before discovery, read, administration, credential lease, dispatch, callback use, workflow continuation, evidence access, export, support, migration, or recovery, Integration evaluates:

1. trusted tenant/environment and principal/workload;
2. current authorization/entitlement/purpose/subject relationship;
3. resource, connector/profile, account, credential, action/workflow, and target binding;
4. policy, classification, representation, egress, residency, lifecycle, approval, and incident constraints;
5. correlation/idempotency/freshness/order/rate/capacity conditions; and
6. required audit evidence and safe outcome.

The guard is re-run at each sensitive boundary. It does not rely solely on a database uniqueness constraint, provider account, RLS policy, or earlier request context.

---

# Administration and Support

Tenant administrators can manage only their own authorized connector configuration and approved representations. Platform operators/support have no implicit broad account, action, credential, payload, or external-resource access.

Exceptional support requires explicit tenant scope, purpose, time bound, delegated authority, least-privilege representation, approval where required, audit, expiry/revocation, and post-access review. Support tooling denies target-existence disclosure on scope mismatch.

---

# Lifecycle, Migration, and Recovery

Tenant creation creates only approved scoped Integration configuration. Suspension/deactivation blocks new connector enablement, credential use, action dispatch, workflow continuation, callback progression, and evidence/export access except explicitly authorized legal/incident operations.

Connector/account/resource migration identifies source/destination scope, authorization, effective time, permitted references/data, credential transition, in-flight treatment, rollback, retention/deletion/hold, and audit. Cross-tenant transfer is exceptional and never occurs through account reuse, callback correlation, cache recovery, or routine support.

Restart/failover restores only durable protected references and revalidates every operation before continuation. It never reconstructs tenant scope from provider payload or unscoped cache.

---

# Outcomes, Observability, and Audit

Normalized outcomes are `ScopeValidated`, `ScopeDenied`, `ScopeAmbiguous`, `ScopeStale`, `ScopeRestricted`, and `ScopeIncident`. A denial does not reveal target existence, owner, connector, provider account, credential, or content.

Telemetry measures scope validation/denial/ambiguity/staleness, cross-tenant attempt, provider/account mismatch, cache/queue isolation failure, support access, migration validation, callback mismatch, and containment. Audit records scope at creation/change, high-risk operation, callback, credential use, workflow step, support, migration, incident, and recovery using protected references.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Integration access-context contract | Defines required bindings, propagation, validation, mismatch, and audit. | Integration with Platform Foundation and Security owners |
| Resource/credential isolation standard | Defines scoped connectors, accounts, grants, actions, workflows, events, and external mappings. | Integration with Security and Data owners |
| Queue/cache/support/migration policy | Defines asynchronous, operational, recovery, and exceptional-access isolation. | Integration with Operations, Data, and Security owners |
| Isolation test suite | Proves no cross-tenant discovery, read, credential use, dispatch, callback, cache, support, or recovery effect. | Integration with Testing and Security owners |

---

# Anti-Patterns

## Provider Account Selects Tenant

Provider evidence is validated against server-resolved tenant scope; it never chooses it.

## Action ID Is a Cross-Tenant Read Key

Every read validates current tenant, purpose, representation, and action binding.

## Shared Queue Is Safe by Default

Every message, key, consumer, retry, and dead letter requires protected tenant/environment scope.

## Support Has Implicit Full Access

Support access is exceptional, purpose-bound, minimized, time-limited, approved, and audited.

---

# Related Documents

| Document | Relationship |
|---|---|
| 04_CONNECTOR_AUTHENTICATION_AND_CREDENTIAL_DELEGATION.md | Defines scoped external grants and leases. |
| 05_ACTION_AUTHORIZATION_AND_APPROVAL.md | Defines current action authority. |
| 07_WORKFLOW_AND_ASYNCHRONOUS_EXECUTION.md | Defines scoped asynchronous continuation. |
| 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md | Defines scoped callback evidence. |
| 12_INTEGRATION_SECURITY_AND_PRIVACY.md | Defines external security and egress controls. |
| 16_PLATFORM_FOUNDATION/README.md | Owns tenant and entitlement facts. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Integration access and tenant isolation architecture covering scope, resources, asynchronous work, support, migration, and recovery. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

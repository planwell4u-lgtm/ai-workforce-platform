# 02_TENANT_ORGANIZATION_AND_MEMBERSHIP_MODEL

**Version:** 1.2  
**Status:** Approved  
**Owner:** Platform Foundation Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines the control-plane facts for organizations, tenants/workspaces, memberships, and their lifecycle. These records establish trusted SaaS scope and accountable relationships for platform contracts; they do not authenticate a principal or decide what any principal may do.

# Ownership and Boundaries

Platform Foundation owns organization, tenant/workspace, membership, lifecycle, provenance, and controlled change facts. Security authenticates identities and makes authorization decisions. Domain platforms own their records and behavior. Data Platform implements storage, retention, deletion, backup, and recovery mechanisms.

An organization is the accountable business boundary. A tenant/workspace is the stable logical operating scope within the platform. A membership records an identity-to-organization/tenant relationship. A role/reference is an input to Security policy, never a direct permission grant.

# Core Model

| Record | Required facts | Boundary |
|---|---|---|
| Organization | Stable reference, lifecycle status, accountable owner/reference, creation/source, environment. | Not a universal authorization group or data container. |
| Tenant/workspace | Stable reference, parent organization, environment, lifecycle/provisioning state, region/profile references. | Does not own domain records, provider accounts, or security policy. |
| Membership | Principal reference, organization/tenant scope, status, source, effective interval, provenance, version. | Requires Security authorization before use. |
| Membership attribute/reference | Bounded role/capability context, source, version, effective interval. | Cannot grant access without current policy. |
| Lifecycle change | Requester, reason, approval, old/new version, correlation, effective time, downstream state. | Does not directly mutate other platforms. |

Stable identifiers are opaque and environment-scoped. Display names, email addresses, provider identifiers, and client-supplied tenant values are not authoritative scope or membership keys. The model prevents ambiguous parentage: a tenant/workspace has one current parent organization unless an explicit governed transfer process completes.

# Lifecycle States and Transitions

| State | Meaning | Allowed transitions |
|---|---|---|
| Provisioning | Record exists but dependencies/readiness are incomplete. | Activate, restrict, cancel. |
| Active | Eligible to supply current scope facts to authorized consumers. | Restrict, offboard, transfer through approved process. |
| Restricted | Scope remains traceable but normal operation/membership use is limited. | Activate after review, offboard. |
| Offboarding | Coordinated retirement, export/hold/deletion/revocation work is pending. | Closed only after downstream evidence; may remain restricted. |
| Closed | No ordinary active use; history remains under lifecycle policy. | New controlled provisioning only, not silent reactivation. |

Membership transitions are pending invitation/proof, active, suspended, revoked, expired, or removed. Activation requires verified identity and authorized change. Suspension/revocation/expiry triggers Security and affected-platform propagation; reactivation is a new reviewed state change, not reuse of stale session, token, delegated access, or cache.

# Provisioning, Change, and Offboarding Flow

1. An authorized requester proposes organization/tenant/membership change with source, environment, owner, purpose, and required dependencies.
2. Foundation validates parentage, identifier uniqueness, current lifecycle/version, request authority, and applicable configuration/entitlement prerequisites.
3. The change is versioned, persisted through Data controls, and applied idempotently with correlation and evidence.
4. Foundation emits a bounded event/reference for Security and affected platforms; each consumer applies its own controlled change.
5. Propagation is observed and reconciled. Partial/delayed delivery is explicit and does not claim completed access, revocation, or offboarding.
6. Offboarding coordinates restriction, Security revocation, Data lifecycle/export/hold, domain retirement, provider cleanup, and final evidence. Foundation does not delete other domains directly.

# Contract and Resolution Rules

Consumers request Foundation facts using verified identity/workload and server-resolved tenant/environment context. Responses include stable references, lifecycle status, version, effective interval, and provenance needed for safe use; they minimize personal attributes. All read/write/cache/event/queue/admin/recovery paths preserve tenant and environment scope.

Client headers, URL parameters, cookies, hostnames, frontend state, and provider claims are candidates to validate, not tenant authority. A consumer rechecks current Foundation status when performing material or delayed work; cached facts have bounded freshness and cannot override revocation, offboarding, or restrictive lifecycle state.

# Security, Privacy, and Evidence

Membership changes are high-risk because they influence later policy decisions. They require current authorization, concurrency/version protection, least disclosure, immutable/tamper-evident evidence where required, and audit of creation, invite/accept, change, suspension, revoke, expiry, transfer, offboarding, recovery, and failed validation.

Evidence identifies trusted scope, actor/workload, operation, old/new version, reason category, outcome, time, correlation, and owner. It excludes credentials and unnecessary identity/profile content. Retention, deletion/hold, residency, export, and support access use Security/Data controls.

# Failure and Recovery

| Condition | Safe outcome |
|---|---|
| Scope/membership lookup unavailable | Defer/restrict or use bounded approved cached fact that cannot widen access. |
| Conflicting/concurrent change | Reject or serialize with version conflict; reconcile explicitly. |
| Propagation delayed | Expose pending/uncertain status, retry idempotently, and reconcile before closure. |
| Suspected compromise or wrong scope | Restrict, preserve evidence, coordinate Security revocation, and revalidate before recovery. |
| Restore/recovery | Recheck current lifecycle, identity, authorization, membership, residency, hold/deletion, and downstream dependencies. |

# Required Artifacts and Tests

Maintain organization/tenant/membership schema and state-transition catalog, contract/version specification, provisioning/offboarding runbooks, propagation/reconciliation map, and audit event catalog. Test invalid parentage, duplicate/ambiguous identity link, cross-tenant/environment misuse, lifecycle transition, invitation/expiry/revocation, optimistic concurrency, delayed/duplicate event, cache staleness, outage, offboarding, restore, and audit evidence.

# Anti-Patterns

## Membership Equals Permission

Membership is a scoped fact consumed by current Security policy; it never bypasses authorization.

## Tenant Identifier Comes From the Browser

Tenant/environment scope is resolved and validated server-side at every protected boundary.

## Offboarding Means Delete One Record

Offboarding is coordinated, observable, lifecycle-aware retirement across Security, Data, providers, and domains.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created tenant, organization, and membership model. |
| 1.1 | 2026-08-07 | Originally approved; reopened after completeness review. |
| 1.2 | 2026-08-07 | Rewritten with full model, lifecycle, contracts, flow, controls, recovery, evidence, and testing detail. |

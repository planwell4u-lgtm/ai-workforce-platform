
**Version:** 1.2  
**Status:** Approved  
**Owner:** Platform Foundation Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how Platform Foundation applies Security Platform controls to organization, tenant, membership, configuration, entitlement, API-edge, and discovery operations. Security owns identity, policy, authorization, secrets, cryptography, enterprise audit, and compliance; Foundation supplies correct current control-plane facts and enforces outcomes at its boundaries.

# Security Control Map

| Control | Foundation responsibility | Security responsibility |
|---|---|---|
| Identity | Require verified human/workload/provider context at protected boundary. | Authentication and trust requirements. |
| Authorization | Present current resource/action/scope/lifecycle facts and enforce result. | Policy, decision, delegation, revocation. |
| Tenant isolation | Preserve trusted tenant/environment on every representation/path. | Protection requirements and assurance. |
| Privilege | Define Foundation admin resource/action; require approval/evidence. | Elevated assurance, policy, break-glass controls. |
| Secrets/trust | Use approved references/workload identity only. | Secret/key/certificate lifecycle and policy. |
| Evidence | Emit Foundation operation outcomes and reconciliation status. | Audit policy, investigation, compliance requirements. |

# Enforcement Points

Foundation enforces at API edge, organization/tenant/membership service, configuration/entitlement resolution, event/queue worker, cache, service discovery, administrative/support interface, import/export, and recovery/reconciliation path. Each point resolves trusted environment and tenant scope, validates identity/workload, obtains current authorization for its resource/action, applies obligations, and records a bounded outcome.

Frontend/client state, tenant headers, role claims, provider data, route knowledge, or stored configuration are never authorization. Membership and entitlement are facts consumed by Security policy and must be rechecked on material/delayed operations.

# Isolation Requirements

Tenant/environment scope is server-resolved and represented in Foundation records, queries, cache keys, queue/event envelopes, discovery entries, configuration precedence, audit references, backups/restores, diagnostics, and administrative views. Cross-tenant access is denied by default. Any approved aggregate/platform administration path has named purpose, minimum scope, strong identity, current policy, time bound, redaction/minimization, audit, and review.

Configuration and membership propagation must not allow stale cache/event/retry to re-enable revoked membership, expired entitlement, restricted tenant, retired route, or forbidden configuration. Recovery revalidates current state rather than replaying prior authority.

# Privileged and Support Operations

Create/transfer/restrict/offboard tenant, change membership/entitlement/configuration, administer route/discovery, inspect scoped evidence, or perform recovery through dedicated protected operations. They require least privilege, current strong assurance as policy requires, reason/approval, concurrency control, time/scope limit, enhanced evidence, and rollback/restriction plan. Break-glass follows Security requirements and cannot be a hidden universal administrator account.

# Security Events, Incidents, and Recovery

Foundation emits trusted operation, denial, scope mismatch, privileged change, cache/propagation failure, export, restriction, and recovery evidence. On suspected wrong-scope access, credential compromise, configuration abuse, or route/discovery tampering, restrict affected capability, preserve evidence, coordinate Security containment, invalidate relevant cache/authority, reconcile dependencies, and recover only after current identity, policy, lifecycle, configuration, residency, and observability checks.

# Required Tests and Artifacts

Maintain Foundation security-control map, enforcement-point inventory, admin/break-glass register, scope-propagation diagram, access/audit event catalog, and incident/recovery runbooks. Test cross-tenant/environment negative cases across data/cache/queue/event/admin/recovery, membership/entitlement revoke, privileged approvals, stale cache, forged headers/claims, route/discovery tamper, support export, outage, and audit evidence.

# Anti-Patterns

## Tenant ID Is Authorization

Tenant ID is a scoped fact; Security makes the current permission decision.

## Admin User Bypasses Normal Controls

Administration has stronger, not fewer, identity, policy, scope, audit, and review requirements.

## Cache Restores Revoked Access

Foundation cache is scoped, bounded, invalidated, monitored, and cannot override current restrictive state.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created Foundation security and tenant-isolation controls. |
| 1.1 | 2026-08-07 | Originally approved; reopened after completeness review. |
| 1.2 | 2026-08-07 | Rewritten with control map, enforcement, isolation, privilege, recovery, evidence, and testing detail. |

# 03_AUTHORIZATION_POLICY_AND_ENFORCEMENT

**Version:** 1.2  
**Status:** Approved  
**Owner:** Security Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how the platform makes, enforces, records, revokes, and safely recovers authorization decisions. Security owns authorization policy and decision architecture. Resource-owning platforms define their resources, actions, lifecycle, and domain facts; Platform Foundation supplies tenant/membership/configuration facts.

Authentication alone, membership, a role, a token, provider identity, network location, or gateway admission is never an unconditional permission grant.

# Principles

## Current, Scoped Decisions

Every decision is evaluated for a verified subject, explicit resource/action, trusted tenant/environment, purpose, relevant lifecycle state, and current policy/configuration version. Decisions have bounded validity and required obligations.

## Policy and Enforcement Are Separate

Security defines policy and the policy-decision contract. API edges, services, workers, data access layers, provider adapters, and administrative paths enforce the applicable result at their own boundary. Enforcement points do not invent local policy or reuse a decision outside its scope.

## Deny by Default and Fail Safely

Unknown resource/action, incomplete context, expired authority, policy/identity uncertainty, or revocation uncertainty produces deny, defer, restrict, or approved challenge. A narrow break-glass route is exceptional, time-bounded, monitored, and auditable.

# Authorization Model

| Element | Security responsibility | Resource-owner responsibility |
|---|---|---|
| Subject | Validate verified principal/assurance/delegation context. | Supply no untrusted substitution. |
| Resource | Define generic resource-reference requirements. | Define stable resource identity, owner, classification, lifecycle, and tenant scope. |
| Action | Define policy action vocabulary/rules. | Define action semantics and safe domain outcome. |
| Context | Define required trusted inputs and policy version. | Supply current domain facts, purpose, risk, and effect class. |
| Outcome | Issue allow/deny/restrict/challenge/defer with validity/obligations. | Enforce and record result before operation. |

# Decision Contract

Every request identifies the verified `principal_ref`, principal type and assurance, requested action, stable resource reference/type, trusted tenant/environment, purpose, relevant membership/entitlement references, lifecycle/classification, delegation or approval reference, risk signals, correlation, and policy version candidate.

The result is one of:

| Outcome | Enforcement behavior |
|---|---|
| Allow | Perform only the stated action/resource/scope while applying returned obligations. |
| Deny | Do not perform the operation; return bounded error and evidence. |
| Restrict | Permit only the explicitly constrained safe subset, such as read-only or redacted operation. |
| Challenge | Require current step-up, confirmation, approval, or other specified control before retry. |
| Defer | Queue or pause without creating an external effect until a current decision is available. |
| Break-glass allow | Execute minimum approved scope with justification, expiry, enhanced monitoring, and post-use review. |

An allow carries resource/action/scope, validity, policy/version, required audit/classification/consent/approval obligations, and revocation/recheck requirements. It cannot be transformed into authority for another action, tenant, environment, provider, representation, or later workflow step.

# Enforcement Points

| Boundary | Required enforcement |
|---|---|
| API edge | Verify identity, route/audience, request scope, admission, and endpoint-level action. |
| Domain service | Recheck resource/action and current domain lifecycle before mutation or disclosure. |
| Data access | Enforce tenant, purpose, classification, lifecycle, export, and administrative access policy. |
| Worker/queue | Carry approved correlation and reauthorize when work is delayed, retried, or changes effect scope. |
| Provider/connector | Enforce delegated credential, tenant, action, approval, and callback trust before external effect. |
| Administration/support | Require elevated assurance, least privilege, reason, time bound, evidence, and review. |

# Delegation, Approval, and Revocation

Delegation is a distinct policy-governed grant with grantor, grantee, resource/action, purpose, constraints, provider, effective interval, approval evidence, and revocation path. It does not transfer unrestricted ownership. High-risk actions may require current explicit approval in addition to ordinary authorization.

Membership/status, resource lifecycle, consent, entitlement, policy, risk, credential, provider, or incident changes trigger re-evaluation or revocation according to defined propagation objectives. An enforcement point cannot rely on stale cached allow beyond its validity or a material change.

# Policy Lifecycle

Policy definitions are owned, versioned, reviewed, tested, staged, observed, reversible, and retained with rationale. A material change includes altered principal/action/resource scope, data/export rule, delegation, effect approval, emergency route, or default. Policy simulation and dry-run results are evidence, not production authorization.

# Break-Glass

Break-glass is permitted only for a documented emergency class. It requires named accountable authority, minimum tenant/resource/action scope, explicit justification, short expiry, current strong identity, enhanced audit/alerting, review, cleanup, and a post-incident decision. It cannot bypass immutable legal/hold constraints or create an unbounded administrative path.

# Evidence and Assurance

Record policy/version changes, decision category, enforcement result, delegated/approval reference, denial/challenge, privileged/break-glass use, revocation, cache invalidation, and reconciliation outcome. Evidence is tenant/environment-scoped, minimized, purpose-bound, access-controlled, and contains no credential or raw protected content unnecessarily.

Required tests cover positive and negative resource/action decisions, cross-tenant/environment misuse, lifecycle and consent changes, role/membership change, delayed job/retry, stale cache, delegated authority, approval expiry, policy rollback, outage, revocation propagation, and break-glass limits.

# Anti-Patterns

## Role or Membership Is a Permission

Roles and memberships are inputs; current policy decides the requested action on a current resource.

## Gateway Authorization Covers Every Call

Each service and effect boundary applies the correct current enforcement.

## Cached Allow Survives Revocation

Decision caches are scoped, short-lived, invalidated, observable, and cannot widen authority.

## Policy Is Buried in Application Code

Material authorization rules remain versioned, reviewable, testable, and traceable to Security ownership.

# Related Documents

| Document | Relationship |
|---|---|
| 02_IDENTITY_AND_AUTHENTICATION_ARCHITECTURE.md | Supplies verified identity context. |
| 04_SESSION_TOKEN_AND_DELEGATED_ACCESS.md | Defines token/session/delegation mechanics. |
| 16_PLATFORM_FOUNDATION/02_TENANT_ORGANIZATION_AND_MEMBERSHIP_MODEL.md | Supplies tenant and membership facts. |
| 07_INTEGRATION_PLATFORM/05_ACTION_AUTHORIZATION_AND_APPROVAL.md | Applies approval to external effects. |

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created authorization policy and enforcement model. |
| 1.1 | 2026-08-07 | Originally approved; reopened after completeness review. |
| 1.2 | 2026-08-07 | Rewritten with decision contract, enforcement, lifecycle, revocation, break-glass, evidence, and assurance detail. |

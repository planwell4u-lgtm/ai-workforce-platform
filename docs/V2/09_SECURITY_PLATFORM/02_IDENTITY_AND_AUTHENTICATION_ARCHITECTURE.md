# 02_IDENTITY_AND_AUTHENTICATION_ARCHITECTURE

**Version:** 1.2  
**Status:** Approved  
**Owner:** Security Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how the platform establishes, verifies, normalizes, maintains, restricts, and revokes identity for humans, organizations' users, administrators, workloads, providers, and public clients.

Authentication produces a trustworthy, bounded identity context. It does not decide whether that identity may read a resource, administer a tenant, invoke a tool, or cause an external effect; Document 03 defines authorization.

# Scope and Boundaries

Security Platform owns identity trust requirements, authentication methods, federation trust, identity lifecycle, assurance/risk signals, and the normalized identity-context contract. Platform Foundation owns organization, tenant, and membership facts. Domain platforms own their resources and business behavior. Data Platform owns physical storage and retention mechanisms.

This document does not define session/token format, renewal, exchange, or delegated access mechanics; those belong to Document 04. It supplies the identity assertions and validation rules that those mechanisms must carry.

# Principles

## Verified Identity, Not Untrusted Claims

Email addresses, tenant identifiers, roles, headers, device identifiers, browser storage, provider metadata, and client-supplied tokens are untrusted until validated under approved issuer, transport, signature, audience, expiry, replay, and environment rules.

## Separate Identity From Access

Authentication answers who or what has presented a credential and at what assurance level. Membership, entitlement, policy, resource state, purpose, lifecycle, and current risk are evaluated by Platform Foundation, Security authorization, and resource owners after authentication.

## Minimum Stable Identity Context

The platform normalizes only the minimum durable identifiers and assurance attributes required by the receiving contract. It avoids copying unnecessary personal attributes into tokens, logs, caches, domain records, or provider calls.

## Lifecycle Is Explicit and Reversible Only With Evidence

Enrollment, verification, linking, activation, suspension, recovery, deprovisioning, and reactivation are explicit state changes with accountable source, trusted scope, effective time, evidence, and revocation propagation. No identity is silently merged or reactivated.

# Identity Model

| Entity | Required attributes | Boundary |
|---|---|---|
| Platform principal | Stable internal subject reference, principal type, status, provenance, effective interval. | Does not itself grant tenant membership or permissions. |
| External identity | Issuer, immutable provider subject, verified attributes, assurance, link status, source evidence. | Mutable names/emails are not stable authorization keys. |
| Organization/user association | Foundation-owned organization and membership references. | Security validates identity; Foundation supplies association facts. |
| Workload identity | Workload reference, runtime/binding evidence, environment, audience, trust status. | Detailed workload trust is Document 05. |
| Provider identity | Provider/client reference, approved trust configuration, callback/federation evidence. | Does not imply access to platform resources. |
| Authentication context | Method, assurance, authentication time, risk/challenge result, issuer, correlation. | Bounded and purpose-specific; avoid personal-content duplication. |

The internal principal is created only after approved verification/linking. A principal can have multiple external identities only through an explicit, authorized account-link operation; the platform never merges principals merely because an email or display name matches.

# Lifecycle

| State | Meaning | Permitted transition |
|---|---|---|
| Pending verification | Identity evidence received but not trusted for protected access. | Verify or expire/reject. |
| Active | Identity is verified and eligible to request authorization. | Challenge, suspend, deprovision, or link under policy. |
| Challenged | Additional authentication/risk verification is required. | Restore active only after approved challenge. |
| Suspended | Identity may not obtain normal authority while risk/administrative review is active. | Deprovision or explicit reactivation. |
| Deprovisioned | Identity linkage is disabled and dependent authority is revoked. | Re-enroll/relink as a new controlled operation. |
| Expired/rejected | Verification/linking attempt is invalid or ended. | Start a new verified process. |

Lifecycle operations record requester/source, reason category, trusted organization/environment scope where applicable, approval, effective time, correlation, and downstream revocation/reconciliation result. Deprovisioning triggers token/session/delegation/credential invalidation under Documents 04–06 and does not itself delete domain or Data Platform records.

# Human and Administrator Authentication

Human authentication uses an approved identity provider and approved protocol/profile. The authentication journey validates the initiating client, redirect/origin, issuer, state/nonce, proof-of-possession or code-exchange requirements where applicable, and anti-replay controls.

Required posture varies by action risk. Standard access uses the approved baseline assurance. Administrative, privileged, security-sensitive, export, credential, billing-equivalent, or recovery actions require current stronger assurance and may require step-up authentication. The relying platform requests a required assurance outcome; it does not implement its own inconsistent password/MFA logic.

Account recovery, account linking, email/phone change, MFA reset, and administrator recovery are high-risk workflows. They require approved proof, delay/challenge or out-of-band controls where warranted, least-privilege temporary status, enhanced evidence, notification, and post-recovery review. They never silently preserve an old session or delegated authority.

# Public Client, Browser, Mobile, and API Requirements

Public clients are treated as untrusted execution environments. They use approved authorization flows, registered redirect URIs/origins, PKCE or equivalent protections where applicable, HTTPS, secure cookie/storage posture, anti-CSRF/state protections, strict content/origin controls, and bounded error handling.

The client receives only the minimum identity/session material appropriate to its contract. It cannot receive long-lived provider secrets, workload credentials, unrestricted tenant context, internal identities, policy internals, or administrative recovery authority. API clients authenticate through an approved client/workload mechanism and are separately authorized for every protected resource/action.

# Federation, Provider, and Callback Trust

Each identity provider or federation connection has a named owner, approved issuer/metadata endpoint, allowed protocol/flow, client registration, audience, redirect/callback allow-list, attribute mapping, assurance expectation, key/JWKS refresh rules, failure posture, region/data implications, monitoring, and exit/revocation plan.

Inbound callbacks and assertions verify source, transport, issuer, signature, audience, time bounds, nonce/state, event/reference identity, and replay protection before changing identity lifecycle. Provider success is evidence to validate, not an automatic platform principal or authorization grant.

# Normalized Identity Context Contract

After successful authentication, Security supplies a bounded context to approved enforcement points:

| Field | Meaning |
|---|---|
| `principal_ref` | Stable internal principal/workload reference. |
| `principal_type` | Human, administrator, workload, provider, or client category. |
| `issuer_ref` and `identity_ref` | Approved provenance reference; not raw credentials. |
| `authentication_assurance` and `authenticated_at` | Assurance/method outcome and time for policy/step-up evaluation. |
| `environment_ref` | Trusted environment boundary. |
| `correlation_ref` | Request/audit tracing reference. |
| `identity_status` | Active/challenged/suspended state at validation time. |

Tenant, membership, role, entitlement, resource/action permission, and business profile are intentionally excluded as unconditional identity claims. Consumers obtain those through their current governed contracts and Document 03 policy decisions.

# Failure, Risk, and Revocation

| Condition | Safe outcome |
|---|---|
| Invalid/expired issuer, signature, audience, nonce, or replay | Deny and record bounded failure evidence. |
| IdP or validation dependency unavailable | Defer/deny or use only a separately approved bounded validation cache that cannot outlive revocation requirements. |
| Elevated risk or sensitive action | Require step-up/challenge; do not silently downgrade assurance. |
| Suspension, deprovisioning, credential compromise, or provider disconnect | Restrict identity, revoke dependent authority, reconcile propagation, and require current reauthentication before recovery. |
| Ambiguous account link or duplicate identity | Stop automatic merge; route to controlled verification and accountable resolution. |

Revocation has an owner, target scope, propagation objective, confirmation evidence, reconciliation deadline, and terminal outcome. Caches, sessions, tokens, delegated credentials, provider connections, and workload access cannot extend authority after current revocation policy requires restriction.

# Evidence, Privacy, and Audit

Security records enrollment, verification, authentication result category, challenge/step-up, link/unlink, lifecycle transition, provider/trust configuration change, recovery, suspension, deprovisioning, revocation, and validation/dependency failure. Evidence contains trusted references, time, method/assurance category, outcome, reason category, correlation, and owner—not credentials, raw tokens, secrets, or unnecessary personal attributes.

Identity data follows classification, minimum-use, retention/deletion/hold, residency, access, export, and audit rules. Investigation or support access is least-privilege, purpose-bound, and auditable.

# Required Tests and Artifacts

| Artifact or test | Required proof |
|---|---|
| Identity/federation inventory | Every issuer/provider/client, owner, mapping, assurance, scopes, and exit plan is known. |
| Lifecycle state and transition tests | Invalid transitions, linking, suspension, deprovisioning, recovery, and reactivation are safe and auditable. |
| Protocol/callback tests | Invalid issuer/signature/audience, expiry, nonce/state, replay, redirect/origin, and substitution are rejected. |
| Client security tests | Browser/mobile/API client cannot retain/expose prohibited credential or identity material. |
| Revocation/outage tests | Revocation propagates; cache/dependency failure fails safely; recovery requires current proof. |
| Tenant and privacy tests | Identities cannot merge, resolve, log, export, or recover across tenant/environment boundaries. |

# Anti-Patterns

## Email Address Is the Principal

Email may be a verified attribute, but the issuer-bound subject and internal principal reference are the stable identity basis.

## Successful Login Is Permission

Authentication success only creates identity context; every protected operation continues through current authorization.

## Client Stores a Provider Secret

Public clients never hold long-lived provider/workload secrets or unrestricted administrative authority.

## Revocation Is Best Effort

Revocation is an observable controlled operation with bounded propagation, reconciliation, and a restrictive interim posture.

# Related Documents

| Document | Relationship |
|---|---|
| 03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md | Defines the decision and enforcement after identity is verified. |
| 04_SESSION_TOKEN_AND_DELEGATED_ACCESS.md | Defines session, token, exchange, delegation, expiry, and revocation mechanics. |
| 05_WORKLOAD_IDENTITY_AND_SERVICE_TRUST.md | Defines detailed workload/service trust controls. |
| 16_PLATFORM_FOUNDATION/02_TENANT_ORGANIZATION_AND_MEMBERSHIP_MODEL.md | Defines tenant and membership facts used by authorization. |

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created identity and authentication architecture. |
| 1.1 | 2026-08-07 | Originally approved; reopened after completeness review. |
| 1.2 | 2026-08-07 | Rewritten with lifecycle, flows, federation, client, context-contract, revocation, evidence, and assurance detail. |

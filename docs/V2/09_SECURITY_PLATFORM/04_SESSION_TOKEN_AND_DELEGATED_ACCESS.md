# 04_SESSION_TOKEN_AND_DELEGATED_ACCESS

**Version:** 1.2  
**Status:** Approved  
**Owner:** Security Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines secure session, token, token-exchange, delegated-access, expiry, renewal, revocation, and recovery controls. It carries verified identity and bounded authority between approved components; it does not replace current authorization at a protected resource.

# Token and Session Classes

| Class | Allowed use | Required limits |
|---|---|---|
| Human session | Browser/mobile interaction after approved authentication. | Secure transport/storage, short lifetime, renewal controls, logout/revocation. |
| Access token | Audience-specific API/service request. | Short-lived, minimum claims, validated at every enforcement point. |
| Refresh/renewal credential | Obtain a new access token only through approved session controls. | Strong protection, rotation/reuse detection, revocable. |
| Workload token | Service/job identity to approved audience. | Document 05 workload trust, short lifetime, no human impersonation by default. |
| Delegated provider credential | User/tenant-approved external provider operation. | Provider, tenant, action/purpose, expiry, consent, and revocation bound. |
| One-time action/approval token | Narrow high-risk confirmation or workflow continuation. | Single purpose/use, short expiry, replay protection, audit. |

# Required Claims and Validation

Tokens contain only stable subject/workload reference, issuer, audience, token identifier, issued/expiry time, environment, authentication assurance where needed, correlation, and bounded delegation/approval reference. Tenant, role, entitlement, resource, and permission claims are not trusted as unlimited current authority.

Every recipient validates issuer, signature/proof, audience, expiry/not-before, token type, environment, revocation/reuse state, binding where required, and scope. It then makes or obtains the current authorization decision for its resource/action. Tokens are never accepted through unapproved query strings, logs, URLs, telemetry, or cross-origin forwarding.

# Session Lifecycle

| Event | Required outcome |
|---|---|
| Issue | Verified identity, approved client/device/origin, assurance, scope, expiry, and evidence. |
| Use | Current validation, audience check, authorization, activity/risk controls, bounded diagnostics. |
| Renew | Reauthenticate or use protected rotating renewal credential; detect reuse/compromise. |
| Step-up | Replace/augment session only after required stronger authentication; do not silently elevate. |
| Logout/revoke | Invalidate relevant session/token/delegation, propagate, reconcile, and record result. |
| Expire | Deny/renew through approved path; never silently extend. |
| Recover | Require current identity proof and revoke old compromised authority before reissue. |

# Delegated Access

Delegation represents a specific grant from an authorized grantor to a named grantee/provider for a defined tenant, resource/action category, purpose, constraints, effective interval, and revocation path. It records the identity/authorization/consent/approval evidence on which it depends.

Delegated provider credentials are stored and used through approved secret controls. The platform never converts a provider refresh token into a generic platform administrator credential. Connector execution rechecks delegation, tenant, action, purpose, approval, provider trust, and current authorization at effect time—especially after queue delay or retry.

# Browser, Mobile, and API Handling

Public clients use approved flows, registered redirect URIs/origins, PKCE or equivalent where relevant, HTTPS, secure cookie/storage rules, CSRF/state protections, and strict content/origin behavior. Tokens must not be exposed to third-party scripts, error messages, analytics, support artifacts, or untrusted native/webview bridges.

API clients and service callers use audience-specific credentials and cannot exchange a user token for broader service authority. Token forwarding across services preserves only approved context and never becomes a substitute for workload identity plus local policy enforcement.

# Revocation, Cache, and Failure Rules

Revocation applies to compromised/suspended/deprovisioned identity, logout, membership/policy/lifecycle change, expired approval/consent, provider disconnect, credential/key rotation, or incident containment. It specifies target, scope, owner, propagation objective, cache invalidation, evidence, reconciliation deadline, and terminal disposition.

| Condition | Safe posture |
|---|---|
| Token validation or issuer uncertain | Deny/defer or use only bounded approved verification cache. |
| Renewal reuse or suspected theft | Revoke credential family, restrict session, investigate, require reauthentication. |
| Delegation expired/disconnected | Stop external effect; record safe terminal outcome. |
| Revocation propagation delayed | Restrict where possible, monitor/reconcile, never claim completed revocation prematurely. |
| Token/key rotation | Accept only approved overlap window; validate migration and retire old material. |

# Evidence and Tests

Record issuance, validation failure category, renewal/rotation, step-up, logout, revoke, delegation grant/change/disconnect, approval use/expiry, reuse detection, and propagation/reconciliation without raw tokens or secrets. Tests prove issuer/audience/type/expiry mismatch, replay, token substitution, redirect/origin abuse, CSRF, storage leakage, renewal theft, cross-tenant use, delayed worker, provider disconnect, revocation, rotation, and outage behavior.

# Anti-Patterns

## Token Possession Is Permanent Authority

Authority is bounded by audience, scope, time, policy, lifecycle, risk, and revocation.

## Refresh Token Is a Service Credential

Renewal credentials are user/session-bound and protected; services use their own workload identity.

## Delegated Credential Authorizes Any Tool

Each external effect is constrained to the original tenant, purpose, provider, action, and current authorization.

# Related Documents

| Document | Relationship |
|---|---|
| 02_IDENTITY_AND_AUTHENTICATION_ARCHITECTURE.md | Defines verified identity and assurance input. |
| 03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md | Defines current resource/action decision. |
| 05_WORKLOAD_IDENTITY_AND_SERVICE_TRUST.md | Defines service/workload trust. |
| 07_INTEGRATION_PLATFORM/04_CONNECTOR_AUTHENTICATION_AND_CREDENTIAL_DELEGATION.md | Applies delegation to connector mechanisms. |

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created session, token, and delegation model. |
| 1.1 | 2026-08-07 | Originally approved; reopened after completeness review. |
| 1.2 | 2026-08-07 | Rewritten with token classes, lifecycle, delegation, client handling, revocation, failure, evidence, and testing detail. |

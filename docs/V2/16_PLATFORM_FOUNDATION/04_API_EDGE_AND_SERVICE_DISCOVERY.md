
**Version:** 1.2  
**Status:** Approved  
**Owner:** Platform Foundation Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines shared API entry, route governance, admission, forwarding, compatibility, and service-discovery contracts. The API edge routes approved traffic to owned platform contracts; it is not a generic internal proxy, a direct database/provider path, or the only authorization control.

# Route Model

| Route record | Required facts |
|---|---|
| Identity | Stable route reference, owner, audience, environment, API/contract version, lifecycle status. |
| Admission | Authentication/authorization requirements, tenant/scope resolution, rate/abuse class, request schema/size limits. |
| Destination | Approved service capability/contract, not arbitrary host or client-selected endpoint. |
| Data/effect | Classification, external-effect level, consent/approval/security obligations, observability needs. |
| Change | Compatibility/deprecation plan, rollout/rollback, consumer inventory, evidence. |

Routes are registered before exposure and retired through a controlled lifecycle. A route has one accountable owner. Unknown, retired, environment-mismatched, or incompatible routes are rejected without leaking internal topology or implementation diagnostics.

# Admission and Forwarding Flow

1. The edge verifies protected transport, request shape/size, client identity, and API/route version.
2. It resolves trusted environment and tenant context using approved Foundation/Security facts; client identifiers are validated inputs, not authority.
3. It applies Security-required authentication, authorization/enforcement, abuse/rate, and required challenge/approval controls.
4. It forwards only approved identity, scope, correlation, contract-version, and obligation context to the named destination.
5. The destination verifies service trust and enforces its own resource/action policy before use or external effect.
6. The edge returns a bounded outcome envelope and emits safe admission/routing evidence.

# Contract Versioning and Compatibility

Public/internal contracts are explicit, typed, and versioned. Additive compatible change is preferred; breaking change has consumer discovery, migration/dual-read or dual-route period where needed, deprecation notice, monitoring, rollback/restriction, and retirement criteria. A gateway transform must preserve documented semantics and must not invent domain state, authorization, or hidden default values.

# Service Discovery

Discovery publishes approved workload-facing capability metadata: stable capability/service reference, environment, contract version, endpoint reference, service identity/audience, health state, lifecycle/deprecation, and configuration version. It does not distribute plaintext secrets, grant access, enable arbitrary host selection, or bypass workload identity, network policy, or destination authorization.

Discovery consumers verify environment, capability, contract compatibility, service identity/audience, lifecycle, freshness, and policy before connection. Cached records are bounded and cannot revive retired/restricted service or use an obsolete endpoint after material trust/configuration change.

# Failure and Recovery

| Condition | Safe posture |
|---|---|
| Identity/policy/scope unavailable | Deny/defer/restrict protected route; no generic prior allow. |
| Invalid/unknown/deprecated route | Reject with bounded client-safe response and evidence. |
| Destination/discovery unavailable | Return retry-safe unavailable/defer outcome; do not fall through to arbitrary service. |
| Version incompatibility | Reject or serve only documented compatible version; never silently coerce unsafe input. |
| Route/service compromise | Restrict/retire, revoke trust/credentials, preserve evidence, coordinate Security and owner recovery. |

Recovery revalidates route lifecycle, identity/policy, scope, destination contract, service trust, configuration, observability, and pending revocation before re-exposure.

# Operational Evidence and Tests

Record route register/change/retire, admission/denial category, contract/version mismatch, rate/abuse action, destination selection, discovery update/failure/staleness, privileged route administration, and recovery/reconciliation. Test untrusted scope/header, client route manipulation, cross-tenant/environment request, invalid schema/version, missing policy, stale discovery, retired route, destination identity mismatch, rate pressure, outage, rollback, and audit/redaction.

# Anti-Patterns

## Gateway Authentication Covers Everything

Every receiving service retains current resource/action enforcement and trusted workload verification.

## Discovery Is Authority

Endpoint knowledge is not a credential or permission; consumers still use identity, policy, and contract controls.

## Gateway Directly Queries Data

The edge routes to owned contracts and never bypasses Data/domain boundaries.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created API-edge and service-discovery architecture. |
| 1.1 | 2026-08-07 | Originally approved; reopened after completeness review. |
| 1.2 | 2026-08-07 | Rewritten with route model, flow, compatibility, discovery, failure, evidence, and test detail. |

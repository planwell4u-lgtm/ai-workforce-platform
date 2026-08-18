# 05_WORKLOAD_IDENTITY_AND_SERVICE_TRUST

**Version:** 1.2  
**Status:** Approved  
**Owner:** Security Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how services, workers, scheduled jobs, deployment automation, provider adapters, and administrative workloads establish and enforce trust. An internal endpoint, network segment, service name, environment variable, or shared secret is never sufficient workload authority.

# Workload Trust Model

| Element | Required requirement |
|---|---|
| Workload identity | Unique stable reference bound to named owner, runtime, environment, and allowed audiences. |
| Credential/certificate | Short-lived where possible, non-exportable where available, rotatable, revocable, and never shared by default. |
| Runtime binding | Approved deployment/runtime attestation or equivalent trusted issuance condition. |
| Peer verification | Validate issuer, audience, certificate/proof, environment, expiry, and revocation before service action. |
| Authorization | Apply current policy to workload, resource, action, tenant/purpose, and execution context. |
| Evidence | Record issuance, use category, denial, rotation, revocation, and recovery without credential material. |

# Identity Classes

Separate identities are required for API services, asynchronous workers, migration/backup/recovery jobs, CI/CD, observability collectors, provider adapters, and emergency administration. Human user identity must not be silently forwarded as service authority; a service acting on behalf of a human carries an explicit bounded delegation and still uses its own workload identity.

# Service-to-Service Flow

1. The caller obtains a current workload credential from an approved issuer/binding.
2. It connects only to an approved discovered audience over protected transport.
3. The receiver verifies caller identity, audience, environment, time bounds, and trust status.
4. The receiver evaluates current authorization for its resource/action and trusted tenant/purpose context.
5. Both sides record bounded correlation and outcome evidence; neither exposes credentials in diagnostics.

# Least Privilege and Segmentation

Policies restrict each workload to necessary service audiences, actions, tenant/purpose patterns, data classes, provider credentials, network paths, and administrative capabilities. Jobs and queues preserve workload identity and reauthorize delayed/retried work. A shared runtime pool or network boundary does not permit cross-service or cross-tenant access.

# Lifecycle and Failure

| Event | Required action |
|---|---|
| Provision | Register owner, purpose, runtime binding, scopes, dependency, expiry/rotation, and evidence. |
| Deploy/change | Revalidate identity binding, policy, audience, configuration, and secrets; retain change evidence. |
| Rotate | Issue/validate new credential, use bounded overlap, revoke old material, reconcile dependents. |
| Retire/compromise | Disable identity, revoke credentials/tokens/delegation, contain access, investigate, and remove discovery/configuration references. |
| Verification outage | Deny/defer or use only bounded approved cache; never accept unknown peer. |

# Provider and Administrative Workloads

Provider adapters use separate identities and credentials per provider/environment/tenant scope where required. They cannot use general application identity to obtain unrestricted provider access. Administrative workloads require elevated assurance, explicit change/approval scope, short lifetime, enhanced audit, and post-operation review.

# Tests and Artifacts

Maintain workload inventory, trust-policy map, audience matrix, credential/rotation register, and revocation runbooks. Test impersonation, audience/environment mismatch, expired/revoked credential, lateral movement, shared-credential misuse, queue retry, provider adapter scope, rotation, outage, and retirement.

# Anti-Patterns

## One Shared Service Secret

Distinct workload identities make attribution, least privilege, rotation, and containment possible.

## Internal Network Means Trusted

Every internal caller is verified and authorized at its protected boundary.

## Job Retry Preserves Yesterday's Authority

Delayed work rechecks current identity, policy, tenant, lifecycle, and approval requirements.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created workload identity and service-trust architecture. |
| 1.1 | 2026-08-07 | Originally approved; reopened after completeness review. |
| 1.2 | 2026-08-07 | Rewritten with trust model, flow, least privilege, lifecycle, failure, provider, and assurance detail. |

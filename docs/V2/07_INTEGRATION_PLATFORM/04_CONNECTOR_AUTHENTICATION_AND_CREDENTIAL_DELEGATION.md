# 04_CONNECTOR_AUTHENTICATION_AND_CREDENTIAL_DELEGATION

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how Integration Platform obtains, applies, rotates, revokes, and audits connector-specific external credentials and delegated grants.

Integration delegates external-system access only for a bounded, current connector operation. It does not own enterprise authentication, authorization policy, secret storage, key management, or identity proofing.

---

# Purpose

The model prevents a provider API key, OAuth token, service account, signed URL, webhook secret, or external session from becoming a broad platform credential. It ensures every external credential use has a current tenant, subject, purpose, connector, capability, target, policy, lifecycle, expiry, and audit scope.

---

# Objectives

Credential delegation must:

- Keep secret material in Security-owned storage and expose only the least privileged usable reference to an adapter.
- Separate platform principal identity, external account identity, delegated grant, credential material, and action authorization.
- Bind every grant and credential use to trusted tenant/environment, connector/capability, purpose, subject, provider account/resource, and expiry.
- Support user-delegated, tenant-managed, platform-managed, and workload-to-workload connector account models without conflating them.
- Enforce rotation, revocation, consent/approval where required, provider callback validation, incident containment, and audit.
- Prevent credentials, provider tokens, authorization codes, raw OAuth responses, and secret URLs from entering public contracts, logs, traces, events, or client code.

---

# Scope

This document defines connector credential and grant records, delegation flows, validation, lifecycle, account models, external consent boundary, revocation, and evidence requirements.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Enterprise authentication, identity proofing, authorization policy engine, secret vault, cryptographic standards, key management, or compliance policy | 09_SECURITY_PLATFORM |
| Tool/capability publication and registry lifecycle | 03_TOOL_AND_CONNECTOR_REGISTRY.md |
| Per-action authorization, confirmation, approval, or business intent | 05_ACTION_AUTHORIZATION_AND_APPROVAL.md and 02_AGENT_PLATFORM |
| Provider request dispatch, idempotency, callback processing, retry, or workflow execution | 06–09 and 13 Integration documents |
| Tenant, membership, entitlement, configuration, and API-edge source of truth | 16_PLATFORM_FOUNDATION |
| Canonical Conversation/participant/work state or notification | 03_CONVERSATION_PLATFORM |

---

# Principles

## Credential Is Not Authorization

Possession of a valid provider credential proves only that an external provider may accept a bounded request. It never proves the platform currently authorizes the action, the target is permitted, the purpose remains valid, or the participant approved the effect.

## Delegation Is Narrow and Time-Bounded

Delegated grants are limited by tenant/environment, principal or workload, connector/capability, provider account/resource, scopes, purpose, expiry, policy, and operation class. A new sensitive operation re-evaluates current scope; no grant is a blanket future-action approval.

## Secret Material Stays Outside Domain Records

Integration records a protected credential reference and validation outcome. Security-owned mechanisms create, store, issue, rotate, revoke, and audit the actual secret material. Client, Agent, Conversation, and channel code never receive broad connector secrets.

## External Consent Does Not Replace Platform Governance

An OAuth consent screen or provider account connection may establish an external grant. It does not establish platform tenant membership, authorization, purpose, entitlement, data-egress permission, or approval for an individual action.

---

# Credential and Grant Model

| Entity | Meaning | Must not become |
|---|---|---|
| `ConnectorAccountBinding` | Approved association between a tenant/profile and an external provider account or account class. | Tenant identity or general platform account. |
| `DelegatedGrant` | Current, bounded permission to use an external account through one connector/capability scope. | A reusable action approval or client token. |
| `CredentialReference` | Security-owned protected reference to secret material/certificate/token. | Secret value, public identifier, or direct provider credential. |
| `CredentialLease` | Short-lived adapter use authorization for one operation class or action. | A broad workload credential or cached grant. |
| `ExternalIdentityBinding` | Protected link between a platform-approved subject/workload and external identity evidence. | Platform authentication or participant identity truth. |
| `CredentialValidationEvidence` | Provider/source, scope, expiry, rotation, revocation, and validation outcome. | Authorization decision or raw token payload. |

Every entity has tenant/environment, connector/profile, provider/account/resource, lifecycle, policy/version, actor/service, correlation, and audit references. Sensitive identifiers are protected adapter references.

---

# Supported Account Models

| Model | Use | Required boundary |
|---|---|---|
| User-delegated | A person authorizes a connector to act within their external account scope. | Bind the external grant to the approved subject/purpose and require per-action policy/approval. |
| Tenant-managed | An authorized tenant administrator connects an organization-owned external account. | Separate administrator enablement from later subject/action scope; prevent tenant-wide implicit access. |
| Platform-managed | The platform uses its own provider account for a defined service capability. | Enforce tenant/resource partitioning, least privilege, usage attribution, and no broad customer-data access. |
| Workload-to-workload | A service authenticates to an external service with a scoped workload identity. | Bind workload, environment, connector role, operation, rotation, and audit; internal network location is insufficient. |

No model permits cross-tenant credential reuse or a provider account to select the platform tenant.

---

# Delegation Lifecycle

~~~text
Proposed -> Authorizing -> Active -> Expiring -> Rotated
                         |        |             |
                         v        v             v
                     Denied    Revoked      Suspended/Retired
~~~

| State | Meaning |
|---|---|
| `Proposed` | No external authority exists; connector setup is being prepared. |
| `Authorizing` | Controlled external consent, account setup, or workload-grant flow is active. |
| `Active` | Current grant may be leased for eligible actions. |
| `Expiring` | Renewal or rotation is required; new use follows policy. |
| `Rotated` | A replacement reference is active; old material is revoked/retired. |
| `Suspended` | New use is blocked by policy, incident, account, health, or lifecycle condition. |
| `Revoked` | Grant or credential may no longer be used. |
| `Retired` | Binding is removed from selection; governed evidence remains. |
| `Denied` | Delegation did not satisfy required current controls. |

---

# Delegation and Use Flow

1. Resolve trusted tenant/environment, connector/capability/profile, account model, principal/workload, purpose, and eligibility.
2. Obtain required external consent or service grant through a Security-approved flow; never accept a raw token as sufficient evidence.
3. Validate provider/source integrity, requested scope, account/resource binding, expiry, policy, residency/egress, and audit requirements.
4. Store secret material in Security-owned mechanisms and create protected binding/grant references.
5. Before an action, re-evaluate current action authorization, approval, target, purpose, tenant, connector profile, grant state/scope, and credential validity.
6. Issue only a short-lived, least-privilege credential lease to the adapter for the permitted operation.
7. Record protected use, outcome, rotation/revocation, anomaly, and incident evidence; never emit secret material.

---

# Scope and Lease Guard

Before a credential is leased or used, Integration validates:

- trusted tenant/environment and current principal/workload identity;
- active connector, capability, profile, and provider account/resource binding;
- approved account model and current delegated-grant state;
- requested scope, purpose, subject, target representation, classification, egress, residency, and operation class;
- current action authorization/approval, lifecycle, cancellation, rate/cost, and idempotency requirements;
- credential expiry, rotation, revocation, policy/version, source-validation, and incident restrictions; and
- minimum lease duration, provider scope, and audit correlation.

A failed or ambiguous check denies or restricts use without disclosing account existence, grant detail, token state, or target data.

---

# Rotation, Revocation, and Incidents

Credential rotation is proactive and auditable. A rotation creates a new protected reference, validates connector compatibility, transitions eligible operations without broadening scope, revokes old material, and records any uncertain in-flight effect for reconciliation.

On suspected compromise, provider-account change, tenant suspension, subject withdrawal, policy restriction, scope mismatch, secret exposure, or failed callback validation, Integration stops new use, revokes or restricts applicable leases/grants through Security controls, contains affected connector/profile scope, preserves minimum protected evidence, and follows the enterprise incident process. Recovery requires current reauthorization and validation; it never reuses a stale grant because a workflow retries.

---

# Platform Foundation and Channel Boundaries

Platform Foundation provides authoritative tenant, membership, entitlement, configuration, and environment facts. Integration applies them to bindings and leases but never derives them from an OAuth subject, provider account, callback, or token claim alone.

Voice and Digital Channel Platforms do not receive connector credentials. They may consume normalized authorized action evidence through approved contracts, but channel transport identity or delivery context cannot broaden a credential grant.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Connector account and grant contract | Defines bindings, account models, scopes, expiry, lifecycle, protected references, and audit. | Integration with Security and Platform Foundation owners |
| Credential-lease service boundary | Defines short-lived adapter access, least privilege, issuance, renewal, revocation, and evidence. | Security with Integration owner |
| External consent and delegation procedure | Defines user/admin/workload delegation, callback/source validation, denial, withdrawal, and recovery. | Integration with Security, Frontend, and Operations owners |
| Rotation and incident runbook | Defines rotation, compromise containment, provider change, in-flight reconciliation, recovery, and audit. | Security with Integration and Operations owners |
| Credential isolation test suite | Proves no secret leakage, cross-tenant reuse, stale grant use, scope widening, or unauthorized lease. | Integration with Security and Testing owners |

---

# Anti-Patterns

## OAuth Consent Is Action Approval

An external grant permits a bounded provider scope only. Every external effect still requires current platform authorization and approval.

## Store the Token in Connector Metadata

Registry and domain records hold protected references and evidence, never raw secret material or client-readable provider tokens.

## One Tenant Admin Grant Authorizes Everyone

Tenant-managed account connection must still be narrowed by subject, purpose, capability, target, and current action controls.

## Retry Reuses a Revoked Credential

Every retry, workflow continuation, and reconciliation step re-evaluates current grant and lease validity.

## Provider Account Identifies the Tenant

Tenant scope is resolved from trusted Platform Foundation context and validated against account binding, never inferred from provider evidence.

---

# Related Documents

| Document | Relationship |
|---|---|
| 03_TOOL_AND_CONNECTOR_REGISTRY.md | Defines connector/capability/profile lifecycle. |
| 05_ACTION_AUTHORIZATION_AND_APPROVAL.md | Defines per-action authorization and approval. |
| 06_ACTION_EXECUTION_AND_IDEMPOTENCY.md | Defines controlled use during dispatch and retry. |
| 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md | Defines callback validation for external delegation flows. |
| 10_INTEGRATION_ACCESS_AND_TENANT_ISOLATION.md | Defines tenant/subject/purpose isolation. |
| 12_INTEGRATION_SECURITY_AND_PRIVACY.md | Defines external trust and data-egress controls. |
| 09_SECURITY_PLATFORM/README.md | Owns enterprise identity, secrets, authorization, and compliance controls. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created credential delegation architecture covering account models, grants, leases, scope, rotation, revocation, and audit. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

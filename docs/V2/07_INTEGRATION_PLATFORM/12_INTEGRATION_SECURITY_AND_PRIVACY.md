# 12_INTEGRATION_SECURITY_AND_PRIVACY

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how Integration Platform applies enterprise security and privacy controls to connectors, external APIs, credentials, actions, workflows, callbacks, provider data, exports, and operations.

Integration enforces security decisions at the external-effect boundary. It does not replace enterprise identity, authorization, secrets, cryptography, compliance, data lifecycle, or incident ownership.

---

# Purpose

The model prevents untrusted external data, provider APIs, credentials, prompts, tool parameters, callbacks, or operator actions from granting authority, exposing protected data, creating cross-tenant effects, or bypassing governed action execution.

---

# Objectives

- Define Integration assets, trust zones, threats, and operation security invariants.
- Enforce current action, credential, tenant, subject, purpose, target, classification, egress, and lifecycle controls.
- Minimize/protect external data and secrets across requests, responses, events, logs, traces, exports, and support.
- Detect and contain source impersonation, replay, injection, scope escalation, data exfiltration, abuse, fraud, supply-chain, and availability risks.
- Produce normalized protected security evidence, alerts, audit, and incident/recovery outcomes.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Enterprise identity, authorization engine, key/secret management, cryptography, compliance, security monitoring, or incident command | 09_SECURITY_PLATFORM |
| Storage encryption, retention/deletion/hold, backups, residency infrastructure, or data-subject request execution | 08_DATA_PLATFORM with 09_SECURITY_PLATFORM |
| Registry, grants, approvals, dispatch, workflows, callbacks, or tenant models | Integration documents 03–11 |
| Agent reasoning/tool safety policy or canonical Conversation state | Agent and Conversation Platforms |

---

# Security Principles

## All External Evidence Is Untrusted

Provider payloads, webhook headers, OAuth responses, API responses, files, URLs, tool parameters, external IDs, rate-limit headers, and operator input are validated only for their exact current operation. They never become broad trust grants.

## Data Egress Is an Explicit Effect

Before any data leaves the platform, Integration validates current tenant, subject, purpose, connector/capability, target, representation, classification, consent/policy, destination, region/residency, credential scope, retention/provider handling, and audit requirements.

## Least Privilege at Every Boundary

Adapters use distinct Security-managed workload identities and minimum short-lived credential leases. An adapter cannot directly write canonical Conversation state, invoke arbitrary Agent tools, bypass action guards, or access broad tenant data.

## Fail Closed for Sensitive Work

Missing, stale, conflicting, uncertain, or invalid security evidence denies, restricts, quarantines, defers, or stops work; it never defaults to sending, exporting, provisioning, approving, or retrying an external effect.

---

# Assets and Threats

| Asset | Required protection |
|---|---|
| Connector/provider accounts, grants, leases, keys, tokens, callback secrets, certificates | Security-managed, scoped, rotated, revocable, absent from public contracts/logs. |
| Action/workflow/callback/external-resource references | Opaque, tenant-bound, non-guessable where externally visible, not bearer authority. |
| External request/response/content and imports/exports | Classified, minimized, purpose-bound, representation-controlled, redacted, audited. |
| Connector/profile/configuration and capability versions | Authorized change, versioned, reviewed, monitored, rollback-capable. |
| High-impact effects | Current guard, idempotency, approval, limits, protected evidence, safe uncertainty. |

Threats include forged/replayed callbacks, credential compromise, OAuth/consent confusion, SSRF/open redirect, prompt/tool injection, malicious content/file, target substitution, data egress/exfiltration, provider-account confusion, tenant leakage, rate/cost/fraud abuse, unsafe SDK/dependency change, and callback/API flood.

---

# Common Security Guard

Every material operation validates source/workload identity; trusted tenant/environment; connector/capability/profile/account/resource binding; current action authorization/approval/purpose/target; credential/grant/lease; classification/egress/residency; schema/version/freshness/replay/order; idempotency/rate/capacity; policy/incident restriction; and audit correlation.

The guard re-runs before credential use, dispatch, external data import/export, callback acceptance, workflow continuation, retry/fallback, compensation, configuration change, evidence access, and recovery.

---

# External Data, Injection, and Egress Controls

External content, tool output, provider metadata, documents, URLs, and errors are treated as data, not instructions. They cannot alter connector configuration, destination, policy, credential scope, approval, or Agent tool selection. Imports pass approved schema, classification, size/type, malware/content, provenance, minimization, and destination-owner controls.

Outbound requests use allowlisted connectors/targets, validated parameters, controlled redirect/URL behavior, minimal representation, protected headers, and destination-specific policy. Raw sensitive content, credentials, direct identifiers, signed URLs, and provider payloads are excluded from routine telemetry.

---

# Secrets, Supply Chain, and Incident Handling

Secrets are created/stored/rotated/revoked through Security-owned mechanisms. Configuration and adapter changes require provenance, version pinning or controlled resolution, software inventory/SBOM evidence, vulnerability monitoring, test/conformance, rollout, rollback, and audit.

On suspected compromise, forgery, egress violation, cross-tenant attempt, credential abuse, injection, or integrity failure, Integration stops affected actions/leases/connector scope, quarantines evidence, preserves minimum protected audit material, alerts responsible owners, and follows enterprise incident handling. Recovery requires current authorization, corrected controls, validation, reconciliation, and audit; it never resumes stale work automatically.

---

# Privacy and Audit

Security events include normalized source/operation/egress/restriction/incident categories, tenant-safe scope, correlation, and protected evidence reference. They do not contain raw content, credentials, full external IDs, direct participant identifiers, or detailed policy internals.

Access/export/replay/support operations are purpose-bound, representation-limited, time-bounded, and audited. Data retention/deletion/hold and provider lifecycle follow Data/Security policy; Integration records action/resource requirements and outcome evidence.

---

# Platform Foundation and Channel Boundaries

Platform Foundation supplies tenant, entitlement, configuration, and API-edge facts. Voice and Digital Channel Platforms own their transport security; an Integration action may correlate to a channel journey but cannot authorize delivery, media, or participant identity.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Integration threat model and control matrix | Defines assets, trust zones, threats, controls, risk, owners, and review. | Integration with Security owner |
| Egress/import and injection standard | Defines target, representation, classification, validation, content, and audit controls. | Integration with Security, Data, and domain owners |
| Adapter secret/supply-chain standard | Defines workload identity, leases, provenance, rotation, patch, rollout, rollback. | Security with Integration and Operations owners |
| Integration incident playbook | Defines containment, evidence, escalation, recovery, reconciliation, and audit. | Integration with Security and Operations owners |
| Security/privacy test suite | Proves source, egress, tenant, credential, injection, abuse, and incident safety. | Integration with Testing and Security owners |

---

# Anti-Patterns

## OAuth or Webhook Is Broad Trust

It is validated only for its current scoped operation and never replaces platform authorization or egress controls.

## Provider Error Can Reach an Agent or User Raw

Errors are normalized and redacted; raw provider evidence is protected and purpose-bound.

## Available Provider Overrides Data Policy

Cost, capability, or availability cannot override classification, residency, purpose, tenant, approval, or security requirements.

## Security Event Changes Conversation State

Integration publishes evidence; Conversation determines canonical consequences through its own current contracts.

---

# Related Documents

| Document | Relationship |
|---|---|
| 04_CONNECTOR_AUTHENTICATION_AND_CREDENTIAL_DELEGATION.md | Defines grants and credential leases. |
| 05_ACTION_AUTHORIZATION_AND_APPROVAL.md | Defines guarded action authority. |
| 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md | Defines untrusted callback intake. |
| 10_INTEGRATION_ACCESS_AND_TENANT_ISOLATION.md | Defines scope isolation. |
| 13_INTEGRATION_RELIABILITY_AND_FAILURE_HANDLING.md | Defines safe recovery and uncertainty. |
| 09_SECURITY_PLATFORM/README.md | Owns enterprise security controls. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Integration security and privacy architecture covering trust, egress, secrets, injection, supply chain, and incident handling. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

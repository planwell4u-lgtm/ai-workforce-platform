# 11_INTEGRATION_GOVERNANCE_AND_AUDIT

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines governance and audit requirements for connector onboarding, capability enablement, account/grant changes, approvals, actions, workflows, external outcomes, support, incidents, and retirement.

Integration owns the domain decisions and evidence required for external-effect governance. Security owns enterprise audit infrastructure, identity, authorization, compliance, and incident policy.

---

# Purpose

Governance ensures every material integration change or external effect has a named owner, bounded authority, review path, protected evidence, and reversible lifecycle. Audit makes that evidence accountable without turning logs into a raw provider-data store.

---

# Objectives

- Define decision rights, separation of duties, approvals, change classification, and review cadence.
- Require auditable evidence for connector/capability/profile/grant/action/workflow/event lifecycle.
- Protect audit records from secret, content, and cross-tenant exposure.
- Support exception, incident, restriction, retirement, and evidence-retention handling.
- Keep governance practical through risk-based controls and explicit automated versus human decisions.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Enterprise audit platform, identity, RBAC/ABAC, compliance policy, legal hold, or incident command | 09_SECURITY_PLATFORM |
| Tenant, entitlement, configuration, and API-edge lifecycle | 16_PLATFORM_FOUNDATION |
| Capability registry, credential, authorization, execution, workflow, or callback mechanics | Integration documents 03–10 |
| Physical audit storage, retention/deletion, backup, or analytics infrastructure | 08_DATA_PLATFORM |
| Business intent, canonical Conversation state, or participant communication | Agent and Conversation Platforms |

---

# Governance Principles

## Decision Rights Follow Ownership

Integration owns connector/action technical governance; Security owns enterprise control policy; Platform Foundation owns tenant/entitlement/configuration facts; Conversation and Agent own canonical work and intent. No provider, adapter, or operator screen changes these boundaries.

## High-Impact Change Requires Separation

The requester, approver, connector administrator, credential custodian, and executor are distinct when policy/risk requires it. One role cannot silently approve its own high-risk privilege, connector scope, or external effect.

## Evidence Is Immutable and Minimal

Governance records append decisions, scope, rationale, policy/version, actor/service, time, correlation, outcome, and protected evidence reference. Corrections and reversals create new records; they do not rewrite history or store raw secrets/payloads.

---

# Governed Decision Types

| Decision | Minimum authority/evidence |
|---|---|
| Connector/capability onboarding | Integration owner, Security/Data/Testing review, conformance, lifecycle and exit plan. |
| Tenant/profile enablement | Authorized tenant/platform owner, entitlement/configuration, account/grant readiness, audit. |
| Credential/grant scope change | Delegated authority, Security controls, expiry/rotation/revocation, separation where required. |
| High-impact action approval | Current request fingerprint, authorized approver, risk/limit/purpose, expiry, audit. |
| Contract/version migration | Owner approval, compatibility, consumer impact, rollout/rollback, observability/test evidence. |
| Suspension/incident restriction | Delegated operational/security authority, scope, reason, effective time, review/expiry. |
| Retirement/migration | Owner approval, active-work treatment, credential/provider exit, audit/lifecycle evidence. |

---

# Roles and Separation of Duties

| Role | May do | Must not do by default |
|---|---|---|
| Integration owner | Define contracts, onboarding, lifecycle, technical evidence. | Override enterprise policy or approve own exceptional access. |
| Tenant administrator | Request/manage own authorized configuration. | Access other tenants, broad provider credentials, or platform controls. |
| Action approver | Approve/reject a bounded request within authority. | Change connector/grant scope through the same approval. |
| Security owner | Define/operate enterprise identity, policy, secrets, compliance, incident controls. | Own Integration business semantics. |
| Operator/support | Execute approved runbook and restricted support work. | Gain implicit content, credential, or action authority. |
| Automation | Apply documented low-risk policy and emit evidence. | Self-expand scope, approve exceptions, or suppress audit. |

---

# Audit Evidence Contract

Each governed event records tenant-safe scope, decision/action/resource category, principal/workload/approver role, purpose, policy/contract/configuration version, before/after or request fingerprint where permitted, effective/expiry time, correlation/causation, outcome/reason category, and protected evidence/incident reference.

Required audit categories include connector/capability/profile lifecycle; account/grant/credential-reference lifecycle; action authorization/approval/denial/cancellation; execution/uncertainty/reconciliation/compensation; webhook validation/quarantine; administration/support; exception/override; incident restriction/recovery; and retirement/migration.

Audit views are tenant-, purpose-, role-, and representation-scoped. They exclude raw credentials, tokens, full provider payloads, sensitive parameters, unredacted content, and unrestricted external IDs.

---

# Exceptions, Review, and Retention

An exception has explicit authority, narrow scope, reason, compensating controls, effective/expiry time, owner, review, and audit. It cannot permanently weaken an action guard, tenant isolation, credential control, or data-egress rule.

Connector/capability/profile/grant/action-risk controls are reviewed at onboarding, material contract/provider/policy/data/residency change, incident, deprecation, and periodic architecture cadence. Audit retention, deletion, export, legal hold, and evidence access follow Data/Security policy; Integration records the domain requirements and outcomes.

---

# Platform Foundation and Channel Boundaries

Platform Foundation supplies tenant, membership, entitlement, configuration, and API-edge facts used in governance decisions. Voice and Digital Channel Platforms own their transport governance; Integration governance cannot authorize channel delivery or reinterpret a channel event as participant approval.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Integration decision-rights matrix | Defines roles, authorities, separation, approval, exception, and review. | Integration with Security and Platform Foundation owners |
| Governance/audit event catalog | Defines evidence fields, representation, retention references, access, and compatibility. | Integration with Security, Data, and Observability owners |
| Connector lifecycle and change procedure | Defines onboarding, enablement, migration, suspension, retirement, and exit evidence. | Integration with Operations, Testing, and Security owners |
| Exception and support-access procedure | Defines narrow override, approval, expiry, post-review, and audit. | Integration with Security and Operations owners |
| Governance conformance suite | Proves separation, audit completeness, privacy, tenant scope, exception expiry, and retirement. | Integration with Testing and Security owners |

---

# Anti-Patterns

## Connector Owner Approves Everything

High-risk connector, grant, action, and exception changes require the configured independent authority and evidence.

## Audit Log Is a Debug Dump

Audit records accountable normalized evidence; raw secrets, provider payloads, and sensitive content use protected evidence paths.

## Exception Has No Expiry

Every exception is narrow, time-bounded, reviewed, auditable, and revoked when no longer necessary.

## Retirement Means Disable and Forget

Retirement handles active actions, credentials, provider mappings, evidence, migration, reconciliation, and governed retention.

---

# Related Documents

| Document | Relationship |
|---|---|
| 03_TOOL_AND_CONNECTOR_REGISTRY.md | Defines connector/capability lifecycle. |
| 05_ACTION_AUTHORIZATION_AND_APPROVAL.md | Defines per-action approval evidence. |
| 10_INTEGRATION_ACCESS_AND_TENANT_ISOLATION.md | Defines scoped governance access. |
| 12_INTEGRATION_SECURITY_AND_PRIVACY.md | Defines security/privacy controls. |
| 09_SECURITY_PLATFORM/README.md | Owns enterprise governance control infrastructure. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Integration governance and audit architecture for decision rights, lifecycle, evidence, exceptions, and review. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

# 05_ACTION_AUTHORIZATION_AND_APPROVAL

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how Integration Platform decides whether a bounded external action may proceed, requires confirmation or approval, is restricted, or is denied.

Integration applies enterprise authorization and policy to a specific external effect. It does not own identity, policy-engine rules, business intent, participant consent law, or canonical Conversation state.

---

# Purpose

The action guard prevents an eligible tool, connected account, or valid credential from producing an unapproved or overbroad effect. It makes authorization, approval, confirmation, expiry, revocation, separation of duties, and evidence explicit for every material action.

---

# Objectives

- Evaluate current principal/workload, tenant, environment, subject, purpose, entitlement, capability, target, credential, policy, lifecycle, and risk scope before effect.
- Classify actions by impact and require the appropriate automatic policy decision, confirmation, delegated approval, or separation of duties.
- Bind approval to an immutable action request; a changed target, parameter, purpose, or effect class requires reauthorization.
- Ensure denial, expiry, cancellation, restriction, and incident conditions stop external execution safely.
- Preserve provider-neutral audit evidence without exposing sensitive parameters, secrets, or raw policy details.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Enterprise authentication, authorization policy engine, role model, cryptography, secrets, compliance, or incident governance | 09_SECURITY_PLATFORM |
| Agent selection, reasoning, business intent, or proposal generation | 02_AGENT_PLATFORM |
| Canonical work state, participant relationship, routing, handoff, or communication | 03_CONVERSATION_PLATFORM |
| Connector/capability lifecycle or credential delegation | 03 and 04 Integration documents |
| Dispatch, idempotency, retries, workflows, or callback mechanics | 06–09 and 13 Integration documents |
| Tenant/entitlement/configuration source of truth | 16_PLATFORM_FOUNDATION |

---

# Principles

## Intent Is Not Permission

Agent tool selection and a valid action request describe an intended effect. They do not authorize it. Integration independently evaluates current constraints immediately before each sensitive effect.

## Approval Is Request-Bound

An approval binds one immutable action request, including its capability, target, minimal parameter representation, purpose, effect class, tenant/environment, expiry, and constraints. It cannot be reused for a changed or future action.

## Credentials Do Not Bypass Approval

A valid delegated grant permits a bounded provider operation only after the current action guard approves it. Credential scope is necessary but never sufficient.

## Deny on Ambiguity

Missing, stale, contradictory, unsupported, or unverified evidence produces `Denied`, `Restricted`, `AwaitingApproval`, or `Deferred`—never an inferred approval or best-effort external effect.

---

# Action Risk Classes

| Class | Examples | Minimum posture |
|---|---|---|
| `ReadLowRisk` | Retrieve a permitted, minimized external status. | Current authorization, purpose, connector/profile, and data-egress guard. |
| `WriteStandard` | Create/update a bounded business record. | Current guard and policy; confirmation when configured. |
| `ExternalContact` | Send message, create invite, schedule contact. | Current guard, recipient/contactability constraints, explicit confirmation where policy requires. |
| `FinancialOrIrreversible` | Payment, refund, deletion, irreversible state change. | Strong approval, limits, separation of duties, idempotency, reconciliation, and audit. |
| `AdministrativeOrScopeChange` | Enable connector, change grant, modify provider/role/configuration. | Privileged authority, separation of duties, change approval, expiry, audit. |
| `SensitiveDataEgress` | Export/share protected content or personal data. | Current purpose, representation, destination, classification, policy, approval, and audit. |

The capability catalog declares the highest possible risk class. A request may be elevated by target, data classification, amount, region, or current policy; it may never be silently downgraded.

---

# Common Action Guard

Before dispatch, retry, workflow continuation, compensation, or sensitive callback-driven transition, Integration validates:

1. trusted principal/workload identity and tenant/environment;
2. current Agent/Conversation correlations and action lifecycle, without treating them as authority;
3. enabled connector/capability/profile, contract version, target resource, and provider account binding;
4. entitlement, purpose, subject relationship, policy, classification, consent/egress, region/residency, limits, and time window;
5. valid delegated grant and least-privilege credential lease;
6. action risk class, required confirmation/approval, separation of duties, expiry, revocation, and cancellation;
7. idempotency, duplicate-effect, rate/cost, fraud/abuse, incident, and reliability constraints; and
8. immutable authorization snapshot and protected audit correlation.

The guard executes the minimum permitted effect or reports a normalized safe outcome. It is re-evaluated rather than cached for a material action transition.

---

# Approval Model

| Approval type | Use | Required evidence |
|---|---|---|
| Policy-only | Low-risk effect fully allowed by current policy. | Guard snapshot, policy version, scope, expiry, audit. |
| Participant confirmation | A current participant must confirm a proposed effect. | Authorized presentation path, request fingerprint, explicit response, expiry, representation/purpose. |
| Delegated business approval | An authorized human/business role approves a bounded action. | Approver authority, separation constraints, reason, request fingerprint, expiry, audit. |
| Multi-party approval | High-impact or regulated action needs distinct approvers. | Required roles, independence, quorum, order/expiry, audit. |
| Emergency restriction/override | A delegated authority restricts or exceptionally permits a defined scope. | Authority, reason, narrow scope, expiry, review, incident/audit reference. |

Approval evidence includes only protected parameter hashes or approved representations when full parameters are sensitive. Provider acceptance, a chat message, verbal statement, or UI click without an approved correlation cannot be interpreted as approval.

---

# Authorization Outcomes

| Outcome | Meaning | Integration behavior |
|---|---|---|
| `Authorized` | Current action guard and required approval pass. | Permit only recorded bounded dispatch. |
| `AwaitingApproval` | Required evidence is absent but action may be presented safely. | Do not dispatch; request approval through owning channel/Conversation contract. |
| `Denied` | Current policy, scope, target, entitlement, or evidence fails. | Suppress effect; record minimal protected reason. |
| `Restricted` | Only a narrower action/profile/representation is allowed. | Apply recorded restriction or stop. |
| `Expired` | Grant, approval, or action window is no longer current. | Require a new request/approval. |
| `Cancelled` | Current authorized cancellation stops remaining work. | Stop or reconcile any already-uncertain effect. |
| `Uncertain` | Existing external effect cannot be confirmed. | Reconcile; do not authorize duplicate retry. |

An outcome is Integration evidence only. Conversation determines whether a participant sees a notice, retry option, or handoff.

---

# Separation of Duties and Limits

High-impact actions require the configured distinction between requester, approver, connector administrator, and executor. One principal/service cannot satisfy multiple roles when policy requires independence. Limits may apply to amount, frequency, target class, data sensitivity, region, capability, tenant tier, and operation window.

Delegated approval never expands a connector's registered capability, credential scope, entitlement, or policy boundary. If constraints conflict, the most restrictive valid result applies.

---

# Platform Foundation and Channel Boundaries

Platform Foundation supplies authoritative tenant, membership, entitlement, configuration, and API-edge facts. Integration consumes those facts but does not create grants or infer entitlement from provider identity.

Voice and Digital Channel Platforms can present an approved confirmation or consume a normalized result only through current Conversation-authorized contracts. They do not approve a business action merely by carrying participant input, and Integration does not choose delivery or claim participant receipt.

---

# Audit and Privacy

Authorization evidence records action/request fingerprint, risk class, scope, policy/approval versions, actor/service/approver role, decision, effective/expiry time, constraints, correlation, and protected evidence reference. It excludes raw secrets, full sensitive parameters, unredacted content, provider tokens, and direct identifiers from routine logs and events.

Approval withdrawal, policy change, grant revocation, tenant suspension, cancellation, or incident restriction invalidates future use and is rechecked before each material effect.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Action-risk and approval matrix | Defines risk classes, required evidence, limits, separation, expiry, and outcome. | Integration with Security and business owners |
| Common action-guard contract | Defines trusted inputs, evaluation order, snapshot, restrictions, and re-evaluation. | Integration with Security, Agent, Conversation, and Platform Foundation owners |
| Approval representation contract | Defines request fingerprints, protected display, confirmation, delegated/multi-party approval, withdrawal, and audit. | Integration with Frontend, Conversation, Security owners |
| Authorization audit/test suite | Proves denial, expiry, cancellation, scope narrowing, separation, egress, and no-duplicate behavior. | Integration with Security and Testing owners |

---

# Anti-Patterns

## Agent Selected the Tool, So Run It

Selection is intent evidence; the current Integration guard and required approval decide whether the external effect may proceed.

## OAuth Consent Approves Every Action

External delegation does not approve a particular platform action, target, purpose, or data representation.

## Approval Survives Parameter Change

Any material request change produces a new fingerprint and requires current authorization/approval.

## Callback Triggers a New Effect

Callbacks are validated evidence, not independent action authority; follow-on effects require their own bounded request and guard.

---

# Related Documents

| Document | Relationship |
|---|---|
| 02_INTEGRATION_DOMAIN_MODEL.md | Defines action, authorization, and approval records. |
| 03_TOOL_AND_CONNECTOR_REGISTRY.md | Defines registered capability risk and contract metadata. |
| 04_CONNECTOR_AUTHENTICATION_AND_CREDENTIAL_DELEGATION.md | Defines external grants and leases. |
| 06_ACTION_EXECUTION_AND_IDEMPOTENCY.md | Applies the guard before execution and retry. |
| 10_INTEGRATION_ACCESS_AND_TENANT_ISOLATION.md | Defines scope and isolation enforcement. |
| 11_INTEGRATION_GOVERNANCE_AND_AUDIT.md | Defines governance and audit review. |
| 09_SECURITY_PLATFORM/README.md | Owns enterprise authorization and policy controls. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created action authorization and approval architecture covering risk, guards, confirmations, separation, limits, and audit. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

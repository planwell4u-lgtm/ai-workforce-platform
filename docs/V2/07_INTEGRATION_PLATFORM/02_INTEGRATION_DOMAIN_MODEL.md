# 02_INTEGRATION_DOMAIN_MODEL

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines the canonical Integration-domain records that describe a connector capability, a bounded external action, its authorization/approval evidence, execution attempt, external outcome, callback, and reconciliation.

These records make external effects traceable and safe without becoming the canonical Conversation, Agent, tenant, identity, credential, business-object, or physical-storage model.

---

# Purpose

The Integration domain model provides stable, provider-neutral identifiers and evidence needed to request, validate, execute, observe, reconcile, and audit approved external actions.

It prevents a provider-specific ID, response, webhook, credential, or workflow status from becoming a cross-platform public identifier, a reusable authorization token, or an implicit statement of business completion.

---

# Objectives

The domain model must:

- Represent one bounded requested external effect and its immutable scope snapshot.
- Separate requested intent, authorization, approval, dispatch, provider interaction, outcome, uncertainty, and reconciliation evidence.
- Bind every record to one trusted tenant and environment and preserve subject, purpose, policy, capability, connector, and external-resource references where applicable.
- Support idempotency, ordering, retry, compensation, cancellation, provider migration, audit, and data-minimization requirements.
- Keep identifiers opaque, provider-neutral, versioned, and safe to expose only through approved representations.
- Preserve Agent ownership of intent and Conversation ownership of canonical work meaning.

---

# Scope

This document defines logical entities, relationships, identifiers, ownership, state vocabulary, invariants, evidence rules, and external-data boundaries for Integration Platform.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Agent goal, reasoning, tool selection, business decision, or prompt/model state | 02_AGENT_PLATFORM |
| Canonical conversation/work/session/participant state, routing, handoff, or participant notification | 03_CONVERSATION_PLATFORM |
| Tenant, organization, membership, entitlement, configuration, or API-edge source of truth | 16_PLATFORM_FOUNDATION |
| Enterprise identity, authorization evaluation engine, credential vault, cryptography, audit infrastructure, compliance, or incident governance | 09_SECURITY_PLATFORM |
| Physical tables, indexes, queues, object storage, backups, retention/deletion execution, or data residency implementation | 08_DATA_PLATFORM |
| Connector capability registry, external credential delegation, detailed authorization policy, execution mechanics, workflow behavior, webhook protocol, or lifecycle controls | Integration documents 03–16 |

---

# Domain Principles

## Integration Evidence Is Not Business Truth

An Integration record proves only what the bounded integration operation observed or did. A `Succeeded` action does not independently mean an order is fulfilled, a case is resolved, a payment is settled, or a participant has been notified. The relevant external-system and Conversation contracts determine those meanings.

## Request, Authority, and Effect Remain Separate

The requested action expresses an intended effect. Authorization and approval evidence decide whether it may proceed. Execution attempts record technical work. External outcomes record observed evidence. No one record substitutes for the others.

## Opaque IDs Are Not Authority

An action ID, provider-operation ID, callback ID, workflow ID, credential reference, external-resource reference, or idempotency key is a scoped correlation reference—not a bearer credential, tenant selector, or permission to read, repeat, alter, or export the underlying operation.

## Immutability Protects the Evidence Trail

Requested scope and recorded evidence are append-only after creation. Correction, cancellation, redaction, reauthorization, retry, migration, or reconciliation creates a related record with causation, version, and actor/evidence references. It does not overwrite history.

---

# Core Entities

| Entity | Meaning | Owned by Integration | Must not become |
|---|---|---|---|
| `Connector` | A provider-neutral integration boundary for one external-system family. | Connector identity, adapter binding, lifecycle reference. | A provider account, tenant, credential, or business object. |
| `Capability` | A versioned operation that a Connector may expose. | Contract schema, constraints, capability profile reference. | Agent authorization, business intent, or direct provider method. |
| `ActionRequest` | A bounded intended external effect submitted through an approved platform contract. | Request envelope, scope snapshot reference, idempotency boundary, lifecycle evidence. | Canonical Conversation work or Agent plan. |
| `ActionAuthorization` | Evidence that the request passed current action guard requirements. | Applied-scope and decision reference. | Security Platform's authorization policy engine. |
| `ApprovalRecord` | Evidence of required confirmation, delegated approval, rejection, expiry, or revocation. | Action-specific linkage and result. | General identity, consent, or policy source of truth. |
| `ExecutionAttempt` | One controlled technical attempt to perform all or part of an action. | Attempt ordering, dispatch/result evidence, retry safety. | Proof of business completion. |
| `ExternalOperation` | Protected mapping to an external provider's operation/resource evidence. | Adapter-scoped reference, provider state category, correlation. | Canonical platform ID or a public provider identifier. |
| `ExternalOutcome` | Normalized evidence of confirmed success, failure, no-effect, restriction, or uncertainty. | Provider-neutral outcome and evidence reference. | Canonical Conversation outcome or participant delivery fact. |
| `CallbackReceipt` | Validated external callback/event evidence. | Source-validation, deduplication, ordering, correlation result. | Authorization or an executable command. |
| `ReconciliationCase` | Governed investigation of uncertain, delayed, conflicting, or failed-after-effect evidence. | Current disposition, deadline, owner, protected evidence references. | A retry queue or a business-workflow owner. |
| `CompensationRecord` | A bounded approved reversing or mitigating external action. | Relationship to original action and effect evidence. | Automatic undo or permission to alter unrelated data. |

---

# Required Shared References

Every material entity includes, where applicable:

- `integrationId`: opaque, stable Integration-domain identifier;
- trusted `tenantId` and `environmentId` references from Platform Foundation;
- `subjectReference` and `purposeReference` when an action concerns a person, organization, or protected data;
- `conversationReference` and `agentWorkReference` only as protected cross-platform correlations;
- connector, capability, configuration/profile, credential-grant, policy, entitlement, approval, and contract-version references;
- classification, representation, data-egress, retention, and residency references where data crosses a boundary;
- causation, correlation, idempotency, ordering, trace, actor/service, and time/clock-quality references; and
- audit, incident, or reconciliation references when required.

References are validated against trusted server-side scope before use. Absence, ambiguity, stale binding, or mismatch denies, restricts, or quarantines the operation; it never selects a default tenant, provider, subject, or external resource.

---

# Action Request Model

An `ActionRequest` is immutable once accepted. It includes:

| Field group | Required meaning |
|---|---|
| Request identity | Integration action ID, request version, idempotency scope/key, correlation/causation, requested time, and actor/service. |
| Intended capability | Connector and capability reference, contract/schema version, allowed parameter representation, and bounded operation class. |
| Scope | Tenant/environment, subject/purpose, Conversation/Agent correlations, entitlement/configuration/profile, and target external-resource reference. |
| Constraints | Policy, approval, credential-grant, classification, egress, residency, rate/cost, deadline, cancellation, and duplicate-safety requirements. |
| Parameters | Validated minimal provider-neutral representation with sensitive values protected by reference when necessary. |
| Evidence | Source request reference, validation result, audit reference, and explicit rejection/restriction reason when applicable. |

An action request cannot be amended in place. A changed target, parameter, purpose, capability, approval condition, or material constraint creates a new request that explicitly supersedes or relates to the prior one.

---

# State and Outcome Vocabulary

## Action State

| State | Meaning | Allowed next direction |
|---|---|---|
| `Requested` | Bounded request received; no external effect is implied. | Validate, deny, cancel. |
| `Validating` | Scope, schema, guard, and idempotency checks are in progress. | Await approval, authorize, deny, defer. |
| `AwaitingApproval` | A required current approval is outstanding. | Authorize, deny, expire, cancel. |
| `Authorized` | Current guard passed within a recorded scope and expiry. | Dispatch, cancel, expire, restrict. |
| `Dispatching` | A controlled external submission is being prepared or sent. | In progress, failed, uncertain. |
| `InProgress` | Provider or workflow work is underway. | Succeed, fail, cancel, uncertain, reconcile. |
| `Succeeded` | Evidence confirms the bounded external effect. | Reconcile only if contradictory later evidence arrives. |
| `Failed` | Evidence confirms no bounded external effect completed. | Re-request or reconcile through current authority. |
| `Denied` | Current controls rejected the request before effect. | New request only. |
| `Cancelled` | Remaining permitted work was stopped by a current cancellation. | Reconcile if effect certainty is incomplete. |
| `Deferred` | Work is not currently eligible and needs a future approved re-evaluation. | New validation only. |
| `Restricted` | A current policy, incident, capacity, or lifecycle condition limits action scope. | Continue only with recorded limits, or resolve. |
| `Uncertain` | External effect cannot be confirmed safely. | Reconcile; no unsafe duplicate retry. |
| `Reconciled` | Reconciliation established the final safe disposition. | Terminal unless a new related action is requested. |

## External Outcome Category

`ConfirmedSuccess`, `ConfirmedFailure`, `ConfirmedNoEffect`, `Denied`, `Cancelled`, `Restricted`, `Unavailable`, `Deferred`, `Degraded`, `OutcomeUncertain`, and `ReconciliationRequired` are normalized Integration evidence categories. Provider-native success codes, errors, statuses, and resource IDs remain adapter-scoped details.

---

# Relationships and Causation

~~~text
Connector -> Capability
ActionRequest -> ActionAuthorization -> ApprovalRecord (when required)
ActionRequest -> ExecutionAttempt (one or more, bounded)
ExecutionAttempt -> ExternalOperation -> ExternalOutcome
CallbackReceipt -> ExternalOperation or ReconciliationCase
ActionRequest -> ReconciliationCase -> ExternalOutcome
ActionRequest -> CompensationRecord -> related ActionRequest
~~~

One request may have multiple attempts only when the action's current idempotency and retry policy permits them. Each attempt has one ordered attempt number and links to the original idempotency boundary. A compensation is a separately authorized action, not an implicit rollback.

---

# Provider Mapping Boundary

The adapter maps a platform `Connector`, `Capability`, `ExecutionAttempt`, `ExternalOperation`, `CallbackReceipt`, and `ExternalOutcome` to provider-specific concepts. Provider account IDs, OAuth subject IDs, webhook event IDs, object IDs, request IDs, raw payloads, and error messages are stored only as protected adapter evidence and never cross public Integration contracts without an approved representation.

The mapping supports provider replacement by preserving the platform action and outcome history independently of any provider. A provider migration creates explicit mapping, readiness, and reconciliation evidence; it does not rewrite prior action or audit records.

---

# Cross-Platform Boundaries

## Platform Foundation and Digital Channel

Platform Foundation supplies trusted tenant, environment, membership, entitlement, configuration, and API-edge references. Integration records and validates them but does not own or duplicate their lifecycle.

Digital Channel Platform owns non-voice transport, delivery, and channel identities. An Integration `ActionRequest` may correlate to a channel journey but does not select a channel, deliver a message, or prove a participant received anything. Voice Platform retains the same boundary for voice media and telephony.

## Agent and Conversation

Agent references express bounded requested intent; they do not turn an action record into an Agent plan or grant execution authority beyond current Integration guards. Conversation references connect a request to canonical work but do not make the action state a Conversation state. Integration publishes normalized evidence; Conversation determines canonical outcome, routing, handoff, and participant communication.

## Data and Security

Data Platform implements durable storage and lifecycle mechanisms for logical Integration records. Security Platform supplies current identity, authorization, credential, cryptographic, compliance, audit-infrastructure, and incident controls. Neither platform cedes ownership to a connector or action record.

---

# Invariants

- Every material Integration entity belongs to exactly one trusted tenant and environment.
- A provider ID or callback cannot create, move, or widen a tenant, subject, purpose, or entitlement binding.
- An external effect has a single bounded `ActionRequest` and idempotency boundary, even when multiple attempts or callbacks exist.
- No attempt begins without current validation, authorization, approval where required, capability/profile, credential scope, and lifecycle checks.
- No uncertain effect is automatically repeated, compensated, or represented as confirmed success/failure.
- Cross-platform references are correlations, not direct object ownership or database access authority.
- Raw credentials, tokens, provider payloads, direct identifiers, and sensitive parameters are excluded from routine events, logs, traces, and public outcome representations.
- A terminal Integration state does not automatically change Agent or Conversation state.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Integration entity and identifier specification | Defines entities, opaque IDs, references, mutability, exposure, and provider mapping. | Integration with Architecture, Data, and Security owners |
| Action-request and outcome schemas | Defines versioned request, guard, state, outcome, error, evidence, and compatibility contracts. | Integration with Agent, Conversation, Security, and Testing owners |
| Idempotency and causation standard | Defines keys, ordering, attempt linkage, replay handling, uncertain-effect suppression, and audit. | Integration with Data, Security, and Operations owners |
| Provider mapping standard | Defines protected provider IDs, raw payload handling, normalization, migration, and replacement. | Integration with Security, Data, and Testing owners |
| Reconciliation and compensation record standard | Defines uncertainty, evidence, deadlines, authority, disposition, and safe compensating-action linkage. | Integration with Conversation, Security, Data, and Operations owners |

---

# Anti-Patterns

## Provider Object Is the Integration Object

Provider records are adapter evidence. They cannot serve as public action IDs, canonical business objects, tenant selectors, or cross-platform contracts.

## One Action Record Is Enough Evidence

Request, authorization, approval, attempt, provider result, and reconciliation answer different questions and must remain distinguishable.

## Success Means the Conversation Is Complete

Integration success confirms only the bounded external effect. Conversation owns canonical work and participant outcome meaning.

## Retry Creates a New Unrelated Action

Safe retries remain causally linked to the original bounded request and idempotency policy. A materially changed request is a new action.

## Callback Can Authorize an Action

A callback is validated external evidence only. It cannot supply missing approval, credentials, tenant binding, intent, or authorization.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_INTEGRATION_PLATFORM_ARCHITECTURE.md | Defines the Integration execution boundary and governed action path. |
| 03_TOOL_AND_CONNECTOR_REGISTRY.md | Defines Connector and Capability registration and lifecycle. |
| 04_CONNECTOR_AUTHENTICATION_AND_CREDENTIAL_DELEGATION.md | Defines credential-grant references and delegation. |
| 05_ACTION_AUTHORIZATION_AND_APPROVAL.md | Defines action guard and ApprovalRecord policy. |
| 06_ACTION_EXECUTION_AND_IDEMPOTENCY.md | Defines attempts, dispatch, idempotency, and normalized outcomes. |
| 07_WORKFLOW_AND_ASYNCHRONOUS_EXECUTION.md | Defines long-running work and compensation. |
| 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md | Defines CallbackReceipt validation and correlation. |
| 13_INTEGRATION_RELIABILITY_AND_FAILURE_HANDLING.md | Defines uncertainty, reconciliation, and safe recovery. |
| 03_CONVERSATION_PLATFORM/README.md | Defines canonical interaction/work ownership. |
| 02_AGENT_PLATFORM/README.md | Defines Agent intent and tool-selection ownership. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Integration domain model for provider-neutral actions, evidence, outcomes, callbacks, reconciliation, and compensation. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

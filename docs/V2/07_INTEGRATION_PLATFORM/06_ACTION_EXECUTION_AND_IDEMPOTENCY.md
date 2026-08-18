# 06_ACTION_EXECUTION_AND_IDEMPOTENCY

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how Integration Platform dispatches one authorized external action, prevents duplicate effects, normalizes provider responses, and reconciles uncertainty.

Execution is a bounded technical effect. It does not decide the action intent, replace the action guard, own business workflow meaning, or make a provider response canonical Conversation state.

---

# Purpose

The model ensures that retried, delayed, duplicated, partial, or contradictory requests do not create duplicate CRM changes, messages, calendar events, financial actions, exports, or administrative effects.

---

# Objectives

- Dispatch only a current authorized, approved, scoped, and non-cancelled action.
- Establish a stable idempotency boundary before any external effect.
- Normalize provider requests, responses, errors, and callbacks behind an adapter.
- Distinguish confirmed success/failure from no-effect, cancellation, restriction, deferred work, and uncertainty.
- Re-evaluate current authority before retry, continuation, compensation, or recovery.
- Preserve protected audit, correlation, and reconciliation evidence without leaking provider payloads or secrets.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Action intent, risk, authorization, approval, or confirmation policy | 02_AGENT_PLATFORM and 05_ACTION_AUTHORIZATION_AND_APPROVAL.md |
| Connector/capability registration or credential delegation | 03 and 04 Integration documents |
| Long-running multi-step workflow/compensation orchestration | 07_WORKFLOW_AND_ASYNCHRONOUS_EXECUTION.md |
| Webhook protocol/source validation | 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md |
| Canonical Conversation/work state or participant communication | 03_CONVERSATION_PLATFORM |
| Enterprise storage, queue, security, or incident infrastructure | 08_DATA_PLATFORM and 09_SECURITY_PLATFORM |

---

# Execution Principles

## Guard Before Effect

The current action guard runs immediately before dispatch. An earlier `Authorized` record, cached profile, provider session, or queued job cannot independently permit a new effect.

## Idempotency Is a Business Boundary

An idempotency key represents one intended external effect within one tenant/environment, capability, target, action request, and parameter fingerprint. It is not merely a transport retry key and cannot be reused for a materially changed action.

## Timeout Means Uncertain Until Proven Otherwise

Network timeout, worker restart, provider acknowledgement, or missing callback does not prove success or failure. Integration suppresses unsafe repeat and opens reconciliation where independent evidence is unavailable.

## Adapter Evidence Is Normalized

Provider requests and responses remain adapter-scoped. Consumers receive provider-neutral outcome categories, protected evidence references, and explicit certainty—not raw provider IDs, payloads, or error text.

---

# Execution Record Model

| Record | Required meaning |
|---|---|
| `ExecutionPlan` | Immutable dispatch-ready view of current request, guard snapshot, connector/capability/profile, minimal parameters, target, idempotency boundary, deadlines, and constraints. |
| `ExecutionAttempt` | Ordered technical attempt with start/end, adapter/version, credential-lease reference, provider request evidence, result category, and correlation. |
| `IdempotencyRecord` | Protected mapping from action fingerprint to permitted effect and latest trustworthy disposition. |
| `ExternalOperation` | Adapter-scoped provider operation reference and normalized provider-state evidence. |
| `ExternalOutcome` | Confirmed success/failure/no-effect, restriction, cancellation, unavailable/deferred, or uncertainty. |
| `ReconciliationCase` | Required when effect certainty or ordering is incomplete or contradictory. |

All records carry trusted tenant/environment, action/capability/version, purpose, subject where applicable, policy/approval, correlation/causation, audit, and protected evidence references.

---

# Dispatch Flow

1. Load the immutable ActionRequest and re-run the current action guard.
2. Validate connector/capability/profile, target, credential lease, data-egress, region, limits, cancellation, and deadline.
3. Resolve or create the idempotency record using the approved action fingerprint.
4. If a prior confirmed or uncertain effect exists, return its governed disposition; do not dispatch a duplicate.
5. Create an ordered ExecutionAttempt and invoke the provider only through the approved adapter.
6. Record the least sensitive normalized provider evidence and determine confirmed result, retry eligibility, or uncertainty.
7. Publish protected outcome evidence to approved consumers; Conversation determines canonical and participant-facing consequences.

---

# Idempotency and Ordering Rules

The idempotency fingerprint includes tenant/environment, capability/version, action request, target representation, material parameters, purpose/effect class, and approved scope. It excludes transient transport metadata so safe retries resolve to the same record.

| Condition | Required behavior |
|---|---|
| Same request, no prior dispatch | Create one permitted attempt. |
| Same request, confirmed success | Return prior outcome; never repeat effect. |
| Same request, confirmed failure/no-effect | Retry only if current policy and operation class permit it. |
| Same request, uncertain effect | Suppress automatic repeat; reconcile. |
| Changed target/parameter/purpose/capability | Require a new ActionRequest, guard, approval, and idempotency boundary. |
| Duplicate/out-of-order callback | Deduplicate, validate ordering, and reconcile if outcome conflict remains. |

Idempotency retention is governed by effect class, provider replay window, audit, lifecycle, and Data/Security policy. Expiry does not permit an unsafe repeat where external effect history is still uncertain.

---

# Retry and Fallback Policy

Retry is allowed only when the current guard passes and evidence proves it cannot duplicate or conflict with an external effect. It has a bounded attempt count, deadline, backoff, rate/cost budget, tenant/provider bulkhead, and audit record.

Automatic retry is normally prohibited for external contact, financial/irreversible effect, sensitive export, provider-side write with unknown state, compensation, or administrative scope change unless the adapter can prove no effect occurred and policy permits it.

Fallback to another provider/account/route/capability is a new eligibility decision. It cannot change recipient, purpose, data representation, residency, approval, credential scope, or effect semantics merely to preserve availability.

---

# Outcome and Reconciliation

| Outcome | Meaning | Next behavior |
|---|---|---|
| `ConfirmedSuccess` | Trusted evidence confirms bounded effect. | Publish outcome; no duplicate retry. |
| `ConfirmedFailure` | Trusted evidence confirms no effect. | Safe retry only if current policy permits. |
| `ConfirmedNoEffect` | Provider/state evidence shows nothing occurred. | Treat according to action policy. |
| `Cancelled` / `Restricted` | Current control stopped or narrowed work. | Do not resume without new guard. |
| `Unavailable` / `Deferred` | Dependency or condition prevents current work. | Bounded re-evaluation only. |
| `OutcomeUncertain` | Effect may have occurred but cannot be confirmed. | Open reconciliation; suppress duplicate. |

Reconciliation compares current scope with trusted provider, callback, data, and idempotency evidence. It may confirm success, failure, no-effect, continued uncertainty, escalation, or a separately authorized compensation. It cannot manufacture a result or execute a new effect without current authority.

---

# Platform Foundation and Channel Boundaries

Platform Foundation supplies trusted tenant, entitlement, configuration, environment, and API-edge facts. Execution validates them at every attempt; provider account or callback data cannot select tenant scope.

Voice and Digital Channel Platforms may consume a normalized external outcome but do not dispatch Integration actions directly or infer participant delivery from provider execution. Conversation owns any participant communication or canonical work transition.

---

# Observability and Audit

Required evidence includes action/attempt/idempotency references, capability/profile/adapter version, guard outcome, provider-state category, certainty, retry/fallback/reconciliation status, timing, rate/cost category, correlation, and protected audit reference.

Routine telemetry excludes credentials, raw requests/responses, full external IDs, sensitive parameters, and content. Detailed evidence is available only through current approved representation and audit paths.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Execution-plan and attempt contract | Defines dispatch inputs, guard recheck, evidence, outcomes, and compatibility. | Integration with Security, Data, and Testing owners |
| Idempotency standard | Defines fingerprint, retention, duplicate suppression, ordering, concurrency, and provider mapping. | Integration with Data, Security, and Operations owners |
| Provider adapter execution contract | Defines request/result normalization, timeout, cancellation, error, and evidence handling. | Integration with Testing and Security owners |
| Retry/fallback/reconciliation matrix | Defines safe eligibility, limits, uncertainty, provider failover, and escalation. | Integration with Operations, Security, and Conversation owners |
| Execution safety test suite | Proves no duplicate effect, stale grant use, cross-tenant dispatch, unsafe fallback, or raw-data leakage. | Integration with Testing and Security owners |

---

# Anti-Patterns

## Queue Delivery Means Execute Again

Queue or worker replay is not proof that the provider did not receive the first request. Resolve the idempotency and external-effect evidence first.

## Provider HTTP 200 Means Business Success

Provider transport success is adapter evidence only; a normalized bounded outcome and any required reconciliation are still needed.

## New Parameter, Same Idempotency Key

Material change creates a new action and approval boundary. Reusing a key would merge distinct effects unsafely.

## Retry Uses Stale Approval or Grant

Every retry and recovery step re-evaluates current guard, approval, credential, policy, lifecycle, and cancellation state.

---

# Related Documents

| Document | Relationship |
|---|---|
| 02_INTEGRATION_DOMAIN_MODEL.md | Defines action, attempt, outcome, and reconciliation records. |
| 05_ACTION_AUTHORIZATION_AND_APPROVAL.md | Defines the guard required before every effect. |
| 07_WORKFLOW_AND_ASYNCHRONOUS_EXECUTION.md | Extends this model for long-running work. |
| 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md | Supplies validated callback evidence. |
| 13_INTEGRATION_RELIABILITY_AND_FAILURE_HANDLING.md | Defines broader failure and recovery controls. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created action execution and idempotency architecture for safe dispatch, normalized outcomes, retries, and reconciliation. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

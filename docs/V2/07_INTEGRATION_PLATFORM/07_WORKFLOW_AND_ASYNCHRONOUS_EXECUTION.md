# 07_WORKFLOW_AND_ASYNCHRONOUS_EXECUTION

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how Integration Platform coordinates bounded, long-running external action steps, delayed callbacks, retries, compensations, deadlines, and recovery.

An Integration workflow is technical orchestration of approved external effects. It is not the owner of Agent reasoning, business-process intent, canonical Conversation work, or participant communication.

---

# Purpose

The workflow model prevents background jobs, queues, provider callbacks, or compensating operations from continuing after authority changes, duplicating effects, crossing tenants, or silently changing business state.

---

# Objectives

- Coordinate asynchronous steps only from a bounded authorized action/workflow definition.
- Preserve per-step guard, idempotency, tenant, purpose, credential, approval, cancellation, and deadline requirements.
- Support delayed provider work, polling, callbacks, wait states, retries, compensation, and reconciliation without unsafe automatic continuation.
- Keep durable workflow evidence independent of provider job IDs and physical queue implementation.
- Make ownership, timeouts, handoff to Conversation/Agent, operational escalation, and terminal outcomes explicit.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Agent plans, business process design, reasoning, or tool selection | 02_AGENT_PLATFORM |
| Canonical Conversation work state, routing, handoff, participant waiting state, or communication | 03_CONVERSATION_PLATFORM |
| Action guard/approval, connector registry, credential delegation, or single-attempt dispatch | 03–06 Integration documents |
| Webhook protocol validation | 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md |
| Enterprise queues, schedulers, storage, incident process, or deployment | Data, Operations, Deployment, and Security Platforms |

---

# Principles

## Workflow Is a Bounded Technical Plan

Every workflow has an immutable definition/version, action/workflow purpose, tenant/environment scope, permitted step graph, deadlines, owner, cancellation behavior, and evidence requirements. It cannot dynamically invoke arbitrary capabilities or expand its own scope.

## Every Effectful Step Rechecks Authority

Waiting for a callback, queue replay, timer, worker restart, or provider recovery does not preserve authorization. Before a step dispatches, retries, compensates, or resumes, it re-runs the current action guard and idempotency checks.

## Compensation Is a New Controlled Effect

Compensation mitigates a prior action only when explicitly defined, currently authorized, safe for the observed state, and auditable. It is not an automatic undo and cannot erase evidence.

## Workflow State Is Not Conversation State

Workflow progress describes Integration technical coordination. Conversation determines the meaning of a business process, participant wait, routing, handoff, or completion.

---

# Workflow Model

| Entity | Meaning |
|---|---|
| `WorkflowDefinition` | Versioned bounded graph of permitted Integration step types and transitions. |
| `WorkflowRun` | One tenant-scoped execution of a definition tied to an ActionRequest or approved trigger. |
| `WorkflowStep` | One ordered wait, validation, dispatch, poll, callback, reconciliation, or compensation activity. |
| `StepAttempt` | One guarded/idempotent execution attempt for a step. |
| `WaitCondition` | Protected provider/callback/time/poll condition with deadline and correlation. |
| `CompensationRecord` | Separately authorized mitigative action linked to a completed effect. |
| `WorkflowReconciliationCase` | Investigation of uncertain, delayed, divergent, or stranded workflow evidence. |

All records contain trusted tenant/environment, action/purpose, connector/capability/profile, policy/approval/credential references where relevant, correlation/causation/idempotency, lifecycle, deadline, and protected audit evidence.

---

# Workflow Lifecycle

~~~text
Requested -> Validating -> Authorized -> Running -> Waiting -> Running -> Completed
                                      |             |              |
                                      v             v              v
                                  Suspended     Uncertain       Compensating
                                      |             |              |
                                      +--------> Reconciliation <-+
                                                     |
                                              Completed / Failed / Cancelled
~~~

| State | Meaning |
|---|---|
| `Requested` / `Validating` / `Authorized` | Workflow scope and current authority are being established. |
| `Running` | A permitted technical step is being coordinated. |
| `Waiting` | No effect is occurring while awaiting a bounded callback, poll time, or external completion. |
| `Suspended` | New progression is blocked by policy, incident, tenant, credential, health, or lifecycle condition. |
| `Uncertain` | An effect or external state cannot be confirmed safely. |
| `Compensating` | A separately authorized mitigative action is being evaluated/executed. |
| `Reconciliation` | Evidence is compared to establish safe disposition. |
| `Completed` / `Failed` / `Cancelled` | Terminal technical workflow result, not canonical business outcome. |

---

# Step Types and Transition Rules

| Step type | Allowed purpose | Prohibited behavior |
|---|---|---|
| Validate | Re-evaluate current scope, guard, and readiness. | Infer authority from prior state. |
| Dispatch | Execute one bounded action through Document 06 controls. | Invoke unregistered connector/provider directly. |
| Wait | Await a correlated external condition under deadline. | Hold broad credentials or assume completion. |
| Poll | Obtain bounded provider state through adapter. | Poll indefinitely or bypass rate/cost limits. |
| Callback | Consume validated normalized event evidence. | Treat callback as new intent or approval. |
| Reconcile | Determine confirmed effect/no-effect/uncertainty. | Retry a duplicate-sensitive effect blindly. |
| Compensate | Mitigate an eligible prior effect. | Undo unrelated data or erase audit history. |
| Finish | Publish normalized technical outcome. | Set canonical Conversation state or notify participants. |

Transitions are deterministic, versioned, and allowlisted by the WorkflowDefinition. Every effectful transition records causation and idempotency.

---

# Time, Cancellation, and Recovery

Each run and step has an owner, start/deadline, maximum attempts, wait/poll limit, cancellation behavior, expiry policy, escalation path, and safe terminal disposition. A deadline produces a governed `Deferred`, `Failed`, or `Uncertain` result; it never causes an unbounded worker loop.

Current cancellation, approval expiry, grant revocation, tenant suspension, policy restriction, or incident condition stops future effectful steps. If a prior effect is uncertain, the workflow opens reconciliation rather than claiming cancellation reversed it.

After restart, failover, or queue replay, workers restore only durable protected references, verify workflow/step version and trusted scope, re-run guards, resolve idempotency, and resume only a still-permitted step. Stale cached state cannot re-enable a retired capability or revoked credential.

---

# Compensation and Saga Boundary

Workflows may model a bounded saga when each effect and potential compensation is explicitly declared. Compensation is considered only after current policy, target state, provider evidence, tenant/purpose, approval, credential, and duplicate-safety checks pass.

When a business decision or human review is needed, Integration publishes normalized evidence to the owning Agent/Conversation/business process contract and waits. It does not decide whether a commercial, legal, customer, or operational consequence should be accepted.

---

# Platform Foundation and Channel Boundaries

Platform Foundation supplies trusted tenant, entitlement, configuration, and environment facts. Workflow runs use and revalidate them but never reconstruct them from queue, provider, or callback data.

Voice and Digital Channel Platforms may consume an approved outcome or present a Conversation-authorized update. Integration workflows do not choose a channel, send a participant message, place a call, or treat delivery evidence as workflow completion.

---

# Observability and Audit

Workflow evidence includes definition/run/step version, state, transition reason, owner, deadline, wait/poll/callback category, guard/idempotency result, effect certainty, compensation/reconciliation status, correlation, and protected audit reference.

Routine telemetry excludes secret material, raw provider payloads, sensitive parameters, and unscoped tenant data. Alerts identify stalled runs, deadline risk, reconciliation age, unexpected transition, compensation failure, callback mismatch, and guard/cancellation rejection.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Workflow definition contract | Defines graph, steps, transitions, scope, deadlines, terminal states, compatibility, and audit. | Integration with Agent, Conversation, Security, and Testing owners |
| Async execution/runbook standard | Defines queue/timer/poll/callback recovery, ownership, limits, escalation, and safe restart. | Integration with Data and Operations owners |
| Compensation and reconciliation matrix | Defines eligible compensation, evidence, approval, failure, and human-decision boundary. | Integration with Security, Conversation, and business owners |
| Workflow resilience test suite | Proves cancellation, stale state, replay, tenant isolation, deadline, uncertainty, and no duplicate effect. | Integration with Testing, Security, and Operations owners |

---

# Anti-Patterns

## Background Job Keeps Its Original Authority

All effectful continuation rechecks current guard, approval, credential, lifecycle, cancellation, and tenant scope.

## Workflow Engine Owns the Business Process

It coordinates technical external steps only. Agent/Conversation/business owners retain intent and canonical meaning.

## Compensation Always Runs on Failure

Compensation is a separate effect with its own safety, state, policy, and approval checks.

## Callback Completes the Workflow Automatically

Callback evidence must be validated, ordered, correlated, and reconciled before it can advance an allowed step.

---

# Related Documents

| Document | Relationship |
|---|---|
| 05_ACTION_AUTHORIZATION_AND_APPROVAL.md | Defines the current guard required for each effectful step. |
| 06_ACTION_EXECUTION_AND_IDEMPOTENCY.md | Defines one action attempt, idempotency, and uncertainty. |
| 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md | Defines callback validation and event normalization. |
| 13_INTEGRATION_RELIABILITY_AND_FAILURE_HANDLING.md | Defines failure/recovery outcomes and operations controls. |
| 03_CONVERSATION_PLATFORM/README.md | Owns canonical work and participant outcome meaning. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created workflow and asynchronous execution architecture covering runs, steps, waits, callbacks, compensation, recovery, and reconciliation. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

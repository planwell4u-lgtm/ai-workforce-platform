# 32_AGENT_FAILURE_HANDLING

**Version:** 2.2  
**Status:** Approved  
**Phase:** Agent Platform

---

# Overview

This document defines how the Agent Platform detects, classifies, contains, recovers from, communicates, and learns from failures across agent execution, context, permissions, dependencies, tools, workflows, channels, delivery, deployment, and observability.

Agent failure handling prioritizes safety, tenant isolation, authorization, data protection, and controlled recovery over completing an action at any cost. A failure must not cause an agent to broaden access, repeat an unsafe external action, expose sensitive information, or silently change behavior.

---

# Purpose

The purpose of the Agent Failure Handling Model is to provide predictable, tenant-safe behavior when an agent or dependency cannot complete expected work.

It establishes the agent-specific failure taxonomy, response patterns, recovery decisions, evidence, and boundary responsibilities. Operations Platform owns organization-wide incident management, on-call, support operations, and service-management procedures.

---

# Objectives

The Agent Failure Handling Model must:

- Detect and classify failures consistently across every agent execution boundary.
- Fail safely when authorization, tenant scope, classification, consent, integrity, or required policy cannot be established.
- Prevent duplicate external actions during retries, recovery, replay, and restart.
- Preserve durable state, audit evidence, correlation, and user-impact context.
- Provide controlled fallback, deferment, human handoff, suspension, rollback, or withdrawal paths.
- Distinguish transient dependency failures from permanent, security, policy, configuration, and business failures.
- Support tenant-scoped recovery without exposing data or allowing cross-tenant impact.
- Feed meaningful failure evidence into observability, evaluation, governance, and improvement processes.

---

# Scope

This document defines:

- Failure categories, severity, response decisions, and ownership for Agent Platform behavior.
- Retry, idempotency, timeout, circuit-breaker, fallback, handoff, replay, recovery, and communication principles.
- Failure handling for runtime execution, version/deployment, context, permissions, tools, workflows, events, channels, delivery, and telemetry.
- Tenant, security, audit, testing, and implementation-artifact requirements.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Enterprise incident command, on-call schedules, support process, post-incident review, and service management | 11_OPERATIONS_PLATFORM |
| Infrastructure failover, backup, disaster recovery, cluster/network recovery, and deployment mechanics | 12_DEPLOYMENT_PLATFORM and 08_DATA_PLATFORM |
| Telemetry infrastructure and alert delivery | 13_OBSERVABILITY_PLATFORM |
| Security incident policy, forensic process, compliance notification, and credential response | 09_SECURITY_PLATFORM and Agent Security Model |
| Detailed event transport, dead-letter infrastructure, or broker implementation | Event Integration Model and Integration Platform |
| Channel-provider recovery, telephony operations, or provider-specific failover | Voice and Channel Platforms |
| Business compensation workflow design | Agent Workflow Integration and Integration Platform |

---

# Failure Handling Principles

## Safety Before Completion

The platform chooses deny, defer, safe fallback, human handoff, suspension, or withdrawal when continuing would violate policy, create an unsafe external action, expose data, or misrepresent an outcome.

## Classify Before Retrying

Not every failure is retryable. The platform distinguishes transient availability failures from permanent validation, authorization, tenant, safety, business, configuration, and security failures before scheduling recovery.

## Idempotency Is Required for Side Effects

Any action that can change state, send a message, make a payment, update a record, or trigger external work has an idempotency strategy. Retrying a request, event, callback, workflow, or tool result must not duplicate the business effect.

## Preserve Evidence and State

A failure record includes tenant, agent/version, execution, trigger, dependency, policy/authorization, outcome, retry state, and correlation references. It records only protected summaries or references, not secrets or unnecessary customer content.

## Bounded Recovery

Retries, queues, replay, fallback, and human handoff are bounded by policy, time, risk, and user impact. Unbounded retry can amplify an incident, consume capacity, and duplicate action.

## Current Policy Applies on Recovery

A delayed retry, replay, resumed workflow, or restored session revalidates current tenant state, authorization, consent, classification, dependency eligibility, and deployment/version status. Historical permission never automatically authorizes recovery.

---

# Failure Taxonomy

| Category | Examples | Default response |
|---|---|---|
| Input and validation | Malformed request, unsupported content, incompatible schema, missing required context | Reject or quarantine; do not retry until corrected |
| Identity, tenant, or permission | Invalid identity, tenant mismatch, revoked consent, denied action, expired delegation | Fail closed; audit and route to verification or authorized review |
| Policy and safety | Unsafe output, approval required, prohibited action, classification restriction | Block, constrain, hand off, or request approval |
| Dependency transient | Timeout, rate limit, temporary provider outage, retryable network failure | Bounded retry with backoff, circuit protection, and fallback |
| Dependency permanent | Unsupported capability, revoked credential, incompatible contract, retired provider | Stop retry; remediate configuration or dependency |
| Runtime and state | Worker restart, cancellation, expired session, concurrency conflict, durable-state failure | Recover from durable state or safely terminate/defer |
| Tool and workflow | Parameter error, duplicate request, business rule rejection, compensation requirement | Apply idempotency, business recovery, or controlled handoff |
| Channel and delivery | Provider rejection, invalid recipient, failed delivery, channel outage | Record outcome; retry/fallback only under delivery and consent policy |
| Version and deployment | Invalid assignment, withdrawn version, failed readiness, rollback/stop condition | Block new work; resolve eligible version or suspend/withdraw |
| Telemetry and audit | Export outage, audit write failure, missing correlation, redaction failure | Use durable path or fail safe for material action; quarantine unsafe signal |

---

# Failure Severity and Ownership

## Severity

| Severity | Meaning | Required response |
|---|---|---|
| Informational | Expected or isolated non-user-impacting condition | Record and trend |
| Degraded | Reduced capability or bounded user impact | Contain, retry/fallback, alert owner |
| Major | Material tenant, channel, dependency, or business-process impact | Suspend expansion, invoke runbook, communicate as policy requires |
| Critical | Security, tenant-isolation, high-risk action, broad availability, or severe data-protection risk | Immediate containment, emergency withdrawal/escalation, preserve evidence |

Severity is based on risk, tenant scope, classification, external impact, recoverability, and affected population. A low-volume tenant-isolation failure can be critical even when ordinary error rate is low.

## Ownership

The component that detects a failure owns immediate safe handling and evidence emission. The platform that owns the failing capability owns remediation. Agent Platform coordinates agent-specific fallback, version/deployment state, and execution outcome; it does not assume ownership of another platform’s infrastructure or provider recovery.

## Failure Code Catalog

Every material failure uses a stable failure code in addition to its category and severity. The catalog defines code, meaning, retryability, safe disposition, user-impact category, owning platform, escalation route, and support guidance.

Failure codes are versioned and may be expanded but are not repurposed to mean a different condition. User-facing messages use approved disposition categories rather than exposing internal codes, sensitive configuration, or security details.

---

# Failure Response Model

~~~text
Failure Detected
    |
    v
Validate Tenant, Correlation, and Current State
    |
    v
Classify Category and Severity
    |
    +--> Reject / Quarantine
    +--> Block or Require Approval
    +--> Bounded Retry
    +--> Safe Fallback or Defer
    +--> Human Handoff
    +--> Suspend / Roll Back / Withdraw
    |
    v
Record Durable Outcome and Notify Authorized Owners
    |
    v
Recover, Close, or Create Improvement Work
~~~

## Failure Record

Every material failure record includes failure identifier, tenant, agent/version/deployment, execution/session/conversation references when applicable, trigger, component/dependency, category, severity, timestamp, retry/idempotency state, safe response, user-impact state, policy/authorization references, correlation, and audit reference.

## User Communication

The platform communicates only confirmed, appropriate information through an authorized channel. It does not claim an action completed when a dependency outcome is unknown. User-facing fallback, delay notification, or human handoff follows consent, classification, channel, and delivery policy.

---

# Retry, Timeout, and Circuit Controls

## Retry Eligibility

Retries are permitted only for transient, idempotent, or safely delegated operations. The retry policy defines maximum attempts, total duration, backoff, jitter, timeout, quota, and stop condition by dependency and risk level.

Validation, permission, tenant, policy, permanent dependency, and unsafe external-action failures are not retried automatically.

## Idempotency and Deduplication

The platform uses stable idempotency keys for inbound interactions, events, workflow actions, tool invocations, delivery requests, and provider callbacks. A receiver records or derives a durable outcome before acknowledging a side-effecting request.

A duplicate may return the earlier controlled outcome but must not repeat the underlying external action.

## Timeouts and Cancellation

Every dependency call, execution, workflow wait, and delivery attempt has a bounded timeout and cancellation behavior. Cancellation preserves durable state and does not leave an action ambiguous; when outcome cannot be determined, the platform uses reconciliation or controlled review rather than retrying blindly.

## Circuit Protection

When a dependency repeatedly fails or violates health thresholds, the platform limits further attempts through a circuit or equivalent protection mechanism. It records the dependency condition, directs work to an approved fallback or queue, and allows controlled re-entry only after health and policy checks succeed.

## Retry Budgets and Storm Protection

Retry policy includes a bounded budget by tenant, agent/version, dependency, operation class, and platform-wide dependency capacity. A retry is denied, deferred, or routed to fallback when its budget is exhausted, even if the individual operation would otherwise be retryable.

The platform applies concurrency limits, backoff, jitter, circuit protection, and priority rules to prevent a retry storm from overwhelming a recovering dependency or starving critical work. Retry exhaustion is an observable failure outcome, not a reason to silently discard work.

---

# Fallback, Handoff, and Compensation

## Safe Fallback

A fallback is an approved reduced behavior, such as providing a safe informational response, deferring work, offering another verified channel, creating a work item, or requesting user verification. It must not expose restricted data or move content to a less secure channel by default.

## Human Handoff

Human handoff is used when confidence, policy, approval, safety, user impact, or dependency failure requires authorized human attention. The handoff includes the minimum permitted context, failure summary, current state, required action, and correlation references.

## Workflow Compensation

When a multi-step business process partially completes, the workflow owner determines compensation or reconciliation. The Agent Platform records the failure relationship and prevents further unauthorized action; it does not invent business compensation.

## User-Impact Communication

The user-impact policy defines whether the platform communicates delay, failure, unknown outcome, fallback, or human handoff; who owns the communication; permitted channel; required wording/disclosure; and when a human assumes responsibility.

No message may state that a business action succeeded while its outcome is unknown. Communication remains subject to tenant, consent, classification, channel, and delivery authorization. A technical failure detail is not automatically appropriate for a user-facing response.

---

# Recovery, Replay, and Reconciliation

## Durable Recovery

After restart, failover, or interruption, the Agent Platform recovers only from durable execution, session, workflow, deployment, and audit references. In-memory model context, transient prompt state, or unconfirmed provider outcome is not treated as authoritative truth.

## Replay

Replay is an operationally controlled action. Before replay, the platform verifies tenant, idempotency, current authorization, consent, classification, dependency compatibility, lifecycle state, version/deployment eligibility, and external-side-effect risk.

## Reconciliation

When an external action may have completed but confirmation is unavailable, the platform reconciles through an approved authoritative interface, event, or human review. It does not retry a potentially completed payment, message, appointment, or record update simply because the initial response was lost.

---

# Data-Integrity Decision Table

| Outcome state | Required behavior |
|---|---|
| Confirmed complete | Record final outcome; prevent duplicate side effect; continue only with authorized follow-up |
| Confirmed failed | Record failure; apply approved retry, fallback, compensation, or handoff policy |
| Unknown outcome | Block duplicate action; mark reconciliation pending; query authoritative source or request review |
| Reconciliation pending | Preserve idempotency key and durable state; communicate only approved uncertainty/disposition |
| Compensation required | Refer to workflow owner; record related action and prevent unapproved continuation |

---

# Escalation and Recovery Objectives

## Escalation Matrix

| Failure condition | Primary escalation owner |
|---|---|
| Agent configuration, version, capability, or runtime behavior | Agent Platform owner |
| Conversation/session/context routing or handoff | Conversation Platform owner |
| Tool, workflow, integration, or external-system action | Integration Platform and workflow owner |
| Voice, telephony, media, or provider call behavior | Voice Platform owner |
| Messaging, email, chat, or channel delivery behavior | Relevant Channel Platform owner |
| Data integrity, storage, retention, or recovery | Data Platform owner |
| Identity, tenant isolation, credential, consent, or security signal | Security Platform owner |
| Broad operational impact, incident coordination, or customer support | Operations Platform owner |

The Agent Platform emits protected failure evidence and applies its immediate safe response before escalation. Multiple owners may be notified, but the escalation record identifies one accountable coordinator.

## Recovery Objectives

Critical failure categories have approved recovery-time and recovery-point objectives appropriate to business impact, tenant commitments, data classification, and external-action risk. Objectives define detection, containment, safe fallback, restoration, reconciliation, and communication expectations.

Failure-rate metrics alone are insufficient. Recovery evidence records elapsed time to containment, user-safe disposition, restoration, reconciliation, and closure, plus any unmet objective and follow-up action.

---

# Security and Tenant Controls

Tenant mismatch, missing tenant context, invalid authorization, revoked consent, classification violation, signature failure, secret exposure, prompt injection, and suspected cross-tenant access are security-relevant failures. They fail closed, preserve protected evidence, and follow the Security Model’s containment and escalation requirements.

Recovery, support, replay, dead-letter inspection, and operational override are separately authorized, tenant-scoped, purpose-bound, time-limited, and auditable. An operator’s broad role does not replace the original tenant and policy context.

Failure messages, retries, logs, and handoffs are redacted and classified. They must not include credentials, raw sensitive payloads, hidden instructions, private reasoning, or another tenant’s references.

---

# Observability, Analytics, and Learning

The platform emits failure category, severity, dependency, retry, fallback, handoff, recovery, reconciliation, user-impact, version/deployment, tenant, and correlation signals. It measures failure rate, retry exhaustion, circuit state, recovery time, duplicate prevention, handoff/fallback outcome, reconciliation delay, rollback/withdrawal, and recurrence.

Analytics and evaluation may identify patterns, but they cannot automatically change agent configuration, policy, deployment, or external behavior. Material recurring failures create an owned improvement item, evaluation update, dependency remediation, version change, or architecture decision through the established governance process.

---

# Testing Strategy

## Failure Contract Tests

Tests validate failure taxonomy, error categories, response records, retry eligibility, idempotency keys, state transitions, redaction, and correlation requirements.

## Resilience and Recovery Tests

Tests simulate dependency timeout, rate limit, provider outage, worker restart, duplicate request, delayed callback, ambiguous external outcome, invalid context, circuit opening/closing, replay, rollback, and withdrawal. They verify bounded recovery and no duplicate external action.

## Security and Tenant Tests

Tests simulate tenant mismatch, permission revocation, consent withdrawal, forged event, signature failure, secret leak, prompt injection, unauthorized dead-letter access, and operator recovery attempt. They verify fail-closed behavior and protected audit evidence.

## User-Impact Tests

Tests verify fallback wording/behavior, delivery restrictions, human handoff, deferred work, reconciliation, and the rule that unconfirmed action is never reported as completed.

---

## Recovery Exercises

High-risk dependencies, critical tools, tenant-isolation controls, replay paths, rollback/withdrawal actions, and user-impact communication paths are exercised on a recurring approved schedule. Exercises simulate realistic partial failure and verify detection, ownership, retry budget, fallback, reconciliation, evidence, and recovery objective behavior.

Findings create owned remediation, regression tests, runbook updates, or architecture decisions. An exercise is not complete merely because the dependency can be restarted.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Agent failure taxonomy registry | Defines category, severity, retry eligibility, owner, and safe response | Agent Platform with Security and Operations review |
| Failure code catalog | Defines stable code, meaning, retryability, disposition, user impact, owner, and escalation | Agent Platform with dependent owners |
| Failure response contract | Defines failure record, status, retry, fallback, handoff, and audit fields | Agent Platform |
| Retry, timeout, and circuit policy | Defines limits, idempotency, quotas, circuit thresholds, and recovery behavior | Agent Platform and Operations owner |
| Retry budget and storm-protection policy | Defines tenant/dependency budgets, priority, concurrency, exhaustion, and recovery controls | Agent, Operations, and dependent owners |
| Fallback and handoff catalog | Defines approved reduced behaviors, channel restrictions, context, and ownership | Agent Platform with Channel and Conversation owners |
| User-impact communication policy | Defines disposition, communication owner, allowed channel, wording, and handoff requirements | Agent, Channel, Conversation, and tenant owners |
| Reconciliation and replay procedure | Defines authoritative checks, authorization, side-effect safeguards, and evidence | Agent, Integration, and Operations owners |
| Data-integrity decision table | Defines confirmed, failed, unknown, reconciliation, and compensation behavior | Agent, Workflow, Integration, and Data owners |
| Failure escalation and recovery-objective matrix | Defines owner, coordinator, detection, containment, restoration, and communication objectives | Operations, Agent, and dependent owners |
| Failure-injection suite | Validates resilience, tenant isolation, security, recovery, and user impact | Agent Platform and Testing Platform |
| Recovery exercise schedule and report | Defines scope, cadence, findings, remediation, and closure evidence | Operations and Agent Platform |
| Failure-learning register | Tracks recurring failure, owner, improvement action, decision, and closure | Agent Platform and Operations owner |

---

# Anti-Patterns

## Retry Every Error

Retrying validation, policy, tenant, or business-rule failures wastes capacity and can create duplicate or unsafe action. Retry only verified transient and idempotent work.

## Report Success Before Confirmation

Telling a user that an appointment, payment, message, or record update succeeded before the authoritative outcome is known creates trust and business risk.

## Fallback to a Less Secure Channel

Moving restricted content from a secure interaction to email, messaging, or another channel by default can violate consent and classification controls.

## Replay Under Operator Context

Replaying tenant work using broad operational identity can bypass original policy. Replay must preserve and revalidate tenant scope and current authorization.

## In-Memory Recovery as Source of Truth

Resuming from transient runtime or prompt memory after failure can create inconsistent or duplicated work. Recover from durable state and reconcile uncertain external outcomes.

## Failure Logs With Secrets

Including credentials, raw sensitive content, hidden instructions, or private reasoning in error logs expands the incident. Use redacted references and protected evidence.

---

# Related Documents

| Document | Relationship |
|---|---|
| 07_AGENT_RUNTIME_ARCHITECTURE.md | Defines runtime recovery, cancellation, and execution boundaries. |
| 08_AGENT_EXECUTION_ENGINE.md | Defines controlled agent execution and outcome behavior. |
| 15_AGENT_TOOL_SYSTEM.md | Defines controlled tool selection and failure references. |
| 16_AGENT_TOOL_EXECUTION_MODEL.md | Defines tool execution, idempotency, and external-action controls. |
| 20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md | Defines Agent use of Integration-owned process compensation and business recovery outcomes. |
| 21_AGENT_EVENT_INTEGRATION.md | Defines event retry, dead-letter, replay, and delivery boundaries. |
| 22_AGENT_MULTI_CHANNEL_MODEL.md | Defines channel fallback, delivery, and handoff boundaries. |
| 24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md | Defines Agent application of security containment, data protection, and incident controls. |
| 25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md | Defines Agent enforcement of authorization required for recovery, replay, and override. |
| 26A_AGENT_TENANT_BOUNDARY_REWRITE_DRAFT.md | Requires tenant-safe failure, support, and recovery paths. |
| 27_AGENT_VERSIONING_MODEL.md | Defines version/dependency eligibility and controlled mitigation. |
| 28_AGENT_DEPLOYMENT_MODEL.md | Defines suspension, rollback, withdrawal, and stop conditions. |
| 29_AGENT_OBSERVABILITY_MODEL.md | Defines failure telemetry, diagnostic evidence, and alerts. |
| 31_AGENT_TESTING_STRATEGY.md | Defines failure injection, resilience, and regression testing. |
| 11_OPERATIONS_PLATFORM | Owns incident, on-call, and support operations. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Agent Failure Handling architecture document. |
| 2.1 | 2026-08-05 | Added failure codes, retry budgets, integrity decisions, escalation, communication, recovery objectives, exercises, and final artifacts. |

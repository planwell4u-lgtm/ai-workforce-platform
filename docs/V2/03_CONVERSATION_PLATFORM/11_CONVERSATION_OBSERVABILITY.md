# 11_CONVERSATION_OBSERVABILITY

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines how the Conversation Platform makes canonical conversation behavior observable across channels, participants, agents, workflows, queues, handoffs, state changes, events, and recovery.

Conversation observability answers operational questions without treating logs, dashboards, analytics, or traces as canonical conversation state. It provides trusted, tenant-safe evidence for experience quality, reliability, security, capacity, cost, and diagnosis.

---

# Purpose

The Conversation Observability Model establishes the domain signals, correlation rules, service objectives, alert conditions, dashboards, diagnostic workflow, and data-quality requirements needed to operate a multi-channel conversation platform safely.

It ensures a team can understand what happened to a conversation, identify degraded behavior early, investigate it with authorized evidence, and improve the system without leaking protected content or duplicating domain ownership.

---

# Objectives

The Conversation Observability Model must:

- Correlate conversation activity across interaction, participant, session, routing, handoff, agent, workflow, channel, event, delivery, and recovery boundaries.
- Define domain-level logs, metrics, traces, events, audit links, outcomes, and freshness indicators.
- Measure reliability, latency, continuity, ownership, handoff, state integrity, security, capacity, quality, and cost signals.
- Distinguish operational telemetry from canonical state, audit evidence, analytics data, and protected conversation content.
- Support tenant-safe, classification-aware, minimal, purpose-limited observation and investigation.
- Detect failures, backlogs, duplicate activity, stale projections, missing ownership, unsafe delivery, and integrity conflicts early.
- Provide service objectives and error-budget inputs without hard-coding a vendor, dashboard, or monitoring implementation.
- Preserve enough evidence to support incident response, reconciliation, support, and continuous improvement.

---

# Scope

This document defines Conversation Platform observability signals, correlation, telemetry semantics, service indicators/objectives, alerting requirements, dashboards, diagnostics, data quality, privacy, testing, and required artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Telemetry collectors, storage, dashboards, tracing backend, alert-routing tooling, log infrastructure, or on-call process implementation | 13_OBSERVABILITY_PLATFORM and 11_OPERATIONS_PLATFORM |
| Canonical conversation state, event schema, routing, handoff, context, session, or lifecycle behavior | Relevant Conversation Platform documents 02–10 |
| Agent reasoning trace, model evaluation, tool execution telemetry, or agent cost allocation | 02_AGENT_PLATFORM |
| Channel/media protocol telemetry, carrier/provider health, recording quality, or voice-quality implementation | 04_VOICE_PLATFORM and relevant Channel Platforms |
| Enterprise security monitoring, SIEM, compliance evidence store, or incident management policy | 09_SECURITY_PLATFORM and 11_OPERATIONS_PLATFORM |
| Data warehouse, long-term reporting, product analytics, billing, or data-retention implementation | 08_DATA_PLATFORM |
| Broker, connector, workflow engine, CRM, notification provider, or external-system telemetry implementation | 07_INTEGRATION_PLATFORM |

---

# Observability Principles

## Domain Evidence, Not a Second Source of Truth

Telemetry records observations about conversation operations. The canonical Conversation State and governed transition history remain authoritative for lifecycle, ownership, routing, handoff, participants, and recovery status.

## Correlation Is Required

Every material conversation operation carries the applicable conversation ID, tenant/environment, aggregate version, interaction/session/work-segment references, correlation and trace IDs, causation where applicable, channel, operation type, and outcome. A signal omits any identifier that is not needed for its purpose or not permitted by classification.

## Minimal and Protected Data

Routine telemetry excludes raw transcripts, recordings, attachments, credentials, participant addresses, unrestricted personal data, and private model reasoning. It uses controlled identifiers, categories, counts, durations, policy references, and protected content references where investigation requires more detail.

## Measure User-Meaningful Outcomes

The platform measures whether a participant interaction was accepted, safely routed, handled by an accountable owner, delivered or deferred with a known outcome, transferred safely, and closed or recovered correctly—not only whether a component returned an HTTP success.

## Designed for Failure and Change

Signals support retries, duplicates, delayed/out-of-order input, partial channel/provider failure, version change, tenant policy change, replay, recovery, and migration. A dashboard must expose uncertainty and data freshness rather than presenting stale derived data as final truth.

---

# Telemetry Model

## Signal Classes

| Signal class | Purpose | Conversation-domain examples |
|---|---|---|
| Structured operation log | Diagnostic record of a bounded operation and outcome | interaction normalization, state transition, routing decision, handoff acceptance, context issuance, delivery request |
| Metric | Aggregated measurement for health, capacity, quality, or cost | acceptance rate, time to owner, routing latency, queue wait, duplicate suppression, projection lag |
| Trace/span | Causal timing path across services | channel ingress to normalized interaction to state transition to agent/workflow request to delivery outcome |
| Governed conversation event | Durable fact for authorized consumers | interaction.accepted, routing.decided, handoff.activated, conversation.reconciliation_required |
| Audit evidence | Security/compliance record of an accountable access or action | protected context retrieval, export, repair approval, break-glass use |
| Derived operational view | Controlled queue, support, or reliability view | awaiting-owner work, expiring handoff offers, unresolved delivery outcomes |

A signal can link to another class but does not replace it. For example, a state transition creates history and may publish an event, emit a trace span, increment a metric, and produce audit evidence for a protected operation.

## Required Signal Attributes

| Attribute | Requirement |
|---|---|
| Identity and scope | Conversation ID where relevant; tenant, organization, environment, service/component, and operation category. |
| Correlation | Correlation ID, trace ID, causation ID where applicable, aggregate version, and interaction/session/work-segment/handoff references as needed. |
| Time | Occurred, recorded, started, ended, observed, and freshness time must be distinguishable when material. |
| Outcome | Accepted, rejected, deferred, queued, retried, delivered, failed, uncertain, reconciled, or other governed outcome/reason category. |
| Policy and integrity | Classification, policy/authorization result reference, idempotency result, source provenance, and state-version/guard result where needed. |
| Privacy | Minimum identifiers, data classification, access scope, redaction state, and no broad sensitive payload by default. |
| Versioning | Signal schema/version and producer version for contracts that evolve. |

## Cardinality and Telemetry Cost Controls

Conversation, participant, session, interaction, handoff, event, and trace identifiers may be used in protected structured logs and traces where investigation requires them. They must not become unrestricted metric labels, dashboard dimensions, or alert grouping keys.

The telemetry schema catalog defines permitted dimensions, aggregation level, sampling, retention class, query/access scope, and expected volume for every material signal. New high-cardinality or sensitive dimensions require explicit observability, privacy, and cost review. Aggregated metrics use governed categories such as channel, outcome, tenant tier, region, classification band, and error class rather than raw identifiers.

---

# Correlation and Journey Model

~~~text
Participant / Provider Input
    |
    v
Interaction Normalization
    |
    v
Canonical State and Lifecycle Transition
    |
    +--> Routing / Queue / Handoff
    |          |
    |          v
    |     Agent or Workflow Boundary
    |
    v
Approved Delivery / Deferred Outcome
    |
    v
Conversation Closure, Recovery, or Reconciliation
~~~

A trace can span this journey, but asynchronous work uses linked correlations rather than pretending one synchronous trace covers all elapsed time. The platform records the boundary and outcome of each stage, including waiting, queueing, timeout, retry, and handoff.

## Correlation Rules

- Conversation ID is the primary domain correlation key; provider, phone, email, browser, or channel-thread IDs are controlled mappings, not universal correlation keys.
- Interaction, session, work-segment, routing-decision, handoff, context-snapshot, event, and delivery references link their own bounded work to the conversation.
- Correlation does not grant access or permit cross-tenant joining.
- A derived view records source aggregate version, update time, and freshness status.
- Missing or invalid correlation is a diagnostic and, when material, security/reconciliation signal; it is not silently invented from untrusted content.

---

# Service Indicators and Objectives

Targets are set per tenant tier, channel, classification, region, and operating window. This document defines the indicator semantics; Operations sets approved target values and escalation policy.

| Indicator | Meaning |
|---|---|
| Valid interaction acceptance | Share of eligible inbound interactions normalized and durably accepted or given a safe explicit rejection/deferment. |
| Time to accountable owner | Time from accepted interaction to a recorded active owner or approved waiting state. |
| Response initiation latency | Time from a participant interaction becoming eligible to authorized response processing beginning. |
| Delivery outcome timeliness | Time from approved delivery request to recorded provider/channel outcome or controlled uncertainty. |
| Routing decision success | Share of routing requests reaching an eligible, explainable decision or safe no-route outcome. |
| Queue and handoff timeliness | Offer/queue-to-acceptance, activation, expiry, reassignment, and completion timing. |
| Conversation continuity | Successful approved continuation across channel/session changes without incorrect merge, split, or visibility exposure. |
| State integrity | Version conflict, duplicate suppression, stale mutation, reconciliation, and repair rates. |
| Projection freshness | Lag, invalidation, rebuild, and mismatch behavior for derived operational views. |
| Security control outcome | Denial, tenant mismatch, reference misuse, validation failure, revocation, break-glass, and quarantine rates. |
| Cost and capacity attribution | Conversation-domain volume, duration, queue pressure, event rate, and channel/agent/workflow consumption references; accounting implementation is owned elsewhere. |

## Error-Budget Inputs

A breach or sustained risk to a defined service objective triggers investigation and may restrict rollout, alter routing/fallback, reduce non-essential load, defer change, or require capacity/reliability work. Error budgets never justify bypassing authorization, consent, tenant isolation, or safe delivery controls.

---

# Alerts and Operational Views

## Alert Requirements

Alerts are actionable, deduplicated, tenant/classification-safe, correlated to an accountable operational owner, and include severity, affected scope, start time, current state, evidence references, customer-impact estimate, and recommended safe next step.

Alerts are required for at least:

- inability to record or read canonical state for material operations;
- sustained absence of accountable owner after accepted interaction;
- abnormal interaction rejection, normalization, routing, handoff, delivery, or authorization failure;
- elevated duplicate, stale-version, tenant mismatch, forged-input, or reference-integrity failure;
- queue/offer expiry, handoff failure, abandoned waiting work, or participant-impacting latency;
- event publication/consumption backlog, dead-letter growth, projection lag, cache inconsistency, or reconciliation backlog;
- increased uncertain provider outcome, failed revocation, break-glass use, or protected-data access anomaly.

## Required Operational Views

| View | Primary question |
|---|---|
| Conversation journey health | Are accepted interactions reaching safe ownership, response, delivery, and closure/recovery? |
| Channel and provider intake | Are inputs authenticating, normalizing, correlating, and being accepted safely by channel? |
| Routing, queue, and handoff | Is work reaching eligible owners with acceptable wait, expiry, failure, and return behavior? |
| State and event integrity | Are state transitions, outbox publication, consumers, projections, and reconciliation coherent and current? |
| Security and access | Are denials, mismatches, revocations, suspicious input, exports, and exceptional access within expected bounds? |
| Tenant and classification operations | Is impact isolated and understandable by authorized tenant, region, classification, and tier? |
| Recovery and change health | Are replays, repairs, migrations, deployments, and policy changes completing without increasing participant impact? |

---

# Instrumentation Coverage

Every material conversation transition and participant-impacting operation has a registered minimum signal set: operation outcome, domain correlation, timing, tenant/classification-safe scope, responsible producer, and failure/uncertainty reason where applicable.

The platform measures signal completeness, lateness, duplication, schema rejection, and correlation gaps by operation type and producer. A release or migration that changes a material journey must demonstrate required telemetry coverage, alert compatibility, and safe rollback visibility before activation.

---

# Diagnostics and Support Workflow

## Investigation Path

1. Confirm investigator identity, tenant scope, purpose, and required visibility.
2. Locate the canonical conversation through authorized identifiers and retrieve current state/version.
3. Follow correlation from accepted interaction through state, routing, handoff, execution boundary, delivery, and recovery evidence.
4. Distinguish observed telemetry from authoritative state and audit evidence.
5. Record diagnosis, impact, safe action, owner, and follow-up evidence through approved operational procedures.

A dashboard, search result, trace, or provider record cannot be used as authority to mutate state or disclose protected content.

## Sampling and Detail Escalation

Routine observability uses aggregate and minimized signals. Higher-detail investigation is time-bounded, tenant-scoped, purpose-bound, access-controlled, and audited. Sampling must not systematically hide security, high-risk, failed, or participant-impacting outcomes; exclusions and blind spots are documented.

---

# Data Quality, Privacy, and Retention

## Signal Quality

Each material signal has an owner, schema/version, expected producer, required attributes, permitted omission/redaction rules, validation, freshness expectation, and known limitations. Missing, malformed, delayed, duplicate, or inconsistent signals are measured and investigated.

## Observability Change Governance

New or changed signals, dimensions, dashboards, service indicators, alert rules, sampling, retention classes, and access views have a recorded owner, purpose, privacy/classification review, cardinality and cost assessment, schema compatibility decision, consumer impact, test evidence, and rollback plan.

Changes must not expose protected data, silently alter an established indicator definition, or make a material alert less actionable without approved Operations and Security review where applicable.

## Retention and Access

Retention, deletion, anonymization, residency, legal hold, and access implementation are owned by Data and Security Platforms. Conversation observability supplies the domain classification, purpose, correlation, and lifecycle references required to apply those controls.

Historical telemetry and traces never override current participant visibility, consent, classification, or authorization. A retained correlation may remain only as policy permits, while protected content references can become unavailable, redacted, or restricted.

---

# Testing Strategy

## Signal Contract Tests

Validate signal names, owners, schema/version, required attributes, outcome/reason categories, correlation, privacy classification, redaction, and compatibility.

## Journey and Failure Tests

Validate end-to-end correlation across accepted interaction, duplicate/provider retry, routing, queue, handoff, agent/workflow boundary, approved delivery, timeout, reconciliation, and closure. Validate that material success, failure, deferment, and uncertainty are observable.

## Synthetic and Canary Journeys

Controlled synthetic or canary journeys exercise critical approved paths at a governed interval: channel intake to safe ownership, authorized response/delivery outcome, queue/handoff activation, and recovery from a known safe failure. They use dedicated tenant, participant, content, and destination controls; they must not contact real participants, distort tenant reporting, or bypass normal authorization.

## Security and Data-Quality Tests

Simulate cross-tenant query, unauthorized dashboard/view, sensitive-content leakage, stale projection, missing correlation, malformed signal, sampling blind spot, telemetry pipeline delay, dropped event, clock skew, provider outage, break-glass investigation, and retention/redaction change. Prove investigation remains safe and does not depend on telemetry as authoritative state.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Conversation telemetry schema catalog | Defines signal classes, names, owners, attributes, privacy, versions, and compatibility | Conversation Platform with Observability owner |
| Correlation and journey contract | Defines identifiers, async links, timing semantics, freshness, and permitted joins | Conversation Platform with Channel, Agent, Integration, and Observability owners |
| Conversation service-indicator catalog | Defines calculations, dimensions, exclusions, data-quality expectations, and target ownership | Conversation Platform with Operations owner |
| Alert and operational-view specification | Defines conditions, severity, ownership, evidence, safe actions, and authorized views | Conversation Platform with Operations, Security, and Observability owners |
| Telemetry coverage and change policy | Defines minimum signals, completeness checks, dimension/cost controls, review, compatibility, and rollback | Conversation Platform with Observability, Security, and Operations owners |
| Synthetic journey specification | Defines approved canaries, safe test scope, expected evidence, frequency, and failure handling | Conversation Platform with Testing, Channel, and Operations owners |
| Diagnostic and detail-escalation procedure | Defines investigation access, evidence hierarchy, sampling, audit, and support boundary | Conversation Platform with Security and Operations owners |
| Observability data-quality test suite | Validates contracts, journeys, privacy, resilience, and signal completeness | Conversation Platform with Testing Platform |

---

# Anti-Patterns

## Dashboard Is the Source of Truth

Telemetry is evidence. Canonical state and transition history decide current conversation ownership, lifecycle, and repair outcome.

## HTTP Success Means Participant Success

A technical response does not prove an interaction was accepted, safely owned, delivered, or recovered. Measure the end-to-end domain outcome.

## One Trace Pretends to Cover Asynchronous Work

Queueing, handoff, waiting, callback, and replay work must use linked correlations and explicit timing boundaries.

## Raw Transcript in Every Log

Routine logs and metrics use minimum information. Protected content is retrieved only through authorized, audited paths when necessary.

## Aggregate Metrics Hide Tenant Harm

Platform-wide averages can hide a tenant, region, channel, or classification incident. Use authorized dimensions and outlier-aware views.

## Alert Has No Owner or Safe Action

An alert that cannot be safely acted upon creates noise and risk. Every material alert needs an accountable owner and response path.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_CONVERSATION_ARCHITECTURE.md | Defines Conversation Platform components and operational boundaries. |
| 02_CONVERSATION_LIFECYCLE.md | Defines lifecycle outcomes and timing states. |
| 03_CONVERSATION_MODEL.md | Defines entity references used for correlation. |
| 04_CONVERSATION_SESSION_MODEL.md | Defines session continuity and execution links. |
| 05_CONVERSATION_CONTEXT_MODEL.md | Defines context issuance, expiry, and access evidence. |
| 06_CONVERSATION_ROUTING.md | Defines routing decisions, ownership, and fallback outcomes. |
| 07_CONVERSATION_EVENTS.md | Defines durable event contracts and consumer telemetry context. |
| 08_CONVERSATION_HANDOFF_MODEL.md | Defines transfer, queue, acceptance, and return outcomes. |
| 09_CONVERSATION_STATE_MANAGEMENT.md | Defines authoritative state, projection freshness, and reconciliation. |
| 10_CONVERSATION_SECURITY.md | Defines authorization, audit, security signals, and incident boundaries. |
| 02_AGENT_PLATFORM | Defines agent execution, evaluation, tool, and model observability. |
| 04_VOICE_PLATFORM | Defines voice/channel media and provider telemetry. |
| 13_OBSERVABILITY_PLATFORM | Defines shared telemetry implementation and operating model. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-06 | Initial Conversation Observability document. |
| 2.1 | 2026-08-06 | Added telemetry cardinality controls, instrumentation coverage, observability change governance, and synthetic journey requirements. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |

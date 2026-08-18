# 12_CONVERSATION_TESTING

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines how the Conversation Platform is verified as a canonical, multi-channel coordination layer for conversations, participants, interactions, sessions, context, routing, handoff, state, events, security, observability, and recovery.

Conversation testing proves domain behavior and safety at platform boundaries. It does not rely only on component success, vendor sandbox results, or happy-path end-to-end demonstrations.

---

# Purpose

The Conversation Testing Strategy provides a risk-based, repeatable approach for showing that the platform preserves continuity, tenant isolation, correct ownership, authorized access, reliable delivery outcomes, and recoverable state under normal and adverse conditions.

It connects architecture contracts to executable tests, release evidence, operational readiness, and long-term regression protection.

---

# Objectives

The Conversation Testing Strategy must:

- Validate the Conversation Platform's canonical ownership, boundaries, contracts, and invariants.
- Prove correct behavior across supported channels, participants, agents, workflows, queues, human operators, and external events.
- Detect regression in lifecycle, state, routing, handoff, context, authorization, tenant isolation, delivery, and recovery behavior.
- Exercise duplicate, delayed, out-of-order, failed, replayed, stale, concurrent, and uncertain conditions.
- Use safe, representative, classification-aware test data and controlled external dependencies.
- Produce traceable evidence for releases, high-risk changes, incidents, migrations, and compliance review.
- Keep domain test intent stable while allowing implementation, vendor, test framework, and deployment tooling to evolve.
- Prevent tests from becoming a source of tenant leakage, participant contact, data corruption, or ungoverned external side effects.

---

# Scope

This document defines Conversation Platform test levels, contract coverage, scenario coverage, test data, environments, quality gates, resilience/security testing, observability validation, release evidence, and required artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Shared test framework, CI/CD runner, test environment provisioning, test-result storage, or test-management tooling | 14_TESTING_PLATFORM, 12_DEPLOYMENT_PLATFORM, and 11_OPERATIONS_PLATFORM |
| Agent model evaluation, prompt testing, tool execution testing, safety evaluation, or agent-runtime benchmark methodology | 02_AGENT_PLATFORM |
| Voice/media quality, telephony/carrier certification, device/browser compatibility, or channel-provider protocol certification | 04_VOICE_PLATFORM and relevant Channel Platforms |
| Database engine, backup, migration tooling, or data-storage implementation testing | 08_DATA_PLATFORM and 12_DEPLOYMENT_PLATFORM |
| Enterprise penetration testing, vulnerability management, identity-provider testing, or organization-wide compliance audit | 09_SECURITY_PLATFORM |
| Connector, CRM, ticketing, workflow-engine, MCP, broker, or third-party integration implementation testing | 07_INTEGRATION_PLATFORM |
| Operational incident process, deployment approval, release calendar, or production change-management process | 11_OPERATIONS_PLATFORM and 12_DEPLOYMENT_PLATFORM |

---

# Testing Principles

## Test the Canonical Contract

Tests validate that Conversation Platform remains the authoritative owner of conversation state, lifecycle, participant relationships, routing/handoff references, and domain events. A provider thread, agent runtime, queue, cache, event consumer, or dashboard must never become an alternate source of truth.

## Test Meaningful Outcomes

Tests assert domain outcomes: accepted interaction, safe rejection/deferment, recorded active owner or waiting state, authorized context availability, correct handoff transfer, controlled delivery outcome, durable event, and recoverable failure. They do not stop at HTTP success, a queued job, or a component mock assertion.

## Test Boundaries, Not Assumptions

Each boundary uses an explicit contract: channel input, agent/workflow request, context/handoff grant, routing decision, state transition, event, delivery outcome, projection, or operational action. Tests must not depend on undocumented internal state or vendor-specific behavior.

## Test Failure as a First-Class Path

Every material journey has tests for duplicate, retry, delay, ordering, stale version, timeout, cancellation, unavailable dependency, partial persistence, authorization change, and uncertain external outcome where applicable.

## Test with Safe Data and Effects

Tests use dedicated tenant/environment scope, synthetic identities, approved fixtures, controlled destinations, and side-effect guards. They do not contact real participants, use production credentials, access unrelated tenant data, or create irreversible external actions.

## Test Evidence Is a Contract

Test results record the contract/scenario version, environment, build/release reference, fixture version, relevant dependency version, execution time, outcome, exclusions, and links to diagnostics. A passing result is meaningful only for the stated scope and evidence.

---

# Test Coverage Model

| Level | Purpose | Conversation examples |
|---|---|---|
| Unit and domain rule | Validate deterministic logic and invariants in isolation. | lifecycle guards, reason-code validation, idempotency key rules, visibility checks, state-transition guards. |
| Contract | Validate published/consumed interfaces and compatibility. | command/event schema, context/handoff grant, channel normalization, routing decision, projection contract. |
| Component integration | Validate collaboration with controlled real dependencies or faithful test doubles. | state/outbox, authorization decision, cache invalidation, event consumer, queue assignment, delivery adapter. |
| Journey integration | Validate a complete domain journey across owned platform boundaries. | inbound interaction to owner to response/delivery; agent-to-human handoff; channel continuation; closure/recovery. |
| End-to-end controlled | Validate approved external/channel paths in a dedicated non-production scope. | signed provider callback to normalized interaction; controlled outbound delivery confirmation. |
| Resilience and chaos | Validate behavior under degraded, failed, duplicate, delayed, and partial conditions. | provider outage, consumer restart, stale projection, state conflict, lost acknowledgement, replay. |
| Security and privacy | Validate denial, isolation, minimization, revocation, abuse, and audit behavior. | cross-tenant request, restricted context, revoked consent, forged callback, unsafe export. |
| Performance and capacity | Validate domain behavior at expected and constrained volume. | concurrent turns, routing/queue pressure, handoff burst, event backlog, projection rebuild. |
| Production-safe validation | Validate live configuration and observability without participant impact. | synthetic canary, readiness check, schema compatibility, alert exercise. |

The required mix is risk-based. A low-risk internal wording change does not need the same coverage as a new channel, state transition, handoff path, authorization rule, or participant-facing delivery capability.

---

# Change-Risk and Evidence Matrix

The change owner classifies the highest applicable risk before release. The matrix establishes minimum evidence; a tenant, classification, safety, incident, or operational condition may require stronger coverage.

| Change class | Examples | Minimum evidence |
|---|---|---|
| Low-risk internal | Non-behavioral refactor, documentation, isolated observability wording. | Relevant unit/contract validation, static checks, and review evidence. |
| Configuration or policy | Routing threshold, queue configuration, feature setting, allowed channel scope. | Affected contract/integration tests, policy guard tests, rollback/feature-control evidence, and observability check. |
| Contract or state evolution | Event, command, context, handoff, state aggregate, projection, or schema change. | Backward/forward compatibility tests, producer/consumer contract tests, migration/rebuild evidence, and dependent-owner approval. |
| New or materially changed journey | Channel path, delivery flow, handoff mode, workflow boundary, participant experience. | Controlled journey and external-boundary tests, adverse-path coverage, synthetic/canary plan, alert/diagnostic evidence, and rollback plan. |
| High-risk security or participant impact | Authorization, identity/continuity, export, sensitive context, tenant isolation, legal/retention, or break-glass change. | Security/privacy tests, adversarial and revocation coverage, Security approval, controlled release plan, and enhanced operational readiness evidence. |

---

# Requirement and Contract Traceability

Every material conversation requirement, invariant, transition, event, authorization rule, and recovery path has a traceable test identifier or approved documented rationale for exclusion.

~~~text
Architecture Requirement / Invariant
    |
    v
Contract or Scenario Identifier
    |
    v
Test Level and Fixture
    |
    v
Execution Evidence and Diagnostics
    |
    v
Release / Change Decision
~~~

Traceability covers both positive and negative cases. A requirement that intentionally cannot be automated has an owner, reason, manual procedure, review cadence, and recorded evidence.

## Compatibility Evidence

For every changed state, command, event, context, routing, handoff, channel, or projection contract, tests prove the declared support policy. This includes supported older consumers reading a newer producer, a newer consumer handling supported older producer data, additive optional fields, unknown-field handling where applicable, deprecation behavior, and migration/retirement conditions.

A compatibility test uses representative versioned fixtures and identifies the producer and consumer versions under test. It must not assume that a shared code deployment proves independent consumer compatibility.

---

# Core Scenario Catalog

## Lifecycle and State

- Create, activate, wait, resume, hand off, suspend, close, archive, reopen where policy permits, retain, delete/anonymize, and legal-hold behavior.
- Guard failure for invalid, stale, duplicate, out-of-order, or unauthorized transition.
- Aggregate version advancement, immutable history, idempotency, repair, migration, reconstruction, and projection rebuild.
- One active owner or approved waiting state for each work segment.

## Participants, Identity, and Channels

- Participant creation/association, visibility change, verification/assurance update, removal, consent change, and multi-party behavior.
- Approved channel mapping and continuity across voice, chat, messaging, email, API, and future channels.
- Language, locale, timezone, accessibility preference, and channel-capability changes without unsafe identity, visibility, ownership, or delivery assumptions.
- Rejection of spoofed, unverified, cross-tenant, stale-session, mismatched-recipient, or unsafe cross-channel continuation.
- Provider authenticity, replay, timestamp, schema, normalization, correlation, and duplicate handling.

## Context, Routing, and Handoff

- Context selection, provenance, minimization, expiry, revocation, redaction, consent change, and restricted retrieval.
- Routing eligibility, precedence, no-route, fallback, capacity, queue, expiry, re-routing, and one response owner.
- Agent-to-human, human-to-agent, agent-to-agent, workflow, queue, supervisor, warm/cold, return, timeout, reassignment, and failed handoff.
- Safe disposition of in-flight agent/workflow/tool/delivery work at ownership transfer.

## Events, Delivery, and Integration Boundaries

- Durable state/outbox behavior; event naming, envelope, schema, classification, version, authorization, idempotency, ordering, retry, dead-letter, replay, and reconciliation.
- Approved delivery request, provider result, uncertain outcome, retry safety, participant notification, and no duplicate participant-facing action.
- Controlled request boundaries for Agent, Channel, Integration, Data, Security, Observability, and Operations consumers.

## Security, Privacy, and Governance

- Deny-by-default authorization; tenant/environment isolation; purpose binding; least privilege; separation of duties; delegated/support access; and break-glass controls.
- Context/handoff grant restriction, participant visibility, classification, retention, residency, legal hold, export/disclosure, audit, and revocation.
- Forged/replayed input, prompt injection as untrusted content, reference misuse, suspicious continuity, abuse control, policy unavailability, and security incident quarantine.

## Observability and Operations

- Required logs/metrics/traces/events/audit links, correlation, schema/version, minimization, redaction, cardinality, freshness, coverage, alerts, operational views, and diagnostic access.
- Synthetic/canary journeys, alert actionability, telemetry failure, sampling blind spot, clock skew, missing correlation, and safe investigation.
- Reconciliation backlog, repair approval, safe retry, migration evidence, rollback visibility, and incident handoff.

---

# Test Data and Fixture Governance

## Dedicated Test Scope

All tests run within a dedicated test tenant and environment unless a controlled production-safe validation explicitly says otherwise. Fixtures use synthetic participants, addresses, recordings, documents, attachments, identifiers, and content approved for their classification.

## Fixture Properties

Fixtures are versioned, minimal, deterministic where possible, provenance-recorded, expiry/retention-managed, and safely reusable. They include normal, boundary, malformed, adversarial, duplicate, delayed, out-of-order, redacted, restricted, multi-party, multi-channel, and migration cases.

## Sensitive and Production Data

Production conversation data is not used by default. Any exception requires documented purpose, minimization, authorization, approved secure environment, access control, retention/deletion plan, and Security/Data owner approval. Test output must not expose protected production content.

## External Side-Effect Controls

External adapters use test accounts, allowlisted destinations, sandboxes, simulators, or controlled stubs. Tests prove idempotency and failure behavior without sending repeated messages, creating real tickets, making charges, or contacting non-test users.

---

# Environment and Dependency Strategy

| Environment class | Purpose | Requirements |
|---|---|---|
| Local/isolated | Fast deterministic domain and contract feedback. | Synthetic fixtures, controlled clocks, fakes/stubs, no external side effects. |
| Shared integration | Validate owned components and selected dependencies. | Tenant isolation, versioned contracts, reset/rebuild capability, controlled identities and destinations. |
| Pre-production journey | Validate representative multi-service/channel paths. | Production-like policy/configuration where safe, dedicated provider accounts, observability, rollback, and controlled data. |
| Production-safe validation | Detect live configuration or integration regressions without participant impact. | Approved canaries/readiness checks, explicit scope, no real participant data/actions, alerting, rollback, and audit. |

A dependency test double must represent the contract and documented failure modes relevant to the scenario. Critical provider paths also receive controlled real-integration coverage before release.

---

# Resilience, Performance, and Recovery Testing

## Resilience

Test dependency timeout, retry/backoff, restart, duplicate callback/event, delayed/out-of-order input, partial persistence, outbox delay, consumer failure, cache loss, projection lag, provider uncertainty, queue saturation, receiver disconnect, and failover behavior.

Expected outcomes preserve canonical state, tenant isolation, idempotency, active ownership, and controlled recovery. Tests must prove that retries do not duplicate participant-facing delivery, handoff, workflow, tool action, or external side effect.

## Performance and Capacity

Load tests exercise realistic channel mix, concurrent conversations/turns, routing and queue pressure, event volume, projection rebuild, handoff burst, and degraded dependency conditions. They measure domain indicators such as time to accountable owner, routing/activation latency, delivery outcome timeliness, conflict rate, backlog, and tenant fairness.

Capacity limits, safe degradation, quota behavior, admission control, and fallback are verified at stated operating tiers. A performance test may not use production participants or remove tenant/security controls to reach volume.

## Recovery and Migration

Test state reconstruction, projection rebuild, event replay, dead-letter handling, reconciliation, repair, policy change, schema evolution, aggregate compatibility, deployment rollback, and approved tenant/environment migration.

A recovery test verifies current authorization, consent, retention, legal hold, classification, residency, idempotency, and external-side-effect checks rather than assuming historical data can be replayed unchanged.

---

# Security and Privacy Testing

Security tests are run throughout development and release, not only as a final gate. They validate threat/control mapping from 10_CONVERSATION_SECURITY.md and include:

- authentication, authorization, purpose, tenant, environment, participant visibility, and session/device binding;
- cross-tenant and cross-participant isolation;
- forged provider/webhook input, replay, malformed data, injection, reference guessing, and confused-deputy attempts;
- consent withdrawal, revocation, expiry, retention, redaction, deletion/anonymization, legal hold, and residency restrictions;
- handoff/context minimization, delegated support, export/disclosure, break-glass, audit, abuse safeguards, and incident quarantine;
- test-data and telemetry safety.

Security findings are triaged through the Security Platform's vulnerability and incident processes. No production exploitation is performed without explicit approved authorization and scope.

---

# Quality Gates and Release Evidence

## Minimum Gates

A release affecting Conversation Platform must have:

1. passing applicable unit/domain, contract, integration, and risk-selected journey tests;
2. no unresolved high-severity defect, security finding, integrity defect, or known participant-impacting regression without an approved exception;
3. compatibility evidence for changed state, event, context, handoff, routing, or channel contracts;
4. required authorization/tenant-isolation, duplicate/retry, and recovery coverage for affected material paths;
5. observability coverage, alert/view compatibility, and diagnostic evidence for the changed journey;
6. controlled external/channel verification when an affected provider path is material;
7. rollback, migration, feature-control, and operational-owner evidence appropriate to the change.

## Exception Process

A gate exception has named accountable owner, scope, risk, rationale, compensating controls, tenant/participant impact assessment, expiry, rollback or remediation plan, required approvals, and follow-up verification. An exception never permits bypass of tenant isolation, authorization, consent, legal hold, or explicit safety controls.

---

# Defect, Regression, and Incident Learning

A defect records the affected contract/scenario, tenant/classification impact, reproduction path, expected/actual domain outcome, diagnostics, severity, owner, fix evidence, and regression test.

After a material incident, review determines whether architecture contract, observability, fixture, test case, quality gate, runbook, or platform boundary needs improvement. The resulting action has an owner and verification evidence; the incident is not considered fully learned from until the appropriate regression or readiness test exists.

---

# Testing Metrics

Testing metrics track contract/scenario coverage, pass/fail/flake rate, execution duration, defect escape, regression recurrence, time to diagnose, release-gate exceptions, recovery exercise outcome, test-data policy exceptions, and coverage of high-risk paths.

Metrics are used to improve confidence and test design, not to claim correctness solely from a percentage. Coverage gaps, manually tested controls, untested combinations, known environment limits, and flaky tests remain visible to release decision-makers.

---

# Test-Result Integrity

Test suites use controlled clocks, deterministic seeds, stable fixtures, and isolated state where practical. Each run identifies fixture, dependency, configuration, contract, and environment versions so an outcome can be reproduced or its limits understood.

A flaky, quarantined, skipped, inconclusive, or environmentally blocked test is reported separately from a pass. It cannot silently satisfy a quality gate. Its owner, impact, workaround, expiry, and remediation path are recorded; high-risk-path flakiness requires an approved exception or alternative reliable evidence.

Fixture cleanup, test-tenant reset, controlled external-effect verification, and retention handling are checked after relevant runs. A failed cleanup or unexpected external effect is treated as a test and security/operations finding, not routine noise.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Conversation test catalog and traceability matrix | Maps requirements, invariants, contracts, scenarios, risks, tests, exclusions, and evidence | Conversation Platform with Testing owner |
| Contract and compatibility suite | Validates commands, events, context, handoff, routing, state, channel, and projection contracts | Conversation Platform with dependent platform owners |
| Change-risk and compatibility matrix | Defines release evidence by change class and supported producer/consumer version combinations | Conversation Platform with Testing, Security, and Operations owners |
| Multi-channel journey suite | Validates controlled end-to-end continuity, ownership, delivery, and recovery across supported channels | Conversation Platform with Channel, Agent, and Integration owners |
| Security and privacy suite | Validates domain threat controls, isolation, revocation, minimization, and audit | Conversation Platform with Security owner |
| Resilience, performance, and recovery suite | Validates adverse conditions, capacity, reconstruction, replay, reconciliation, repair, migration, and rollback | Conversation Platform with Data, Operations, and Testing owners |
| Test-data and external-effect policy | Defines fixtures, classification, access, retention, test destinations, sandbox/stub use, and cleanup | Conversation Platform with Data, Security, and Integration owners |
| Release-evidence and exception template | Defines quality gates, approvals, diagnostics, compatibility, observability, rollback, and exception expiry | Conversation Platform with Operations, Deployment, and Testing owners |

---

# Anti-Patterns

## Happy Path Only

A successful inbound message and response does not prove the platform handles retries, concurrent ownership, handoff, revocation, or external uncertainty safely.

## Provider Sandbox Is the Whole Test Plan

A sandbox validates only part of a channel boundary. Domain contracts, security, state, recovery, and adverse conditions need their own coverage.

## Mock Proves the Contract

A mock can prove local behavior but not a real producer/consumer compatibility claim. Material contracts need shared schema and controlled integration tests.

## Test Fixture Is a Production Export

Production data is not a convenient fixture source. Use synthetic, minimized, governed data and approved exceptions only.

## Test Retries Create Real Side Effects

Tests must use controlled destinations and prove idempotency without repeatedly contacting users or changing external business systems.

## Passing Percentage Means Safe Release

Coverage percentages cannot replace risk-based evidence, security review, recovery tests, observability, and accountable release decisions.

## Fix Has No Regression Test

A defect or incident that changes domain behavior must produce durable regression coverage or a documented, owned reason why it cannot.

---

# Related Documents

| Document | Relationship |
|---|---|
| 00_CONTROL/AI_DEVELOPMENT_GUIDE.md | Defines project-wide engineering and validation expectations. |
| 01_CONVERSATION_ARCHITECTURE.md | Defines platform components and boundaries under test. |
| 02_CONVERSATION_LIFECYCLE.md | Defines lifecycle requirements and transition tests. |
| 03_CONVERSATION_MODEL.md | Defines entities, relationships, and contract fixtures. |
| 04_CONVERSATION_SESSION_MODEL.md | Defines session continuity and recovery tests. |
| 05_CONVERSATION_CONTEXT_MODEL.md | Defines context authorization, lifecycle, and safety tests. |
| 06_CONVERSATION_ROUTING.md | Defines routing, ownership, fallback, and capacity tests. |
| 07_CONVERSATION_EVENTS.md | Defines event contract, replay, and consumer tests. |
| 08_CONVERSATION_HANDOFF_MODEL.md | Defines transfer, collaboration, timeout, and return tests. |
| 09_CONVERSATION_STATE_MANAGEMENT.md | Defines state integrity, concurrency, reconstruction, and repair tests. |
| 10_CONVERSATION_SECURITY.md | Defines threat/control, authorization, isolation, and revocation tests. |
| 11_CONVERSATION_OBSERVABILITY.md | Defines signal coverage, synthetic, alert, and diagnostic tests. |
| 14_TESTING_PLATFORM | Defines shared test tooling and platform-wide test governance. |
| 02_AGENT_PLATFORM | Defines agent-specific test, evaluation, and execution coverage. |
| 04_VOICE_PLATFORM | Defines voice and channel-specific test coverage. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-06 | Initial Conversation Testing Strategy document. |
| 2.1 | 2026-08-06 | Added change-risk evidence, compatibility, inclusive multi-channel, and test-result integrity requirements. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |

# 31_AGENT_TESTING_STRATEGY

**Version:** 2.2  
**Status:** Approved  
**Phase:** Agent Platform

---

# Overview

This document defines how the Agent Platform is tested to prove that agents behave as approved, remain secure and tenant-isolated, use tools and workflows safely, work consistently across channels, and can evolve without regressions.

Agent testing validates the complete controlled path from an authorized trigger to an observable outcome. It combines deterministic contract and policy tests with controlled evaluation of non-deterministic model behavior.

---

# Purpose

The purpose of the Agent Testing Strategy is to establish a repeatable, risk-based testing model for agent configuration, runtime execution, context, permissions, tools, workflows, events, deployments, and user-facing outcomes.

It defines the Agent Platform test obligations and evidence required before release. The Testing Platform owns shared testing infrastructure, organization-wide quality standards, test environments, and execution services.

---

# Objectives

The Agent Testing Strategy must:

- Validate functional behavior, policy compliance, security, tenant isolation, reliability, and user-impact outcomes.
- Test deterministic controls separately from probabilistic model behavior.
- Protect customer data, secrets, and privacy in test data, prompts, fixtures, and results.
- Provide regression protection for agent versions, dependencies, tools, workflows, channels, and deployments.
- Support unit, contract, integration, evaluation, resilience, security, performance, and production-verification testing.
- Tie test depth and release evidence to agent risk, capability, data classification, and external-action impact.
- Produce traceable evidence linking requirements, version, test cases, results, exceptions, and release decisions.
- Remain independent of a specific framework, model provider, test runner, or CI vendor.

---

# Scope

This document defines:

- Agent Platform test layers, test types, environments, data controls, and release evidence.
- Required testing for agent versions, runtime, context, policy, permissions, tools, workflows, events, channels, deployment, and observability.
- Risk-based coverage, regression, failure injection, production verification, and test governance.
- Agent-specific test artifacts and ownership boundaries.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Shared test framework, runner, CI infrastructure, test environment provisioning, and enterprise quality policy | 14_TESTING_PLATFORM and 20_ENGINEERING |
| Quality rubric, benchmark design, model scoring, and evaluation methodology | 33_AGENT_EVALUATION_FRAMEWORK |
| Production monitoring, incident response, and operational alerting | 11_OPERATIONS_PLATFORM and 13_OBSERVABILITY_PLATFORM |
| Security policy, penetration-test program, compliance, and enterprise threat model | 09_SECURITY_PLATFORM and Agent Security Model |
| Channel provider certification, telephony media test harnesses, or provider sandboxes | Relevant Channel and Voice Platforms |
| Data anonymization service, warehouse testing, and data-retention implementation | 08_DATA_PLATFORM and Security Platform |

---

# Testing Principles

## Test the Boundary, Not Just the Prompt

A well-written prompt is not proof of correct behavior. Tests validate deterministic boundaries around model behavior: authorization, tenant scope, context access, capability eligibility, parameter validation, tool execution, workflow transitions, delivery, and audit.

## Separate Deterministic and Probabilistic Expectations

Deterministic controls use exact expected assertions. Model behavior uses approved rubrics, structured assertions, bounded scenarios, multiple runs where appropriate, and evaluation thresholds. The platform does not require identical wording when it requires correct intent, safety, or outcome.

## Risk-Based Depth

High-risk actions, sensitive data, external side effects, financial or regulated operations, and tenant-administration controls require stronger test evidence, independent review, failure injection, and release approval than low-risk informational behavior.

## Test With Safe Representative Data

Test fixtures are synthetic, anonymized, or explicitly authorized. Production customer data, credentials, secrets, private prompts, recordings, and regulated content are not copied into general test suites.

## Evidence Is Versioned

A test result records the agent version, manifest digest, dependency versions, environment, fixture set, test definition, evaluator/rubric version where applicable, time, outcome, and exception reference. Evidence is not reused when a material dependency changes.

## Shift Left and Verify in Production

Tests run as early as possible in draft and integration environments, but safe post-deployment verification is required because channels, providers, configuration, capacity, and real operational dependencies can differ from test conditions.

---

# Test Architecture

~~~text
Draft and Component Tests
    |
    v
Contract and Policy Tests
    |
    v
Integration and End-to-End Tests
    |
    v
Evaluation, Security, Resilience, and Performance Tests
    |
    v
Release Readiness Decision
    |
    v
Safe Production Verification and Continuous Regression
~~~

## Test Layers

| Layer | Primary purpose |
|---|---|
| Unit | Validate isolated deterministic components, transformations, and rule logic |
| Contract | Validate schemas, API/event behavior, version compatibility, and boundary obligations |
| Policy | Validate authorization, consent, classification, tenant scope, approval, and deny behavior |
| Integration | Validate interactions among runtime, context, tools, workflows, events, channels, and dependencies |
| End-to-end | Validate an approved user or event journey through controlled outcomes |
| Evaluation | Assess model behavior against approved quality, safety, and task rubrics |
| Resilience | Validate retries, idempotency, recovery, degradation, replay, and failure handling |
| Security | Validate identity, access, isolation, injection resistance, secrets protection, and abuse controls |
| Performance | Validate latency, concurrency, capacity, quota, and dependency behavior |
| Production verification | Confirm a deployed assignment works safely in its actual target environment |

## Test Case Lifecycle

```text
Draft
    -> Reviewed
    -> Approved
    -> Active
    -> Deprecated
    -> Retired
```

Every active test case has a stable identifier, requirement/risk trace, owner, scope, fixture reference, expected outcome, evaluation method, environment eligibility, and review date. A deprecated case remains historically traceable but is labeled with its replacement or retirement reason.

---

# Required Test Domains

## Agent Definition and Version

Tests validate manifest completeness, immutable versioning, dependency pinning, compatibility, change classification, release eligibility, experiment assignment, rollback eligibility, and execution-version provenance.

## Runtime and Context

Tests validate trigger handling, version resolution, session/context boundaries, context minimization, source authorization, execution pinning, cancellation, expiry, worker reuse, and recovery after restart.

## Instructions, Capabilities, and Model Behavior

Tests validate instruction authority, expected capability selection, refusal behavior, safe response constraints, model fallback, structured output validation, and prevention of untrusted content overriding approved controls.

## Permission, Security, and Tenant Isolation

Tests validate subject/workload identity, action/resource scope, deny precedence, delegation, approval, revocation, cross-tenant access prevention, session fixation, event integrity, prompt injection, data exfiltration, secret redaction, and diagnostic access.

## Tools and Workflows

Tests validate capability-to-tool authorization, tool parameter constraints, idempotency, external-action approval, workflow initiation, state transitions, compensation, retries, failure handling, and audit correlation.

## Events, Channels, and Delivery

Tests validate event schemas, subscription filters, duplicate/out-of-order delivery, channel normalization, identity/consent checks, response adaptation, delivery authorization, provider callbacks, fallback, and human handoff.

## Deployment and Observability

Tests validate readiness checks, target assignment, channel eligibility, stop conditions, activation, suspension, rollback, withdrawal, trace propagation, telemetry redaction, SLI/SLO calculation, and alert input signals.

---

# Test Data and Environment Controls

## Fixture Classes

| Fixture class | Use | Control |
|---|---|---|
| Synthetic | Default functional, policy, and regression tests | Generated, non-production, versioned |
| Anonymized | Realistic patterns where authorized | Re-identification review, restricted access, retention limit |
| Provider sandbox | Channel, tool, and integration validation | Isolated account, test credentials, quota and cleanup controls |
| Controlled production verification | Post-deployment smoke checks | Minimal scope, authorized tenant, no unsafe external side effect |

## Environment Separation

Development, test, staging, preview, and production verification environments use isolated tenants, credentials, integrations, channels, data, and observability. Tests must not reach production systems unless an explicit controlled verification policy permits it.

## Fixture Lifecycle

Fixtures include tenant scope, classification, purpose, version, owner, expiry, and cleanup behavior. A fixture that represents a high-risk scenario is reviewed and protected like a test asset, not casually copied into prompts or examples.

## Test Double Strategy

| Test double | Use when | Required control |
|---|---|---|
| Mock | Validating an isolated request, response, or failure contract | Must mirror the approved contract and not hide authorization or parameter behavior |
| Fake or simulator | Validating deterministic workflow, tool, channel, or state behavior | Versioned behavior, representative failure modes, and contract conformance |
| Provider sandbox | Validating a real provider integration without production side effects | Isolated tenant/account, test credential, quota, cleanup, and audit |
| Controlled real dependency | Validating release readiness or production verification | Explicit approval, minimal scope, safe operation, observability, and rollback/fallback |

Mocks and fakes improve speed but do not replace contract, integration, or controlled real-dependency tests for material boundaries.

## Test Environment Readiness

Before an integration, evaluation, resilience, or production-verification suite runs, the environment confirms approved test tenant, credentials, dependencies, model/provider eligibility, feature flags, channel/tool sandbox, observability, cleanup/reset behavior, capacity/quota, and owner availability.

An environment that cannot establish these controls is not treated as a passing test environment. The result is blocked or explicitly marked inconclusive rather than reported as a product failure or success.

---

# Release Evidence and Risk Gates

## Minimum Release Evidence

Every release candidate requires versioned evidence of:

- Manifest and dependency validation.
- Contract and policy tests.
- Relevant integration and regression tests.
- Evaluation results for the approved use cases and risk profile.
- Security and tenant-isolation tests.
- Resilience and failure tests for material dependencies or side effects.
- Observability and deployment readiness tests.
- Exceptions, known limitations, approvals, and rollback readiness.

## Risk Gates

| Risk level | Minimum additional evidence |
|---|---|
| Low | Contract, functional, policy, regression, and safe deployment verification |
| Moderate | Integration, evaluation, tenant-isolation, observability, and failure-path evidence |
| High | Security review, external-action tests, resilience/failure injection, approval, staged rollout, and rollback drill |
| Critical | Independent review, dual-control approval, adversarial evaluation, production readiness review, restricted cohort, continuous monitoring, and tested emergency withdrawal |

A failed required gate blocks release or activation unless an approved time-bound exception documents scope, risk, compensating control, owner, expiry, and follow-up.

## Performance Acceptance

Each risk and channel profile has approved performance expectations for execution latency, dependency latency, concurrency, throughput, quota behavior, timeout, and degradation. Voice-related journeys include end-to-end interactive latency, interruption, transcription/synthesis timing, and call-continuity expectations owned jointly with the Voice Platform.

Performance evidence compares the candidate against an approved baseline and capacity condition. A faster result does not pass if it weakens safety, authorization, tenant isolation, quality, delivery, or external-action correctness.

---

# Regression and Change Management

Every material change to agent instructions, capabilities, tools, workflows, model eligibility, knowledge/memory access profile, channel behavior, security policy, permission rules, event contract, deployment policy, or evaluation rubric triggers targeted regression selection.

The regression suite maintains a traceability map from changed artifact to affected test domains, dependencies, risks, and release gates. A passing general test suite is not sufficient when a high-impact dependency changed outside its coverage.

Regression baselines are versioned. A test expectation changes only through reviewed update of the requirement, metric, policy, or evaluation rubric; it is not changed merely to make a failing candidate pass.

---

# Failure Injection and Resilience

Failure tests simulate unavailable or slow model providers, invalid/expired authorization, tenant mismatch, malformed context, tool timeout, duplicate action, workflow interruption, event replay, channel outage, provider callback delay, worker restart, telemetry failure, quota exhaustion, and rollback/withdrawal during active work.

Tests verify bounded retry, idempotency, durable state, safe fallback, human handoff, audit evidence, tenant isolation, and absence of duplicated external actions. Failures must not cause the agent to bypass policy or leak data to continue a task.

## Adversarial and Abuse Testing

The adversarial test catalog covers prompt injection, jailbreak attempts, untrusted event or tool-result instructions, cross-tenant identifier guessing, identity spoofing, privilege escalation, secret extraction, data exfiltration, unsafe tool parameters, consent bypass, delivery abuse, and denial-of-service patterns.

Tests use controlled fixtures and expected safe outcomes. A discovered abuse path is triaged through Security and the owning platform; it becomes a regression test or an approved documented exception before affected capability release.

---

# Production Verification

Production verification occurs after an authorized deployment or configuration change. It uses a minimal approved tenant scope, safe representative inputs, controlled tool/channel behavior, and version-specific telemetry.

Verification confirms version resolution, tenant routing, policy enforcement, channel readiness, required dependency health, trace/metric emission, delivery path where applicable, rollback target, and stop-condition monitoring. It does not use production verification to discover fundamental missing requirements that should have been caught earlier.

---

# Test Governance and Ownership

Every test suite, fixture set, evaluation set, quality gate, and release report has a business owner, technical owner, risk classification, review cycle, and retirement policy.

Feature owners create and maintain agent-specific tests. Dependent platform owners own their boundary contracts and test environments. Testing Platform provides common execution capability and quality guidance. Security, Operations, and tenant/business owners provide approval or review when required by risk.

Test failures, flaky tests, gaps, exceptions, and known limitations are tracked with impact, owner, workaround, priority, and expiry. A repeatedly flaky safety, permission, tenant, or side-effect test is treated as a release risk, not ignored.

## Model Evaluation Repeatability

For probabilistic model behavior, the evaluation policy defines the run count, allowed variance, sampling and seed configuration where available, evaluator version, calibration method, confidence threshold, and flaky-result handling. Results outside the permitted range are investigated, rerun under controlled conditions, or marked inconclusive; they are not averaged away without explanation.

## Defect-to-Regression Rule

Every confirmed escaped defect, incident, security finding, tenant-isolation failure, unsafe action, or material customer-impacting issue is analyzed for a regression test. The owner adds or updates the relevant test, fixture, contract, evaluation case, or failure-injection scenario unless an approved exemption records why automated coverage is infeasible and what compensating control applies.

---

# Testing Metrics

The platform tracks test coverage by requirement/risk/domain, pass rate, execution time, flake rate, defect escape rate, mean time to detect regression, evaluation variance, security finding closure, tenant-isolation regression, production-verification result, and release-gate exception count.

Coverage is measured by meaningful scenarios and risks, not simply code-line count. Metrics are used to improve test confidence, not to reward superficial test volume.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Agent test plan template | Defines scope, risk, environments, domains, evidence, and release gates | Agent Platform and Testing Platform |
| Test-case registry | Defines lifecycle, owner, traceability, fixture, expectation, review, and retirement | Agent Platform |
| Requirement-to-test traceability map | Maps capabilities, versions, dependencies, and risks to test cases and evidence | Agent Platform |
| Agent fixture catalog | Defines safe fixtures, tenant/classification scope, owner, expiry, and permitted use | Agent Platform and Data/Security owners |
| Test-double catalog | Defines mock, fake, simulator, sandbox, and controlled-dependency behavior and coverage limits | Agent Platform and Testing Platform |
| Test-environment readiness contract | Defines required tenant, dependency, sandbox, flag, telemetry, cleanup, quota, and owner checks | Testing, Operations, and Agent Platform |
| Contract and policy test suite | Validates schemas, authorization, tenant scope, obligations, and compatibility | Agent Platform |
| Integration and end-to-end journey suite | Validates controlled cross-platform journeys and outcomes | Agent Platform with dependent owners |
| Resilience and failure-injection catalog | Defines failure scenarios, expected safe behavior, and recovery evidence | Agent, Operations, and Testing owners |
| Adversarial-test catalog | Defines abuse scenarios, safe outcomes, triage, and regression coverage | Security and Agent Platform |
| Model-evaluation repeatability policy | Defines runs, variance, calibration, confidence, and flaky-result handling | Agent Platform and Evaluation owner |
| Performance acceptance catalog | Defines risk/channel expectations, baseline, load profile, and pass criteria | Agent, Voice, Operations, and Testing owners |
| Defect-to-regression procedure | Defines incident analysis, coverage update, exemption, and verification | Agent, Security, Operations, and Testing owners |
| Release evidence report | Records results, evaluator/rubric version, exceptions, approvals, and rollback readiness | Agent Platform |
| Production-verification checklist | Defines safe post-deployment checks, scope, owners, and completion evidence | Agent and Operations owners |

---

# Anti-Patterns

## Prompt-Only Testing

Asking whether an agent gives a good answer without testing permissions, tools, context, tenant scope, and delivery leaves the most dangerous failures untested.

## Production Data as Default Fixture

Copying customer conversations, documents, memories, credentials, or recordings into test suites creates privacy, retention, and access-control risk. Use safe representative fixtures.

## Exact Wording as the Only Quality Assertion

Model outputs may vary while still satisfying approved intent and safety requirements. Use structured, rubric-based, and outcome-focused assertions where appropriate.

## Unit Tests Without Boundary Tests

Isolated components may pass while contracts, events, authorization, channel delivery, and dependencies fail in integration. Test the full controlled path.

## Release Without Failure Tests

Testing only the happy path does not prove safe behavior during provider outage, duplicate event, tenant mismatch, or tool failure. Material paths require resilience evidence.

## Treating Flaky Tests as Noise

Flaky safety, authorization, isolation, or external-action tests can hide real regressions. Investigate, stabilize, or block the affected release scope.

---

# Related Documents

| Document | Relationship |
|---|---|
| 07_AGENT_RUNTIME_ARCHITECTURE.md | Defines runtime behavior validated by execution and resilience tests. |
| 08_AGENT_EXECUTION_ENGINE.md | Defines controlled reasoning and execution behavior under test. |
| 15_AGENT_TOOL_SYSTEM.md | Defines tool selection and authorization boundary tests. |
| 16_AGENT_TOOL_EXECUTION_MODEL.md | Defines tool execution, idempotency, and external-action tests. |
| 20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md | Defines workflow transition and process tests. |
| 21_AGENT_EVENT_INTEGRATION.md | Defines event contract, subscription, replay, and resilience tests. |
| 22_AGENT_MULTI_CHANNEL_MODEL.md | Defines channel, delivery, consent, and handoff tests. |
| 24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md | Defines Agent security, injection, access, and data-protection tests. |
| 25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md | Defines authorization, approval, and revocation tests. |
| 26A_AGENT_TENANT_BOUNDARY_REWRITE_DRAFT.md | Defines isolation and cross-tenant regression tests. |
| 27_AGENT_VERSIONING_MODEL.md | Defines version, compatibility, and regression evidence. |
| 28_AGENT_DEPLOYMENT_MODEL.md | Defines deployment readiness and production verification tests. |
| 29_AGENT_OBSERVABILITY_MODEL.md | Defines telemetry and diagnostic evidence tests. |
| 33_AGENT_EVALUATION_FRAMEWORK.md | Defines model-quality and rubric-based evaluation. |
| 14_TESTING_PLATFORM | Owns shared testing capabilities and quality standards. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Agent Testing Strategy architecture document. |
| 2.1 | 2026-08-05 | Added test-case lifecycle, test doubles, environment readiness, performance acceptance, adversarial tests, repeatability, defect regression, and final artifacts. |

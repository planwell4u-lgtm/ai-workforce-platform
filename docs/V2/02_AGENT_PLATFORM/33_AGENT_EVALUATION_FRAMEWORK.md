# 33_AGENT_EVALUATION_FRAMEWORK

**Version:** 2.2  
**Status:** Approved  
**Phase:** Agent Platform

---

# Overview

This document defines how the Agent Platform evaluates whether an agent version performs its approved role effectively, safely, reliably, and consistently across supported channels and business scenarios.

Evaluation is a controlled quality-assessment discipline. It assesses model-mediated behavior using versioned scenarios, rubrics, datasets, reviewers, automated evaluators, and outcome evidence. It does not replace deterministic testing, authorization, security controls, production observability, or tenant business judgment.

---

# Purpose

The purpose of the Agent Evaluation Framework is to make agent quality measurable, reviewable, comparable, and improvable before and after deployment.

It provides a common method for deciding whether an agent version is fit for its intended purpose, whether a change improves or regresses behavior, and whether an observed production issue should lead to evaluation, remediation, experiment, or withdrawal.

---

# Objectives

The Agent Evaluation Framework must:

- Evaluate task quality, safety, policy compliance, usefulness, resolution, and channel-appropriate behavior.
- Use versioned scenarios, rubrics, evaluator configurations, datasets, and evidence.
- Distinguish deterministic pass/fail requirements from probabilistic quality assessment.
- Support automated, human, hybrid, offline, pre-release, online, and post-incident evaluation.
- Tie evaluation depth and release gates to agent risk, business purpose, data classification, and external-action impact.
- Preserve tenant isolation, consent, privacy, data minimization, and reviewer access controls.
- Enable comparable version, cohort, channel, model, tool, workflow, knowledge, and memory assessments.
- Provide explainable results, calibration, variance handling, and a controlled improvement loop.

---

# Scope

This document defines:

- Evaluation concepts, lifecycle, scenario types, rubric dimensions, datasets, evaluators, and scoring.
- Pre-release, continuous, incident-driven, and experiment evaluation requirements.
- Human-review, automated-evaluator, calibration, bias, privacy, and governance controls.
- Evaluation evidence, release gates, analytics links, testing links, and required implementation artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Unit, contract, integration, security, resilience, and performance test execution | 31_AGENT_TESTING_STRATEGY and 14_TESTING_PLATFORM |
| Production telemetry collection, trace storage, dashboards, and alerting | 29_AGENT_OBSERVABILITY_MODEL and 13_OBSERVABILITY_PLATFORM |
| Analytics warehouse, transformations, BI, and long-term reporting | 30_AGENT_ANALYTICS_MODEL and 08_DATA_PLATFORM |
| Authorization, tenant isolation, privacy policy, or security incident handling | 24_AGENT_SECURITY_MODEL, 25_AGENT_PERMISSION_MODEL, 26_AGENT_TENANT_ISOLATION, and Security Platform |
| Agent versioning, release, activation, rollback, and deployment mechanics | 27_AGENT_VERSIONING_MODEL and 28_AGENT_DEPLOYMENT_MODEL |
| Business policy, legal advice, regulatory interpretation, or tenant-owned success targets | Tenant business owner and applicable governance owner |

---

# Evaluation Principles

## Evaluate the Approved Purpose

An agent is evaluated against its documented purpose, capabilities, constraints, risk profile, and intended channels. A generic benchmark cannot prove that an appointment agent, support agent, or workflow agent meets its own business responsibility.

## Separate Quality From Authority

A high score does not authorize an action, bypass permission, permit sensitive data access, or replace a required approval. Evaluation measures behavior; deterministic security and policy controls remain authoritative.

## Version Everything That Affects a Result

Evaluation results reference the agent version and manifest, scenario/dataset version, rubric version, evaluator configuration, model/provider eligibility, environment, dependency profile, time, reviewer identity or evaluator identity, and applicable policy.

## Measure More Than Fluency

Natural wording alone is insufficient. Evaluation measures task completion, factual grounding, policy adherence, safety, correct refusal, tool/workflow behavior, channel suitability, escalation, and user-impact outcome where applicable.

## Use Representative and Safe Evidence

Evaluation scenarios reflect approved user journeys, channels, languages, risks, and failure conditions without copying ungoverned customer data. Sensitive or production-derived material requires explicit authorization, minimization, classification, and restricted reviewer access.

## Make Uncertainty Visible

Scores, labels, and recommendations record confidence, variance, missing data, evaluator disagreement, sampling limits, and known bias. A single score must not conceal unresolved safety or quality uncertainty.

---

# Evaluation Model

~~~text
Approved Agent Purpose and Risk Profile
    |
    v
Versioned Scenario and Dataset
    |
    v
Execution Under Controlled Configuration
    |
    v
Automated Evaluator, Human Reviewer, or Hybrid Review
    |
    v
Rubric Scores, Findings, and Evidence
    |
    v
Release Gate, Experiment Decision, Improvement Work, or Incident Action
~~~

## Evaluation Unit

An evaluation unit is one controlled assessment of an agent response, execution, tool/workflow outcome, channel delivery, or multi-turn journey against a defined scenario and rubric.

## Scenario

A scenario defines the user/event context, approved tenant or synthetic fixture, expected task, channel/capability constraints, risk, required policy conditions, permitted dependencies, and outcome assertions. It is not an unrestricted prompt collection.

## Rubric

A rubric defines the dimensions, scale, thresholds, hard-fail criteria, evidence requirement, weighting, reviewer instructions, and interpretation guidance for a scenario or scenario family.

## Evaluator

An evaluator may be deterministic logic, a controlled model-assisted evaluator, a qualified human reviewer, or a hybrid process. Evaluator use is approved for the data classification and purpose; evaluator output is evidence, not unreviewed truth.

---

# Evaluation Lifecycle

~~~text
Design
    -> Review and Calibrate
    -> Approve
    -> Execute
    -> Validate Results
    -> Gate, Compare, or Investigate
    -> Improve or Retire
    -> Archive Evidence
~~~

## Design and Approval

New scenarios and rubrics identify purpose, owner, risk, data classification, allowed evaluators, expected behavior, hard-fail conditions, baseline, and release-gate use. High-risk or tenant-sensitive evaluations require the applicable security, business, and reviewer approval.

## Execution

Evaluation executes an approved agent version in a controlled environment or approved monitored cohort. It captures the minimum necessary result references, scores, findings, evaluator evidence, timing, and variance.

## Validation and Interpretation

Results are checked for schema validity, evaluator eligibility, data quality, calibration, outliers, incomplete runs, policy violations, and comparability. A conclusion distinguishes passed, failed, inconclusive, blocked, and exception states.

## Improvement and Retirement

Findings produce a controlled improvement record, test addition, knowledge/memory remediation, tool/workflow correction, version change, experiment, deployment action, or no-change decision. Scenarios, rubrics, and evaluators are deprecated when no longer representative or valid, while historical results remain traceable.

## Reference Answers and Golden Cases

Golden cases are approved scenarios with a stable expected outcome, critical assertion, or reference answer. They are used when exact structured behavior, policy outcome, tool parameter, workflow state, refusal, or factual result is required.

Rubric judgment is used where multiple safe and useful responses are valid. Golden cases and reference answers identify their owner, purpose, source authority, version, validity period, data classification, approval, and retirement reason. They are not copied from customer content without the required authorization and minimization.

---

# Evaluation Dimensions

## Core Dimensions

| Dimension | Assesses |
|---|---|
| Task success | Whether the approved goal or safe disposition was reached |
| Grounding and accuracy | Whether claims/actions are supported by authorized context and correct information |
| Instruction and policy adherence | Whether approved instructions, safety rules, permissions, and constraints were followed |
| Safety and refusal | Whether prohibited, risky, uncertain, or unauthorized actions were refused, escalated, or constrained correctly |
| Tool and workflow correctness | Whether controlled actions, parameters, state, idempotency, and outcomes were correct |
| Communication quality | Whether the response is clear, truthful, appropriate, and channel-suitable |
| Efficiency | Whether the agent uses reasonable time, steps, dependencies, and cost for the task |
| Recovery and handoff | Whether failure, uncertainty, approval, and human handoff behavior is appropriate |
| Privacy and tenant protection | Whether data access, disclosure, redaction, and tenant boundaries are preserved |

## Hard-Fail Criteria

Hard-fail criteria are non-negotiable outcomes such as tenant-data exposure, unauthorized external action, secrets disclosure, bypassed approval, unsafe instruction following, prohibited content, materially false completion claim, or failure to follow a required safety escalation.

A candidate with a hard fail cannot be accepted based on a higher average score. It is blocked, remediated, or handled through the approved exception process.

---

# Evaluation Types

## Offline Pre-Release Evaluation

Offline evaluation uses approved fixtures and scenarios before release. It validates candidate versions against baseline, critical safety cases, representative user journeys, edge cases, tool/workflow paths, channel forms, and known regressions.

## Human Review

Qualified reviewers assess scenarios requiring domain expertise, sensitive judgment, nuanced safety, or calibration. Reviewer access is scoped to the minimum data and tenant purpose needed. Review instructions, disagreements, and overrides are recorded.

## Automated and Hybrid Evaluation

Automated evaluators support scale and repeatability for approved criteria. Hybrid evaluation combines automation with human calibration, spot checks, and escalation of uncertain or high-risk findings. Automated evaluators are tested and versioned like other dependencies.

## Online and Continuous Evaluation

Approved production evidence may be sampled or aggregated for post-deployment evaluation under tenant, consent, classification, and privacy policy. Online evaluation never becomes unrestricted surveillance or automatic live-agent modification.

## Channel Evaluation Profiles

Each supported channel has an approved evaluation profile in addition to common agent-quality dimensions.

| Channel | Additional assessment focus |
|---|---|
| Voice | Interactive latency, interruption, transcription confidence, speech clarity, turn-taking, call continuity, and safe escalation |
| Web or app chat | Structured controls, session continuity, rich-content accessibility, identity handling, and response timing |
| Messaging and email | Consent, template/window constraints, delivery behavior, concise presentation, recipient safety, and asynchronous expectation management |
| API | Structured output validity, schema adherence, idempotency, error contract, client authorization, and deterministic integration behavior |

Channel profiles do not create separate agent intelligence. They assess whether the same approved Agent Brain is presented safely and effectively through a specific delivery surface.

## Incident-Driven Evaluation

A defect, incident, safety signal, complaint, or recurring failure can create targeted evaluation scenarios. Results determine whether remediation, withdrawal, regression tests, retraining of reviewers, or architecture change is required.

---

# Calibration, Repeatability, and Bias

## Evaluator Calibration

Evaluators are calibrated against approved reference cases with known expected assessment. Calibration measures agreement, drift, false positive/negative patterns, and reviewer consistency. Evaluators that fall outside approved calibration range are retrained, limited, or suspended.

## Reviewer Qualification and Independence

Human reviewers have documented domain qualification, required training, tenant/classification access, calibration status, and review authority. A reviewer is excluded when they have a material conflict of interest, lack required expertise, or should not access the evaluation evidence.

High-risk evaluation defines independent review, escalation, disagreement resolution, and override restrictions. Reviewer identity and access are recorded, while reports expose only the minimum reviewer information required by policy.

## Repeatability and Variance

Probabilistic evaluations define run count, sampling/model settings where available, allowed variance, confidence threshold, aggregation rule, and handling of flaky or inconclusive results. A result with excessive variance is investigated rather than averaged into a false conclusion.

## Bias and Representation

Scenario sets cover approved languages, channels, user needs, risk conditions, and tenant use cases proportionally to their intended scope. The framework records coverage gaps, potential bias, disparate outcome indicators where lawful and appropriate, and limitations on interpretation.

Evaluation must not create protected-class profiling or discriminatory decision-making. Any material fairness or harm concern is escalated to the appropriate security, governance, product, or tenant authority.

## Dataset Drift and Refresh

Scenario and dataset relevance is reviewed when agent purpose, policy, product information, knowledge source, memory profile, tool, workflow, model, channel, language, tenant use case, regulation, incident pattern, or observed production behavior changes materially.

The evaluation registry records last review, coverage gap, drift signal, refresh owner, and required action. Outdated scenarios may remain for historical comparison but are labeled and cannot be the sole evidence for a current release gate.

---

# Evaluation Gates and Decisions

## Release Gates

Evaluation gates are determined by risk. A release candidate must meet required hard-fail, quality, safety, and regression thresholds before release or activation. High-risk changes require independent or human review, stronger scenario coverage, and staged deployment evidence.

## Decision States

| State | Meaning |
|---|---|
| Pass | Required thresholds and evidence are met |
| Conditional pass | Allowed only with documented bounded limitation, compensating control, and follow-up |
| Fail | Required threshold, hard-fail rule, or evidence requirement is not met |
| Inconclusive | Data, variance, evaluator, or environment issue prevents a valid conclusion |
| Blocked | Required dependency, approval, policy, or safe environment is unavailable |

A conditional pass never overrides a hard-fail, tenant, security, authorization, or regulatory restriction.

## Evaluation-to-Change Contract

Every decision-relevant finding records evidence, agent/version, scenario/rubric/evaluator versions, scope, risk, recommendation, decision owner, and resulting action. Actions may request a new test, version, knowledge update, tool/workflow change, deployment rollback, incident, or no change. Evaluation findings do not directly mutate production behavior.

---

## Gate Override

An override is permitted only when policy allows it and no hard-fail, tenant, security, authorization, regulatory, or critical safety restriction is present. The override records the unmet requirement, scope, risk, compensating control, authorized decision maker, affected tenant/cohort, expiry, monitoring, rollback/withdrawal condition, and mandatory follow-up.

Overrides are time-bound and reviewed before expiry. A conditional release does not become a permanent quality standard merely because it was once approved.

---

# Privacy, Security, and Tenant Controls

Evaluation data is tenant-scoped and purpose-limited. Synthetic data is the default. Use of production-derived data, recordings, transcripts, documents, memories, or customer feedback requires documented authorization, classification, consent/legal basis where applicable, minimization, retention, and restricted access.

Reviewers and automated evaluators receive only authorized evidence. Evaluation outputs do not contain secrets, raw unnecessary content, hidden instructions, private reasoning, or cross-tenant comparisons. Export, benchmark, model-provider use, and retention follow current policy.

Tenant-specific evaluation results are visible only to authorized tenant users and platform roles. Cross-tenant analysis requires the anonymization, cohort, opt-in, and governance controls established by the Analytics Model.

---

## Evaluator Security

Every model-assisted, third-party, or external evaluator has an approved assurance record covering identity, allowed data classification, tenant eligibility, region/residency, data-use and retention terms, prompt/result handling, logging, access, and incident obligations.

Evaluator selection is revalidated for the scenario’s tenant, classification, and purpose. If no eligible evaluator is available, the evaluation is blocked, reduced to an approved deterministic/human method, or marked inconclusive; restricted data is never silently routed to an ineligible evaluator.

---

# Evaluation Capacity and Cost

Evaluation scheduling uses approved budgets, queues, prioritization, and capacity limits for model-assisted and human review. Critical safety, release-gate, incident-driven, and high-risk regression evaluations take precedence over lower-priority exploratory analysis.

The platform records evaluation cost and resource use by tenant, agent, version, scenario set, evaluator type, risk, and purpose where permitted. Budget exhaustion does not bypass a required release gate; it blocks, defers, or escalates the candidate according to policy.

---

# Observability, Analytics, and Testing Boundaries

Evaluation consumes protected references from testing, observability, analytics, feedback, and incident processes. It produces score, finding, gate, and improvement references that other systems may use under authorization.

Testing proves deterministic and integration expectations. Observability describes live system behavior. Analytics aggregates governed outcomes over time. Evaluation assesses whether the behavior meets approved quality and safety criteria. These activities share evidence but do not replace one another.

---

# Testing the Evaluation System

## Contract and Dataset Tests

Tests validate scenario, rubric, evaluator, score, finding, gate, and evidence schemas; dataset versioning; classification; tenant scope; and prohibited-content controls.

## Calibration and Consistency Tests

Tests verify evaluator calibration, human-review agreement, automated-evaluator drift, repeatability, variance, threshold application, hard-fail precedence, and correct inconclusive handling.

## Security and Privacy Tests

Tests verify reviewer authorization, tenant isolation, synthetic-data default, redaction, retention, export restrictions, evaluator/provider eligibility, and prevention of private reasoning or secrets entering evaluation records.

## Regression and Adversarial Tests

The framework includes known defect, safety, injection, refusal, tool misuse, policy bypass, data-exfiltration, and failure/handoff scenarios. A material escaped issue becomes an evaluation case or an approved documented exception.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Evaluation scenario schema | Defines scenario context, constraints, risk, fixtures, and expected outcome | Agent Platform |
| Golden-case and reference-answer policy | Defines exact assertions, source authority, approval, lifecycle, and retirement | Agent and tenant business owners |
| Rubric catalog | Defines dimensions, scales, thresholds, hard fails, weights, and interpretation | Agent and tenant business owners |
| Evaluation dataset registry | Defines dataset version, classification, provenance, permitted use, owner, and retention | Agent, Data, and Security owners |
| Dataset-drift and refresh register | Tracks change signals, coverage gaps, review date, refresh owner, and action | Agent Platform and Evaluation owner |
| Evaluator configuration registry | Defines evaluator type, version, eligibility, calibration, and allowed data | Agent Platform and Security owner |
| Reviewer qualification and independence register | Defines expertise, training, access, calibration, conflict, and authority | Agent Platform and tenant governance owner |
| Channel evaluation-profile catalog | Defines additional voice, chat, messaging, email, and API assessment criteria | Agent Platform with Channel owners |
| Calibration and variance policy | Defines reference cases, agreement, run count, confidence, drift, and flaky handling | Agent Platform and Evaluation owner |
| Evaluation gate policy | Defines risk-based evidence, thresholds, approval, exception, and decision states | Agent Platform and tenant policy owner |
| Gate-override procedure | Defines eligibility, approver, scope, control, expiry, monitoring, and follow-up | Agent, Security, and tenant policy owners |
| Evaluator security-assurance register | Defines provider, region, classification, data use, retention, and incident eligibility | Security and Agent Platform owners |
| Evaluation capacity and cost policy | Defines budget, prioritization, queueing, cost attribution, and exhaustion behavior | Agent, Operations, and tenant owners |
| Evaluation result and finding schema | Defines evidence, score, recommendation, owner, action, and lineage | Agent Platform |
| Evaluation coverage map | Maps agent purpose, channel, risk, capability, and dependency to scenarios | Agent Platform and Testing Platform |
| Evaluation audit report | Provides assessment, gate, reviewer, version, and action traceability | Agent Platform |

---

# Anti-Patterns

## One Generic Benchmark

A generic benchmark cannot prove that a tenant-specific agent fulfills its documented purpose, uses tools safely, handles channels correctly, or follows policy.

## Average Score Overrides Hard Fail

A high average score does not compensate for tenant exposure, unsafe action, secret disclosure, policy bypass, or materially false completion claim.

## Evaluator as Final Authority

An automated evaluator or reviewer score is evidence, not permission to bypass security, tenant, deployment, or business approval controls.

## Unversioned Rubric or Dataset

Changing evaluation instructions, cases, or scoring without versioning makes results incomparable and hides quality regression.

## Production Content by Convenience

Copying raw customer data into evaluation sets without controlled authorization, minimization, and retention creates privacy and ownership problems.

## Optimize for the Evaluator

Tuning an agent to score well against a narrow evaluator while degrading real task, safety, or user outcome is a quality failure. Use diverse scenarios, outcome evidence, and guardrails.

---

# Related Documents

| Document | Relationship |
|---|---|
| 06_AGENT_CONFIGURATION_MODEL.md | Defines agent configuration assessed by evaluation. |
| 07_AGENT_RUNTIME_ARCHITECTURE.md | Provides execution context and controlled evaluation execution. |
| 08_AGENT_EXECUTION_ENGINE.md | Defines behavior and outcomes assessed by rubrics. |
| 15_AGENT_TOOL_SYSTEM.md | Provides tool-selection and action evidence. |
| 20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md | Provides workflow/process outcome evidence. |
| 22_AGENT_MULTI_CHANNEL_MODEL.md | Defines channel-specific presentation and delivery behavior assessed by evaluation. |
| 24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md | Defines Agent application of security, privacy, and model-provider controls for evaluation. |
| 26A_AGENT_TENANT_BOUNDARY_REWRITE_DRAFT.md | Requires tenant-scoped scenarios, data, results, and reviewers. |
| 27_AGENT_VERSIONING_MODEL.md | Requires versioned evaluation evidence for release and comparison. |
| 28_AGENT_DEPLOYMENT_MODEL.md | Uses evaluation evidence for readiness, rollout, and withdrawal. |
| 29_AGENT_OBSERVABILITY_MODEL.md | Provides protected live behavior evidence and anomaly signals. |
| 30_AGENT_ANALYTICS_MODEL.md | Uses governed evaluation results for trends and improvement analysis. |
| 31_AGENT_TESTING_STRATEGY.md | Defines deterministic test obligations and when evaluation evidence is required. |
| 32_AGENT_FAILURE_HANDLING.md | Creates incident-driven scenarios and safe response evidence. |
| 14_TESTING_PLATFORM | Owns shared test execution and quality infrastructure. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Agent Evaluation Framework architecture document. |
| 2.1 | 2026-08-05 | Added golden cases, channel profiles, reviewer governance, drift, overrides, evaluator security, capacity, and final artifacts. |

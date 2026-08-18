# 09_MEMORY_QUALITY_AND_EVALUATION

**Version:** 1.1
**Status:** Approved
**Owner:** Memory Platform Owner
**Phase:** Memory Platform

---

# Overview

This document defines how Memory Platform evaluates the accuracy, usefulness, freshness, safety, consent compliance, and harmful-memory risk of durable personal context. Evaluation produces evidence and governed improvement proposals; it never makes a candidate durable, changes a record, broadens policy, or restores restricted memory automatically.

Quality is not the same as operational observability. Quality asks whether Memory behavior and content are fit for an approved purpose. Observability records the signals needed to operate and diagnose the platform.

---

# Purpose

The quality model prevents the platform from equating a successful retrieval with a correct or appropriate memory outcome. It detects stale, unsupported, over-broad, conflicting, low-value, unsafe, biased, or policy-violating memory and channels the result into accountable review.

---

# Scope and Boundaries

| Topic | Owner |
|---|---|
| Memory quality objectives, evaluation scenarios/datasets/rubrics, quality signals, gap classification, and improvement proposals | Memory Platform |
| Memory policy, consent/use rules, review authority, participant rights, and policy decisions | 08_MEMORY_GOVERNANCE_AND_CONSENT.md |
| Capture/admission, correction, lifecycle, deletion, access, and retrieval execution | Their respective Memory documents |
| Shared evaluation/test infrastructure, runners, reporting, and test standards | 14_TESTING_PLATFORM |
| Shared telemetry infrastructure, dashboards, alerts, and operational diagnostics | 13_OBSERVABILITY_PLATFORM |
| Enterprise privacy/security assessment and compliance controls | 09_SECURITY_PLATFORM |
| Agent reasoning/model behavior and prompt quality | 02_AGENT_PLATFORM |

Memory owns the domain definition of quality and the evidence needed to improve it safely. It does not own the shared platforms that run or visualize evaluations.

---

# Quality Principles

## Useful Is Not Enough

A highly relevant fact fails quality if it is unauthorized, stale, unsupported, incorrectly attributed, too broad for the purpose, or harmful to the participant. Quality gates consider suitability and safety together.

## Evaluate the Whole Memory Path

Evaluation covers candidate origin, evidence, admission, profile semantics, retrieval eligibility, representation, lifecycle, suppression/deletion, access, and failure behavior. It does not assess only a search/ranking score.

## Governed Data Only

Evaluation data is synthetic, minimized, de-identified, or otherwise authorized for the specific evaluation purpose. Production-derived memory data requires documented purpose, classification, access, retention, secure environment, and owner approval. Evaluation copies are not an ungoverned shadow profile store.

## Evaluation Cannot Change Memory

An evaluator may detect a gap or create an improvement proposal. It may not admit a candidate, revise a memory, alter consent, change a policy, suppress/delete a record, or publish a model/configuration change without the existing governed workflows.

## Failures Matter

Evaluation explicitly tests no-memory, restricted, stale, suppressed, deleted, cross-tenant, wrong-subject, malformed, delayed, duplicate, provider-impaired, and unavailable cases. A test that only proves successful retrieval is incomplete.

## Explainable Evidence

Every material score or conclusion links to a versioned scenario, data source classification, rubric, evaluator configuration, policy context, result, and review status. Opaque aggregate scores cannot authorize a change.

---

# Quality Dimensions

| Dimension | Question | Examples of evidence |
|---|---|---|
| Admission accuracy | Did durable memory represent an allowed, evidence-supported claim? | Evidence coverage, verification state, duplicate/conflict outcome, review agreement. |
| Semantic correctness | Does the record's type/value/scope express the intended meaning without overreach? | Schema validation, human review, counterexample tests. |
| Freshness | Is the memory current enough for its approved use? | Observed/verified time, expiry, source refresh, stale-result rate. |
| Retrieval fitness | Does an authorized request receive the minimum useful eligible context? | Scenario pass rate, precision/recall within eligible set, budget/precedence adherence. |
| Constraint compliance | Are tenant, subject, purpose, consent/use, classification, representation, and lifecycle rules enforced? | Adversarial access tests, restricted-result correctness, audit evidence. |
| Participant impact | Is the context respectful, understandable, correctable, and free of avoidable harm? | Correction/dispute patterns, transparency review, human-impact rubric. |
| Lifecycle integrity | Do suppression, withdrawal, expiry, and deletion remove operational use everywhere required? | Invalidation lag, stale representation detection, deletion target completion. |
| Reliability | Does safe behavior persist under timeout, replay, partial dependency, recovery, and load? | Degraded/unavailable correctness, reconciliation and recovery tests. |
| Operational efficiency | Is the quality path sustainable within approved latency, cost, and review capacity? | Evaluation cost/latency, review aging, provider usage, capacity evidence. |

No single metric represents Memory quality. Scores are segmented by record category, sensitivity, tenant configuration, purpose, representation, and risk tier where doing so is permitted and privacy-safe.

---

# Evaluation Assets

| Asset | Required controls |
|---|---|
| `EvaluationScenario` | Versioned purpose, requester/subject scope, policy context, expected outcome, and adverse-path conditions. |
| `EvaluationDataset` | Provenance, classification, authorization, minimization, retention, tenant/use isolation, and access owner. |
| `EvaluationRubric` | Versioned criteria, thresholds, severity, human-review rules, and limitations. |
| `EvaluatorConfiguration` | Versioned method/model/provider/tool settings, allowed data, known limitations, and fallback behavior. |
| `EvaluationRun` | Correlation, environment, input asset versions, policy/version context, results, failures, and reproducibility metadata. |
| `QualityFinding` | Detected gap, severity, affected scope, evidence, confidence, and non-automatic recommended action. |
| `ImprovementProposal` | Scoped candidate change with owner, impact, test plan, approval path, rollout/rollback, and result review. |

Evaluation assets use logical IDs and controlled versions. Provider run IDs, temporary prompts, raw hidden reasoning, and unminimized source content are not canonical quality artifacts.

---

# Scenario Catalog

## Admission and Profile Semantics

- Explicit low-risk preference is admitted only with required evidence, purpose/use basis, and duplicate checks.
- Inferred, disputed, sensitive, malformed, cross-tenant, expired, or unauthorized candidate is held/rejected as policy requires.
- Profile scope and preference precedence honor current interaction instruction, restrictions, specific scope, and safe no-result behavior.
- Relationship context remains minimal/reference-first and does not recreate CRM or interaction history.

## Retrieval, Access, and Representation

- Eligible fact is returned only to the correct tenant, subject, requester relationship, purpose, and representation.
- Unsupported, restricted, stale, degraded, and unavailable outcomes are distinct, privacy-safe, and handled without broadening request scope.
- Context budget, field minimization, provenance/freshness indication, and representation redaction are enforced.
- Repeated guessing, alternate representation, cache, index, and similarity probes cannot reveal hidden memory.

## Lifecycle and Participant Rights

- Correction produces a controlled revision and does not mutate prior evidence.
- Suppression/withdrawal stops operational retrieval immediately and invalidates derived representations.
- Retention expiry/deletion covers canonical and dependent targets, with hold/exception handling and no false completion claim.
- Transparency, export, correction, deletion, and delegate requests preserve subject/tenant scope and secure delivery.

## Reliability and Provider Change

- Timeout, retry, duplicate/out-of-order event, worker restart, index lag, provider outage, policy change, and restore exercise preserve safe outcomes.
- Technology migration, re-embedding, schema evolution, and policy narrowing retain provenance and do not resurrect restricted data.

---

# Evaluation Methods

| Method | Use | Guardrail |
|---|---|---|
| Deterministic contract checks | IDs, schemas, states, eligibility, precedence, outcome vocabulary, and deletion/invalidation rules. | Required for every material change. |
| Curated scenario review | Human review of nuanced accuracy, harm, transparency, and policy interpretation. | Reviewer expertise, minimized data, and documented rubric. |
| Adversarial/security evaluation | Scope forgery, cross-tenant/subject probes, prompt/content injection, enumeration, and provider leakage. | Coordinate with Security; no live data exposure. |
| Replay/simulation | Controlled reproduction of lifecycle, failure, and recovery behavior. | Preserve authorization, tenant, and data-minimization constraints. |
| Comparative evaluation | Compare approved retrieval/configuration versions against a fixed governed baseline. | No silent policy/representation change during comparison. |
| Production-safe canary | Synthetic or approved low-risk verification of deployed behavior. | No durable capture, participant impact, or policy bypass. |

Automated evaluators may assist triage, but hard policy/access/lifecycle requirements use deterministic checks or accountable review. An evaluator's confidence is not an authorization decision.

---

# Findings and Improvement Flow

```text
Evaluation evidence
    |
    +--> QualityFinding (scope, severity, evidence, confidence)
    |
    +--> triage: defect / data issue / policy gap / training need / unknown
    |
    +--> ImprovementProposal with owner and approval path
    |
    +--> governed change, test, staged rollout, and outcome review
```

Findings may recommend a correction campaign, source/evidence improvement, stricter admission rule, policy review, dataset update, representation change, training, or no action. They do not automatically modify memory records, enable a category, or increase capture scope.

Severity reflects participant impact, rights/privacy/security risk, scope, confidence, reversibility, and operational urgency. A high-severity finding triggers the applicable incident, suppression, hold, or governance path; it does not wait for a periodic quality cycle.

---

# Release and Change Evidence

| Change class | Minimum quality evidence |
|---|---|
| Internal non-behavioral change | Relevant contract/regression evidence and review. |
| Record schema, admission rule, or preference logic | Scenario/rubric update, positive/adverse tests, provenance/constraint regression, and rollback evidence. |
| Retrieval/representation/provider change | Eligible-set, access/tenant, freshness, minimization, lifecycle/invalidation, cost/latency, and comparative evidence. |
| Consent/use, access, retention, or deletion change | Rights/withdrawal/exception scenarios, Security/privacy review, migration/invalidation, and controlled release. |
| New category or high-risk capability | Policy approval, representative governed scenarios, adversarial/harm evaluation, human review, staged release, alert/runbook, and rollback. |

A change cannot pass quality merely by improving relevance or reducing latency if it weakens an access, purpose, lifecycle, minimization, or participant-impact requirement.

---

# Quality Signals and Privacy

Quality signals are privacy-minimized and access-controlled. They use aggregate, synthetic, or de-identified evidence by default and avoid raw memory values, transcripts, prompts, subject identifiers, and hidden evaluator reasoning. Re-identification for a specific finding follows a separate governed review path with a narrow purpose and audit.

Quality data has its own retention and deletion requirements. Deleting/suppressing source Memory causes affected evaluation artifacts to be removed, redacted, re-scoped, or retained only under a documented lawful/audit exception; it must never leave an operationally usable shadow copy.

---

# Integrity Invariants

- Evaluation cannot admit, revise, suppress, delete, restore, or retrieve personal Memory outside the normal governed paths.
- Every material quality result is attributable to versioned scenario, dataset, rubric, evaluator, policy, and result context.
- Evaluation of successful retrieval is incomplete without negative, restricted, lifecycle, tenant/subject, and failure scenarios.
- Quality evidence must not become a less-governed repository of personal context.
- A finding or metric cannot broaden policy, purpose, retention, or access scope without the required governance decision.
- Participant-impact and constraint-compliance failures outweigh a relevance or efficiency gain.

---

# Related Documents

| Document | Relationship |
|---|---|
| 03_MEMORY_CAPTURE_AND_ADMISSION.md | Defines admission behavior evaluated for accuracy and policy compliance. |
| 05_MEMORY_RETRIEVAL_AND_CONTEXT.md | Defines retrieval outcomes, context limits, and eligibility behavior. |
| 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md | Defines lifecycle/invalidation/deletion behavior evaluated here. |
| 07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md | Defines access and isolation behavior evaluated here. |
| 08_MEMORY_GOVERNANCE_AND_CONSENT.md | Defines policy/change approval and participant-rights paths. |
| 10_MEMORY_SECURITY_AND_PRIVACY.md | Defines threat and privacy requirements. |
| 11_MEMORY_OBSERVABILITY.md | Defines operational signals distinct from quality evaluation. |
| 13_MEMORY_TESTING.md | Defines broader test evidence and shared Testing Platform relationship. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Memory quality and evaluation model with quality dimensions, governed assets, scenarios, findings, and release evidence. |
| 1.1 | 2026-08-06 | Finalized after review for completeness, ownership overlap, and long-term maintainability. |

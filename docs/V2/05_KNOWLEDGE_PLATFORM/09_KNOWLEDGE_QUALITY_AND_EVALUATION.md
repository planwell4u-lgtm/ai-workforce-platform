# 09_KNOWLEDGE_QUALITY_AND_EVALUATION

**Version:** 1.1  
**Status:** Approved  
**Owner:** Knowledge Platform Owner  
**Phase:** Knowledge Platform

---

# Overview

This document defines how the Knowledge Platform evaluates the quality, coverage, freshness, citation completeness, retrieval usefulness, and governance readiness of knowledge evidence.

Evaluation measures whether governed evidence is fit for an approved purpose. It does not replace deterministic testing, source rights, access control, agent evaluation, business judgment, or publication approval.

---

# Purpose

The Quality and Evaluation model turns knowledge gaps, retrieval failures, stale evidence, citation defects, and observed outcomes into reviewable improvement evidence—without automatically changing sources, retrieval policy, published knowledge, or agent behavior.

---

# Scope and Boundaries

| Topic | Owner |
|---|---|
| Knowledge-quality dimensions, evaluation scenarios, datasets, rubrics, results, gap signals, and improvement proposals | Knowledge Platform |
| Agent response quality, reasoning, tool/action success, and agent-release evaluation | 02_AGENT_PLATFORM |
| Retrieval execution, ranking, citations, and outcomes | 05_KNOWLEDGE_INDEXING_AND_RETRIEVAL.md |
| Publication approval and change governance | 08_KNOWLEDGE_GOVERNANCE_AND_PUBLICATION.md |
| Shared testing infrastructure and deterministic test standards | 14_TESTING_PLATFORM |
| Telemetry infrastructure, logs, alerts, and operational dashboards | 13_OBSERVABILITY_PLATFORM |
| Authorization, privacy, retention, and evaluator eligibility | 09_SECURITY_PLATFORM |

---

# Evaluation Principles

## Evaluate Evidence, Not Agent Intent

Knowledge evaluation assesses source-to-retrieval behavior: whether approved evidence is available, current, accessible, traceable, and suitable for the stated query/purpose. It does not judge the agent's final language, reasoning chain, policy decision, or business action.

## Versioned, Reproducible Evaluation

Scenarios, datasets, rubrics, retrieval profiles, policies, corpus versions, evaluator configuration, and results are versioned. A score without this context is not comparable release evidence.

## Hard Failures Are Not Averaged Away

Cross-tenant exposure, unauthorized retrieval, missing required citation, revoked/stale prohibited source, unsupported result presented as supported, or material provenance break are hard failures. Aggregate scores cannot override them.

## Evidence Is Minimized

Synthetic, approved, or minimized fixtures are the default. Production-derived evidence requires current tenant, consent, classification, purpose, retention, evaluator, and export controls. Evaluation data never becomes a back door to customer or restricted source content.

## Improvement Is Governed

An evaluation result may create a gap signal or improvement proposal. It cannot auto-ingest a source, modify a retrieval policy, publish a version, change an agent, or relax a threshold.

---

# Quality Dimensions

| Dimension | Question answered |
|---|---|
| Provenance completeness | Can every returned item and citation trace to current governed source/version evidence? |
| Citation completeness | Does supported evidence include the required, correctly scoped citations and attribution? |
| Retrieval relevance | Do returned eligible items materially address the bounded request under the rubric? |
| Coverage and gap rate | Are required topics, entities, procedures, languages, and source scopes sufficiently represented? |
| Freshness | Is evidence current enough for the source class, risk, and requested purpose? |
| Access correctness | Are required items returned only to authorized scopes, while restricted material stays unavailable? |
| Representation quality | Are extraction, segmentation, language, structure, redaction, and locator quality sufficient for intended retrieval/citation? |
| Resilience and consistency | Do degradation, fallback, invalidation, and lifecycle changes produce safe explicit outcomes? |
| Governance readiness | Does a candidate have required review, source rights, classification, validation, and rollback evidence? |

No universal score is sufficient. Tenant purpose, risk tier, source class, classification, freshness policy, and intended consumer determine required measures and thresholds.

---

# Evaluation Model

~~~text
Versioned Scenario + Approved Fixture/Corpus + Retrieval Profile
    |
    v
Controlled Authorized Retrieval
    |
    v
Rubric / Deterministic Checks / Authorized Evaluator
    |
    v
Evaluation Result and Confidence
    |
    +--> Release/Governance Evidence
    +--> Quality or Coverage Gap Signal
    +--> Reviewable Improvement Proposal
~~~

## Evaluation Scenario

An Evaluation Scenario defines tenant scope or approved synthetic equivalence, purpose, risk/classification, query/request form, expected evidence/citation characteristics, hard-fail conditions, rubric, baseline, evaluator eligibility, corpus/profile versions, owner, expiry/refresh, and permitted release-gate use.

## Evaluation Dataset

An Evaluation Dataset contains approved fixtures, labels, expected evidence references, known gaps, language/format/category coverage, provenance, classification, retention, and access restrictions. It never contains secrets, raw customer data, unrestricted content, or hidden agent reasoning by default.

## Evaluation Result

An Evaluation Result records scenario/dataset/rubric and corpus/profile/policy versions, execution evidence, deterministic checks, evaluator outcome, score/category, confidence/variance, incomplete/blocked status, hard-fail findings, citations, gap signals, and audit reference.

Results are immutable. A corrected judgment or recalibration creates a new result with its relationship to the prior result.

---

# Evaluation Methods

| Method | Appropriate use | Constraint |
|---|---|---|
| Deterministic contract check | Provenance, citation schema, access/lifecycle/freshness, invalidation, and hard safety boundaries | Does not measure semantic usefulness alone. |
| Human review | High-risk, nuanced, regulated, source-quality, or disputed evidence | Reviewer must be eligible, calibrated, and purpose-authorized. |
| Automated evaluation | Repeatable relevance, coverage, citation, structure, and regression assessment | Evaluator/model/prompt is versioned and cannot access disallowed data. |
| Hybrid evaluation | Scale with human calibration, spot checks, and escalation | Disagreement and uncertainty are explicit. |
| Production signal review | Governed aggregate/sampled gaps, staleness, unsupported/restricted patterns | Never becomes unrestricted surveillance or automatic change. |

Automated evaluators provide assessment evidence, not publication authority or business truth. Evaluator confidence, disagreement, bias, missing data, and variance are recorded rather than hidden in an average.

---

# Quality Gates and Decisions

Knowledge quality gates are risk-based. A candidate may require defined hard-fail checks, provenance/citation completeness, source-rights validity, freshness, coverage, relevance, access correctness, regression comparison, and independent review before publication.

| Result status | Meaning | Permitted action |
|---|---|---|
| `Passed` | Required checks and applicable thresholds are met. | May serve as governance evidence; does not publish alone. |
| `Failed` | A required check or threshold failed. | Block/restrict candidate or create remediation. |
| `Inconclusive` | Insufficient, inconsistent, high-variance, or disputed evidence. | Hold/escalate; cannot satisfy a required gate. |
| `Blocked` | Required evaluator, data, policy, or dependency unavailable. | Defer/escalate; do not waive silently. |
| `Exception` | Time-bounded authorized deviation with risk/owner/expiry. | Follow governance policy and enhanced monitoring. |

Threshold changes, rubric changes, evaluator replacement, and dataset changes are versioned and reviewed before comparison or release use.

---

# Coverage, Gap, and Improvement Model

A Quality/Gap Signal identifies a bounded absence, conflict, staleness, retrieval weakness, citation defect, source-quality issue, access anomaly, or evaluation regression. It records affected tenant/scope, evidence, severity, recurrence, confidence, owner, and proposed next action.

An Improvement Proposal can recommend a source change, refresh, processing adjustment, retrieval-profile change, additional evaluation fixture, governance policy review, or agent-facing dependency review. It includes expected benefit, risk, affected versions, required approval, validation plan, rollback, and audit reference.

No signal or proposal auto-publishes, auto-ingests, modifies a live retrieval profile, or changes the agent. It enters the relevant Source, Lifecycle, Retrieval, Governance, or Agent change process.

---

# Security, Tenant, and Privacy Controls

- Evaluation scenarios, fixtures, results, evaluator access, and reports are tenant/environment/purpose/classification scoped.
- Cross-tenant comparisons use only approved anonymized, aggregated, or synthetic evidence and cannot reveal source/corpus membership, content, or performance of a named tenant.
- Evaluators receive only the minimum representation needed; raw sources, credentials, private reasoning, customer profiles, and unrelated transcripts are excluded.
- Reviewer authority, qualification, conflict-of-interest restrictions, calibration, and disagreement resolution follow the governance policy.
- Evaluation exports, dashboards, and feedback routes use separate authorization and retention controls from runtime retrieval.

---

# Observability, Reliability, and Testing

Quality telemetry includes scenario coverage, evaluation completion, hard-fail rate, provenance/citation completeness, relevance/coverage/freshness/access metrics, evaluator disagreement, variance, gap recurrence, improvement status, and gate/exception outcome. It records safe aggregate dimensions and protected references only.

Evaluation runs are idempotent and recoverable. Corpus/profile/policy drift during an evaluation is recorded and the result is marked incomparable or rerun under a consistent snapshot. A failed evaluator, unavailable fixture, timeout, or budget limit produces `Blocked` or `Inconclusive`, not a false pass.

Test evaluation contracts, data minimization, scenario/dataset versioning, hard-fail enforcement, evaluator eligibility, reproducibility, drift, tenant isolation, restricted-data handling, gap-to-proposal workflow, approval separation, and refusal to auto-publish.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Knowledge quality model and metric catalog | Defines dimensions, measures, hard failures, thresholds, aggregation, and limitations | Knowledge Platform |
| Scenario, dataset, and rubric registry | Defines versioned scenarios, fixtures, labels, coverage, evaluator eligibility, and expiry | Knowledge Platform with Testing and Security |
| Evaluation-result contract | Defines execution context, checks, confidence, variance, findings, gaps, and audit | Knowledge Platform |
| Evaluator and calibration policy | Defines human/automated/hybrid evaluator use, qualification, bias, disagreement, and escalation | Knowledge Platform with Governance and Security |
| Quality-gate and exception policy | Defines risk-based release evidence, thresholds, exception authority, expiry, monitoring, and rollback | Knowledge Platform with Governance and Operations |
| Gap and improvement-proposal workflow | Defines signals, ownership, triage, approval, validation, and linkage to change processes | Knowledge Platform with Agent and Operations owners |
| Quality telemetry and test suite | Defines dashboards, alerts, audit, contract, regression, tenant, privacy, and resilience evidence | Knowledge Platform with Observability and Testing |

---

# Anti-Patterns

## Retrieval Hit Rate Is Quality

A hit may be irrelevant, stale, uncited, unauthorized, or incomplete. Assess multiple applicable dimensions and hard failures.

## Evaluation Score Publishes Knowledge

Evaluation supplies evidence for governance. Only a scoped PublicationDecision can make a version eligible.

## Use Raw Production Content by Default

Use synthetic/minimized data unless a separately authorized policy permits production-derived evidence.

## Tune to One Evaluator

Single-model or narrow-rubric optimization can hide regressions. Use versioned diverse scenarios, deterministic controls, calibration, and outcome evidence.

## Gap Signal Automatically Changes Live Knowledge

Signals create proposals and governed work. They do not modify sources, policies, indexes, or agent behavior directly.

---

# Related Documents

| Document | Relationship |
|---|---|
| 04_KNOWLEDGE_CONTENT_PROCESSING.md | Supplies representation-quality and uncertainty evidence. |
| 05_KNOWLEDGE_INDEXING_AND_RETRIEVAL.md | Supplies retrieval, citation, outcome, and profile evidence. |
| 06_KNOWLEDGE_LIFECYCLE_AND_VERSIONING.md | Defines quality-result effects on lifecycle and versioning. |
| 08_KNOWLEDGE_GOVERNANCE_AND_PUBLICATION.md | Uses quality evidence for review and publication decisions. |
| 02_AGENT_PLATFORM/33_AGENT_EVALUATION_FRAMEWORK.md | Defines agent-response evaluation distinct from Knowledge evaluation. |
| 13_OBSERVABILITY_PLATFORM | Provides shared telemetry infrastructure. |
| 14_TESTING_PLATFORM | Provides shared deterministic-test infrastructure. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Knowledge quality, coverage, citation, freshness, evaluation, and governed-improvement model. |
| 1.1 | 2026-08-06 | Finalized and approved the Knowledge Quality and Evaluation model. |

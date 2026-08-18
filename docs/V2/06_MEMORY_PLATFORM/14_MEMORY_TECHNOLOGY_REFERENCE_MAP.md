# 14_MEMORY_TECHNOLOGY_REFERENCE_MAP

**Version:** 1.2
**Status:** Approved
**Owner:** Memory Platform Owner
**Phase:** Memory Platform

---

# Overview

This document maps the bounded technical roles needed by Memory Platform to technology categories, standards, and approved references. It preserves stable Memory contracts for subject-bound context, evidence, admission, policy/use basis, retrieval, lifecycle, suppression, deletion, and audit while keeping technology choices replaceable.

It is not a vendor selection, procurement list, or implementation mandate. A technology may support Memory only after its reference and use are evaluated through the Architecture Reference Registry and, when material, the Decision Log.

---

# Purpose

The map prevents a convenient database, vector index, model, CRM connector, identity provider, cache, or analytics tool from becoming the accidental owner of durable personal memory. It gives implementers a durable selection and migration framework without reopening approved ownership boundaries.

---

# Scope and Boundaries

| Topic | Owner |
|---|---|
| Memory logical entities, evidence, admission, profile semantics, use constraints, retrieval outcomes, lifecycle, deletion requirements, and domain acceptance criteria | Memory Platform |
| Tenant/organization/membership/entitlement/configuration and API-edge capabilities | 16_PLATFORM_FOUNDATION |
| Identity, authorization, secrets, cryptography, audit infrastructure, compliance controls, and incident governance | 09_SECURITY_PLATFORM |
| Connector implementation, external API mechanics, and workflow execution | 07_INTEGRATION_PLATFORM |
| Storage, queues, caches, indexes, backup, physical deletion, and data-service operations | 08_DATA_PLATFORM |
| Channel delivery, channel identities, and delivery opt-in/opt-out | 04_VOICE_PLATFORM and 17_DIGITAL_CHANNEL_PLATFORM |
| Shared telemetry and test infrastructure | 13_OBSERVABILITY_PLATFORM and 14_TESTING_PLATFORM |

Memory defines the logical contract and acceptance evidence for technology used in its domain. It does not acquire a technology, operate shared infrastructure, or absorb another platform's business capability.

---

# Technology Principles

## Contract Before Technology

Canonical logical identifiers, subject binding, evidence, admission/lifecycle decisions, policy/use-basis references, retrieval outcomes, invalidation, deletion targets, and audit events are specified before an implementation is selected. Provider IDs, SDK objects, storage keys, cache keys, and index document IDs remain internal references.

## No Default Commitment

Naming a category or external reference does not approve a product. Only current, approved references in `00_CONTROL/13_ARCHITECTURE_REFERENCE_REGISTRY.md` may inform implementation. A decision record is required when a choice materially affects privacy, security, data portability, cost, participant impact, retrieval behavior, or another platform.

## Approved Shared Data Foundation

Supabase-managed PostgreSQL and the `pgvector` extension are approved shared data-stack references for Data Platform-managed persistence and derived vector representations. Memory may use them only behind subject-, tenant-, purpose-, and lifecycle-governed contracts; they do not establish personal-memory truth, policy/use basis, authorization, or deletion completion.

## Technology Is Not Authority

No model decides a fact is durable, no CRM sync decides policy, no index decides eligibility, no cache establishes truth, no provider decides deletion completion, and no channel opt-in grants Memory capture/use. Memory rules remain authoritative even when a product offers a similarly named feature.

## Narrow Adapters and Stable Contracts

Providers, parsers, extractors, indexes, CRM systems, and model services are accessed through narrow, versioned adapters. The adapter exposes only required capability, request/result, error, provenance, usage, data-class, and deletion/invalidation information; it does not leak provider control planes into public Memory contracts.

## Portability and Rebuildability

Canonical Memory records, revisions, evidence, admission/lifecycle decisions, use constraints, policies, and deletion evidence must be exportable independently of a provider. Embeddings, summaries, search documents, caches, and provider representations are derived and must be rebuildable or removable from canonical eligible state.

## Safety and Exit Are Selection Criteria

Functional fit alone is insufficient. Selection evaluates tenant/subject isolation, purpose/use basis, classification, residency, provider retention/training, deletion confirmation, reliability, observability, cost, support, licensing, migration, and incident response.

---

# Technology Role Map

| Bounded role | Possible technology category or standard | Required Memory contract/evidence | Must not own |
|---|---|---|---|
| Candidate source adapter | Approved CRM, case, profile, interaction, file, API, event, or interface adapter; API/webhook standards where applicable. | Source authority, field permission, origin integrity, evidence locator, idempotency, freshness, callback verification, and minimal payload. | Admission, policy/use basis, canonical Memory truth, or lifecycle. |
| Evidence capture and normalization | Deterministic schema validation, transformation, redaction, document/parser/OCR tools, and isolated worker runtime. | Reproducible transformation version, classification, minimization, locator preservation, uncertainty, and adversarial-input behavior. | Identity, consent/use decision, durable admission, or provider trust. |
| Admission/policy evaluation | Rule/policy engine, workflow/review queue, and controlled decision service. | Versioned policy/use-basis inputs, risk tier, separation of duties, reason code, idempotency, and immutable decision evidence. | Enterprise authorization mechanism, legal authority, or automatic high-risk approval. |
| Personal-context enrichment | Classification, normalization, language, entity, embedding, or confidence services behind adapters. | Provider/method/version, allowed data class/egress, evaluation evidence, fallback, cost/rate bounds, and no hidden reasoning persistence. | Truth, participant preference, eligibility, or durable memory admission. |
| Canonical Memory persistence | Data Platform-approved relational, object, event, or append-only storage services. | Logical schema, revision/decision immutability, tenant/subject boundaries, retention, export, backup/recovery, and physical deletion support. | Memory semantics, governance judgment, or cross-platform ownership. |
| Retrieval representation | Structured, lexical, vector, hybrid, or graph index technology. | Tenant/subject/purpose filters, canonical revalidation, representation lineage, freshness, invalidation/deletion, safe outcome, and benchmark evidence. | Authorization, policy/use basis, lifecycle truth, or citation/evidence completeness. |
| Cache, queue, and asynchronous work | Approved cache, broker, scheduler, worker, and dead-letter services. | Tenant/subject/purpose scoped keys/envelopes, idempotency, expiry, ordering, retry, invalidation, reconciliation, and non-use on uncertainty. | Durable truth, deletion completion, authorization, or entitlement. |
| Access, identity, and secrets | Security Platform-approved identity, policy, key, secret, and cryptography services. | Server-resolved access context, least privilege, subject relationship, audit, rotation, emergency revocation, and scoped provider credentials. | Memory category/purpose policy, lifecycle decision, or participant preference semantics. |
| Contract/schema boundary | Versioned API/event schemas; OpenAPI, JSON Schema, and AsyncAPI where appropriate. | Explicit outcome vocabulary, correlation, access context requirements, compatibility, error privacy, and consumer contract tests. | Direct database coupling or provider-specific public identity. |
| Telemetry and audit export | Observability/Security-approved logs, metrics, traces, audit export, and secure diagnostics. | Redaction/minimization, correlation, retention, access tiers, alerting, and no raw-memory default. | Canonical Memory record, policy decision, or general profile browse access. |
| Evaluation and testing support | Approved fixtures, runners, compatibility/load/adversarial tools, and evaluation harnesses. | Governed datasets, repeatability, data cleanup, result/version capture, release evidence, and no production-control bypass. | Automatic admission, policy broadening, or operational participant profiling. |

Combining categories in one deployment does not combine their ownership. Combined products must still satisfy the strictest applicable access, lifecycle, deletion, retention, provider, and recovery requirements.

---

# Required Technology Controls

## Provider and Adapter Control

Every external provider, parser, CRM connector, model service, index, or workflow has a named adapter owner, supported capability set, input/output classification rule, tenant/subject/purpose validation, timeout/retry/fallback policy, telemetry contract, deletion/invalidation behavior, and removal path. Provider SDK types, opaque policy decisions, record IDs, and raw error payloads do not cross the public Memory contract.

## Derived Representation Control

Embeddings, extracted values, normalized payloads, summaries, search documents, indexes, caches, queues, exports, provider copies, and UI projections are derived representations. Each carries the canonical Memory revision, tenant, subject binding, constraint/policy version as needed, classification, freshness, and invalidation/deletion linkage required to stop use after correction, suppression, expiry, withdrawal, or deletion.

## External Data and Model Control

Before any Memory content reaches an external service, the accountable owners establish permitted data classes, purpose, tenant/region/residency, subject scope, minimization/transformation, provider retention/training terms, credential scope, incident response, deletion process, subprocessor constraints, and evidence of current approval. If a condition cannot be proven, that capability is unavailable for that data.

## Lifecycle and Deletion Control

Technology must support—or be bounded by an adapter that supports—immediate logical non-use, target tracking, invalidation, physical deletion/disposition, acknowledgement/exception evidence, retry/reconciliation, backup/restore revalidation, and no unauthorized resurrection. A provider's best-effort deletion statement is not completion evidence unless it satisfies the approved policy requirement.

## Failure and Safe-Degradation Control

Selection documents how timeout, partial result, policy/access outage, stale representation, provider failure, cache loss, index lag, duplicate event, dependency recovery, and budget exhaustion affect explicit Memory outcomes. A fallback preserves tenant, subject, purpose, policy/use basis, classification, lifecycle, freshness, and representation limits—or it is disabled.

---

# Selection and Adoption Process

| Gate | Required outcome |
|---|---|
| Define the bounded role | Identify capability, logical contract, owner, data classes, non-ownership constraints, and risk tier. |
| Check approved references | Use current official references from the Architecture Reference Registry; community examples are inspiration, not authority. |
| Evaluate candidates | Compare contract fit, privacy/security, isolation, residency, provider terms, deletion, reliability, observability, cost, portability, support, and exit. |
| Prove critical behavior | Run contract, tenant/subject, purpose, adversarial, egress, invalidation/deletion, recovery, and quality tests appropriate to risk. |
| Record the decision | Update the Registry and create a Decision Log entry for material, long-lived, or cross-platform choices. |
| Adopt safely | Version adapter/contract, define migration/rollback, set alerts/runbooks/ownership, and release in controlled stages. |
| Reassess | Re-evaluate on provider, policy, cost, security, privacy, data-class, legal, workload, contract, or lifecycle change. |

The Architecture Reference Registry records technical guidance; this document records role and constraints; the Decision Log records durable selection rationale. None substitutes for operational readiness or test evidence.

---

# Evaluation Criteria

| Dimension | Required question |
|---|---|
| Contract fit | Can it preserve subject-bound, versioned evidence/decisions, explicit outcomes, and lifecycle without leaking provider semantics? |
| Privacy/security | Can it enforce permitted data classes, purpose, tenant/subject isolation, scoped credentials, encryption/protection, audit, deletion, and incident response? |
| Admission integrity | Can it preserve evidence, idempotency, review/separation-of-duties, conflict behavior, and no automatic high-risk memory? |
| Retrieval integrity | Can it enforce eligibility before relevance, controlled filters, minimization, currentness, and result privacy? |
| Lifecycle integrity | Can it invalidate/suppress/delete all derived state and prove target completion/exception without resurrection on restore/replay? |
| Reliability | Are timeout, retry, ordering, idempotency, recovery, capacity, reconciliation, and safe-degradation behaviors known and testable? |
| Operability | Can it expose health, latency, backlog, target state, cost, usage, and correlation without disclosing personal values? |
| Portability | Can canonical data/evidence be exported and derived state rebuilt/migrated within the approved recovery objective? |
| Commercial/legal fit | Are licensing, support, provider terms, regional availability, data rights, retention, and cost growth acceptable for the intended scope? |
| Change safety | Can versions coexist, policy/data contracts migrate, dependencies roll back, and consumers remain safe through a controlled change? |

---

# Technology Change and Exit Requirements

A technology introduction, replacement, material upgrade, or configuration change requires a documented change plan when it affects a public contract, data class, provider egress, stored/derived representation, admission behavior, retrieval eligibility, lifecycle/deletion, tenant/subject boundary, retention, recovery, or operating cost.

The plan includes:

- affected canonical/derived data and a migration, rebuild, invalidation, or deletion strategy;
- contract compatibility and consumer communication;
- dual-run, shadow, staged, or canary evidence where appropriate;
- re-evaluation of provider terms, residency, retention/training, and data-rights behavior;
- rollback trigger, method, retained evidence, and safe no-use behavior;
- correction/suppression/deletion and source/provider acknowledgement behavior during transition;
- updated tests, quality evidence, dashboards, alerts, runbooks, ownership, and Decision Log record; and
- an exit plan that preserves canonical records, participant-rights outcomes, and auditable lifecycle history.

No migration may silently broaden purpose, classification, access, egress, retention, or representation; drop evidence; weaken deletion; or resurrect restricted/deleted memory.

---

# Anti-Patterns

- Exposing provider, index, cache, CRM, or SDK identifiers as canonical Memory identity.
- Treating model output, CRM update, channel opt-in, parser success, or similarity score as authority to admit or use durable personal memory.
- Making an embedding, cache, index, provider, or export the only surviving copy of a Memory decision or evidence record.
- Sending an entire profile or transcript to a provider because an adapter lacks a minimum-necessary contract.
- Relying on provider retention/deletion claims without target-specific policy evidence and reconciliation.
- Treating a generic tenant filter as adequate subject/purpose/representation isolation.
- Hiding a technology/provider/configuration change as an internal refactor when it changes participant impact, egress, retrieval, or lifecycle behavior.
- Reusing production Memory content in experiments, benchmarks, logs, or support tooling without specific governed purpose and controls.

---

# Related Documents

| Document | Relationship |
|---|---|
| 00_CONTROL/13_ARCHITECTURE_REFERENCE_REGISTRY.md | Registers approved external technical references. |
| 00_CONTROL/08_DECISION_LOG.md | Records material technology decisions. |
| 02_MEMORY_DOMAIN_MODEL.md | Defines canonical identifiers, entities, and provider-independent truth. |
| 03_MEMORY_CAPTURE_AND_ADMISSION.md | Defines controlled candidate/admission behavior. |
| 05_MEMORY_RETRIEVAL_AND_CONTEXT.md | Defines eligibility and bounded context outcomes. |
| 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md | Defines invalidation, deletion, and recovery requirements. |
| 07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md | Defines tenant/subject/purpose/representation boundaries. |
| 10_MEMORY_SECURITY_AND_PRIVACY.md | Defines privacy, security, and provider control requirements. |
| 12_MEMORY_RELIABILITY_AND_FAILURE_HANDLING.md | Defines safe degradation and reconciliation. |
| 13_MEMORY_TESTING.md | Defines technology adoption/change test evidence. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Memory technology reference map with bounded roles, provider controls, selection criteria, portability, and exit requirements. |
| 1.1 | 2026-08-06 | Finalized after review for completeness, ownership overlap, and long-term maintainability. |
| 1.2 | 2026-08-06 | Recorded Supabase-managed PostgreSQL and pgvector as the approved shared data foundation for governed Memory use. |

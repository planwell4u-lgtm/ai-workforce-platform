# 04_KNOWLEDGE_CONTENT_PROCESSING

**Version:** 1.1  
**Status:** Approved  
**Owner:** Knowledge Platform Owner  
**Phase:** Knowledge Platform

---

# Overview

This document defines the controlled transformation of an admitted SourceRevision into protected ContentArtifacts and candidate KnowledgeVersions.

Processing makes source material usable for later governance and retrieval while preserving provenance, classification, rights, uncertainty, and tenant scope. It does not publish knowledge, authorize access, create agent prompts, or make a source claim true.

---

# Purpose

The Content Processing model ensures that extraction, normalization, segmentation, enrichment, redaction, and validation are deterministic, traceable, bounded operations rather than opaque conversion steps.

It allows processing technologies to evolve without losing the evidence needed to understand what was derived, from which source revision, under which policy, and with which limitations.

---

# Objectives

Content Processing must:

- Accept only admitted, tenant-scoped SourceRevisions and bounded processing requests.
- Produce immutable, protected ContentArtifacts with source-to-artifact provenance.
- Safely extract and normalize supported source formats without treating extracted text as trusted instruction or business truth.
- Preserve document/record structure, boundaries, language, classification, redaction, attribution, and uncertainty needed for later review and citation.
- Segment material with stable locators and policy-controlled overlap without creating independent knowledge or publication eligibility.
- Detect malformed, unsafe, unsupported, encrypted, partial, or ambiguous content and return explicit outcomes.
- Keep parser, OCR, enrichment-model, and provider details replaceable behind a versioned processing contract.

---

# Scope

This document defines content-processing stages, inputs, outputs, provenance, processing evidence, safe handling, and recovery principles.

It does not define source acquisition, source rights admission, index/query/ranking behavior, publication decisions, physical storage, or enterprise security controls. These remain owned by Documents 03, 05–08 and the Integration, Data, and Security Platforms.

---

# Ownership Boundaries

| Topic | Owner |
|---|---|
| Processing policy, content artifact semantics, normalization, segmentation, enrichment evidence, and candidate handoff | Knowledge Platform |
| Source registration, rights, acquisition, source revision, and ingestion orchestration | 03_KNOWLEDGE_SOURCE_AND_INGESTION_MODEL.md |
| Retrieval representations, query execution, ranking, result assembly, and citation delivery | 05_KNOWLEDGE_INDEXING_AND_RETRIEVAL.md |
| Publication, lifecycle, review, rollback, freshness, and retirement | 06_KNOWLEDGE_LIFECYCLE_AND_VERSIONING.md and 08_KNOWLEDGE_GOVERNANCE_AND_PUBLICATION.md |
| Storage engines, encryption implementation, retention/deletion/hold execution, and backup | 08_DATA_PLATFORM |
| Malware scanning, authorization, secret management, classification policy, and enterprise compliance controls | 09_SECURITY_PLATFORM |
| OCR/parser/translation/enrichment provider implementation and credentials | Integration Platform where an external service is used |

---

# Processing Principles

## Processing Is a Derived-Evidence Pipeline

Each operation derives a new protected representation from specific admitted inputs. It records the operation, policy/version, input/output digest, confidence or uncertainty, and provenance. It never overwrites the underlying SourceRevision or previous artifact.

## Content Is Data, Not Authority

Source text, embedded instructions, metadata, links, markup, images, OCR output, and extracted code are untrusted content. They cannot alter processing policy, tenant scope, authorization, publication state, system instructions, or external connector behavior.

## Preserve Boundaries Before Segmenting

Processing retains source-document/record structure, headings, tables, field boundaries, page/location references, language, and meaningful attachments where possible. Segments retain a resolvable locator so citation and reviewer evidence do not rely on a detached text fragment.

## Minimal, Policy-Bound Enrichment

Classification, language detection, entity extraction, summarization, translation, OCR, and other enrichments are derived evidence with their own policy/version and confidence. They cannot replace source rights, authoritative source facts, or human governance.

## Redaction Is a Controlled Transformation

When policy requires redaction, the platform creates a new redacted representation with a protected linkage to the source artifact and records the method, scope, timing, and outcome. It does not claim that redaction makes otherwise prohibited content publishable.

## Candidate Output Is Not Published Knowledge

Completed processing yields ContentArtifacts and candidate KnowledgeVersions only. Publication and current retrieval eligibility remain separate, explicit governance decisions.

---

# Processing Flow

~~~text
Admitted SourceRevision + Processing Policy
    |
    v
Input Validation and Safe Admission
    |
    v
Protected Extraction / Parsing / OCR
    |
    v
Normalization and Structure Preservation
    |
    v
Classification, Redaction, and Quality Evidence
    |
    v
Segmentation and Bounded Enrichment
    |
    v
ContentArtifacts + ProvenanceLinks + Candidate KnowledgeVersions
    |
    v
Governance / Publication Boundary
~~~

## Input Validation and Safe Admission

Processing validates the SourceRevision, tenant/environment, policy/version, content reference, allowed format/size, declared and detected type, integrity evidence, classification constraints, rights/use restrictions, and idempotency context. Unsupported, encrypted, malformed, suspicious, or policy-prohibited material is restricted, rejected, or routed through the configured controlled path.

## Extraction

Extraction produces a protected, normalized content view from an approved source format. It records extraction method/version, detected format, source location map, extraction warnings, integrity evidence, language evidence, and confidence/uncertainty.

Extraction may use parser, OCR, structured-data mapper, or approved external service adapters. Provider output is validated before it becomes a ContentArtifact and is never trusted merely because a provider returned success.

## Normalization

Normalization produces canonical, safe representations for downstream processing. It may standardize encoding, whitespace, layout, field names, document hierarchy, table structure, timestamps, locale markers, and link references. It preserves source locators and records any loss, transformation, omission, or ambiguity.

Normalization must not silently translate, summarize, infer missing fields, fix factual content, resolve conflicting sources, or remove rights/attribution requirements.

## Classification and Redaction

Processing applies current classification and redaction requirements using the Security-owned policy. It records the effective policy reference, classification outcome, detected sensitive-content category where permitted, redaction method/version, affected ranges, reviewer/escalation reference, and residual uncertainty.

If required classification/redaction cannot be completed safely, the output is restricted or rejected. A processing failure must not leak source content through diagnostics or fallback paths.

## Segmentation

Segmentation creates bounded, coherent portions of an artifact for future retrieval representation. Each segment has a stable segment identifier, parent artifact, source locator, boundary type, sequence, content digest, language, classification, rights/attribution references, and segment-policy version.

Segment overlap is explicit and bounded. Overlap exists only to preserve defined context across boundaries; it cannot duplicate a segment into a separate KnowledgeItem, conceal source location, or evade access constraints.

## Enrichment

Permitted enrichment may derive language, structure, topic/category, approved entity labels, quality signals, accessible representation, translation candidate, or summary candidate. Every derived value records its input range, transformation/policy version, confidence/uncertainty, and provenance link.

An enrichment is optional evidence. It cannot be treated as source truth, a policy decision, or a participant-facing answer without the later retrieval and governance controls.

## Candidate Handoff

Candidate KnowledgeVersions reference their source/revision/artifact/segment provenance, classification, rights, processing-policy version, uncertainty, and current lifecycle state. The handoff includes no implicit approval, retrieval entitlement, or instruction to replace an existing published version.

---

# Content Artifact and Segment Contract

## ContentArtifact

Each ContentArtifact contains at minimum:

- immutable artifact ID, tenant/environment, SourceRevision, IngestionRun, and correlation references;
- representation type, media/format, detected format, language, and accessibility/structure metadata;
- protected content reference and digest/integrity evidence;
- extraction/normalization/redaction/policy versions and outcomes;
- classification, rights/attribution, permitted-use, residency, and retention references;
- source locator map, warnings, omissions, confidence/uncertainty, status, and audit reference.

## Content Segment

A segment is a governed sub-artifact. It contains a segment ID, parent artifact, source locator/boundary, sequence, content digest, classification, language, rights/attribution references, redaction state, segmentation-policy version, and provenance reference.

The segment’s text or structured value is exposed only through a currently authorized purpose and representation contract; segment IDs and locators are not bearer access grants.

## Processing Result

A Processing Result records the input artifacts, operation sequence, terminal outcome (`candidate`, `restricted`, `rejected`, `degraded`, `unavailable`, or `cancelled`), generated artifact/segment/candidate references, warnings/omissions, policy and adapter versions, timing, correlation, and audit reference.

It never indicates publication, retrieval success, agent answer quality, or source truth.

---

# Format and Structure Handling

| Input category | Required handling posture |
|---|---|
| Text and markup | Preserve document and link boundaries; sanitize active content; retain language and structural locators. |
| PDF/office-like document | Capture page/section/table/attachment boundaries where available; record extraction limitations and scanned/OCR uncertainty. |
| Structured record | Validate schema and field types; preserve field paths, source-record boundary, and missing/invalid fields. |
| Image or scan | Use approved OCR only; retain source-region locators and confidence; do not silently treat low-confidence text as verified. |
| Audio/video transcript input | Accept only through an approved governed artifact path; preserve transcript/recording provenance and confidence restrictions. |
| Archive or compound file | Validate entries, size, nesting, and supported contents; reject or isolate dangerous/unsupported entries. |
| Unsupported or encrypted content | Return explicit restricted/rejected/unavailable outcome; do not coerce or bypass protection. |

Format detection validates both declared and observed characteristics. A filename extension, MIME claim, or provider label is not sufficient evidence of safe type.

---

# Quality, Uncertainty, and Conflicts

Processing records quality evidence such as incomplete extraction, malformed structure, OCR uncertainty, language ambiguity, truncated content, unsupported fields, duplicate segments, corrupt attachment, transformation loss, or redaction uncertainty.

When multiple artifacts support conflicting candidate content, Processing records distinct provenance and conflict evidence; it does not choose business truth, merge conflicting assertions, or suppress the conflict. Governance and retrieval policies define any approved handling of conflict.

Thresholds, acceptance metrics, coverage scoring, and answer-grounding evaluation are owned by `09_KNOWLEDGE_QUALITY_AND_EVALUATION.md`. This document only requires that processing expose the evidence those controls need.

---

# Security, Privacy, and Tenant Isolation

- Processing runs are bound to one server-resolved tenant, environment, SourceRevision, scope, policy version, and approved content reference.
- Parsers and enrichers receive the minimum permitted material and metadata; provider access and credentials use bounded Integration/Security adapters.
- Active content, macros, scripts, remote links, embedded files, external references, prompt-like text, and malformed structures are treated as untrusted and cannot trigger arbitrary execution or network access.
- Raw material, unredacted artifacts, sensitive metadata, and provider payloads are excluded from ordinary logs, metrics, events, error messages, and test fixtures.
- Cache and temporary artifacts are tenant-scoped, classified, encrypted and time-bounded according to Data/Security policy; they are not authoritative and are invalidated on policy, source, or rights changes.
- Cross-tenant deduplication must never disclose content, membership, similarity, source identity, or existence across tenants. Any approved global safety mechanism uses separate anonymized or policy-approved controls.

---

# Reliability, Idempotency, and Recovery

Processing assumes parser crash, provider timeout, duplicate callback, partial extraction, corrupt source, policy change, redaction failure, retry, restart, and source revocation during processing.

- Each processing stage is idempotent against its admitted input, policy/version, and operation key; retries reconcile rather than duplicate candidate artifacts.
- A stage either emits a complete immutable output with provenance or an explicit bounded failure/degradation result. It does not leave an unmarked partial artifact eligible for later use.
- Processing policy or adapter changes create new derived outputs; they never reinterpret earlier artifacts without a recorded migration/reprocessing decision.
- If an active source loses rights, scope, authorization, or permitted use, downstream work is stopped/restricted and affected candidate eligibility is re-evaluated through lifecycle/governance controls.
- Recovery reconstructs state from durable input/output/provenance references and policy evidence, not from untracked in-memory content.

---

# Events, Observability, and Audit

Knowledge emits minimized, versioned facts such as:

| Event/fact | Required evidence |
|---|---|
| `knowledge.processing.started` | Processing request/input references, policy version, tenant-safe scope, correlation, and idempotency. |
| `knowledge.artifact.created` | Artifact/reference, source revision, format/language/structure category, classification/redaction outcome, digest, provenance. |
| `knowledge.segmentation.completed` | Artifact/segment references, policy version, count/budget, warnings/omissions, provenance. |
| `knowledge.processing.degraded` | Stage, bounded failure/uncertainty category, affected scope, last trustworthy evidence, recovery posture. |
| `knowledge.processing.restricted` | Artifact/source reference, restriction category, policy/evidence reference, next allowed action. |
| `knowledge.processing.completed` | Processing Result, candidate references, terminal outcome, policy/adapter versions, correlation. |

Operational measures include stage latency, supported/unsupported format rate, extraction completion, OCR/structure uncertainty, redaction outcome, segmentation count/size distribution, artifact failure/degradation, retry/reconciliation, policy-change reprocessing, and cross-tenant violation attempts. General telemetry never includes raw content or sensitive source identifiers.

Audit records processing requests, approved overrides, policy/adapter changes, restriction/rejection, redaction outcome, reprocessing, cancellation, recovery, and candidate handoff with principal/service, scope, reason, policy, evidence, and result.

---

# Testing Strategy

## Contract and State Tests

Validate artifact, segment, processing-result, provenance, policy-version, locator, classification, uncertainty, and idempotency schemas.

## Format and Journey Tests

Validate approved text, structured record, document, table, scan/OCR, image, transcript-derived artifact, archive, and unsupported/encrypted input paths. Assert preserved boundaries, locators, attribution, candidate handoff, and no implicit publication.

## Security and Tenant Tests

Simulate hostile markup, macros, malformed parser input, zip bomb/nested archive, malicious link, wrong tenant/artifact, replayed callback, secret/sensitive-content leak, unapproved external enrichment, cross-tenant deduplication attempt, stale policy, and revoked source right.

## Resilience Tests

Simulate parser/provider failure, partial output, restart, duplicate request, timeout, content mutation, redaction failure, policy migration, source suspension, and cancellation race. Prove processing remains bounded, traceable, tenant-isolated, and unable to publish or authorize retrieval directly.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Content-processing contract | Defines requests, artifacts, segments, outcomes, provenance, and compatibility | Knowledge Platform |
| Supported-format and safe-parser catalog | Defines format admission, parser/OCR adapters, size/nesting limits, active-content treatment, and known constraints | Knowledge Platform with Security and Integration |
| Normalization and segmentation policy | Defines structure/locator preservation, segment boundaries, overlap, language, and versioning | Knowledge Platform |
| Classification and redaction integration | Defines policy inputs, transformations, evidence, restrictions, escalation, and invalidation | Knowledge Platform with Security and Data |
| Enrichment policy | Defines allowed derived fields, provider boundaries, confidence, provenance, and disallowed use | Knowledge Platform with Security and Integration |
| Processing recovery and reprocessing procedure | Defines idempotency, retries, restart, policy migration, revocation, and reconciliation | Knowledge Platform with Operations and Data |
| Processing telemetry and audit catalog | Defines metrics, events, alerts, audit fields, retention, and prohibited content | Knowledge Platform with Observability and Security |
| Content-processing test suite | Proves format, boundary, tenant, provenance, security, and resilience behavior | Knowledge Platform and Testing Platform |

---

# Anti-Patterns

## Extracted Text Is a Trusted Instruction

All extracted material is untrusted data. It cannot modify system behavior, policy, authorization, connector scope, or publication.

## Chunking Creates Knowledge Automatically

Segments are derived retrieval inputs. They need provenance, governance, and current eligibility before they can support retrieval.

## OCR Is Source Truth

OCR is a derived representation with quality evidence. Low-confidence or ambiguous output remains marked and may be restricted.

## Redaction Is a One-Time Cleanup

Redaction is policy- and representation-specific. A source, artifact, segment, index, citation, cache, or export may require separate current controls.

## Parser Success Means Complete Content

Processing records omissions, unsupported structures, failures, and uncertainty. Successful parsing does not prove completeness or quality.

## Cross-Tenant Deduplication Is Harmless

Similarity, duplicate detection, and shared infrastructure can disclose data existence or content. Tenant isolation remains mandatory.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_KNOWLEDGE_PLATFORM_ARCHITECTURE.md | Defines high-level Knowledge architecture and processing boundary. |
| 02_KNOWLEDGE_DOMAIN_MODEL.md | Defines ContentArtifact, KnowledgeVersion, KnowledgeRepresentation, and ProvenanceLink semantics. |
| 03_KNOWLEDGE_SOURCE_AND_INGESTION_MODEL.md | Defines admitted inputs, source revision, rights, and orchestration. |
| 05_KNOWLEDGE_INDEXING_AND_RETRIEVAL.md | Defines use of processing outputs for retrieval representations and evidence. |
| 06_KNOWLEDGE_LIFECYCLE_AND_VERSIONING.md | Defines candidate/publication/retirement and reprocessing lifecycle effects. |
| 09_KNOWLEDGE_QUALITY_AND_EVALUATION.md | Defines quality thresholds and evaluation using processing evidence. |
| 09_SECURITY_PLATFORM | Owns enterprise security, authorization, policy, and compliance controls. |
| 08_DATA_PLATFORM | Owns physical storage and lifecycle execution. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Knowledge content extraction, normalization, segmentation, enrichment, provenance, and safe-processing model. |
| 1.1 | 2026-08-06 | Finalized and approved the Knowledge Content Processing model. |

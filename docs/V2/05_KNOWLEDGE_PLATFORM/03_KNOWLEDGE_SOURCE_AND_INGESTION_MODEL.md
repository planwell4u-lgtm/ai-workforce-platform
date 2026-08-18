# 03_KNOWLEDGE_SOURCE_AND_INGESTION_MODEL

**Version:** 1.1  
**Status:** Approved  
**Owner:** Knowledge Platform Owner  
**Phase:** Knowledge Platform

---

# Overview

This document defines how the Knowledge Platform registers approved knowledge sources, validates their provenance and rights, and coordinates governed ingestion into candidate knowledge.

It treats external content, connectors, operator submissions, callbacks, and refresh signals as untrusted evidence. Successful acquisition or processing never publishes knowledge, authorizes retrieval, or changes agent behavior on its own.

---

# Purpose

The Source and Ingestion Model provides a controlled, traceable path from a proposed business source to a candidate KnowledgeVersion.

It makes source ownership, permitted use, freshness, ingestion intent, processing evidence, failure, and reviewability explicit before material can enter the publication lifecycle.

---

# Objectives

The model must:

- Admit only authorized, tenant-scoped source registrations with accountable ownership and rights evidence.
- Keep external acquisition and credentials behind Integration and Security boundaries.
- Capture immutable SourceRevision and IngestionRun evidence for every processing attempt.
- Support initial ingestion, approved refresh, partial processing, retries, cancellation, reconciliation, and retirement without duplicate publication.
- Validate source class, scope, provenance, classification, rights, integrity, and current policy before a candidate proceeds.
- Produce explicit candidate, restricted, rejected, unavailable, degraded, or uncertain outcomes.
- Preserve source-to-artifact provenance while minimizing source contents in cross-platform contracts and telemetry.

---

# Scope

This document defines source admission, registration, acquisition coordination, ingestion orchestration, refresh, source-revision handling, and the resulting contracts and evidence.

It does not define detailed content extraction and segmentation, retrieval/index behavior, publication approval workflow, lifecycle/retention execution, enterprise authorization implementation, or connector code. Those belong respectively to Documents 04–08 and the Data, Security, and Integration Platforms.

---

# Ownership Boundaries

| Topic | Owner |
|---|---|
| Source registration, source classes, source/provenance/rights semantics, ingestion intent, source revision, and ingestion evidence | Knowledge Platform |
| Connector implementation, source crawling/fetching, webhook transport, external API workflow, and external OAuth/API credentials | 07_INTEGRATION_PLATFORM with 09_SECURITY_PLATFORM |
| Source-content extraction, normalization, segmentation, enrichment, redaction representation, and candidate generation | 04_KNOWLEDGE_CONTENT_PROCESSING.md |
| Candidate review, publication, rollback, suspension, and retirement authority | 06_KNOWLEDGE_LIFECYCLE_AND_VERSIONING.md and 08_KNOWLEDGE_GOVERNANCE_AND_PUBLICATION.md |
| Storage, backup, deletion/hold execution, and physical data residency | 08_DATA_PLATFORM |
| Identity, authorization, secrets, classification policy, compliance controls, and security monitoring | 09_SECURITY_PLATFORM |
| Agent decisions, prompt assembly, and participant-facing answer/action behavior | 02_AGENT_PLATFORM |

---

# Source Principles

## Registration Precedes Acquisition

Knowledge may request external acquisition only for a registered, approved source scope. A connector, URL, document upload, webhook, or API response does not become a source merely by reaching the platform.

## Rights and Provenance Are Current Evidence

Source rights, attribution, permitted use, origin, classification, and freshness expectations are recorded as evidence and re-evaluated at material lifecycle changes. A prior successful ingestion does not indefinitely prove that a source remains usable.

## Acquisition Is Bounded and Replaceable

Integration obtains source material through a bounded contract. Knowledge specifies what is required and records the outcome; it does not implement provider-specific crawling, callbacks, tokens, pagination, or credential exchange.

## Ingestion Produces Candidates, Not Live Knowledge

An accepted SourceRevision and completed IngestionRun may create ContentArtifacts and candidate KnowledgeVersions only. Governance separately decides whether any candidate is published.

## Refresh Is a New Observation

Each refresh creates or reconciles a new SourceRevision. It does not mutate previously observed material, silently replace a published version, or retain removed content merely because it was previously available.

## Uncertainty Is Preserved

Missing rights, partial acquisition, unclear revision identity, low-integrity evidence, extraction uncertainty, or source unavailability are recorded as bounded outcomes. The platform does not convert them into assumed source validity.

---

# Source Classes and Admission Profile

Source classes determine the allowed acquisition methods, proof required, content constraints, freshness expectations, and reviewer roles. They do not grant access or publication eligibility by themselves.

| Source class | Examples | Minimum admission evidence |
|---|---|---|
| Managed document | Approved policy, handbook, product sheet, uploaded business document | Tenant owner, submitter authority, origin/provenance, rights/use, classification, intended scope. |
| Managed structured source | Product/service catalog, approved FAQ record, policy table | Accountable system/business owner, schema/scope, source authority, rights/use, refresh expectation. |
| Website or web collection | Approved public/private site section | Domain/scope approval, acquisition authority, crawl boundaries, rights/use, refresh and exclusion rules. |
| Connected business system | Approved CRM, CMS, file repository, or internal knowledge base | Connector authorization reference, system owner, object/scope filter, rights/use, change/refresh expectations. |
| Operator-curated source | Manually authored or assembled knowledge material | Author/reviewer accountability, basis/provenance, intended use, classification, approval scope. |
| Imported archive or migration | Controlled historical corpus transfer | Migration authority, origin inventory, rights/classification mapping, integrity evidence, rollback and retention plan. |

New source classes require an approved admission profile before use. A generic connector or file type must not be treated as a catch-all source class.

---

# Source Registration Model

## Registration Request

An authorized registration request contains:

- server-resolved `tenantId` and `environmentId`;
- requested source class and bounded scope;
- protected origin or submission reference;
- source owner and requesting principal/service references;
- intended business use, audience, and classification constraints;
- rights, attribution, permitted-use, and restriction evidence;
- acquisition method/connector capability reference, without credentials;
- refresh/freshness expectation and change-detection preference;
- required review/approval path, correlation, idempotency, and audit references.

The request must not contain reusable credentials, unbounded access scopes, unredacted sensitive contents in ordinary metadata, a client-supplied tenant authority, or a claim that external availability proves rights.

## Admission Outcomes

| Outcome | Meaning | Default next step |
|---|---|---|
| `Registered` | Required source identity and admission evidence are accepted. | Eligible for a separately authorized ingestion request. |
| `Restricted` | Source is known but its intended scope, classification, rights, or policy limits use. | Resolve restriction or retain without acquisition. |
| `PendingReview` | Additional source-owner, rights, or policy decision is required. | Hold; do not acquire/process as live knowledge. |
| `Rejected` | Admission criteria are not met or source is prohibited. | Record decision; no ingestion. |
| `Suspended` | A previously registered source is no longer currently usable. | Stop new ingestion/refresh and invoke lifecycle handling. |

Registration is idempotent only within a tenant, environment, source-class, protected-origin, and approved scope. Ambiguous duplicate registrations require reconciliation rather than merging records silently.

---

# Ingestion Orchestration Model

~~~text
Authorized Source / Approved Refresh Trigger
    |
    v
Registration and Current Admission Validation
    |
    v
Ingestion Request and Idempotency Reservation
    |
    v
Integration Acquisition Contract
    |
    +--> accepted source evidence / source revision
    +--> rejected, unavailable, partial, or uncertain evidence
    |
    v
SourceRevision Registration and Integrity Validation
    |
    v
Content Processing Boundary
    |
    v
Candidate Knowledge Evidence
    |
    v
Governance and Publication Boundary
~~~

## Ingestion Request

An ingestion request is created only for a currently registered source and includes `ingestionRunId`, source/source-scope reference, requested revision or refresh basis, processing-policy version, acquisition constraints, idempotency key, requester authority, time/budget limits, correlation reference, and audit reference.

The request authorizes a bounded attempt. It does not authorize expanded connector scopes, source changes, publication, deletion, external sharing, or a new use purpose.

## Acquisition Contract

Integration receives a minimum request describing the approved source scope, retrieval constraints, freshness/checkpoint expectation, and a protected authorization reference. It returns normalized source evidence: acquisition result, source-origin reference, observed revision identity where available, integrity/size/type metadata, bounded content/protected content reference, ordering/change evidence, source timestamp, and provider/connector evidence reference.

Connector-specific payloads, credentials, raw access tokens, redirects, cookies, and transport logs remain within Integration and Security boundaries. Knowledge accepts only the normalized evidence required for its source and ingestion records.

## Source Revision Admission

Knowledge creates a SourceRevision only after checking source registration, tenant/environment, scope, content type/size constraints, origin match, current rights/classification evidence, integrity evidence, duplicate/replay indicators, and current policy.

When the provider cannot reliably identify a revision, Knowledge records the observation basis and uncertainty. It does not fabricate a source version from a timestamp alone.

## Processing Handoff

The accepted SourceRevision is handed to Content Processing with its tenant, scope, classification, rights/use constraints, provenance, policy version, protected content reference, and correlation evidence. Content Processing cannot broaden scope, weaken restrictions, or publish a result.

## Completion and Candidate Handoff

An IngestionRun records its terminal acquisition and processing outcome. Candidate artifacts or KnowledgeVersions retain the IngestionRun, SourceRevision, policy, and provenance links necessary for governance review. A completed run is not a successful publication result.

---

# Ingestion States and Outcomes

Detailed lifecycle rules are defined in Document 06. The following states apply to the ingestion operation:

| State | Meaning |
|---|---|
| `Requested` | Authorized attempt is recorded but no acquisition has started. |
| `Validating` | Registration, authority, scope, rights, and policy checks are in progress. |
| `Acquiring` | Integration is performing the bounded external or managed-source acquisition. |
| `RevisionAdmitted` | Source evidence has passed admission and an immutable SourceRevision exists. |
| `Processing` | Content Processing is producing governed candidates/artifacts. |
| `Completed` | Candidate outcome is recorded and available for the separate governance path. |
| `Restricted` | Material or operation is retained only within defined policy limits. |
| `Rejected` | Validation, rights, scope, integrity, or policy prevented progression. |
| `Degraded` | A bounded partial result is recorded with explicit omissions/uncertainty. |
| `Unavailable` | A required dependency or source could not be safely accessed. |
| `Cancelled` | Authorized cancellation ended further work; partial evidence follows policy. |
| `Reconciled` | An uncertain, duplicated, or delayed external outcome has been resolved. |

No terminal ingestion outcome implicitly publishes, supersedes, retires, or deletes a KnowledgeVersion.

---

# Refresh, Change Detection, and Duplicate Control

## Refresh Triggers

Refresh may be initiated by an authorized operator, source-owner request, approved schedule, valid Integration change signal, quality/freshness policy, or controlled recovery procedure. A trigger records its reason, authority, expected scope, and correlation reference.

Schedules and webhooks are triggers, not approval. They must pass the same current source, tenant, rights, classification, and policy checks as an initial ingestion.

## Change Detection

Knowledge compares normalized revision evidence such as protected source version, content digest, source checkpoint, schema version, and approved scope. It records `unchanged`, `changed`, `partial`, `unknown`, or `conflicting` rather than treating any provider timestamp as authoritative.

An unchanged result may update freshness evidence but must not create a duplicate KnowledgeVersion. A changed or uncertain result creates a new SourceRevision and follows the candidate/governance path.

## Idempotency and Ordering

Each request uses a tenant-scoped idempotency key and source-scope/version basis. Duplicate callbacks, retries, and delayed reports reconcile to the same IngestionRun or create explicitly linked reconciliation evidence. Out-of-order revisions do not overwrite newer approved source evidence without governed review.

## Cancellation and Revocation

If source rights, authorization, policy, classification, or source scope changes during acquisition or processing, Knowledge stops or restricts further work where possible and records the reason. It preserves only the minimum evidence permitted for audit, recovery, and required retention. Publication eligibility is re-evaluated separately for affected candidates and versions.

---

# Source Rights, Attribution, and Provenance

Every SourceRevision carries or references the current source identity, owner, origin, acquisition evidence, permitted use, attribution obligation, geographic/residency constraint, classification, and restriction state.

Rights are not inferred from public reachability, connector access, file upload success, a user role, or a provider label. When rights are unavailable, conflicting, expired, or ambiguous, the source is held, restricted, or rejected according to policy.

Attribution requirements propagate from source through artifact, KnowledgeVersion, retrieval result, and citation. A later derived representation cannot remove an attribution or use restriction without an approved governing change.

---

# Security, Privacy, and Tenant Controls

- Tenant and environment are server-resolved at registration, acquisition request, revision admission, processing handoff, refresh, and cancellation.
- Source URLs, repository paths, document names, object IDs, metadata, webhooks, uploaded files, and connector callbacks are untrusted until validated for their intended use.
- Source content is classified and minimized; full contents, credentials, provider payloads, and sensitive metadata are excluded from ordinary events, logs, analytics, and error messages.
- Connector credentials, external tokens, signing keys, and external authorization exchanges are owned by Security and Integration and are never stored in Knowledge records.
- Ingestion privilege is separated from publication authority. An actor permitted to register or refresh a source cannot automatically approve candidate knowledge.
- Managed uploads and external acquisition use malware/content safety, format/size, redirect, network, and abuse controls defined with Security and Integration before processing.

---

# Reliability and Recovery

Ingestion assumes source outage, connector timeout, partial crawl/listing, duplicate event, delayed callback, provider pagination race, content change during acquisition, malformed material, restart, and uncertain external completion.

- Acquisition retries use bounded backoff and current scope/policy checks; externally visible source effects are not repeated blindly.
- A partial or failed acquisition does not delete or replace previously published knowledge. Governance decides any freshness or availability consequence.
- IngestionRun state and idempotency evidence are durable enough to reconcile after restart without replaying acquisition unnecessarily.
- If integrity, revision identity, rights, tenant association, or scope cannot be verified, the run produces a restricted, unavailable, or uncertain outcome rather than a candidate.
- Reprocessing uses a new run and explicit policy/version reference; it does not mutate old artifacts or provenance.

---

# Events and Audit Evidence

Knowledge emits versioned, minimized domain events or audit facts such as:

| Event/fact | Required evidence |
|---|---|
| `knowledge.source.registered` | Source, tenant/environment, source class/scope, registration outcome, authority, policy and audit references. |
| `knowledge.source.restricted` | Source reference, restriction category, reason/evidence reference, affected scope, current action. |
| `knowledge.ingestion.requested` | IngestionRun, source scope/revision basis, trigger, idempotency, policy, authority, correlation. |
| `knowledge.acquisition.completed` | Run/source revision references, normalized outcome, integrity/change evidence, omission/uncertainty status. |
| `knowledge.ingestion.completed` | Run, candidate/artifact references, terminal outcome, processing policy, provenance, correlation. |
| `knowledge.ingestion.degraded` | Run, bounded failure/omission category, last trustworthy evidence, retry/reconciliation posture. |
| `knowledge.source.suspended` | Source reference, scope, reason, authority, affected-ingestion and lifecycle references. |

Events contain protected references and normalized categories, not raw documents, source URLs, connector payloads, credentials, unrestricted rights data, or customer information.

Audit records include registration, admission, source-scope/rights changes, ingestion and refresh initiation, cancellation, restricted/rejected outcome, override, reconciliation, and handoff to governance with principal/service, scope, reason, policy, evidence, correlation, and result.

---

# Testing Strategy

## Contract and State Tests

Validate source-class profiles, registration and ingestion schemas, server-resolved tenant context, idempotency, source/revision relationships, state transitions, attribution propagation, and contract compatibility.

## Integration Tests

Validate authorized managed upload, website scope acquisition, connected-source refresh, unchanged and changed revision handling, partial acquisition, source-to-processing handoff, candidate provenance, cancellation, and governance separation.

## Security and Tenant Tests

Simulate wrong tenant/source scope, forged or replayed callback, path/redirect abuse, malicious file, stale connector authority, overscoped acquisition, public-but-unapproved origin, missing/conflicting rights, sensitive metadata leak, unauthorized source update, and cross-tenant duplicate key.

## Resilience Tests

Simulate provider outage, timeout, restart during processing, pagination race, duplicate/out-of-order callback, source mutation during acquisition, integrity mismatch, partial result, revoked rights, cancellation race, and uncertain completion. Prove no test silently publishes, replaces a live version, exposes protected source material, or crosses tenant scope.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Source-class admission catalog | Defines eligible classes, evidence, restrictions, reviewers, acquisition methods, and refresh rules | Knowledge Platform with Security and Integration |
| Source registration contract | Defines required scope, provenance, rights, classification, authority, idempotency, and audit fields | Knowledge Platform |
| Acquisition adapter contract | Defines bounded Integration request/result, normalized source evidence, errors, ordering, and protected references | Knowledge Platform with Integration and Security |
| Ingestion orchestration contract | Defines state, idempotency, cancellation, retries, processing handoff, reconciliation, and candidate outcomes | Knowledge Platform |
| Source rights and attribution policy | Defines verification, restrictions, propagation, expiry, and revocation treatment | Knowledge Platform with Security and legal/compliance owners |
| Refresh and change-detection policy | Defines trigger authority, schedule/webhook validation, revision comparison, duplicate control, and stale handling | Knowledge Platform with Integration and Operations |
| Source/ingestion audit and telemetry catalog | Defines events, metrics, audit fields, alerts, retention, and prohibited content | Knowledge Platform with Observability and Security |
| Source and ingestion test suite | Proves boundary, security, tenant, provenance, lifecycle, and resilience behavior | Knowledge Platform and Testing Platform |

---

# Anti-Patterns

## Connector Access Means Source Approval

An external token or successful connector call proves neither business ownership, permitted use, classification, nor publication eligibility.

## Crawl Success Means Knowledge Is Current

Acquisition success is an observation. Freshness, completeness, processing quality, review, and publication are separate governed outcomes.

## Scheduled Refresh Bypasses Review

Schedules and change events may request ingestion but cannot silently change the published corpus.

## One Source Revision Replaces All Earlier Knowledge

New source evidence creates candidate versions. Supersession, rollback, retirement, and source-removal consequences are governed lifecycle decisions.

## Store Credentials in Source Metadata

Knowledge records protected references to authority and acquisition capability only. Credentials and tokens remain Security/Integration-managed secrets.

## URL or Filename Is the Tenant Boundary

Tenant scope is server-resolved and enforced on every operation. An origin string is untrusted evidence, not an authorization or tenant key.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_KNOWLEDGE_PLATFORM_ARCHITECTURE.md | Defines the overall Knowledge ownership and ingestion boundary. |
| 02_KNOWLEDGE_DOMAIN_MODEL.md | Defines KnowledgeSource, SourceRevision, IngestionRun, ContentArtifact, and provenance entities. |
| 04_KNOWLEDGE_CONTENT_PROCESSING.md | Defines how admitted source material becomes governed content artifacts and candidates. |
| 06_KNOWLEDGE_LIFECYCLE_AND_VERSIONING.md | Defines detailed source, candidate, publication, rollback, and retirement transitions. |
| 07_KNOWLEDGE_ACCESS_AND_TENANT_ISOLATION.md | Defines current tenant/purpose/access enforcement. |
| 08_KNOWLEDGE_GOVERNANCE_AND_PUBLICATION.md | Defines review and publication decisions. |
| 07_INTEGRATION_PLATFORM | Owns connector and external-workflow implementation. |
| 08_DATA_PLATFORM | Owns physical storage and lifecycle execution. |
| 09_SECURITY_PLATFORM | Owns identity, authorization, secrets, and enterprise security controls. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Knowledge source-registration, acquisition, ingestion, refresh, provenance, and recovery model. |
| 1.1 | 2026-08-06 | Finalized and approved the Knowledge Source and Ingestion Model. |

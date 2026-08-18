# 02_KNOWLEDGE_DOMAIN_MODEL

**Version:** 1.1  
**Status:** Approved  
**Owner:** Knowledge Platform Owner  
**Phase:** Knowledge Platform

---

# Overview

This document defines the logical, tenant-scoped domain model for governed business knowledge.

It establishes the entities and relationships required to trace an authorized retrieval result from published evidence back through its knowledge version, processed content, source revision, source, rights, and governance decision. It is contract-first and independent of databases, vector stores, file systems, embedding models, or connector providers.

---

# Purpose

The Knowledge Domain Model provides one stable representation for reusable business knowledge without making a document, website URL, connector record, vector, chunk, agent prompt, conversation transcript, or customer profile the source of truth.

It enables controlled ingestion, processing, publication, retrieval, citation, freshness, review, rollback, retirement, and audit while preserving tenant isolation and clear ownership boundaries.

---

# Objectives

The model must:

- Define canonical knowledge entities, immutable identifiers, ownership, relationships, and lifecycle references.
- Preserve source-to-result provenance and policy evidence.
- Separate source material, processing artifacts, published knowledge, retrieval representations, and retrieval-use evidence.
- Support one source contributing to multiple knowledge items and one knowledge item being supported by multiple source revisions.
- Support versioning, supersession, rollback, freshness, classification, rights, and publication state without mutating historical evidence.
- Return citations that identify evidence precisely without exposing unrestricted source material.
- Keep personal memory, conversation state, agent reasoning, connector internals, and physical storage outside this model.

---

# Scope

This document defines logical entities and relationships, identifier rules, lifecycle references, integrity constraints, and public-model expectations.

It does not define source acquisition, content-processing algorithms, indexing/ranking, detailed lifecycle transitions, access enforcement, governance workflow, evaluation methods, security controls, operations, or physical persistence. Those details belong to the follow-on Knowledge Platform documents and their owning platforms.

---

# Domain Boundaries

| Topic | Owner |
|---|---|
| Reusable business knowledge, source provenance, version relationships, publication eligibility, citations, and retrieval evidence | Knowledge Platform |
| Agent instructions, prompt composition, model reasoning, response generation, tools, and workflows | 02_AGENT_PLATFORM |
| Canonical conversation, interaction, participant, session, context, routing, handoff, and events | 03_CONVERSATION_PLATFORM |
| Voice recordings, transcripts, media, and transport evidence | 04_VOICE_PLATFORM |
| Customer-specific profiles, preferences, history, and personal memory | 06_MEMORY_PLATFORM |
| Connector execution, external API calls, and external authorization exchange | 07_INTEGRATION_PLATFORM |
| Storage engines, physical records, backups, deletion execution, and residency infrastructure | 08_DATA_PLATFORM |
| Enterprise identity, authorization, classification policy, secrets, encryption, and audit infrastructure | 09_SECURITY_PLATFORM |

---

# Model Principles

## Logical Records, Not Physical Storage

This model defines the meaning and relationship of Knowledge records. Data Platform decides how those records are stored, indexed, replicated, retained, backed up, and deleted according to the Knowledge lifecycle and security requirements.

## Immutable Evidence and Explicit Change

Source revisions, processing runs, knowledge versions, publication decisions, retrieval results, and citations are immutable once issued. A correction creates a new version or decision with an explicit predecessor/supersession relationship; it does not rewrite historical evidence.

## Provenance Is a Required Relationship

Every retrievable knowledge version must have an unbroken path to at least one source revision and its rights/provenance evidence. A result without this path is not eligible for participant-facing retrieval.

## Publication Gates Retrieval

A processed representation is not live merely because it exists. Only a current, eligible publication decision can make a knowledge version retrievable for its approved scope.

## References Are Not Authorization

An entity ID, citation, source reference, content reference, or retrieval-result reference never grants access. Each operation re-evaluates tenant, purpose, actor/service authority, classification, rights, and policy through Security and Knowledge controls.

## Business Knowledge Is Not Personal Memory

Personal or customer-specific data cannot become reusable business knowledge by being processed, chunked, embedded, or cited. It requires a separately approved source, purpose, classification, and governance path.

---

# Entity Model

~~~text
KnowledgeSource
    |
    +--> SourceRevision
    |        |
    |        +--> IngestionRun
    |        |       |
    |        |       +--> ContentArtifact
    |        |               |
    |        |               +--> KnowledgeItem
    |        |                       |
    |        |                       +--> KnowledgeVersion
    |        |                               |
    |        |                               +--> KnowledgeRepresentation
    |        |                               |
    |        |                               +--> PublicationDecision
    |        |
    |        +----------------------------------> ProvenanceLink
    |
AuthorizedRetrievalRequest
    |
    +--> RetrievalResult
             |
             +--> Citation ------> KnowledgeVersion / ContentArtifact / SourceRevision
~~~

## KnowledgeSource

A `KnowledgeSource` is the logical registered origin of reusable business knowledge for one tenant and environment.

Required attributes include:

- `knowledgeSourceId` — immutable opaque identifier.
- `tenantId` and `environmentId` — server-resolved ownership scope.
- `sourceClass` — approved category such as document collection, website, product catalog, policy corpus, or operator-managed structured source.
- `sourceOriginRef` — protected reference to the external or managed origin; never a credential.
- `sourceOwnerRef` and `registrationAuthorityRef` — accountable business owner and registration evidence.
- `rightsProfileRef` — rights, attribution, permitted-use, and restriction evidence.
- `intendedUse` and `freshnessPolicyRef` — allowed purpose and currentness expectations.
- `classificationRef`, `status`, `createdAt`, and `auditRef`.

`KnowledgeSource` is not the source contents, an external connector configuration, a tenant authorization grant, or a published knowledge item.

## SourceRevision

A `SourceRevision` is an immutable observed or submitted version of one KnowledgeSource. It records the source state used by a specific ingestion attempt.

Required attributes include `sourceRevisionId`, `knowledgeSourceId`, source-version or observation reference, observed/acquired time, integrity/digest reference, acquisition evidence, rights/classification snapshot, scope, and prior/superseded revision references where known.

A connector may report duplicate or uncertain revisions. The model preserves those facts; it does not assume a provider timestamp or URL uniquely identifies a revision.

## IngestionRun

An `IngestionRun` is the bounded processing attempt for one or more source revisions under a declared ingestion policy/version.

It includes `ingestionRunId`, tenant/environment, requested and resolved source-revision references, idempotency key, processing-policy version, state/outcome, start/finish time, failure/degradation reference, correlation reference, and audit reference.

An ingestion run does not itself publish knowledge or replace a source revision.

## ContentArtifact

A `ContentArtifact` is a governed, protected representation produced or accepted during ingestion, such as an extracted document view, normalized structured record, approved image/OCR representation, or content segment source.

It includes `contentArtifactId`, source-revision and ingestion-run references, representation type/format/language, protected content or storage reference, integrity/digest, classification, redaction state, extraction confidence/uncertainty, and lifecycle status.

It does not expose raw source content in ordinary contracts, logs, citations, or retrieval results by default.

## KnowledgeItem

A `KnowledgeItem` is the stable logical subject managed by Knowledge Platform: for example, a policy statement, product fact, service description, procedure, FAQ topic, or structured business record.

It includes `knowledgeItemId`, tenant/environment, item type, logical subject key, business owner reference, classification, current lifecycle reference, and creation/audit metadata.

One item may be supported by multiple sources and may have many versions. The logical subject key is scoped to the tenant and item type; it is not a global natural identifier or a cross-tenant join key.

## KnowledgeVersion

A `KnowledgeVersion` is an immutable, reviewable version of a KnowledgeItem derived from one or more artifacts and provenance links.

It includes `knowledgeVersionId`, `knowledgeItemId`, semantic/content version, source and artifact provenance references, normalized knowledge representation reference, classification, language, effective scope, processing-policy/version references, freshness status, predecessor/supersession references, and lifecycle/publication eligibility references.

A version can be processed but not published. It must not be retrieved outside an explicitly eligible publication decision.

## KnowledgeRepresentation

A `KnowledgeRepresentation` is a retrieval-oriented derived representation of a KnowledgeVersion, such as a searchable segment, structured field projection, embedding reference, lexical index entry, or reranking feature reference.

It includes `knowledgeRepresentationId`, `knowledgeVersionId`, representation type and schema version, segment/field boundary, content digest, language, classification, index-policy/version reference, and availability state.

The representation is not independently authoritative. A vector, chunk, embedding, or index entry cannot outlive or override the eligibility, rights, classification, or publication state of its KnowledgeVersion.

## ProvenanceLink

A `ProvenanceLink` records a precise, immutable relationship between a target KnowledgeVersion or ContentArtifact and an origin SourceRevision, ContentArtifact, or approved transformation.

It includes `provenanceLinkId`, source and target references, relationship type, source location/boundary reference, transformation and policy versions, integrity evidence, confidence/uncertainty marker, and creation/audit metadata.

This supports multiple sources, partial support, derived representations, and later correction without treating provenance as a simple document ID.

## PublicationDecision

A `PublicationDecision` is the authoritative, auditable decision that sets eligibility for a specific KnowledgeVersion within a defined tenant, audience, purpose, classification, and effective period.

It includes `publicationDecisionId`, `knowledgeVersionId`, decision/outcome, effective scope, reviewer or authorized automation reference, governance/policy version, reason/evidence references, effective time, predecessor/revocation/rollback references, and audit reference.

Only a current eligible decision may support participant-facing retrieval. Publication does not authorize a particular consumer request; request authorization remains current and purpose-bound.

## AuthorizedRetrievalRequest

An `AuthorizedRetrievalRequest` records the bounded request presented to Knowledge Platform.

It includes `retrievalRequestId`, tenant/environment, consumer reference, purpose, authorization reference, audience/classification constraints, protected query or query reference, requested result constraints, context/correlation reference, and request time. It may reference Conversation context but does not contain or become canonical conversation state.

## RetrievalResult

A `RetrievalResult` is the immutable outcome returned for one AuthorizedRetrievalRequest. It includes `retrievalResultId`, request reference, bounded outcome (`supported`, `unsupported`, `restricted`, `stale`, `degraded`, or `unavailable`), result-policy/version reference, result-count/budget outcome, freshness and availability indicators, citation references, timing, correlation, and audit reference.

It is evidence of a retrieval operation, not a durable knowledge item, prompt, agent decision, or authorization grant.

## Citation

A `Citation` is a minimized, consumer-safe evidence pointer in a RetrievalResult. It includes `citationId`, retrieval-result reference, cited knowledge-version/representation reference, provenance-link reference, bounded locator or excerpt reference, attribution requirement, freshness/status marker, and access/presentation constraint.

It must permit an authorized reviewer to trace support without disclosing broader content, cross-tenant metadata, restricted sources, or sensitive location details.

---

# Relationship Rules

| Relationship | Rule |
|---|---|
| KnowledgeSource → SourceRevision | A source has zero or more immutable revisions. A revision belongs to exactly one source. |
| SourceRevision → IngestionRun | A revision may be processed by multiple runs. A run records every revision it resolved, including an empty or failed outcome. |
| IngestionRun → ContentArtifact | A run may produce zero or more artifacts. Each artifact records its producing or accepted run and source-revision relationship. |
| KnowledgeItem → KnowledgeVersion | An item has one or more versions. A version belongs to exactly one item. |
| KnowledgeVersion → ProvenanceLink | Every retrievable version has one or more provenance links. |
| KnowledgeVersion → KnowledgeRepresentation | A version may have multiple representations. Each representation belongs to one version. |
| KnowledgeVersion → PublicationDecision | A version may have multiple historical decisions; only one effective decision per overlapping tenant/audience/purpose scope may be eligible at a time. |
| RetrievalRequest → RetrievalResult | A request produces at most one terminal result per idempotency scope; retries return or reconcile with that result. |
| RetrievalResult → Citation | A supported result may have one or more citations. A result with no eligible evidence must explicitly state its non-supported outcome. |

---

# Identifier, Version, and Reference Rules

- Knowledge identifiers are immutable, opaque, non-guessable, and scoped by tenant and environment. They do not encode source URLs, provider IDs, classification, or business content.
- Provider, storage, connector, vector-store, and file identifiers remain protected implementation references; they are never substituted for a Knowledge identifier.
- Natural business keys may be retained only as protected source/subject attributes and are not public cross-tenant lookup keys.
- Entity versions are immutable and monotonically ordered within their owning entity. A version does not imply publication or currentness.
- Cross-platform contracts carry the minimum references needed for the receiver's approved purpose. A reference is verified against current policy rather than treated as a bearer token.
- Correlation IDs support scoped diagnostics only and cannot be used to enumerate sources, items, or results across tenants.

---

# Lifecycle References

Detailed state transitions are defined in `06_KNOWLEDGE_LIFECYCLE_AND_VERSIONING.md`. This model uses the following bounded lifecycle meanings:

| Record | Typical states or outcomes |
|---|---|
| KnowledgeSource | registered, active, suspended, retired |
| SourceRevision | observed, accepted, rejected, superseded, unavailable |
| IngestionRun | requested, running, completed, failed, degraded, cancelled, reconciled |
| ContentArtifact | candidate, restricted, accepted, rejected, redacted, unavailable |
| KnowledgeVersion | candidate, reviewed, published, superseded, suspended, retired |
| KnowledgeRepresentation | prepared, indexed, unavailable, invalidated |
| PublicationDecision | approved, rejected, revoked, expired, superseded |
| RetrievalResult | supported, unsupported, restricted, stale, degraded, unavailable |

The lifecycle state of a representation, source, or storage reference cannot independently make a KnowledgeVersion retrievable.

---

# Integrity and Tenant Constraints

1. Every Knowledge entity is bound to exactly one tenant and environment; cross-tenant relationships are invalid.
2. A KnowledgeVersion cannot become retrievable without a complete provenance path, current eligible publication decision, and current request authorization.
3. A Citation must resolve to evidence included in the associated RetrievalResult and must preserve its tenant, classification, and presentation constraints.
4. A SourceRevision, ContentArtifact, or KnowledgeRepresentation may be retained for governed audit/lifecycle purposes without being eligible for retrieval.
5. Revocation, source-rights loss, classification change, redaction, or policy invalidation prevents new retrieval and triggers the defined downstream invalidation process.
6. Historical versions and decisions remain traceable according to retention policy, but historical traceability does not grant ordinary access to their content.
7. A retrieval result never changes publication state, source rights, agent configuration, conversation state, or customer memory.
8. The model must record uncertainty rather than convert low-confidence extraction, partial source availability, or ambiguous provenance into asserted fact.

---

# Anti-Patterns

## A Vector Is the Knowledge Record

Vectors and index entries are derived representations. They cannot establish source rights, publication state, access entitlement, provenance, or truth.

## A Document Is Automatically a Published Knowledge Item

One document may contain many items, no eligible item, or restricted material. Ingestion success does not create participant-facing knowledge.

## Retrieval Result Becomes Conversation Memory

A retrieval result is purpose-bound evidence. Conversation and Memory Platforms separately control any allowed context or memory reference.

## Citation Is an Access Grant

A citation points to governed support. It does not permit unrestricted source viewing, export, sharing, or reuse.

## Source URL Is a Stable Identity

URLs, filenames, and provider identifiers can change, collide, or be reused. The model uses opaque Knowledge identifiers and retains such values only as governed provenance attributes.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Knowledge domain schema | Defines entity, identifier, relationship, version, and reference contracts | Knowledge Platform |
| Provenance and citation schema | Defines traceability, locators, attribution, minimization, and presentation constraints | Knowledge Platform with Security and Data |
| Publication-eligibility projection | Defines the current eligible version/decision view without exposing internal storage or history by default | Knowledge Platform |
| Entity lifecycle and invalidation matrix | Defines allowed states, transitions, revocation, rollback, and downstream effects | Knowledge Platform with Data and Security |
| Contract compatibility policy | Defines version negotiation, migrations, rollback, and deprecation for source, publication, retrieval, and citation contracts | Knowledge Platform with affected owners |
| Tenant and reference-integrity test suite | Proves scoped identity, relationship validity, authorization rechecks, provenance completeness, and safe invalidation | Knowledge Platform and Testing Platform |

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_KNOWLEDGE_PLATFORM_ARCHITECTURE.md | Defines the Knowledge Platform architecture and ownership boundary. |
| 03_KNOWLEDGE_SOURCE_AND_INGESTION_MODEL.md | Defines source registration, acquisition, and ingestion behavior. |
| 04_KNOWLEDGE_CONTENT_PROCESSING.md | Defines artifacts, transformation, classification, and processing controls. |
| 05_KNOWLEDGE_INDEXING_AND_RETRIEVAL.md | Defines representations, request execution, ranking, result, and citation behavior. |
| 06_KNOWLEDGE_LIFECYCLE_AND_VERSIONING.md | Defines detailed lifecycle, publication, freshness, rollback, and retirement behavior. |
| 07_KNOWLEDGE_ACCESS_AND_TENANT_ISOLATION.md | Defines current access and tenant enforcement. |
| 08_KNOWLEDGE_GOVERNANCE_AND_PUBLICATION.md | Defines review and publication authority. |
| 03_CONVERSATION_PLATFORM/03_CONVERSATION_MODEL.md | Defines canonical conversation entities; retrieval references do not replace them. |
| 06_MEMORY_PLATFORM | Owns personal/customer memory distinct from reusable business knowledge. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the canonical Knowledge Platform entity, provenance, publication, retrieval-result, and citation model. |
| 1.1 | 2026-08-06 | Finalized and approved the Knowledge Domain Model. |

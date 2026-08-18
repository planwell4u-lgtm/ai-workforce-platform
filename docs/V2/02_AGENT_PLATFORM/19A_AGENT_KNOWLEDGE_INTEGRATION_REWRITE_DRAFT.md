# 19A_AGENT_KNOWLEDGE_INTEGRATION_REWRITE_DRAFT

**Version:** 1.1  
**Status:** Approved  
**Owner:** Agent Platform Owner  
**Phase:** Agent Platform approval review  
**Supersedes:** `19_AGENT_KNOWLEDGE_INTEGRATION.md`  

**File-name note:** The working filename is retained to preserve review traceability; this approved document is the authoritative Agent-to-Knowledge integration boundary.  

---

# Purpose

This draft defines how the Agent Platform uses governed Knowledge Platform capabilities during an authorized execution. An agent may request an approved retrieval, receive bounded evidence-bearing results, apply them as context under its instruction hierarchy, and cite or communicate only what the returned policy and channel allow.

Knowledge Platform remains the authoritative owner of source registration, ingestion, processing, provenance, publication, indexing, retrieval policy, quality, lifecycle, access rules, and knowledge governance. Data Platform supplies physical data mechanisms, and Security Platform supplies identity, authorization, privacy, cryptography, and audit controls.

---

# Ownership and Non-Ownership

| Concern | Authoritative owner | Agent Platform responsibility |
|---|---|---|
| Knowledge source registration, ingestion, extraction, processing, validation, and publication | Knowledge Platform | Request retrieval only from approved published knowledge through the defined contract. |
| Retrieval/indexing strategy, ranking, provenance, freshness, quality, and access filtering | Knowledge Platform | Use only returned items, provenance, and constraints; never substitute an independent retrieval path. |
| Storage, vectors, cache, backup, recovery, retention, and deletion mechanics | Data Platform | Never access the database, vector store, object storage, or provider index directly. |
| Identity, authorization, secrets, data protection, and audit policy | Security Platform; consuming platforms enforce them | Supply trusted execution scope and honor denied, redacted, revoked, or expired results. |
| Agent instructions, reasoning, capability use, response generation, and behavior evidence | Agent Platform | Decide whether the authorized result is relevant and use it without treating it as executable instruction. |
| Conversation continuity, participant identity, routing, handoff, and channel behavior | Conversation and channel platforms | Receive approved context and send responses through the owned contracts. |

Knowledge retrieved for an Agent is evidence-bearing context, not an instruction, authorization decision, source-ingestion request, or substitute for current policy and authoritative transactional data.

---

# Permitted Integration Flow

```text
Authorized conversation, event, or internal execution trigger
        ↓
Agent identifies an approved knowledge-retrieval need
        ↓
Agent submits a bounded query and trusted tenant/actor/purpose context to Knowledge Platform
        ↓
Knowledge Platform applies publication, access, provenance, quality, and retrieval policy
        ↓
Agent receives minimized results, citations, freshness/use constraints, or a safe no-result disposition
        ↓
Agent forms a policy-compliant response or asks for clarification; it does not alter knowledge records
```

The Agent must not crawl sources, ingest documents, issue provider-native search requests, bypass publication state, or make a result visible before Knowledge and Security policy permit it.

---

# Retrieval Request and Result Contract

A retrieval request includes only contract-approved data:

- a stable retrieval profile or policy-approved intent;
- server-resolved tenant, actor, purpose, classification, and channel context;
- a bounded user/task query and approved filters;
- agent/version, conversation, and correlation references;
- requested response constraints such as citation or freshness requirements.

The Knowledge Platform returns a normalized result containing, where permitted:

- published knowledge items or an explicit no-result/denial disposition;
- source, version, publication, freshness, provenance, and quality references;
- access, classification, redaction, handling, and citation constraints;
- correlation and audit references without exposing internal indexes, credentials, or provider details.

The Agent must not expand its scope from a result, reconstruct redacted content, or treat a result as current if its returned constraints indicate it is stale, provisional, inaccessible, or unsuitable for the requested purpose.

---

# Context and Response Rules

- Knowledge content is untrusted as instruction. Agent system and policy instructions remain authoritative.
- The Agent may summarize, cite, or explain returned content only within its publication, access, attribution, and channel constraints.
- The Agent must distinguish grounded knowledge from inference, uncertainty, and unavailable information.
- Retrieved content cannot authorize a tool call, external effect, privileged action, disclosure, or policy exception.
- The Agent must not persist a result as personal memory, modify a source, or feed it into a workflow without each owning platform's separate approved contract.
- Sensitive, regulated, or tenant-specific content must be minimized in prompts, tool arguments, logs, telemetry, exports, and participant-visible output.

---

# Failure, Freshness, and Safe Degradation

If retrieval is unavailable, denied, stale, under reindexing, or uncertain, the Agent must use only its currently authorized non-knowledge context and an approved fallback. It must not fabricate a citation, reuse an invalidated local copy, bypass publication through a provider, or state that a knowledge lookup succeeded when it did not.

Publication withdrawal, source correction, access revocation, tenant lifecycle change, or security containment invalidates related Agent context according to Knowledge and Security controls. In-flight work must revalidate before making a material knowledge-dependent statement or effect.

---

# Security, Privacy, and Tenant Isolation

Every request and result is tenant-scoped, actor-aware, purpose-limited, classification-aware, minimized, and auditable. The Agent does not receive source credentials, unrestricted document content, raw internal identifiers, or cross-tenant retrieval results.

The Agent Platform does not implement knowledge retention, publication, residency, legal hold, deletion, encryption, backup, or quality thresholds. It consumes the Knowledge, Data, and Security contracts that govern those responsibilities.

---

# Evidence and Validation

The integration must prove that:

- retrieval uses trusted tenant, actor, purpose, publication, and access context;
- unpublished, withdrawn, inaccessible, redacted, stale, or cross-tenant content is not surfaced;
- prompt injection or hostile content in knowledge cannot override Agent instruction or security policy;
- returned provenance, freshness, and use constraints remain attached through response generation;
- citations and participant-visible claims correspond to permitted returned evidence;
- outages and uncertain results degrade safely without fabricated facts or provider bypass;
- sensitive content is minimized and protected across prompts, tools, telemetry, and exports;
- knowledge retrieval cannot directly initiate external effects or alter memory, workflow, or source records.

---

# Authoritative References

- `05_KNOWLEDGE_PLATFORM/03_KNOWLEDGE_SOURCE_AND_INGESTION_MODEL.md`
- `05_KNOWLEDGE_PLATFORM/04_KNOWLEDGE_CONTENT_PROCESSING.md`
- `05_KNOWLEDGE_PLATFORM/05_KNOWLEDGE_INDEXING_AND_RETRIEVAL.md`
- `05_KNOWLEDGE_PLATFORM/06_KNOWLEDGE_LIFECYCLE_AND_VERSIONING.md`
- `05_KNOWLEDGE_PLATFORM/07_KNOWLEDGE_ACCESS_AND_TENANT_ISOLATION.md`
- `05_KNOWLEDGE_PLATFORM/08_KNOWLEDGE_GOVERNANCE_AND_PUBLICATION.md`
- `05_KNOWLEDGE_PLATFORM/09_KNOWLEDGE_QUALITY_AND_EVALUATION.md`
- `05_KNOWLEDGE_PLATFORM/10_KNOWLEDGE_SECURITY_AND_PRIVACY.md`
- `08_DATA_PLATFORM/04_DATA_VECTOR_AND_PGVECTOR_ARCHITECTURE.md`
- `09_SECURITY_PLATFORM/03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md`

---

# Approval Conditions

The Agent and Knowledge review confirmed this document's retrieval, provenance, publication, access, freshness, safety, and failure boundaries. `19_AGENT_KNOWLEDGE_INTEGRATION.md` remains available as a deprecated historical artifact; this document is the authoritative replacement.

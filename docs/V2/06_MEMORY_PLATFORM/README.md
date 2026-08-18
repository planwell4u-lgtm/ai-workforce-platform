# 06_MEMORY_PLATFORM

**Version:** 1.16
**Status:** Approved
**Owner:** Memory Platform Owner
**Phase:** Platform Architecture

---

# Overview

The Memory Platform manages governed, tenant-scoped customer and participant memory: the durable facts, preferences, relationship context, consent-bound observations, and continuity signals that may be used over time.

It supports a consistent experience across channels without turning an agent's transient reasoning, a conversation transcript, or reusable business knowledge into uncontrolled personal memory.

---

# Purpose

This README is the navigation and boundary document for the Memory Platform. It identifies its authoritative documents, intended reading order, ownership, cross-platform dependencies, and approval state.

It does not replace the detailed architecture documents listed below.

---

# Ownership

Memory Platform owns:

- Tenant-scoped participant profiles, memory records, memory evidence, preference and relationship context, consent/use constraints, and memory lifecycle.
- The rules for capturing, validating, classifying, retaining, correcting, retrieving, suppressing, expiring, and deleting personal or customer memory.
- Purpose-bound memory retrieval and the evidence needed to explain what memory was used, withheld, corrected, or removed.
- Memory-domain requirements for governance, access control, tenant isolation, privacy, quality, observability, reliability, and testing.

Memory Platform does not own:

- Agent identity, reasoning, prompt assembly, model invocation, tool selection, or action decisions.
- Canonical conversations, interactions, channel sessions, routing, handoff, or interaction transcripts.
- Reusable business knowledge, source publishing, organizational knowledge retrieval, or general document ingestion.
- Connector implementation, external workflow execution, enterprise identity/security infrastructure, physical data storage, shared telemetry, or shared testing infrastructure.

---

# Reading Order

Read these documents in order when designing, implementing, or reviewing Memory Platform behavior:

1. 01_MEMORY_PLATFORM_ARCHITECTURE.md
2. 02_MEMORY_DOMAIN_MODEL.md
3. 03_MEMORY_CAPTURE_AND_ADMISSION.md
4. 04_MEMORY_PROFILE_AND_PREFERENCE_MODEL.md
5. 05_MEMORY_RETRIEVAL_AND_CONTEXT.md
6. 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md
7. 07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md
8. 08_MEMORY_GOVERNANCE_AND_CONSENT.md
9. 09_MEMORY_QUALITY_AND_EVALUATION.md
10. 10_MEMORY_SECURITY_AND_PRIVACY.md
11. 11_MEMORY_OBSERVABILITY.md
12. 12_MEMORY_RELIABILITY_AND_FAILURE_HANDLING.md
13. 13_MEMORY_TESTING.md
14. 14_MEMORY_TECHNOLOGY_REFERENCE_MAP.md

---

# Document Map

| Document | Primary question answered |
|---|---|
| 01_MEMORY_PLATFORM_ARCHITECTURE.md | What does Memory Platform own, and how does it relate to the rest of the platform? |
| 02_MEMORY_DOMAIN_MODEL.md | Which canonical memory entities, identities, evidence, relationships, and states must exist? |
| 03_MEMORY_CAPTURE_AND_ADMISSION.md | How may memory candidates be proposed, verified, classified, consent-checked, and admitted? |
| 04_MEMORY_PROFILE_AND_PREFERENCE_MODEL.md | How are profiles, preferences, relationship context, corrections, and confidence represented without creating uncontrolled profiles? |
| 05_MEMORY_RETRIEVAL_AND_CONTEXT.md | How is eligible memory selected, bounded, explained, refreshed, and provided as context? |
| 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md | How does memory expire, get corrected, suppressed, deleted, and proven removed? |
| 07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md | How are tenant, participant, role, purpose, consent, and representation boundaries enforced? |
| 08_MEMORY_GOVERNANCE_AND_CONSENT.md | Who may set policy, approve sensitive capture, correct memory, manage consent, and audit decisions? |
| 09_MEMORY_QUALITY_AND_EVALUATION.md | How do we measure accuracy, usefulness, consent compliance, staleness, and harmful-memory risk? |
| 10_MEMORY_SECURITY_AND_PRIVACY.md | How are sensitive personal data, abuse, retention, deletion, and privacy incidents controlled? |
| 11_MEMORY_OBSERVABILITY.md | Which signals make capture, access, suppression, deletion, and failures observable? |
| 12_MEMORY_RELIABILITY_AND_FAILURE_HANDLING.md | How do capture, retrieval, deletion, recovery, and safe degradation behave under failure? |
| 13_MEMORY_TESTING.md | Which evidence proves memory behavior is safe, accurate, isolated, and privacy-respecting? |
| 14_MEMORY_TECHNOLOGY_REFERENCE_MAP.md | Which standards and technologies may fill bounded memory roles, and what may they not own? |

---

# Cross-Platform Boundaries

| Platform | Memory Platform relationship |
|---|---|
| 16_PLATFORM_FOUNDATION | Provides tenant, membership, configuration, entitlement, and API-edge facts. Memory does not define control-plane identity or configuration. |
| 02_AGENT_PLATFORM | May propose memory candidates and consume purpose-bound memory context. Agent Platform does not decide what becomes durable memory or override suppression and consent rules. |
| 03_CONVERSATION_PLATFORM | Provides authorized interaction facts and context references. Conversation owns canonical interactions; Memory owns neither transcripts nor sessions. |
| 04_VOICE_PLATFORM | May supply validated voice-derived interaction facts through approved contracts. Voice owns media and telephony, not personal-memory lifecycle. |
| 17_DIGITAL_CHANNEL_PLATFORM | May supply validated digital-channel interaction facts through Conversation contracts. Digital Channel owns delivery opt-in signals; Memory independently governs durable capture and use under Memory consent/purpose policy. |
| 05_KNOWLEDGE_PLATFORM | Provides reusable business knowledge. Memory owns participant-specific context and must not republish it as organizational knowledge. |
| 07_INTEGRATION_PLATFORM | Implements CRM, profile, and external-system connectors behind approved contracts. Memory owns memory semantics and evidence, not connector internals. |
| 08_DATA_PLATFORM | Provides storage, data-lifecycle mechanisms, and approved data services. Memory owns its logical records, retention requirements, and deletion semantics. |
| 09_SECURITY_PLATFORM | Provides enterprise identity, authorization, secrets, compliance, and security controls. Memory applies them to capture, retrieval, correction, and deletion. |
| 10_FRONTEND_PLATFORM | Provides operator and participant interfaces. Memory defines permissions, notices, evidence, corrections, and privacy actions those interfaces require. |
| 13_OBSERVABILITY_PLATFORM | Provides shared telemetry infrastructure. Memory defines domain signals for capture, use, suppression, deletion, and policy outcomes. |
| 14_TESTING_PLATFORM | Provides test standards and infrastructure. Memory defines privacy-safe fixtures, domain scenarios, and release evidence. |

---

# Current Status

The complete 14-document Memory Platform architecture set is approved. It is the current source of truth for participant-specific Memory ownership, admission, profiles, retrieval, lifecycle, tenant isolation, governance, privacy, quality, observability, reliability, testing, and technology-adoption boundaries.

The initial delivery goal is a narrow, governed continuity path: an authorized tenant can admit a limited, purpose-appropriate participant preference with evidence and consent, use it in a later authorized interaction, correct or suppress it, and prove its lifecycle outcome. Memory capture and use must never bypass consent, tenant isolation, purpose limits, or deletion obligations.

---

# Change Rules

Changes to this module must:

- Preserve Memory Platform ownership of durable personal/customer context and Conversation Platform ownership of canonical interaction history.
- Preserve Platform Foundation ownership of tenant/control-plane facts and Digital Channel Platform ownership of non-voice delivery and delivery opt-in signals.
- Preserve Knowledge Platform ownership of reusable business knowledge; personal memory must not become a shared knowledge source by default.
- Treat a memory candidate as untrusted and non-durable until its evidence, purpose, consent, classification, and policy requirements are satisfied.
- Use controlled APIs, events, or contracts rather than direct cross-module database access.
- Preserve tenant, participant, purpose, consent, suppression, retention, correction, and deletion boundaries across primary and derived representations.
- Keep system-specific connector behavior behind Integration Platform boundaries.
- Update affected governance, privacy, access, quality, observability, reliability, testing, and reference documents together.
- Create or update a decision record when changing a long-lived memory model, consent policy, retention rule, sensitive-data posture, retrieval rule, or ownership boundary.

---

# Related Documents

| Document | Relationship |
|---|---|
| 00_CONTROL/02_PROJECT_ROADMAP.md | Defines the long-term customer-intelligence delivery outcome. |
| 00_CONTROL/03_ARCHITECTURE_PRINCIPLES.md | Defines platform-wide architectural principles. |
| 00_CONTROL/04_SYSTEM_BOUNDARIES.md | Defines platform ownership boundaries. |
| 00_CONTROL/05_MODULE_OWNERSHIP.md | Defines module responsibilities. |
| 00_CONTROL/06_DOCUMENTATION_STANDARDS.md | Defines document lifecycle and approval rules. |
| 00_CONTROL/07_DOCUMENTATION_INDEX.md | Registers this module and document set. |
| 00_CONTROL/08_DECISION_LOG.md | Records material architecture and technology decisions. |
| 02_AGENT_PLATFORM/README.md | Defines agent intelligence and execution ownership. |
| 03_CONVERSATION_PLATFORM/README.md | Defines canonical interaction ownership. |
| 05_KNOWLEDGE_PLATFORM/README.md | Defines reusable business-knowledge ownership. |
| 16_PLATFORM_FOUNDATION/README.md | Defines tenant-aware control-plane and shared configuration ownership. |
| 17_DIGITAL_CHANNEL_PLATFORM/README.md | Defines non-voice channel transport, delivery, and delivery-opt-in ownership. |
| 07_INTEGRATION_PLATFORM/README.md | Defines connector and external-workflow ownership. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Memory Platform navigation, ownership, planned document set, delivery boundary, and cross-platform relationships. |
| 1.1 | 2026-08-06 | Recorded approval of the Memory Platform Architecture document. |
| 1.2 | 2026-08-06 | Finalized the README after review for completeness, ownership overlap, and long-term maintainability; added Platform Foundation and Digital Channel boundaries. |
| 1.3 | 2026-08-06 | Recorded approval of the Memory Domain Model. |
| 1.4 | 2026-08-06 | Recorded approval of the Memory Capture and Admission model. |
| 1.5 | 2026-08-06 | Recorded approval of the Memory Profile and Preference model. |
| 1.6 | 2026-08-06 | Recorded approval of the Memory Retrieval and Context model. |
| 1.7 | 2026-08-06 | Recorded approval of the Memory Lifecycle, Retention, and Deletion model. |
| 1.8 | 2026-08-06 | Recorded approval of the Memory Access and Tenant Isolation model. |
| 1.9 | 2026-08-06 | Recorded approval of the Memory Governance and Consent model. |
| 1.10 | 2026-08-06 | Recorded approval of the Memory Quality and Evaluation model. |
| 1.11 | 2026-08-06 | Recorded approval of the Memory Security and Privacy model. |
| 1.12 | 2026-08-06 | Recorded approval of the Memory Observability model. |
| 1.13 | 2026-08-06 | Recorded approval of the Memory Reliability and Failure Handling model. |
| 1.14 | 2026-08-06 | Recorded approval of the Memory Testing model. |
| 1.15 | 2026-08-06 | Recorded approval of the Memory Technology Reference Map and completion of the Memory Platform architecture set. |
| 1.16 | 2026-08-06 | Recorded the approved Supabase-managed PostgreSQL and pgvector shared data foundation. |

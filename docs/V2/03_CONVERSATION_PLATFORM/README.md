# 03_CONVERSATION_PLATFORM

**Version:** 1.2  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Platform Architecture

---

# Overview

The Conversation Platform is the canonical coordination layer for interactions across voice, chat, messaging, email, API, and future channels.

It supports the project's One Brain, Multi-Channel architecture by preserving one tenant-scoped conversation experience while channels provide transport and Agent Platform provides intelligence and execution.

---

# Purpose

This README is the navigation and boundary document for the Conversation Platform. It identifies the authoritative documents, recommended reading order, cross-platform dependencies, and current approval state.

It does not replace the detailed architecture documents listed below.

---

# Ownership

Conversation Platform owns:

- Canonical conversations, participants, normalized interactions, and approved channel-thread associations.
- Conversation lifecycle, canonical state, sessions, continuity, work ownership, routing, handoff, and governed conversation events.
- Conversation context availability, including purpose-bound snapshots and references.
- Conversation-domain requirements for security, observability, and testing.

Conversation Platform does not own:

- Agent identity, reasoning, instructions, model invocation, tool execution, or workflow implementation.
- Voice/media transport, telephony, provider protocol implementation, or channel-native media behavior.
- Knowledge, long-term memory, external connectors, enterprise identity/security infrastructure, storage infrastructure, telemetry infrastructure, or testing infrastructure.

---

# Reading Order

Read these documents in order when designing, implementing, or reviewing Conversation Platform behavior:

1. 01_CONVERSATION_ARCHITECTURE.md
2. 02_CONVERSATION_LIFECYCLE.md
3. 03_CONVERSATION_MODEL.md
4. 04_CONVERSATION_SESSION_MODEL.md
5. 05_CONVERSATION_CONTEXT_MODEL.md
6. 06_CONVERSATION_ROUTING.md
7. 07_CONVERSATION_EVENTS.md
8. 08_CONVERSATION_HANDOFF_MODEL.md
9. 09_CONVERSATION_STATE_MANAGEMENT.md
10. 10_CONVERSATION_SECURITY.md
11. 11_CONVERSATION_OBSERVABILITY.md
12. 12_CONVERSATION_TESTING.md

---

# Document Map

| Document | Primary question answered |
|---|---|
| 01_CONVERSATION_ARCHITECTURE.md | What does the Conversation Platform own and how does it relate to other platforms? |
| 02_CONVERSATION_LIFECYCLE.md | Which lifecycle states and transitions are permitted? |
| 03_CONVERSATION_MODEL.md | Which canonical entities and relationships represent a conversation? |
| 04_CONVERSATION_SESSION_MODEL.md | How do bounded sessions and continuity work across channels? |
| 05_CONVERSATION_CONTEXT_MODEL.md | Which authorized context can be assembled, shared, refreshed, or revoked? |
| 06_CONVERSATION_ROUTING.md | Who owns the next response and how is a destination selected safely? |
| 07_CONVERSATION_EVENTS.md | Which conversation facts are published and consumed through governed events? |
| 08_CONVERSATION_HANDOFF_MODEL.md | How does accountable work transfer between agent, queue, workflow, and human? |
| 09_CONVERSATION_STATE_MANAGEMENT.md | How is canonical state protected under concurrency, failure, and recovery? |
| 10_CONVERSATION_SECURITY.md | How are conversation-domain access, trust, revocation, and incidents controlled? |
| 11_CONVERSATION_OBSERVABILITY.md | Which signals make conversation outcomes and failures observable? |
| 12_CONVERSATION_TESTING.md | Which evidence proves safe, reliable Conversation Platform behavior? |

---

# Cross-Platform Boundaries

| Platform | Conversation Platform relationship |
|---|---|
| 02_AGENT_PLATFORM | Receives authorized execution work and bounded context; reports outcomes through controlled contracts. It does not own canonical conversation/session state. |
| 04_VOICE_PLATFORM and other Channel Platforms | Own channel/provider transport and media behavior; Conversation owns normalized interaction continuity after validation. |
| 05_KNOWLEDGE_PLATFORM | Provides governed knowledge access; it does not own conversation state or context snapshots. |
| 06_MEMORY_PLATFORM | Provides governed memory/profile access; it does not own canonical conversation history. |
| 07_INTEGRATION_PLATFORM | Owns connectors, workflow implementation, and shared event transport; it does not own conversation facts or state. |
| 08_DATA_PLATFORM | Provides storage and lifecycle mechanisms; Conversation owns its domain state and requirements. |
| 09_SECURITY_PLATFORM | Provides enterprise identity, authorization, compliance, and security controls; Conversation applies them to domain operations. |
| 13_OBSERVABILITY_PLATFORM | Provides telemetry infrastructure; Conversation defines domain signals and outcome semantics. |
| 14_TESTING_PLATFORM | Provides test standards and infrastructure; Conversation defines domain scenarios and release evidence. |

---

# Current Status

The planned 12-document Conversation Platform architecture set is complete, internally consistent, and approved as the current source of truth.

It remains Draft while cross-module architecture approval is completed. Agent documents 21–23 have been re-scoped to defer canonical conversation, interaction, session, routing, handoff, delivery, and conversation-event ownership to this module. The remaining approval work is a human architecture review and formal status decision.

---

# Change Rules

Changes to this module must:

- Preserve canonical Conversation Platform ownership.
- Use controlled APIs, events, or contracts rather than direct database access.
- Update affected documents, references, test evidence, and the documentation index.
- Trigger cross-platform review when they affect Agent, Channel, Integration, Data, Security, Observability, or Testing boundaries.
- Create or update a decision record when they change module ownership or a long-lived architectural pattern.

---

# Related Documents

| Document | Relationship |
|---|---|
| 00_CONTROL/04_SYSTEM_BOUNDARIES.md | Defines platform ownership boundaries. |
| 00_CONTROL/05_MODULE_OWNERSHIP.md | Defines platform responsibilities. |
| 00_CONTROL/06_DOCUMENTATION_STANDARDS.md | Defines document lifecycle and approval rules. |
| 00_CONTROL/07_DOCUMENTATION_INDEX.md | Registers this module and document set. |
| 00_CONTROL/09_CHANGE_MANAGEMENT.md | Defines significant-change review process. |
| 02_AGENT_PLATFORM/21_AGENT_EVENT_INTEGRATION.md | Defines Agent producer/consumer behavior for events. |
| 02_AGENT_PLATFORM/22_AGENT_MULTI_CHANNEL_MODEL.md | Defines Agent multi-channel integration boundary. |
| 02_AGENT_PLATFORM/23_AGENT_SESSION_MANAGEMENT.md | Defines Agent execution-session integration boundary. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Conversation Platform module navigation, ownership, reading order, and approval-status document. |
| 1.1 | 2026-08-06 | Moved to Review with the completed Conversation Platform document set. |
| 1.2 | 2026-08-06 | Approved with the complete Conversation Platform architecture set. |

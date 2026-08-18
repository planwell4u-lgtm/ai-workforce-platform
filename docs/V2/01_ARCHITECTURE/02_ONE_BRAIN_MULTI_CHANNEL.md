# 02_ONE_BRAIN_MULTI_CHANNEL

**Title:** One Brain, Multi-Channel Architecture Model  
**Version:** 2.1  
**Status:** Approved

---

# Overview

This document defines the One Brain, Multi-Channel model that keeps each AI employee's intelligence consistent across supported communication channels. It establishes a single authoritative Agent Brain while preserving separate ownership for canonical conversations, channel transport, knowledge, memory, integrations, security, and platform operations.

The model is a logical architecture rule. It does not require one deployable service, one model provider, one channel vendor, or a shared database across modules.

# Purpose

This document exists to:

- Define what “one brain” means and what it does not mean.
- Prevent channel-specific duplication of reasoning, prompts, tools, knowledge, and memory.
- Preserve one canonical conversation and participant-safe continuity across channels.
- Define the contracts through which channels, intelligence, and supporting platforms cooperate.
- Provide implementation invariants that remain valid as channels and providers evolve.

# Core Model

```text
Participant through an approved channel
        |
        v
Voice or Digital Channel Platform
        |
        v
Conversation Platform: canonical interaction, state, routing, handoff
        |
        v
Agent Platform: one approved Agent Brain and versioned behavior
        |
        +--> Knowledge Platform: governed business information
        +--> Memory Platform: governed participant continuity
        +--> Integration Platform: approved external actions
        |
        v
Approved response/action outcome through the originating or authorized channel
```

Each layer exposes its own contract. A channel delivers and adapts channel-native input/output; Conversation owns canonical continuity; Agent owns intelligence and decision-making; Knowledge and Memory own governed context; Integration owns external effects. None receives ownership merely because it participates in one interaction.

# One Brain Definition

For an approved agent version, the Agent Brain is the single authority for:

- Agent identity, instructions, goals, policies, model/runtime selection, and behavior version.
- Reasoning, tool-selection intent, response/action planning, and approved use of knowledge and memory.
- Versioned configuration and evaluation requirements that apply consistently across supported channels.

One Brain does not mean:

- One global agent for every tenant, organization, or use case.
- One shared memory record or conversation for unrelated participants.
- One physical process, model, prompt file, database, or provider.
- Direct Agent access to channel transport, provider credentials, or ungoverned external actions.
- A channel may ignore a valid channel-specific consent, capability, delivery, safety, or legal restriction.

# Multi-Channel Definition

Multi-channel means that the same approved Agent Brain can serve Voice, web chat, messaging, email, API-mediated interaction, and future approved channels through channel-specific adapters and the canonical Conversation boundary.

Each channel retains its native responsibilities: participant/channel identity translation, transport, media/message handling, capability declaration, consent signals, delivery evidence, provider reliability, and channel-specific safety requirements. A channel does not create an independent reasoning loop, prompt variant, tool framework, knowledge store, customer-memory system, or canonical conversation state merely for convenience.

# Ownership and Contract Boundaries

| Concern | Authoritative owner | Multi-channel rule |
|---|---|---|
| Agent identity, instructions, behavior, reasoning, and tool selection | Agent Platform | One approved agent version is selected through an authorized contract, independent of the incoming channel. |
| Canonical conversation, session, routing, handoff, and response-turn authority | Conversation Platform | Channel events must associate through approved correlation/routing; no channel independently redefines continuity or owner. |
| Voice media and telephony | Voice Platform | Voice translates approved interaction/output contracts; it does not implement the Agent Brain. |
| Non-voice transport, consent, and delivery evidence | Digital Channel Platform | Digital adapters preserve channel-specific requirements without duplicating domain intelligence. |
| Business knowledge and retrieval semantics | Knowledge Platform | Knowledge is retrieved through governed contracts, not copied into per-channel configuration. |
| Participant memory and lifecycle/use policy | Memory Platform | Memory use remains approved and scoped; channel identity alone is not permission to merge participants. |
| External tools, connectors, workflows, and effects | Integration Platform | Agent intent is executed only through approved, authorized, auditable Integration controls. |
| Tenant/control-plane scope and configuration facts | Platform Foundation | Channel/environment identifiers never replace trusted tenant/membership/entitlement context. |
| Identity, authorization, secrets, privacy, and security policy | Security Platform | All channel and agent actions remain subject to current Security controls. |

# Interaction Invariants

Every supported multi-channel interaction must preserve these invariants:

1. A trusted tenant and authorized agent/context scope are established before intelligence or protected context is used.
2. Exactly one platform owns each canonical fact: Agent behavior, Conversation continuity, channel delivery, knowledge, memory, and external effect.
3. A response, handoff, cancellation, or workflow decision has a correlation reference and current owning contract; competing channel/agent decisions are deferred or rejected safely.
4. Channel-native capabilities and restrictions are explicit. A response is adapted only when the selected channel can safely deliver it.
5. Participant delivery, provider acceptance, agent completion, and external business-action completion remain distinct outcomes.
6. Channel switch, reconnect, duplicate, delay, interruption, or provider uncertainty cannot create a second Agent Brain, unbounded duplicate delivery, or silent loss of canonical state.
7. Tenant, authorization, consent, data-classification, retention, and audit requirements apply across every channel boundary.

# Channel Transition and Continuity

A participant may continue an approved interaction through another channel only when Conversation Platform has an authorized association, the receiving channel supports the needed capability, Security/consent controls permit the context exposure, and the Agent Brain version/context is still valid for the next turn.

The transition record identifies source/destination channel, canonical conversation/session reference, participant/tenant scope, authorization/consent evidence, context grant, current owner, correlation, and uncertainty. Voice and Digital Channel platforms may supply transport evidence; they must not infer a successful cross-channel handoff from a matching identifier, provider callback, or user claim alone.

# Versioning and Evolution

Agent behavior, channel adapters, conversation contracts, knowledge/memory policy, integration tools, and delivery schemas evolve independently through versioned, compatible contracts. A channel-specific presentation/configuration change that affects Agent behavior, tool eligibility, context use, consent, tenant scope, delivery semantics, or a participant-visible outcome requires the owning platform's review and appropriate rollout/evidence.

New channels must prove that they can preserve the interaction invariants before being exposed to tenants. They may begin with a deliberately narrow capability set or safe-defer path; they must not approximate unsupported behavior by bypassing Conversation, Agent, Security, or Integration contracts.

# Initial Implementation Slice

The first implementation proves one authorized tenant can use one approved agent through one Voice path and one approved Digital Channel path while both associate to canonical Conversation state, use governed Knowledge/Memory as authorized, invoke one bounded Integration action, and expose verified outcomes through an authorized operator view.

The slice excludes automatic cross-channel identity merging, unrestricted context sharing, duplicate participant delivery, channel-owned business logic, direct provider/database access from the agent or client, and autonomous policy/configuration changes.

# Required Evidence

Before implementation approval, retain evidence of tenant/authorization scoping; agent/version selection; canonical conversation correlation; channel capability and consent behavior; duplicate/ordering/interruption safety; context-access and redaction controls; distinct delivery/action outcome reporting; cross-channel continuity or safe rejection; failure/recovery/reconciliation behavior; and end-to-end Testing, Security, Operations, Observability, and domain-owner review.

# Related Documents

- `01_SYSTEM_OVERVIEW.md`
- `03_PLATFORM_LAYER_MODEL.md`
- `04_MULTI_TENANT_ARCHITECTURE.md`
- `05_SYSTEM_DATA_FLOW.md`
- `03_CONVERSATION_PLATFORM/01_CONVERSATION_ARCHITECTURE.md`
- `02_AGENT_PLATFORM/01_AGENT_PLATFORM_OVERVIEW.md`
- `04_VOICE_PLATFORM/01_VOICE_PLATFORM_ARCHITECTURE.md`
- `17_DIGITAL_CHANNEL_PLATFORM/01_DIGITAL_CHANNEL_ARCHITECTURE.md`
- `00_CONTROL/03_ARCHITECTURE_PRINCIPLES.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-09 | Created the One Brain, Multi-Channel architecture model. |
| 2.1 | 2026-08-09 | Finalized after cross-platform ownership, continuity, overlap, and maintainability review. |

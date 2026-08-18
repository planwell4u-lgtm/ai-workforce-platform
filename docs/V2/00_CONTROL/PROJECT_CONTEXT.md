# Voice Agent SaaS Platform — Project Context

**Version:** 1.2

**Status:** Active

**Purpose:** AI Development Context File

---

# Project Overview

The Voice Agent SaaS Platform is an enterprise-grade, multi-tenant AI agent platform designed to create, deploy, and operate intelligent AI agents across multiple communication channels.

The platform enables organizations to build AI-powered:

* Customer support agents
* Sales agents
* Reception agents
* Appointment agents
* Workflow automation agents
* Business process agents

The system is designed for production environments with strong requirements for:

* Scalability
* Security
* Multi-tenancy
* Reliability
* Observability
* Extensibility

---

# Core Architecture Philosophy

## One Brain, Multi-Channel

The platform follows the principle:

> One intelligent core, multiple communication channels.

The intelligence layer remains independent from the delivery channel.

The same agent capability should work across:

* Voice
* Web chat
* Mobile applications
* WhatsApp
* SMS
* Email
* API integrations

Channels are responsible for communication.

The Agent Platform is responsible for intelligence.

---

# Architectural Vision

The platform is organized into independent but connected capability platforms.

High-level architecture:

```
Users
 |
 v
Conversation Platform
 |
 v
Agent Platform
 |
 +----------------+
 |                |
 v                v
Knowledge      Memory
Platform       Platform
 |
 v
Integration Platform
 |
 v
Data Platform
 |
 v
Security / Operations / Deployment
```

---

# Platform Structure

```
00_CONTROL
01_ARCHITECTURE

02_AGENT_PLATFORM

03_CONVERSATION_PLATFORM

04_VOICE_PLATFORM

05_KNOWLEDGE_PLATFORM

06_MEMORY_PLATFORM

07_INTEGRATION_PLATFORM

08_DATA_PLATFORM

09_SECURITY_PLATFORM

10_FRONTEND_PLATFORM

11_OPERATIONS_PLATFORM

12_DEPLOYMENT_PLATFORM

13_OBSERVABILITY_PLATFORM

14_TESTING_PLATFORM

15_EXAMPLES

20_ENGINEERING
    infrastructure
    packages
    protocols
```

---

# Core Platform Responsibilities

## Agent Platform

Responsible for:

* Agent identity
* Agent behavior
* Capabilities
* Tools
* Workflows
* Reasoning orchestration
* Agent lifecycle

The Agent Platform defines what an agent can do.

---

## Conversation Platform

Responsible for:

* Conversation lifecycle
* Conversation state
* Context management
* Routing
* Handoff
* Multi-channel conversation abstraction

The Conversation Platform connects users with intelligence.

---

## Voice Platform

Responsible for:

* Voice communication
* Telephony
* SIP
* LiveKit
* Audio processing
* Speech-to-text
* Text-to-speech

---

## Knowledge Platform

Responsible for:

* Organizational knowledge
* Documents
* Website ingestion
* Search
* Retrieval
* RAG support
* Knowledge governance

Knowledge answers:

"What information does the organization provide?"

---

## Memory Platform

Responsible for:

* User history
* Preferences
* Previous interactions
* Long-term context
* Memory lifecycle

Memory answers:

"What has happened before?"

---

## Integration Platform

Responsible for:

* External APIs
* MCP
* CRM systems
* Webhooks
* Automation systems
* Third-party services

---

## Data Platform

Responsible for:

* PostgreSQL
* Redis
* Vector storage
* Data lifecycle
* Database standards
* Analytics storage

---

# Technology Foundation

Primary technologies:

## AI

* OpenAI models
* Realtime models
* Whisper
* TTS providers
* LangChain
* LangGraph
* MCP

## Voice

* LiveKit
* Twilio SIP
* WebRTC

## Backend

* Python
* FastAPI
* PostgreSQL
* Redis
* WebSockets

## Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

## LiveKit Implementation Ecosystem

* TypeScript is the preferred language for browser/client integration and is an approved option for LiveKit-facing services where the owning platform selects it.
* React is the approved web UI framework for LiveKit client experiences, used through Frontend and Voice contracts rather than as a source of tenant, authorization, or canonical conversation truth.
* Python is the preferred language for LiveKit Agent/runtime evaluation and an approved backend option where the owning platform selects it.
* LiveKit examples may demonstrate these technologies, but an example's repository layout, data model, security model, or business logic is not adopted automatically.

## Infrastructure

* Docker
* Kubernetes
* Helm
* Terraform
* CI/CD

---

# Development Philosophy

The project follows:

## Documentation First

Architecture decisions are documented before implementation.

## Production First

Design decisions should consider:

* Security
* Reliability
* Scaling
* Operations
* Monitoring

## Modular Architecture

Each platform owns its responsibility.

Avoid unnecessary coupling.

## Long-Term Maintainability

The architecture should remain understandable years after implementation.

---

# AI Assistant Rules

Any AI tool working on this project should:

1. Read `00_CONTROL` before making changes.
2. Understand architecture boundaries.
3. Avoid creating duplicate responsibilities.
4. Follow existing naming conventions.
5. Preserve architectural decisions.
6. Update documentation when architecture changes.
7. Prefer simple solutions over unnecessary complexity.
8. Never introduce implementation details into architecture documents unless required.

---

# Current Development Phase

Current phase:

Implementation Readiness and First Vertical Slice.

The project has completed the approved architecture and Engineering planning sets. The immediate work is:

- Engineering workspace and module boundaries
- Safe local configuration, quality checks, and CI baseline
- First-slice provider and contract choices under their approved owners
- Tenant-aware API entry as the first product implementation task

The initial Architecture Diagrams set is review-ready; PNG exports and final reviewer metadata remain documentation finalization work. Coding may begin with B0 Engineering Foundation while that finalization proceeds.

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.2 | 2026-08-09 | Updated project phase after completion of architecture and Engineering planning; named B0 Engineering Foundation as next work. |
| 1.1 | 2026-08-08 | Updated shared project context after architecture boundary review. |

---

# Source of Truth

The authoritative project knowledge is stored inside:

```
00_CONTROL/
```

AI assistants should treat these documents as the primary project context.

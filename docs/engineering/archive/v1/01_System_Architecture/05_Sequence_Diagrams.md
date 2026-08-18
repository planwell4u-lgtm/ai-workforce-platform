# Sequence Diagrams

**Document Version:** 1.0
**Project:** AI Voice Agent SaaS Platform
**Status:** Draft
**Last Updated:** 2026-07-23

---

# 1. Overview

This document defines the major system interaction sequences inside the AI Voice Agent SaaS Platform.

Sequence diagrams describe:

* Component communication order
* API interactions
* Event flow
* Voice processing lifecycle
* AI reasoning lifecycle
* External integrations

These diagrams are used for:

* Development planning
* Architecture reviews
* Debugging
* Implementation reference

---

# 2. Core System Actors

The main actors in the platform are:

| Actor            | Responsibility                   |
| ---------------- | -------------------------------- |
| Customer         | Business user managing agents    |
| Caller           | Person interacting with AI agent |
| Frontend         | Web dashboard                    |
| Backend API      | Application control layer        |
| LiveKit          | Real-time voice infrastructure   |
| Twilio           | Telephony provider               |
| Agent Runtime    | AI conversation engine           |
| PostgreSQL       | Persistent storage               |
| Redis            | Real-time state storage          |
| External Systems | Third-party services             |

---

# 3. User Authentication Flow

## Scenario

A customer logs into the SaaS dashboard.

```mermaid
sequenceDiagram

participant User

participant Frontend

participant API

participant AuthService

participant Database


User->>Frontend: Enter credentials

Frontend->>API: Login Request

API->>AuthService: Validate User

AuthService->>Database: Query User

Database-->>AuthService: User Record

AuthService->>AuthService: Generate Token

AuthService-->>API: Access Token

API-->>Frontend: Authentication Success

Frontend-->>User: Dashboard Access
```

---

# 4. Organization Creation Flow

## Scenario

A new business creates a SaaS account.

```mermaid
sequenceDiagram

participant User

participant Frontend

participant API

participant TenantService

participant Database


User->>Frontend: Create Organization

Frontend->>API: Organization Request

API->>TenantService: Create Tenant

TenantService->>Database: Store Organization

Database-->>TenantService: Organization ID

TenantService-->>API: Success

API-->>Frontend: Organization Created
```

---

# 5. AI Agent Creation Flow

## Scenario

A customer creates a new voice agent.

```mermaid
sequenceDiagram

participant Admin

participant Dashboard

participant API

participant AgentService

participant Database


Admin->>Dashboard: Configure Agent

Dashboard->>API: Create Agent Request

API->>AgentService: Validate Settings

AgentService->>Database: Save Agent Configuration

Database-->>AgentService: Agent ID

AgentService-->>API: Agent Created

API-->>Dashboard: Display Agent
```

---

# 6. Knowledge Upload and Indexing Flow

## Scenario

A customer uploads company documents.

```mermaid
sequenceDiagram

participant User

participant Frontend

participant API

participant Storage

participant RAGService

participant VectorDB


User->>Frontend: Upload Document

Frontend->>API: Upload Request

API->>Storage: Store File

API->>RAGService: Start Processing

RAGService->>RAGService: Extract Text

RAGService->>RAGService: Create Chunks

RAGService->>RAGService: Generate Embeddings

RAGService->>VectorDB: Store Vectors

VectorDB-->>RAGService: Indexed

RAGService-->>API: Complete

API-->>Frontend: Knowledge Ready
```

---

# 7. Incoming Phone Call Flow

## Scenario

A customer calls the business phone number.

```mermaid
sequenceDiagram

participant Caller

participant Twilio

participant LiveKit

participant VoiceWorker

participant AgentRuntime

participant Database


Caller->>Twilio: Dial Number

Twilio->>LiveKit: SIP INVITE

LiveKit->>VoiceWorker: Create Agent Session

VoiceWorker->>AgentRuntime: Initialize Agent

AgentRuntime->>Database: Load Configuration

Database-->>AgentRuntime: Agent Settings

AgentRuntime-->>VoiceWorker: Ready

VoiceWorker-->>Caller: Greeting
```

---

# 8. Real-Time Conversation Flow

## Scenario

Caller asks a question.

```mermaid
sequenceDiagram

participant Caller

participant STT

participant Agent

participant Memory

participant RAG

participant LLM

participant TTS


Caller->>STT: Voice Input

STT->>Agent: Text Message

Agent->>Memory: Retrieve Context

Memory-->>Agent: Previous Context

Agent->>RAG: Search Knowledge

RAG-->>Agent: Relevant Information

Agent->>LLM: Generate Response

LLM-->>Agent: Answer

Agent->>TTS: Convert Speech

TTS-->>Caller: Voice Response
```

---

# 9. Tool Execution Flow

## Scenario

The AI agent needs external information.

Example:

* Booking appointment
* Checking CRM
* Creating ticket

```mermaid
sequenceDiagram

participant User

participant Agent

participant ToolExecutor

participant ExternalAPI

participant Agent


User->>Agent: Request Action

Agent->>ToolExecutor: Execute Tool

ToolExecutor->>ExternalAPI: API Request

ExternalAPI-->>ToolExecutor: Response

ToolExecutor-->>Agent: Tool Result

Agent->>User: Final Response
```

---

# 10. Human Transfer Flow

## Scenario

AI transfers conversation to a human.

```mermaid
sequenceDiagram

participant Caller

participant Agent

participant TransferService

participant HumanAgent


Caller->>Agent: Request Human

Agent->>TransferService: Transfer Request

TransferService->>HumanAgent: Connect Call

HumanAgent-->>Caller: Human Conversation

TransferService->>Database: Store Transfer Event
```

---

# 11. Outbound Campaign Call Flow

## Scenario

System calls customers from a campaign list.

```mermaid
sequenceDiagram

participant Scheduler

participant CampaignService

participant Twilio

participant LiveKit

participant Agent


Scheduler->>CampaignService: Start Campaign

CampaignService->>Twilio: Initiate Call

Twilio->>LiveKit: SIP Connection

LiveKit->>Agent: Start Conversation

Agent->>Customer: Voice Interaction

Agent->>CampaignService: Update Result
```

---

# 12. Call Completion Flow

## Scenario

Call finishes and data is stored.

```mermaid
sequenceDiagram

participant Agent

participant CallService

participant Database

participant Analytics


Agent->>CallService: Call Completed

CallService->>Database: Save Call Record

CallService->>Database: Save Transcript

CallService->>Analytics: Send Metrics

Analytics->>Database: Store Analytics
```

---

# 13. Event Processing Flow

## Scenario

Background events are processed asynchronously.

```mermaid
sequenceDiagram

participant Service

participant EventBus

participant Worker

participant Database


Service->>EventBus: Publish Event

EventBus->>Worker: Consume Event

Worker->>Database: Update State

Database-->>Worker: Complete
```

---

# 14. Complete Voice AI Pipeline

```mermaid
flowchart LR

Phone[Phone Call]

SIP[Twilio SIP]

RTC[LiveKit]

STT[Speech Recognition]

Agent[Agent Runtime]

Memory[Memory]

RAG[RAG]

LLM[LLM]

TTS[Speech Generation]

PhoneOut[Caller Response]


Phone --> SIP

SIP --> RTC

RTC --> STT

STT --> Agent

Agent --> Memory

Agent --> RAG

Agent --> LLM

LLM --> TTS

TTS --> RTC

RTC --> PhoneOut
```

---

# 15. Error Handling Sequence

## Example: AI Model Failure

```mermaid
sequenceDiagram

participant Agent

participant LLM

participant Fallback

participant Caller


Agent->>LLM: Request Response

LLM--xAgent: Failure

Agent->>Fallback: Use Backup Model

Fallback-->>Agent: Response

Agent->>Caller: Continue Conversation
```

---

# 16. Security Validation Flow

```mermaid
sequenceDiagram

participant Client

participant API

participant Auth

participant Authorization

participant Service


Client->>API: Request

API->>Auth: Verify Token

Auth-->>API: Valid

API->>Authorization: Check Permission

Authorization-->>API: Allowed

API->>Service: Execute Request
```

---

# 17. Related Documents

| Document                      | Purpose             |
| ----------------------------- | ------------------- |
| 01_System_Overview.md         | System introduction |
| 02_High_Level_Architecture.md | Architecture layers |
| 03_Component_Architecture.md  | Components          |
| 04_Data_Flow.md               | Data movement       |
| 29_Database_Schema            | Database design     |
| 30_OpenAPI_Specs              | API contracts       |

---

# 18. Conclusion

The sequence diagrams define the runtime behavior of the AI Voice Agent SaaS Platform.

They provide a blueprint for implementing:

* Voice communication
* AI reasoning
* Knowledge retrieval
* Memory handling
* Workflow execution
* External integrations

---

**End of Document**

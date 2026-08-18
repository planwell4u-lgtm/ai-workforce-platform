# Data Flow Architecture

**Document Version:** 1.0
**Project:** AI Voice Agent SaaS Platform
**Status:** Draft
**Last Updated:** 2026-07-23

---

# 1. Overview

This document describes how data moves through the AI Voice Agent SaaS Platform.

It explains:

* User request flow
* Voice call flow
* AI processing flow
* Knowledge retrieval flow
* Memory flow
* Database persistence flow
* External integration flow

Understanding data movement is critical for:

* System debugging
* Performance optimization
* Security reviews
* Scaling decisions

---

# 2. Data Flow Principles

## 2.1 Clear Data Ownership

Each component owns its data domain.

Example:

```text
Agent Service

Owns:
- Agent configuration
- Agent settings


Call Service

Owns:
- Call records
- Call lifecycle
```

---

## 2.2 Event Driven Communication

Real-time and asynchronous operations use events.

Examples:

```text
Call Started Event

Document Uploaded Event

Agent Updated Event

Conversation Completed Event
```

---

## 2.3 Persistent vs Temporary Data

## Persistent Data

Stored permanently:

* Users
* Organizations
* Agents
* Calls
* Conversations
* Documents

Storage:

* PostgreSQL
* Object Storage

---

## Temporary Data

Short-lived:

* Active sessions
* Real-time state
* Queues

Storage:

* Redis

---

# 3. Complete Platform Data Flow

```mermaid
flowchart TD

User[Customer]

Frontend[Next.js Frontend]

API[FastAPI Backend]

Services[Application Services]

Voice[LiveKit Voice Platform]

Agent[AI Agent Runtime]

RAG[RAG Knowledge System]

Memory[Memory System]

DB[(PostgreSQL)]

Redis[(Redis)]

Storage[(Object Storage)]

External[External Services]


User --> Frontend

Frontend --> API

API --> Services

Services --> Voice

Voice --> Agent

Agent --> RAG

Agent --> Memory

Agent --> DB

Agent --> Redis

RAG --> Storage

RAG --> DB

Services --> External
```

---

# 4. User Configuration Data Flow

## Scenario

Customer creates a new AI voice agent.

---

## Flow

```mermaid
sequenceDiagram

participant User

participant Frontend

participant API

participant AgentService

participant Database


User->>Frontend: Create Agent

Frontend->>API: POST /agents

API->>AgentService: Validate Configuration

AgentService->>Database: Save Agent

Database-->>AgentService: Agent ID

AgentService-->>API: Success

API-->>Frontend: Agent Created
```

---

## Data Stored

Agent configuration includes:

```json
{
"name":"Sales Agent",
"voice":"professional",
"model":"GPT",
"instructions":"Handle sales inquiries"
}
```

---

# 5. Incoming Voice Call Data Flow

## Scenario

A customer calls a business phone number.

---

## Complete Flow

```mermaid
sequenceDiagram

participant Caller

participant Twilio

participant LiveKit

participant VoiceWorker

participant AgentRuntime

participant Database


Caller->>Twilio: Phone Call

Twilio->>LiveKit: SIP Connection

LiveKit->>VoiceWorker: Create Session

VoiceWorker->>AgentRuntime: Start Agent

AgentRuntime->>Database: Load Agent Configuration

Database-->>AgentRuntime: Agent Settings

AgentRuntime->>Caller: Begin Conversation
```

---

# 6. Real-Time Conversation Data Flow

During an active call:

```mermaid
flowchart LR

Audio[Caller Audio]

STT[Speech To Text]

State[Conversation State]

Memory[Memory Retrieval]

RAG[RAG Search]

LLM[Language Model]

TTS[Speech Generation]

Response[AI Voice]


Audio --> STT

STT --> State

State --> Memory

State --> RAG

Memory --> LLM

RAG --> LLM

LLM --> TTS

TTS --> Response
```

---

# 7. Speech Processing Flow

## Input Pipeline

```text
Caller Voice

↓

Audio Stream

↓

Speech Recognition

↓

Text

↓

AI Processing
```

---

## Output Pipeline

```text
AI Response

↓

Text

↓

Text To Speech

↓

Audio Stream

↓

Caller
```

---

# 8. Agent Decision Flow

The AI agent processes every user message:

```mermaid
flowchart TD

Input[User Message]

Context[Build Context]

Memory[Retrieve Memory]

Knowledge[Retrieve Knowledge]

Reasoning[LLM Reasoning]

Action{Need Tool?}

Tool[Execute Tool]

Response[Generate Response]


Input --> Context

Context --> Memory

Context --> Knowledge

Memory --> Reasoning

Knowledge --> Reasoning

Reasoning --> Action

Action --> Tool

Tool --> Reasoning

Action --> Response
```

---

# 9. RAG Knowledge Data Flow

## Document Ingestion

```mermaid
flowchart LR

Upload[Document Upload]

Extract[Text Extraction]

Chunk[Document Chunking]

Embed[Embedding Generation]

Vector[Vector Database]

Metadata[Metadata Database]


Upload --> Extract

Extract --> Chunk

Chunk --> Embed

Embed --> Vector

Chunk --> Metadata
```

---

## Retrieval Flow

```mermaid
flowchart LR

Question[User Question]

Embedding[Query Embedding]

Search[Vector Search]

Context[Relevant Chunks]

LLM[Generate Answer]


Question --> Embedding

Embedding --> Search

Search --> Context

Context --> LLM
```

---

# 10. Memory Data Flow

## Short-Term Memory

```mermaid
flowchart LR

Call[Active Call]

State[Conversation State]

Redis[(Redis)]


Call --> State

State --> Redis
```

Used for:

* Current conversation
* Agent state
* Session information

---

## Long-Term Memory

```mermaid
flowchart LR

Conversation[Completed Conversation]

Processor[Memory Processor]

Database[(PostgreSQL)]


Conversation --> Processor

Processor --> Database
```

Stores:

* Customer history
* Preferences
* Previous interactions

---

# 11. Call Completion Data Flow

When a call ends:

```mermaid
sequenceDiagram

participant Agent

participant CallService

participant Database

participant Analytics


Agent->>CallService: Call Completed Event

CallService->>Database: Save Call Record

CallService->>Database: Save Transcript

CallService->>Analytics: Send Metrics

Analytics->>Database: Store Analytics Data
```

---

# 12. External Integration Data Flow

Examples:

* CRM update
* Calendar booking
* Ticket creation

```mermaid
flowchart LR

Agent[AI Agent]

Tool[Integration Tool]

API[External API]

Result[Response]


Agent --> Tool

Tool --> API

API --> Result

Result --> Agent
```

---

# 13. Security Data Flow Controls

All data flows enforce:

## Authentication

Verify identity.

---

## Authorization

Verify permissions.

---

## Tenant Filtering

Every query includes:

```sql
organization_id
```

---

## Encryption

Protected communication:

```text
Client

↓

HTTPS/TLS

↓

Backend
```

---

# 14. Event Flow Architecture

Important platform events:

```text
Agent.Created

Agent.Updated

Call.Started

Call.Completed

Message.Created

Document.Uploaded

Knowledge.Indexed

Workflow.Completed
```

---

# 15. Monitoring Data Flow

System metrics flow through:

```mermaid
flowchart LR

Application

Logs

Metrics

Tracing

Monitoring


Application --> Logs

Application --> Metrics

Application --> Tracing

Logs --> Monitoring
Metrics --> Monitoring

Tracing --> Monitoring
```

---

# 16. Performance Considerations

Optimization areas:

## Voice Latency

Target:

* Low audio delay
* Fast model response

## Database

Use:

* Indexing
* Connection pooling
* Query optimization

## AI Processing

Optimize:

* Prompt size
* Retrieval quality
* Model selection

---

# 17. Related Documents

| Document                     | Purpose                 |
| ---------------------------- | ----------------------- |
| 03_Component_Architecture.md | Components              |
| 05_Sequence_Diagrams.md      | Detailed interactions   |
| 29_Database_Schema           | Database implementation |
| 30_OpenAPI_Specs             | API contracts           |
| 37_Observability             | Monitoring              |

---

# 18. Conclusion

The data flow architecture defines how information travels across the AI Voice Agent SaaS Platform.

This design ensures:

* Predictable communication
* Clear ownership
* Secure data handling
* Efficient scaling
* Easier troubleshooting

---

**End of Document**

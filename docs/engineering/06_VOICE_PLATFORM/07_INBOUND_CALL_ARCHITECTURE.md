# 06 Inbound Call Architecture

**Version:** 2.0  
**Status:** Production Architecture  
**Owner:** Voice Platform Engineering

---

# 1. Purpose

This document defines the inbound call architecture of the Voice Agent SaaS Platform.

It describes how incoming PSTN calls are received, authenticated, routed, processed, handled by AI agents, and persisted throughout their lifecycle.

The architecture is designed to support:

- Enterprise telephony
- Multi-tenant routing
- AI-powered conversations
- Low-latency voice processing
- Horizontal scalability
- High availability

---

# 2. Objectives

The inbound call architecture provides:

- Automatic AI call answering
- Intelligent agent routing
- Tenant isolation
- Secure call establishment
- Real-time audio processing
- Conversation persistence
- Human escalation
- Workflow execution

---

# 3. High-Level Architecture

```
                Customer

                    │

                    ▼

             PSTN Network

                    │

                    ▼

            Twilio Voice Cloud

                    │

                    ▼

             Elastic SIP Trunk

                    │

                    ▼

          LiveKit SIP Gateway

                    │

                    ▼

            LiveKit Server

                    │

                    ▼

       LiveKit Agent Runtime

                    │

                    ▼

              AI Runtime

                    │

     ┌──────────────┼──────────────┐

     ▼              ▼              ▼

 Memory         RAG Service     Tool Execution

     │              │              │

     └──────────────┼──────────────┘

                    ▼

             Backend Services

                    │

                    ▼

 PostgreSQL • Redis • Supabase Storage
```

---

# 4. Call Lifecycle

```
Incoming Call

↓

Identify Phone Number

↓

Locate Tenant

↓

Load Voice Configuration

↓

Authenticate Request

↓

Create Voice Session

↓

Create LiveKit Room

↓

Assign AI Agent

↓

Join Agent Runtime

↓

Realtime Conversation

↓

Persist Conversation

↓

Generate Analytics

↓

Call Completed
```

---

# 5. Detailed Processing Flow

## Phase 1 – Call Arrival

A caller dials a business telephone number.

```
Caller

↓

PSTN

↓

Twilio
```

Twilio accepts the incoming call and forwards it through the configured SIP trunk.

---

## Phase 2 – SIP Processing

```
Twilio

↓

Elastic SIP Trunk

↓

LiveKit SIP Gateway
```

The LiveKit SIP Gateway:

- validates the SIP request
- extracts metadata
- creates a media session
- forwards audio

---

## Phase 3 – Tenant Resolution

The backend identifies:

- Tenant
- Phone number
- Business
- Routing policy

```
Phone Number

↓

Tenant

↓

Configuration

↓

Voice Agent
```

---

## Phase 4 – Agent Selection

The routing engine determines which AI agent should answer.

Routing criteria may include:

- Dialed number
- Department
- Language
- Time zone
- Business hours
- Customer profile
- Campaign
- Skill group

---

# 6. Voice Session Creation

A new voice session is initialized.

```
Voice Session

├── Session ID

├── Call ID

├── Tenant ID

├── Agent ID

├── Room ID

├── Direction

├── Caller Number

└── Start Time
```

Session metadata is persisted in PostgreSQL.

---

# 7. LiveKit Room Creation

A dedicated room is created.

```
Room

│

├── Caller

├── AI Agent

└── Media Tracks
```

Each inbound call receives its own isolated room.

---

# 8. Agent Initialization

Before joining the conversation, the runtime loads:

- Agent prompt
- Voice model
- Language
- Available tools
- Workflow definition
- Memory policy
- Knowledge sources
- Tenant configuration

---

# 9. Audio Pipeline

```
Caller Speech

↓

Audio Track

↓

Voice Activity Detection

↓

Speech-to-Text

↓

Transcript

↓

AI Runtime

↓

LLM

↓

Text-to-Speech

↓

Generated Audio

↓

Caller
```

---

# 10. AI Runtime Processing

The AI Runtime performs:

- Intent detection
- Reasoning
- Tool selection
- Workflow execution
- Response generation
- Memory updates
- RAG retrieval

The LiveKit Agent Runtime remains responsible only for media orchestration.

---

# 11. Memory Integration

During the conversation:

```
Transcript

↓

Memory Service

↓

Relevant Context

↓

AI Runtime
```

Memory retrieval occurs before response generation.

Conversation memory is updated after each interaction.

---

# 12. Knowledge Retrieval

If external knowledge is required:

```
Question

↓

Embedding

↓

pgvector Search

↓

Relevant Chunks

↓

AI Runtime

↓

Response
```

Knowledge retrieval is performed by the RAG Service.

---

# 13. Tool Execution

The AI Runtime may invoke tools such as:

- CRM
- Calendar
- Appointment scheduler
- Ticketing
- ERP
- Custom APIs

Execution flow:

```
AI Runtime

↓

Backend API

↓

Tool

↓

Result

↓

AI Runtime
```

---

# 14. Human Escalation

Calls may be transferred when:

- requested by the caller
- confidence is low
- business rules require escalation
- emergency conditions exist

```
AI Agent

↓

Transfer Request

↓

Backend

↓

Twilio

↓

Human Agent
```

---

# 15. Recording

If enabled:

```
Conversation

↓

Recording Service

↓

Supabase Storage

↓

Metadata

↓

PostgreSQL
```

Retention follows tenant-specific policies.

---

# 16. Call Completion

At call termination:

- close LiveKit room
- release resources
- persist transcript
- update analytics
- publish events
- archive recording

---

# 17. Events Published

Examples:

```
CALL_STARTED

CALL_CONNECTED

CALL_RECORDING_STARTED

TRANSCRIPT_UPDATED

TOOL_EXECUTED

CALL_TRANSFERRED

CALL_COMPLETED

CALL_FAILED
```

Events are published through the platform event bus.

---

# 18. Persistence

Conversation data is stored as follows:

| Data | Storage |
|------|---------|
| Session metadata | PostgreSQL |
| Conversation | PostgreSQL |
| Active session | Redis |
| Recording | Supabase Storage |
| Embeddings | pgvector |

---

# 19. Failure Handling

Recovery scenarios include:

### SIP Failure

- Retry
- Alternate route
- Log failure

### LiveKit Failure

- Reject session
- Publish alert

### AI Runtime Failure

- Retry worker
- Transfer to fallback agent
- Escalate to human

### Backend Failure

- Queue events
- Retry persistence

---

# 20. Security

Security controls include:

- SIP authentication
- TLS encryption
- SRTP media encryption
- JWT validation
- Tenant isolation
- Audit logging
- Secret management

---

# 21. Observability

Metrics collected:

- Calls received
- Answer rate
- Call setup latency
- AI response latency
- STT latency
- TTS latency
- Average call duration
- Transfer rate
- Call completion rate
- Failure rate

---

# 22. Scalability

The inbound architecture supports:

- Thousands of concurrent calls
- Multiple LiveKit clusters
- Distributed AI workers
- Regional deployments
- Automatic scaling
- High availability

---

# 23. Related Documentation

- 05_TWILIO_SIP_INTEGRATION.md
- 07_OUTBOUND_CALL_ARCHITECTURE.md
- 09_CALL_SESSION_MANAGEMENT.md
- 10_AUDIO_PIPELINE_ARCHITECTURE.md
- 15_VOICE_AGENT_HANDOFF.md
- 16_HUMAN_TRANSFER_ARCHITECTURE.md

---

# 24. Summary

The inbound call architecture defines the complete processing pipeline for incoming telephone calls.

By combining Twilio Elastic SIP Trunking, LiveKit, the LiveKit Agent Runtime, the AI Runtime, Backend Services, PostgreSQL, Redis, pgvector, and Supabase Storage, the platform delivers secure, low-latency, enterprise-grade AI voice interactions while maintaining strict tenant isolation, scalability, and operational reliability.
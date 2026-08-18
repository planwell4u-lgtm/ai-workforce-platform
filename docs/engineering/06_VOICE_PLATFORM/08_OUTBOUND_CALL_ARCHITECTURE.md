# 07 Outbound Call Architecture

**Version:** 2.0  
**Status:** Production Architecture  
**Owner:** Voice Platform Engineering

---

# 1. Purpose

This document defines the outbound call architecture of the Voice Agent SaaS Platform.

Outbound calling enables AI agents to proactively initiate telephone calls to customers for sales, support, reminders, surveys, collections, follow-ups, and automated business workflows.

The architecture is designed to support:

- AI-initiated outbound calls
- Campaign management
- Scheduled calling
- Intelligent retries
- High-volume dialing
- Multi-tenant isolation
- Horizontal scalability

---

# 2. Objectives

The outbound calling platform provides:

- AI-powered outbound conversations
- Scheduled call execution
- Campaign management
- Dynamic agent assignment
- Call retry logic
- Voicemail handling
- Workflow automation
- Call analytics

---

# 3. High-Level Architecture

```
               Campaign

                   │

                   ▼

        Campaign Scheduler

                   │

                   ▼

        Outbound Call Queue

                   │

                   ▼

        Call Dispatcher Service

                   │

                   ▼

             Twilio Voice API

                   │

                   ▼

          Elastic SIP Trunk

                   │

                   ▼

        LiveKit SIP Gateway

                   │

                   ▼

            LiveKit Room

                   │

                   ▼

      LiveKit Agent Runtime

                   │

                   ▼

             AI Runtime

                   │

     ┌─────────────┼─────────────┐

     ▼             ▼             ▼

  Memory        RAG         Tool Calls

                   │

                   ▼

          Backend Services

                   │

                   ▼

PostgreSQL • Redis • Supabase Storage
```

---

# 4. Outbound Call Lifecycle

```
Campaign Created

↓

Import Contacts

↓

Validate Contacts

↓

Schedule Calls

↓

Dispatch Call

↓

Twilio

↓

LiveKit

↓

AI Agent

↓

Conversation

↓

Store Results

↓

Analytics
```

---

# 5. Campaign Management

A campaign defines the business purpose of outbound calls.

Examples:

- Sales campaign
- Appointment reminders
- Payment reminders
- Customer surveys
- Follow-up calls
- Marketing campaigns
- Support callbacks

Campaign configuration includes:

```
Campaign

├── Name

├── Tenant

├── AI Agent

├── Schedule

├── Retry Policy

├── Target List

├── Business Hours

├── Time Zone

└── Completion Rules
```

---

# 6. Contact Import

Contacts may originate from:

- CSV upload
- Excel upload
- CRM integration
- REST API
- Scheduled synchronization

Each contact includes:

- Name
- Phone number
- Language
- Customer ID
- Variables
- Tags
- Priority

---

# 7. Call Scheduling

The scheduler determines when each call should be placed.

Scheduling considers:

- Tenant time zone
- Customer time zone
- Business hours
- Campaign limits
- Retry windows
- Rate limits
- Compliance rules

---

# 8. Call Dispatching

The dispatcher selects the next eligible call.

```
Scheduled Call

↓

Validate Rules

↓

Reserve Worker

↓

Create Call Request

↓

Twilio
```

---

# 9. Twilio Call Initiation

Twilio establishes the outbound PSTN connection.

```
Backend

↓

Twilio Voice API

↓

PSTN

↓

Customer
```

When the call is answered, Twilio connects the media stream to LiveKit.

---

# 10. LiveKit Session

A dedicated LiveKit room is created.

```
Room

├── AI Agent

├── Customer

└── Media Tracks
```

Each outbound call has its own isolated room.

---

# 11. Agent Initialization

The LiveKit Agent Runtime loads:

- Agent prompt
- Voice model
- Language
- Campaign context
- Customer variables
- Available tools
- Workflow
- Memory policy

---

# 12. Conversation Flow

```
Customer Answers

↓

Greeting

↓

Intent Detection

↓

Conversation

↓

Workflow Execution

↓

Closing

↓

Call Complete
```

---

# 13. Personalization

Campaign variables may include:

```
Customer Name

Company

Order Number

Appointment Date

Outstanding Balance

Custom CRM Fields
```

Variables are injected into prompts before the conversation begins.

---

# 14. Tool Integration

The AI Runtime may invoke:

- CRM lookup
- Calendar booking
- Order management
- Payment systems
- Ticket creation
- ERP
- Custom APIs

---

# 15. Memory Integration

If enabled:

```
Customer

↓

Memory Retrieval

↓

Previous Conversations

↓

AI Runtime
```

Memory allows personalized follow-up conversations.

---

# 16. Knowledge Retrieval

Questions requiring external knowledge follow:

```
Customer Question

↓

Embedding

↓

pgvector

↓

Relevant Context

↓

LLM

↓

Voice Response
```

---

# 17. Retry Strategy

Retries are configurable.

Reasons include:

- No answer
- Busy
- Failed connection
- Temporary network error

Retry policy defines:

- Maximum attempts
- Delay between attempts
- Retry window
- Maximum campaign duration

---

# 18. Voicemail Detection

If voicemail is detected, the platform may:

- Leave a prerecorded message
- Generate AI voicemail
- End the call
- Schedule another attempt

Behavior is configured per campaign.

---

# 19. Call Outcomes

Possible outcomes include:

- Completed
- Customer declined
- Voicemail
- Busy
- No answer
- Failed
- Human transfer
- Callback requested

Outcomes drive follow-up workflows.

---

# 20. Recording

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

# 21. Persistence

| Data | Storage |
|------|---------|
| Campaign | PostgreSQL |
| Contact metadata | PostgreSQL |
| Active campaign state | Redis |
| Call metadata | PostgreSQL |
| Transcript | PostgreSQL |
| Recording | Supabase Storage |
| Embeddings | pgvector |

---

# 22. Events Published

Examples:

```
CAMPAIGN_STARTED

CALL_DISPATCHED

CALL_CONNECTED

VOICEMAIL_DETECTED

CALL_COMPLETED

CALL_FAILED

CALL_RETRY_SCHEDULED

CAMPAIGN_COMPLETED
```

---

# 23. Security

Security controls include:

- API authentication
- SIP security
- TLS encryption
- SRTP media encryption
- Tenant isolation
- Audit logging
- Secret management

---

# 24. Monitoring

Operational metrics include:

- Calls initiated
- Calls connected
- Connection rate
- Average duration
- Voicemail rate
- Retry rate
- Campaign completion
- AI response latency
- Cost per campaign
- Calls per minute

---

# 25. Scalability

The outbound architecture supports:

- Multiple concurrent campaigns
- Distributed dispatchers
- Horizontal AI worker scaling
- Queue-based scheduling
- Regional deployments
- High-volume dialing

---

# 26. Compliance

Campaigns must support:

- Business hour restrictions
- Regional calling regulations
- Opt-out handling
- Do-not-call lists
- Consent tracking
- Call recording policies

Compliance rules are enforced before each outbound call.

---

# 27. Related Documentation

- 05_TWILIO_SIP_INTEGRATION.md
- 06_INBOUND_CALL_ARCHITECTURE.md
- 09_CALL_SESSION_MANAGEMENT.md
- 15_VOICE_AGENT_HANDOFF.md
- 16_HUMAN_TRANSFER_ARCHITECTURE.md
- 17_CALL_RECORDING_SYSTEM.md

---

# 28. Summary

The outbound call architecture provides a scalable framework for AI-driven outbound communications.

By combining campaign management, intelligent scheduling, Twilio Voice, LiveKit, the LiveKit Agent Runtime, AI Runtime, Backend Services, PostgreSQL, Redis, pgvector, and Supabase Storage, the platform supports enterprise-grade outbound calling with personalization, workflow automation, compliance, analytics, and reliable execution.
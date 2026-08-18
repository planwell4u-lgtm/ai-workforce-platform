# 10 Call State Machine

**Version:** 2.0

**Status:** Production Architecture

**Owner:** Voice Platform Engineering

---

# 1. Purpose

This document defines the authoritative Call State Machine for the Voice Agent SaaS Platform.

Every inbound and outbound call progresses through a well-defined sequence of states.

The Call State Machine provides:

- Consistent call lifecycle management
- Predictable state transitions
- Distributed system synchronization
- Reliable event processing
- Recovery after failures
- Accurate analytics and billing

Every platform component must use this state model.

---

# 2. Design Goals

The state machine is designed to provide:

- Deterministic transitions
- Stateless processing
- Event-driven execution
- Failure recovery
- Horizontal scalability
- Complete observability
- Multi-tenant isolation

---

# 3. High-Level State Diagram

```
                 CREATED
                     │
                     ▼
                 ROUTING
                     │
                     ▼
                 CONNECTING
                     │
                     ▼
                 CONNECTED
                     │
                     ▼
              AI_INITIALIZING
                     │
                     ▼
                 AI_ACTIVE
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   HUMAN_TRANSFER         TERMINATING
          │                     │
          ▼                     ▼
    HUMAN_CONNECTED       COMPLETED
```

Failure states may be entered from any phase.

---

# 4. State Definitions

| State | Description |
|---------|-------------|
| CREATED | Call request received |
| ROUTING | Routing engine selecting destination |
| CONNECTING | SIP and media being established |
| CONNECTED | Media connection established |
| AI_INITIALIZING | AI Runtime loading |
| AI_ACTIVE | AI conversation in progress |
| HUMAN_TRANSFER | Transfer process started |
| HUMAN_CONNECTED | Human agent connected |
| TERMINATING | Session cleanup in progress |
| COMPLETED | Successful completion |
| FAILED | Call terminated because of error |
| CANCELLED | Cancelled before connection |
| TIMEOUT | Connection timeout |

---

# 5. State Details

## CREATED

Entry Conditions

- Incoming call received
- Outbound campaign started

Actions

- Generate Call ID
- Create session request
- Publish CALL_CREATED event

Exit

- ROUTING

---

## ROUTING

Actions

- Resolve tenant
- Identify phone number
- Load routing policy
- Select AI agent
- Apply business rules

Possible Exit States

- CONNECTING
- FAILED
- CANCELLED

---

## CONNECTING

Actions

- Create LiveKit room
- Reserve AI worker
- Establish SIP media
- Authenticate participants

Possible Exit States

- CONNECTED
- FAILED
- TIMEOUT

---

## CONNECTED

Actions

- Media established
- Session initialized
- Begin audio streaming

Possible Exit

- AI_INITIALIZING

---

## AI_INITIALIZING

Actions

Load:

- Prompt
- Voice
- Language
- Memory
- Knowledge
- Tools
- Workflow

Possible Exit

- AI_ACTIVE
- FAILED

---

## AI_ACTIVE

Conversation is active.

Allowed Activities

- STT
- LLM reasoning
- Tool execution
- Memory updates
- RAG retrieval
- TTS generation

Possible Exit States

- HUMAN_TRANSFER
- TERMINATING
- FAILED

---

## HUMAN_TRANSFER

Actions

- Locate human destination
- Notify backend
- Create transfer request
- Update session

Possible Exit

- HUMAN_CONNECTED
- AI_ACTIVE
- FAILED

---

## HUMAN_CONNECTED

Actions

- Bridge media
- Continue recording
- Preserve analytics

Possible Exit

- TERMINATING

---

## TERMINATING

Actions

- Stop recording
- Persist transcript
- Update billing
- Publish events
- Close LiveKit room
- Release resources

Possible Exit

- COMPLETED

---

## COMPLETED

Actions

- Archive session
- Generate analytics
- Remove Redis session
- Finish processing

Terminal State

---

## FAILED

Reasons include:

- SIP failure
- Worker crash
- Authentication failure
- Backend unavailable
- LiveKit unavailable

Terminal State

---

## CANCELLED

Examples

- Outbound campaign cancelled
- User hung up before connection
- Administrator cancelled

Terminal State

---

## TIMEOUT

Examples

- No answer
- SIP timeout
- Connection timeout

Terminal State

---

# 6. Valid State Transitions

```
CREATED
    │
    ▼
ROUTING
    │
    ▼
CONNECTING
    │
    ▼
CONNECTED
    │
    ▼
AI_INITIALIZING
    │
    ▼
AI_ACTIVE
    │
    ├─────────────► HUMAN_TRANSFER
    │                     │
    │                     ▼
    │              HUMAN_CONNECTED
    │                     │
    ▼                     ▼
TERMINATING
    │
    ▼
COMPLETED
```

Failures may occur from any active state.

---

# 7. Invalid Transitions

Examples

```
COMPLETED

↓

AI_ACTIVE
```

Not allowed.

---

```
FAILED

↓

CONNECTED
```

Not allowed.

---

```
CANCELLED

↓

AI_ACTIVE
```

Not allowed.

Terminal states cannot transition to active states.

---

# 8. Events

Each transition generates an event.

Examples

```
CALL_CREATED

ROUTING_STARTED

CALL_CONNECTED

AI_READY

AI_STARTED

TRANSFER_REQUESTED

TRANSFER_COMPLETED

CALL_COMPLETED

CALL_FAILED
```

---

# 9. Session Persistence

Current active state

↓

Redis

↓

Fast synchronization

---

Historical state

↓

PostgreSQL

↓

Permanent storage

---

# 10. Recovery

Recoverable States

- ROUTING
- CONNECTING
- AI_INITIALIZING
- AI_ACTIVE

Recovery uses:

- Redis session
- Event replay
- Worker reassignment

---

# 11. Timeout Handling

Timeout policies

| State | Timeout |
|---------|----------|
| ROUTING | Configurable |
| CONNECTING | Configurable |
| AI_INITIALIZING | Configurable |
| HUMAN_TRANSFER | Configurable |

Timeout values are defined in platform configuration.

---

# 12. Monitoring

Metrics include:

- State transition latency
- Failed transitions
- Average state duration
- Active calls by state
- Recovery success rate
- Timeout rate

---

# 13. Security

Every state transition is:

- Authenticated
- Authorized
- Audited
- Timestamped
- Tenant isolated

---

# 14. Integration

The Call State Machine is consumed by:

- Backend Services
- Live
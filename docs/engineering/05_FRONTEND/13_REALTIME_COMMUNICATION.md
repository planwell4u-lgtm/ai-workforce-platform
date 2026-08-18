# 13 Realtime Communication Architecture

**Version:** 2.0  
**Status:** Production Architecture  
**Owner:** Frontend Engineering

---

# 1. Purpose

This document defines the frontend realtime communication architecture for the Voice Agent SaaS Platform.

Realtime communication enables the frontend application to receive and process immediate updates from the backend platform.

The system supports:

- Live voice sessions
- Agent state updates
- Call events
- Transcript streaming
- Workflow execution updates
- Notifications
- Operational monitoring

---

# 2. Realtime Communication Goals

The realtime architecture provides:

- Low latency communication
- Reliable event delivery
- Scalable connections
- Consistent frontend state
- Real-time user feedback
- Production observability

---

# 3. Realtime Architecture Overview

```
                         Frontend

                            │

        ┌───────────────────┼───────────────────┐

        ▼                   ▼                   ▼

    LiveKit            WebSocket              SSE

        │                   │                   │

        ▼                   ▼                   ▼

 Voice Streams       Application Events    Notifications

                            │

                            ▼

                    Backend Event System

                            │

                            ▼

                 Voice Agent Platform
```

---

# 4. Realtime Technologies

The platform uses:

| Technology | Purpose |
|---|---|
| LiveKit SDK | Voice communication |
| WebSocket | Bidirectional events |
| Server Sent Events | One-way updates |
| TanStack Query | Data synchronization |
| Zustand | Realtime client state |

---

# 5. Communication Channels

The platform separates realtime communication by purpose.

---

## LiveKit Channel

Used for:

- Audio streaming
- Voice sessions
- Participant management
- Media tracks

---

## WebSocket Channel

Used for:

- Application events
- Agent status
- Call lifecycle
- Transcript updates

---

## Server Sent Events

Used for:

- Long-running job progress
- Processing updates
- Notifications

---

# 6. Realtime Data Flow

Example:

```
Voice Input

↓

LiveKit

↓

Agent Runtime

↓

Backend Event

↓

WebSocket

↓

Frontend State Update

↓

UI Refresh
```

---

# 7. Event Driven Architecture

Realtime events follow a standardized structure.

Example:

```json
{
  "event": "call.started",
  "timestamp": "2026-01-01T10:00:00Z",
  "data": {
    "call_id": "123"
  }
}
```

---

# 8. Event Naming Convention

Events use:

```
resource.action
```

Examples:

```
call.started

call.connected

call.completed

agent.updated

agent.status_changed

workflow.completed

knowledge.indexed
```

---

# 9. WebSocket Connection Lifecycle

Connection flow:

```
Application Start

        ↓

Authenticate User

        ↓

Create WebSocket Connection

        ↓

Subscribe To Events

        ↓

Receive Updates

        ↓

Reconnect If Required
```

---

# 10. WebSocket Client Responsibilities

The frontend WebSocket client manages:

- Connection handling
- Authentication
- Event parsing
- Subscriptions
- Reconnection
- Error handling

---

# 11. WebSocket Client Structure

Recommended:

```
lib/

realtime/

├── websocket-client.ts

├── event-types.ts

├── event-handler.ts

└── subscriptions.ts
```

---

# 12. Connection Management

The client supports:

## Connection

```
CONNECTING

↓

CONNECTED
```

---

## Failure Recovery

```
DISCONNECTED

↓

RECONNECTING

↓

CONNECTED
```

---

# 13. Reconnection Strategy

The client uses:

- Exponential backoff
- Maximum retry limits
- Session restoration

Example:

```
Attempt 1

1 second


Attempt 2

2 seconds


Attempt 3

4 seconds
```

---

# 14. Subscription Architecture

Frontend components subscribe only to required events.

Example:

```
Call Monitoring Page

Subscribes:

call.*

agent.status_changed
```

---

Avoid:

```
Global subscription to all events
```

---

# 15. Realtime State Management

Realtime state is separated from server state.

Architecture:

```
Realtime Events

        ↓

Event Handler

        ↓

Zustand Store

        ↓

UI Components
```

---

# 16. Call Event Architecture

Call lifecycle events:

```
call.created

        ↓

call.ringing

        ↓

call.connected

        ↓

call.transcript_received

        ↓

call.completed
```

---

# 17. Agent Runtime Events

Agent events include:

```
agent.listening

agent.processing

agent.responding

agent.tool_execution

agent.completed
```

---

# 18. Transcript Event Streaming

Transcript events:

Example:

```
transcript.received

transcript.updated

transcript.completed
```

Flow:

```
STT Engine

↓

Backend

↓

WebSocket

↓

Transcript Store

↓

Transcript UI
```

---

# 19. Workflow Execution Events

Workflow updates include:

```
workflow.started

workflow.node_started

workflow.node_completed

workflow.failed
```

Used for:

- Workflow builder monitoring
- Debugging
- Automation visibility

---

# 20. Notification Events

Realtime notifications include:

- System alerts
- Billing updates
- Processing completion
- Security events

---

# 21. Tenant Isolation

Realtime connections must maintain:

```
User

↓

Tenant

↓

Workspace

↓

Permissions
```

Every event must be authorized before reaching the frontend.

---

# 22. Security Requirements

Realtime communication must:

- Authenticate connections
- Validate sessions
- Encrypt transport
- Validate event permissions
- Prevent unauthorized subscriptions

---

# 23. Error Handling

Realtime errors include:

## Connection Failure

Response:

- Retry connection
- Display status

---

## Invalid Event

Response:

- Ignore event
- Log error

---

## Authentication Failure

Response:

- Refresh session
- Redirect login

---

# 24. Performance Optimization

Realtime systems should:

- Limit subscriptions
- Batch updates
- Avoid unnecessary renders
- Clean inactive listeners
- Use efficient state selectors

---

# 25. Monitoring Requirements

Monitor:

- Connection count
- Connection failures
- Event latency
- Dropped messages
- Reconnection frequency

---

# 26. Testing Strategy

Testing includes:

## Unit Tests

Test:

- Event parsing
- State updates
- Handlers

---

## Integration Tests

Test:

- WebSocket connection
- Event delivery

---

## End-to-End Tests

Example:

```
Start Voice Call

↓

Receive Events

↓

Display Transcript

↓

Complete Session
```

---

# 27. Future Expansion

The architecture supports:

- Multi-user collaboration
- Live dashboards
- Real-time agent analytics
- Mobile clients
- Additional realtime channels

---

# 28. Summary

The Realtime Communication Architecture defines how the Voice Agent SaaS Platform frontend receives and processes live platform events.

By combining LiveKit, WebSockets, event-driven design, and isolated realtime state management, the frontend can provide responsive voice experiences and operational visibility at enterprise scale.
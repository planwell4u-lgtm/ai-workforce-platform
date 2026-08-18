# 06 Event Driven Service Example
# Event-Driven Service Example

**Version:** 2.0

---

# 1. Overview

This document provides a production-ready example of implementing event-driven communication between services in the Voice Agent SaaS platform.

Rather than tightly coupling services through synchronous API calls, an event-driven architecture enables services to publish domain events that other services can consume independently. This approach improves scalability, resiliency, and maintainability.

Typical use cases include:

- Agent lifecycle events
- Voice call events
- Conversation updates
- RAG indexing
- Memory consolidation
- Billing usage tracking
- Notifications
- Audit logging
- Analytics processing
- Workflow automation

---

# 2. Architecture

```
                  Service A
          (Agent Management)
                     │
                     ▼
             Publish Event
                     │
                     ▼
              Event Broker
        (Redis Streams / Kafka)
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 Memory Service  Analytics   Notification
      │              │              │
      ▼              ▼              ▼
 PostgreSQL     Data Warehouse    Email/SMS
```

---

# 3. Event Flow

```
API Request

      │

Business Validation

      │

Database Transaction

      │

Commit Changes

      │

Publish Domain Event

      │

Event Broker

      │

Subscribers Process Event

      │

Update Independent Services
```

Events should only be published **after** a successful transaction has committed.

---

# 4. Recommended Technologies

| Component | Recommended Technology |
|-----------|------------------------|
| Event Broker | Redis Streams |
| Large Scale Broker | Apache Kafka |
| Lightweight Messaging | RabbitMQ |
| Serialization | JSON / Avro |
| Monitoring | Prometheus |
| Tracing | OpenTelemetry |

---

# 5. Example Event Types

Common domain events include:

- AgentCreated
- AgentUpdated
- AgentDeleted
- CallStarted
- CallEnded
- ConversationCreated
- KnowledgeIndexed
- MemoryStored
- WorkflowExecuted
- UserCreated
- SubscriptionUpdated
- PaymentCompleted

Event names should use **past tense** to represent completed actions.

---

# 6. Event Schema

Example:

```json
{
    "event_id": "evt_01HKXYZ123",
    "event_type": "AgentCreated",
    "timestamp": "2026-07-31T12:30:15Z",
    "tenant_id": "tenant_001",
    "correlation_id": "corr_abc123",
    "producer": "agent-service",
    "version": "1.0",
    "data": {
        "agent_id": "agent_1001",
        "name": "Support Assistant"
    }
}
```

---

# 7. Event Publisher Example

```python
import json

from redis import Redis

redis = Redis()


def publish_agent_created(event):

    redis.xadd(

        "agent.events",

        {

            "payload": json.dumps(event)

        }

    )
```

The publishing service should not know which services consume the event.

---

# 8. Event Consumer Example

```python
def handle_agent_created(event):

    data = event["data"]

    agent_id = data["agent_id"]

    print(

        f"Processing {agent_id}"

    )
```

Consumers should be independent and isolated.

---

# 9. Event Topics

Recommended stream organization:

```
agent.events

call.events

workflow.events

knowledge.events

memory.events

billing.events

notification.events

audit.events
```

Avoid combining unrelated domains into a single stream.

---

# 10. Delivery Guarantees

Recommended delivery model:

```
Publisher

      │

Persist Event

      │

Broker

      │

Consumer

      │

Acknowledge
```

Target delivery semantics:

- At-least-once delivery
- Idempotent consumers
- Durable event storage

---

# 11. Idempotent Consumers

Consumers must safely handle duplicate events.

Example:

```
Receive Event

      │

Check Event ID

      │

Already Processed?

      │

Yes → Ignore

      │

No

      │

Process Event

      │

Store Event ID
```

This prevents duplicate processing after retries.

---

# 12. Error Handling

Consumer workflow:

```
Receive Event

      │

Process

      │

Success?

      │

Yes → ACK

      │

No

      │

Retry

      │

Max Retries?

      │

Yes

      │

Dead Letter Queue
```

Failed events should never be silently discarded.

---

# 13. Dead Letter Queue (DLQ)

A Dead Letter Queue stores events that cannot be processed successfully.

Typical reasons:

- Invalid payload
- Missing dependencies
- Corrupt data
- Permanent processing failures

DLQs allow later inspection and replay.

---

# 14. Ordering

When ordering matters:

- Partition by aggregate ID
- Preserve event sequence
- Process sequentially

Example:

```
AgentCreated

↓

AgentUpdated

↓

AgentActivated

↓

AgentDeleted
```

Consumers should not assume ordering across unrelated entities.

---

# 15. Observability

Each published event should include:

- Event ID
- Correlation ID
- Tenant ID
- Producer
- Timestamp
- Version

Monitor:

- Published events/sec
- Consumer lag
- Failed events
- Retry count
- Processing latency

---

# 16. Security

Event systems should:

- Encrypt communication
- Authenticate producers
- Authorize consumers
- Validate schemas
- Avoid sensitive payloads
- Mask confidential information

Personally identifiable information (PII) should not be broadcast unless required.

---

# 17. Testing

Test scenarios should include:

- Event publication
- Consumer processing
- Duplicate events
- Retry behavior
- Dead Letter Queue handling
- Ordering
- Schema compatibility
- High-volume event processing

---

# 18. Best Practices

Always:

- Publish immutable events
- Version event schemas
- Keep payloads compact
- Use correlation IDs
- Design idempotent consumers
- Log event processing
- Monitor broker health

Avoid:

- Synchronous dependencies between publishers and consumers
- Large event payloads
- Breaking schema changes
- Business logic inside the broker
- Circular event chains

---

# 19. Example End-to-End Workflow

```
Create Agent Request

        │

Agent Service

        │

Save Agent

        │

Publish AgentCreated

        │

Redis Streams

   ┌────┼────┬────────┐
   ▼    ▼    ▼        ▼

Memory Analytics Audit Notification

   │    │    │        │

Independent Processing

   │    │    │        │

Complete
```

Each subscriber processes the event independently without affecting the others.

---

# 20. Summary

An event-driven architecture enables loose coupling between services while supporting scalability, resilience, and extensibility.

By publishing immutable domain events and designing idempotent consumers, the Voice Agent SaaS platform can evolve independently across services, simplify integrations, and support high-throughput production workloads with reliable asynchronous communication.
# 21. Message Queue Design

**Version:** 2.0  
**Status:** Production Ready  
**Owner:** Platform Engineering

---

# 1. Purpose

The Message Queue Architecture defines how asynchronous communication is implemented across backend services.

Message queues provide reliable delivery, workload buffering, service decoupling, and fault tolerance for the Voice Agent SaaS platform.

The message queue layer enables:

- Background processing
- Event distribution
- Task execution
- Service decoupling
- Retry handling
- Failure recovery
- Traffic smoothing

---

# 2. Objectives

The Message Queue system provides:

- Reliable message delivery
- Asynchronous processing
- Horizontal scalability
- Fault isolation
- Message persistence
- Retry capabilities
- Dead-letter handling
- Monitoring and observability

---

# 3. High-Level Architecture

```text
                 Backend Services

                       │

                       ▼

                Message Producer

                       │

                       ▼

              Message Broker Layer

                       │

        ┌──────────────┼──────────────┐

        ▼              ▼              ▼

     Queue A        Queue B        Queue C

        │              │              │

        ▼              ▼              ▼

    Worker A       Worker B       Worker C

                       │

                       ▼

               Processing Complete

                       │

                       ▼

                  Event Published
```

---

# 4. Why Message Queues Are Required

Synchronous communication creates tight dependencies.

Example:

Without Queue:

```text
API Request

↓

Generate Embeddings

↓

Send Email

↓

Create Report

↓

Return Response
```

The user waits for every operation.

---

With Queue:

```text
API Request

↓

Create Job

↓

Return Response

↓

Background Processing
```

The system becomes faster and more reliable.

---

# 5. Message Queue Use Cases

The platform uses queues for:

## AI Processing

- Embedding generation
- Document processing
- Summarization
- Agent evaluation

---

## Voice Processing

- Recording processing
- Transcription
- Call analytics
- Quality analysis

---

## Notifications

- Email delivery
- SMS delivery
- Push notifications
- Webhook delivery

---

## Billing

- Usage calculation
- Invoice generation
- Payment reconciliation

---

## System Operations

- Scheduled tasks
- Data cleanup
- Synchronization jobs
- Report generation

---

# 6. Message Broker Options

Supported technologies:

| Technology | Best Use |
|---|---|
| RabbitMQ | Task queues and reliable messaging |
| Apache Kafka | High-volume event streaming |
| Redis Streams | Lightweight queues |
| NATS | Low-latency messaging |
| AWS SQS | Managed cloud queues |

---

# 7. Recommended Platform Strategy

For the Voice Agent SaaS platform:

```
Primary Event Streaming:

Apache Kafka

↓

Business Events

--------------------------------

Task Processing:

RabbitMQ / Redis Streams

↓

Background Jobs
```

This separates:

- Event streaming
- Task execution

---

# 8. Queue Types

## Task Queues

Used for background jobs.

Examples:

```
embedding_jobs

email_jobs

billing_jobs

report_jobs
```

---

## Event Topics

Used for broadcasting events.

Examples:

```
call.completed

payment.successful

agent.created
```

---

## Dead-Letter Queues

Used for failed messages.

Examples:

```
failed_notifications

failed_embeddings

failed_payments
```

---

# 9. Message Structure

All messages should follow a standard format.

Example:

```json
{
  "message_id": "uuid",
  "message_type": "embedding.generate",
  "version": "1.0",
  "created_at": "2026-07-25T12:00:00Z",
  "tenant_id": "tenant_uuid",
  "correlation_id": "request_uuid",
  "payload": {
    "document_id": "123",
    "chunks": 50
  }
}
```

---

# 10. Message Metadata

Required metadata:

| Field | Purpose |
|---|---|
| message_id | Unique identifier |
| message_type | Message category |
| version | Schema version |
| timestamp | Creation time |
| tenant_id | Tenant isolation |
| correlation_id | Request tracking |
| retry_count | Retry tracking |
| priority | Processing priority |

---

# 11. Message Lifecycle

```text
Message Created

↓

Published

↓

Stored

↓

Consumed

↓

Processing

↓

Acknowledged

↓

Completed
```

---

# 12. Message Acknowledgement

Consumers must acknowledge successful processing.

Flow:

```text
Receive Message

↓

Process

↓

Success

↓

ACK

↓

Remove Message
```

If processing fails:

```text
Receive Message

↓

Failure

↓

NACK

↓

Retry
```

---

# 13. Retry Strategy

Retry policies include:

- Maximum attempts
- Retry delay
- Exponential backoff
- Retry classification
- Failure tracking

Example:

```text
Attempt 1

↓

10 seconds

↓

Attempt 2

↓

60 seconds

↓

Attempt 3

↓

Move to DLQ
```

---

# 14. Dead-Letter Queue Strategy

Messages enter DLQ when:

- Maximum retries exceeded
- Invalid payload
- Permanent failure
- Consumer error

DLQ provides:

- Investigation
- Manual retry
- Debugging
- Failure analytics

---

# 15. Message Ordering

Some workflows require ordering.

Examples:

```
Call Started

↓

Call Connected

↓

Call Completed
```

Ordering strategies:

- Partition keys
- FIFO queues
- Sequence numbers

---

# 16. Message Priority

Priority levels:

| Priority | Examples |
|---|---|
| Critical | Payment processing |
| High | Voice events |
| Normal | Notifications |
| Low | Reports |
| Background | Cleanup |

---

# 17. Idempotent Consumers

Consumers must safely handle duplicate messages.

Example:

```text
Message Received

↓

Check message_id

↓

Already Processed?

↓

Ignore

```

This prevents:

- Duplicate billing
- Duplicate notifications
- Duplicate workflows

---

# 18. Queue Scaling

Queues scale using:

- Multiple consumers
- Worker pools
- Partitioning
- Auto-scaling
- Load balancing

Example:

```text
Queue

↓

Worker 1

Worker 2

Worker 3

Worker 4
```

---

# 19. Monitoring

Important metrics:

- Queue depth
- Processing latency
- Message throughput
- Consumer lag
- Retry count
- DLQ size
- Failed messages
- Broker health

---

# 20. Security

Message security includes:

- Encryption in transit
- Authentication
- Authorization
- Tenant validation
- Schema validation
- Access control
- Audit logging

---

# 21. Failure Handling

The system handles failures through:

- Automatic retries
- Dead-letter queues
- Circuit breakers
- Consumer recovery
- Message replay
- Manual intervention

---

# 22. Integration Points

Message Queues integrate with:

- Event-Driven Architecture
- Background Workers
- Workflow Service
- Notification Service
- Billing Service
- Integration Service
- Agent Runtime
- Knowledge Service
- RAG Service
- Memory Service

---

# 23. Example Message Flows

## Document Processing

```text
User Uploads Document

↓

Knowledge Service

↓

document.process.requested

↓

Message Queue

↓

Document Worker

↓

Chunk Generation

↓

Embedding Worker

↓

knowledge.ready Event
```

---

## Voice Call Processing

```text
Call Completed

↓

Voice Service

↓

call.completed Event

↓

Message Broker

↓

Billing Worker

↓

Analytics Worker

↓

Memory Worker
```

---

# 24. Future Enhancements

Planned capabilities:

- Global event streaming platform
- Schema registry
- Message replay UI
- Queue analytics dashboard
- Automatic workload balancing
- AI-based failure prediction
- Cross-region replication

---

# 25. Design Principles

The Message Queue Architecture follows:

- Reliable delivery
- Loose coupling
- Async-first design
- Idempotent processing
- Fault tolerance
- Horizontal scalability
- Observability
- Security by default
- Schema governance

---

# 26. Summary

The Message Queue layer provides reliable asynchronous communication throughout the Voice Agent SaaS backend. It enables scalable background processing, event distribution, workload isolation, and failure recovery. Combined with event-driven architecture and background workers, it forms the foundation for building a resilient, production-grade AI platform capable of handling large-scale voice and automation workloads.
# ADR-0008: Event Driven Architecture Decision

**Project:** Voice Agent SaaS Platform  
**Document:** Event Driven Architecture Strategy  
**ADR Number:** ADR-0008  
**Version:** 2.0  
**Status:** Accepted  
**Date:** 2026-07-24


---

# 1. Decision Summary

The Voice Agent SaaS Platform will implement an event-driven architecture for asynchronous communication between platform components.

The approved event architecture is:

| Capability | Decision |
|---|---|
| Event communication | Domain events |
| Primary event format | JSON events |
| Event transport | Message broker abstraction |
| Initial broker | Redis Streams / compatible queue system |
| Future enterprise broker | Kafka / NATS |
| Event ownership | Domain services |
| Event storage | PostgreSQL event tables where required |
| Processing model | Async workers |


The event system will support:

- Voice lifecycle events
- Agent execution events
- Knowledge processing events
- Billing events
- Audit events
- Integration events


---

# 2. Context

The platform contains multiple independent capabilities:



Voice Platform

AI Runtime

Agent Management

Knowledge System

Billing

Analytics

Integrations

Notifications



These components must communicate without creating tight dependencies.


A synchronous-only architecture creates problems:


- Slow operations
- Service coupling
- Difficult scaling
- Poor fault isolation


The platform requires asynchronous communication for long-running operations.


---

# 3. Problem Statement


The system must support:


## Real-Time Events

Examples:


- Call started
- Agent joined
- User message received
- Tool executed


---

## Background Processing

Examples:


- Document processing
- Embedding generation
- Call analysis
- Report generation


---

## Business Automation

Examples:


- New lead created
- Appointment booked
- Payment completed


---

## System Observability

The platform needs a reliable history of important actions.


---

# 4. Event Architecture Goals


The event system must provide:


## Loose Coupling


Services should communicate through events instead of direct dependencies.


---

## Scalability


Consumers should scale independently.


---

## Reliability


Events should support:


- Retry
- Failure handling
- Monitoring


---

## Auditability


Important business events should be traceable.


---

# 5. Options Considered


---

# Option 1: Direct Service Communication Only


Architecture:



Service A

|

API Call

|

Service B



## Advantages

- Simple
- Easy debugging


## Disadvantages

- Tight coupling
- Poor scalability
- Failure propagation


## Decision

Rejected as the only communication method.


---

# Option 2: Database Polling


Architecture:



Database Change

  |

Polling Worker

  |

Process Event



## Advantages

- Simple implementation


## Disadvantages

- Inefficient
- Higher latency
- Database pressure


## Decision

Rejected.


---

# Option 3: Event Driven Architecture


Architecture:



Service

|

Domain Event

|

Event Broker

|

Consumers



## Advantages

- Loose coupling
- Independent scaling
- Better resilience
- Async processing


## Disadvantages

- Requires event design discipline


## Decision

Accepted.


---

# 6. Final Event Architecture


The platform will implement:


             Domain Service


                   |


                   v


            Event Publisher


                   |


                   v


            Event Broker


                   |


    --------------------------------


    |              |               |

AI Worker Analytics Integrations

    |

    v

Event Consumer



---

# 7. Event Ownership Model


Each domain owns its events.


Examples:


## Voice Domain


Owns:



call.started

call.connected

call.completed

call.recording.created



---

## Agent Domain


Owns:



agent.created

agent.updated

agent.execution.started

agent.execution.completed



---

## Knowledge Domain


Owns:



document.uploaded

document.processed

embedding.generated



---

## Billing Domain


Owns:



usage.recorded

subscription.updated

invoice.created



---

# 8. Event Structure


All events follow a standard format.


Example:


```json
{
  "event_id": "uuid",
  "event_type": "call.completed",
  "version": "1.0",
  "tenant_id": "tenant-id",
  "timestamp": "2026-07-24T12:00:00Z",
  "source": "voice-service",
  "data": {}
}
9. Event Categories

Events are divided into:

Domain Events

Represent business changes.

Examples:

AgentCreated

CallCompleted

DocumentProcessed
Integration Events

Communicate with external systems.

Examples:

CRMLeadCreated

CalendarAppointmentBooked
System Events

Infrastructure events.

Examples:

WorkerFailed

ServiceStarted

DeploymentCompleted
10. Voice Event Architecture

Voice events include:

Call Lifecycle
call.initiated

call.ringing

call.connected

call.completed

call.failed
AI Interaction
agent.started

conversation.started

message.received

response.generated
Recording
recording.started

recording.completed

transcript.created
11. AI Runtime Events

AI Runtime publishes:

agent.execution.started

agent.execution.completed

tool.called

tool.completed

memory.updated

Consumers:

Analytics
Monitoring
Billing
12. Knowledge Processing Events

Knowledge pipeline events:

document.uploaded

document.extracted

chunk.created

embedding.generated

knowledge.indexed
13. Event Processing Model

Processing flow:

Event Created


      |


Published


      |


Broker


      |


Consumer


      |


Handler


      |


Success / Retry / Failure
14. Failure Handling

The event system must support:

Retry

Temporary failures retry automatically.

Dead Letter Queue

Failed events move to:

DLQ

for investigation.

Idempotency

Consumers must safely process duplicate events.

15. Event Ordering

Critical events require ordering.

Examples:

call.started

before

call.completed

The system must preserve ordering where required.

16. Event Storage Strategy

Not every event requires permanent storage.

Stored events include:

Business audit events
Billing events
Compliance events

Temporary events:

Runtime signals
Metrics events
17. Event Security

Events must include:

Tenant validation
Authentication
Authorization
Sensitive data protection
18. Observability Requirements

Track:

Event Metrics
Published events
Processed events
Failed events
Performance
Processing latency
Queue depth
Reliability
Retry count
Consumer failures
19. Implementation Rules
Rule 1

Domains own their events.

Rule 2

Events are immutable.

Rule 3

Consumers must be idempotent.

Rule 4

Event schemas require versioning.

Rule 5

Critical events require monitoring.

20. Consequences
Positive Consequences
Better scalability
Loose coupling
Independent services
Reliable background processing
Negative Consequences
More architectural complexity
Requires event discipline
Debugging distributed flows is harder
21. Future Evolution

Future improvements:

Kafka deployment
Event sourcing
Advanced workflow orchestration
Cross-region event replication

Major changes require a new ADR.

22. Related Documents

Architecture:

08_Event_Architecture.md
07_Data_Flow_Architecture.md
16_Observability_Architecture.md
19_Service_Communication.md

Implementation:

Event Schema Registry
Message Broker Configuration
Worker Architecture
Integration Framework
Final Statement

The Voice Agent SaaS Platform will use event-driven architecture to enable scalable asynchronous communication between platform domains.

This approach provides:

Loose coupling
Reliable background processing
Better scalability
Improved observability
Future distributed system readiness

while maintaining clear ownership boundaries between services.



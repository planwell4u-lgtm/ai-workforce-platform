# ADR-0038: Event Driven Architecture Strategy Decision

**Project:** Voice Agent SaaS Platform  
**Document:** Event Driven Architecture Strategy  
**ADR Number:** ADR-0038  
**Version:** 2.0  
**Status:** Accepted  
**Date:** 2026-07-24


---

# 1. Decision Summary

The Voice Agent SaaS Platform will adopt an event-driven architecture for asynchronous communication, workflow coordination, auditability, and scalable service integration.

The event architecture will support:

- Voice call events
- Agent lifecycle events
- Workflow events
- Tenant events
- Billing events
- Security events
- Analytics events
- Integration events


Architecture:


             Platform Services


                   |


          Event Publishing Layer


                   |


          Event Infrastructure


                   |

| | | |

Workers Analytics Integrations Audit



---

# 2. Context


The platform consists of multiple distributed services:



Frontend

API Backend

Voice Gateway

AI Runtime

Agent Workers

RAG System

Memory System

Billing

Analytics

External Integrations



Direct service-to-service communication creates:

- Tight coupling
- Difficult scaling
- Complex failure handling


An event-driven model allows services to communicate asynchronously.

---

# 3. Problem Statement


The platform requires:


## Loose Coupling


Services should evolve independently.


---

## Scalability


High-volume operations should not block core workflows.


---

## Reliability


Temporary failures should not lose important information.


---

## Auditability


Important system actions must be traceable.


---

# 4. Goals


The event strategy provides:


## Asynchronous Processing


Long-running operations execute independently.


---

## Real-Time Reactions


Services respond automatically to events.


---

## System Extensibility


New consumers can subscribe without modifying producers.


---

## Operational Visibility


All important actions become traceable.


---

# 5. Options Considered


---

# Option 1: Synchronous API Communication Only


Architecture:



Service A

|

HTTP Request

|

Service B



## Advantages


- Simple
- Easy to understand


## Disadvantages


- Tight coupling
- Poor scalability
- Cascading failures


## Decision

Rejected.


---

# Option 2: Database Polling


Architecture:



Database

|

Polling Workers



## Advantages


- Simple implementation


## Disadvantages


- Inefficient
- Delayed processing


## Decision

Rejected.


---

# Option 3: Event Driven Architecture


Architecture:



Service

|

Event Bus

|

Consumers



## Advantages


- Scalable
- Flexible
- Reliable


## Decision

Accepted.


---

# 6. Final Event Architecture


             Service


                |


          Event Publisher


                |


          Event Bus


                |

| | | |

Consumer A Consumer B Consumer C Audit



---

# 7. Event Categories


The platform defines:


---

# 7.1 Voice Events


Examples:



call.started

call.connected

call.completed

call.transferred

call.recording.created



---

# 7.2 Agent Events


Examples:



agent.created

agent.updated

agent.executed

agent.failed

agent.completed



---

# 7.3 Conversation Events


Examples:



conversation.started

message.created

conversation.completed

conversation.escalated



---

# 7.4 Workflow Events


Examples:



workflow.started

workflow.step.completed

workflow.failed

workflow.finished



---

# 7.5 Tenant Events


Examples:



tenant.created

tenant.updated

tenant.deleted

subscription.changed



---

# 7.6 Billing Events


Examples:



usage.recorded

invoice.created

payment.completed



---

# 7.7 Security Events


Examples:



login.success

permission.changed

security.alert



---

# 8. Event Structure


All events follow a standard schema:


```json
{
  "event_id": "uuid",
  "event_type": "call.started",
  "tenant_id": "tenant-id",
  "timestamp": "datetime",
  "source": "voice-service",
  "version": "1.0",
  "payload": {}
}
9. Event Naming Convention

Format:

domain.entity.action

Examples:

call.started

agent.created

document.indexed

user.invited

10. Event Delivery Guarantees

The platform supports:

At Least Once Delivery

Events may be delivered multiple times.

Consumers must be idempotent.

Retry Handling

Failed processing should retry.

Dead Letter Queue

Failed events are stored for investigation.

11. Event Processing Model

Flow:

Event Created

      |

Published

      |

Consumed

      |

Processed

      |

Acknowledged

12. Event Infrastructure

Possible technologies:

Message Brokers

Examples:

Kafka
NATS
RabbitMQ
Redis Streams
Cloud Services

Examples:

Managed Kafka
Cloud messaging services
13. Event Driven Use Cases
Call Processing
Call Started

 |

Create Conversation

 |

Assign Agent

 |

Begin Runtime

Analytics Processing
Conversation Completed

 |

Generate Analytics

 |

Update Dashboard

Billing
Usage Recorded

 |

Calculate Cost

 |

Update Invoice

RAG Processing
Document Uploaded

 |

Process Document

 |

Create Embeddings

 |

Index Knowledge

14. Event Storage Strategy

Important events may be stored for:

Audit
Debugging
Analytics
Compliance

Storage:

PostgreSQL

+

Event Storage

15. Event Security

Controls:

Authentication
Authorization
Encryption
Tenant isolation
16. Observability

Track:

Event volume
Processing latency
Failed events
Consumer health
17. Implementation Rules
Rule 1

Events must have documented schemas.

Rule 2

Consumers must be idempotent.

Rule 3

Events must include tenant context.

Rule 4

Critical events require audit storage.

Rule 5

Breaking event changes require versioning.

18. Consequences
Positive Consequences
Better scalability
Service independence
Improved reliability
Easier integrations
Negative Consequences
More infrastructure
Event debugging complexity
Requires schema governance
19. Future Evolution

Future capabilities:

Event sourcing
Real-time analytics platform
AI event monitoring
Automated workflow triggers
Cross-tenant analytics

Major changes require new ADRs.

20. Related Documents

Architecture:

08_Event_Architecture.md
19_Service_Communication.md
17_Integration_Architecture.md

Related ADRs:

ADR-0030_Platform_Monitoring_and_SLO_Strategy.md
ADR-0031_Developer_Experience_and_Platform_Tooling_Strategy.md
ADR-0037_Voice_AI_Provider_Abstraction_Strategy.md
Final Statement

The Voice Agent SaaS Platform will use event-driven architecture as a core communication pattern to support scalable, reliable, and extensible AI operations.

This enables:

Distributed service coordination
Real-time processing
Enterprise scalability
Future platform expansion
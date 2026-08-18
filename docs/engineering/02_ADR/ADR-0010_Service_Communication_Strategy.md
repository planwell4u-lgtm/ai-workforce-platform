# ADR-0010: Service Communication Strategy Decision

**Project:** Voice Agent SaaS Platform  
**Document:** Service Communication Architecture Strategy  
**ADR Number:** ADR-0010  
**Version:** 2.0  
**Status:** Accepted  
**Date:** 2026-07-24


---

# 1. Decision Summary

The Voice Agent SaaS Platform will use a hybrid service communication architecture combining:

- Synchronous APIs for immediate request/response operations
- Asynchronous events for distributed workflows
- gRPC for selected high-performance internal communication


The approved communication model:


| Communication Type | Technology | Usage |
|---|---|---|
| External clients → Platform | REST API | User and application access |
| Frontend → Backend | REST + WebSocket | Dashboard and real-time updates |
| Service → Service | REST / Events | Domain communication |
| AI Runtime communication | Internal APIs + Events | Agent execution |
| High-performance internal calls | gRPC | Selected services |
| Background processing | Event queues | Async workloads |


---

# 2. Context


The platform contains multiple independent domains:



Authentication Service

Tenant Service

Agent Service

Voice Service

AI Runtime Service

Knowledge Service

Memory Service

Integration Service

Billing Service

Analytics Service



Each domain owns its own responsibilities.

Services must communicate without creating strong dependencies.

---

# 3. Problem Statement


Poor service communication creates:


- Tight coupling
- Difficult deployments
- Cascading failures
- Database dependencies
- Poor scalability


The platform requires communication patterns that support:


- Real-time voice operations
- AI workflows
- Background processing
- External integrations
- Future scaling


---

# 4. Communication Principles


The architecture follows these principles:


## Principle 1: Services Own Their Data


A service owns its database tables.


Example:



Agent Service

owns

agent tables



Other services must not directly modify those tables.


---

## Principle 2: APIs Over Database Access


Incorrect:



Service A

  |

Direct Database Access

  |

Service B Tables



Correct:



Service A

  |

Service B API

  |

Service B Database



---

## Principle 3: Events For State Changes


Services publish events when important business changes occur.


Example:



Agent Created

  |

agent.created event

  |

Consumers



---

# 5. Options Considered


---

# Option 1: Shared Database Communication


Architecture:



Service A

  |

Shared Database

  |

Service B



## Advantages

- Simple initially
- Fast development


## Disadvantages

- Strong coupling
- No ownership boundaries
- Difficult scaling
- Security risks


## Decision

Rejected.


---

# Option 2: API Only Communication


Architecture:



Service A

  |

REST API

  |

Service B



## Advantages

- Clear ownership
- Easy understanding


## Disadvantages

- Poor for asynchronous workloads
- Increased dependencies
- Difficult event processing


## Decision

Not sufficient alone.


---

# Option 3: Hybrid Communication Model


Architecture:



Service A

| \

API Event

| \

Service B Consumers



## Advantages

- Flexible
- Scalable
- Clear boundaries
- Better resilience


## Decision

Accepted.


---

# 6. Final Communication Architecture


             API Gateway


                  |


    --------------------------------


    |              |               |

Authentication Agent API Voice API

    |              |               |


    --------------------------------


                  |


          Domain Services


                  |


    --------------------------------


    |                              |


 REST APIs                    Event Bus


                                  |


                     -----------------------


                     |          |           |


                  Workers   Analytics   Integrations


---

# 7. Communication Patterns


The platform uses:


---

# 7.1 Synchronous Communication


Used when immediate response is required.


Examples:



Create Agent

Get Call Status

Check Appointment Availability



Technology:



REST API



---

# 7.2 Asynchronous Communication


Used for long-running operations.


Examples:



Document Processing

Call Analysis

Embedding Generation

Billing Calculation



Technology:



Events + Workers



---

# 7.3 Real-Time Communication


Used for:


- Live call status
- Agent state
- Dashboard updates


Technology:



WebSocket

WebRTC



---

# 8. Service Communication Rules


## Rule 1

Services must not directly access another service database.


---

## Rule 2

Services communicate through APIs or events.


---

## Rule 3

Each service owns its domain events.


---

## Rule 4

Events must be versioned.


---

## Rule 5

All communication requires observability.


---

# 9. Core Service Communication Map


---

# Authentication Service


Communicates with:



Tenant Service

User Service

API Gateway



Responsibilities:


- Identity validation
- Token generation
- Access control


---

# Tenant Service


Communicates with:



Authentication

All Domain Services



Responsibilities:


- Tenant context
- Organization management


---

# Agent Service


Communicates with:



AI Runtime

Voice Service

Knowledge Service



Responsibilities:


- Agent configuration
- Agent lifecycle


---

# Voice Service


Communicates with:



Agent Service

AI Runtime

Analytics



Responsibilities:


- Call handling
- SIP integration
- Voice sessions


---

# AI Runtime Service


Communicates with:



Agent Service

Memory Service

Knowledge Service

Tool Services



Responsibilities:


- Agent execution
- Reasoning
- Tool calling


---

# Knowledge Service


Communicates with:



AI Runtime

Document Processing Workers



Responsibilities:


- Document ingestion
- Retrieval


---

# Billing Service


Communicates with:



Usage Events

Subscription System



Responsibilities:


- Usage tracking
- Billing calculation


---

# 10. Event Communication Rules


Events must contain:


```json
{
 "event_id": "uuid",
 "event_type": "agent.created",
 "tenant_id": "tenant-id",
 "timestamp": "datetime",
 "source": "agent-service",
 "data": {}
}
11. Avoid Shared Database Access

Services should not directly modify another service's tables.

Incorrect:

Voice Service

      |

UPDATE agent_table

      |

Agent Database
``` id="7q0f8v"


Correct:



Voice Service

  |

Agent API

  |

Agent Service

  |

Agent Database



---

# 12. Error Handling


Communication failures require:


## Retry

Temporary failures retry automatically.


---

## Timeout

Every external call requires timeout handling.


---

## Circuit Breaker

Prevent cascading failures.


---

## Dead Letter Queue

Failed events require investigation.


---

# 13. Security Requirements


Communication must enforce:


- Authentication
- Authorization
- Tenant validation
- Encryption
- Service identity verification


---

# 14. Observability Requirements


All communication must include:



Request ID

Correlation ID

Tenant ID

Service Name



Track:


- Latency
- Failures
- Retries
- Event processing time


---

# 15. Consequences


## Positive Consequences


- Clear service ownership
- Better scalability
- Easier maintenance
- Reduced coupling


---

## Negative Consequences


- More infrastructure
- Distributed debugging complexity
- Requires governance


---

# 16. Future Evolution


Future improvements:


- Service mesh
- Advanced message broker
- Event sourcing
- Cross-region communication


Major changes require new ADRs.


---

# 17. Related Documents


Architecture:


- 19_Service_Communication.md
- 18_API_Architecture.md
- 08_Event_Architecture.md
- 16_Observability_Architecture.md


Related ADRs:


- ADR-0008_Event_Driven_Architecture.md
- ADR-0009_API_Architecture_Strategy.md


---

# Final Statement


The Voice Agent SaaS Platform will use a hybrid service communication architecture based on REST APIs, asynchronous events, and selective gRPC communication.

This approach provides:

- Clear service boundaries
- Scalable communication
- Reliable distributed workflows
- Strong ownership models
- Future enterprise readiness

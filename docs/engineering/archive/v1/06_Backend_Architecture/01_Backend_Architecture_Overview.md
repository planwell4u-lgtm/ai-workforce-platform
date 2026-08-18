# Backend Architecture Overview

**Document Version:** 1.0
**Project:** AI Voice Agent SaaS Platform
**Phase:** 06 - Backend Architecture
**Backend Framework:** FastAPI (Python)
**Architecture Style:** Modular Service-Oriented Architecture
**Database:** Supabase PostgreSQL
**Cache:** Redis
**Realtime:** LiveKit
**AI Runtime:** LangChain + LangGraph
**Status:** Draft
**Last Updated:** 2026-07-23

---

# 1. Overview

This document defines the backend architecture of the AI Voice Agent SaaS platform.

The backend is responsible for:

* API management
* Authentication
* Tenant management
* AI agent orchestration
* Voice call processing
* RAG retrieval
* Workflow execution
* Billing
* Integrations
* Background processing

---

# 2. Backend Architecture Goals

The backend must provide:

```text
✓ Scalable SaaS architecture

✓ Multi-tenant isolation

✓ Production API design

✓ Real-time voice processing

✓ AI agent orchestration

✓ Secure integrations

✓ Background processing

✓ Observability
```

---

# 3. High-Level Backend Architecture

```text
                    Client Applications

                            |

                            v

                    API Gateway Layer

                            |

                            v

                    FastAPI Backend

 ------------------------------------------------

 Authentication Service

 Tenant Service

 Agent Service

 Voice Service

 Conversation Service

 Knowledge Service

 Workflow Service

 Billing Service

 Integration Service

 Analytics Service

 Notification Service

 ------------------------------------------------

                            |

             ---------------------------------

             |              |               |

       PostgreSQL        Redis          External

       Supabase          Cache          Services

                                     

             |

             v

        AI Agent Runtime

             |

    ----------------------------

    |            |             |

 LangGraph   LangChain     Tools

```

---

# 4. Backend Technology Stack

| Layer          | Technology           |
| -------------- | -------------------- |
| API Framework  | FastAPI              |
| Language       | Python               |
| ORM            | SQLAlchemy           |
| Migration      | Alembic              |
| Database       | PostgreSQL           |
| Platform       | Supabase             |
| Cache          | Redis                |
| Queue          | Celery / Redis Queue |
| AI Framework   | LangChain            |
| Agent Runtime  | LangGraph            |
| Voice Runtime  | LiveKit              |
| Authentication | JWT                  |
| Testing        | Pytest               |

---

# 5. Backend Components

```text id="d8q2me"
Backend

├── API Layer

├── Authentication

├── Domain Services

├── Repository Layer

├── AI Runtime

├── Background Workers

├── Event System

├── Integration Layer

└── Infrastructure Layer
```

---

# 6. Request Flow

Example:

Customer sends API request:

```text id="7i8m2r"
Client

↓

FastAPI Router

↓

Authentication Middleware

↓

Tenant Validation

↓

Service Layer

↓

Repository Layer

↓

Database

↓

Response
```

---

# 7. Voice Call Processing Flow

```text id="v6q8m3"
Incoming PSTN Call

        |

        v

Twilio SIP

        |

        v

LiveKit Room

        |

        v

FastAPI Voice Service

        |

        v

Agent Runtime

        |

 -----------------------

 |          |            |

STT       LLM          TTS


        |

        v

Customer Response
```

---

# 8. AI Agent Runtime Integration

The backend coordinates:

```text id="9m4x2q"
FastAPI

    |

    v

Agent Manager

    |

    v

LangGraph Workflow

    |

 ----------------

 |              |

Tools        Memory

    |

    v

LLM Provider
```

---

# 9. Modular Backend Design

Each business capability is isolated.

Example:

```text id="m7x1q9"
agent/

    api/

    service/

    repository/

    models/

    schemas/


voice/

    api/

    service/

    repository/

```

---

# 10. Backend Layers

## API Layer

Responsible for:

* HTTP endpoints
* Validation
* Authentication checks

---

## Service Layer

Responsible for:

* Business logic
* Workflows
* Domain rules

---

## Repository Layer

Responsible for:

* Database access
* Queries
* Persistence

---

## Infrastructure Layer

Responsible for:

* External APIs
* Redis
* Storage
* Messaging

---

# 11. Dependency Flow

Correct:

```text
API

↓

Service

↓

Repository

↓

Database
```

Never:

```text
API

↓

Database Directly
```

---

# 12. Multi-Tenant Request Context

Every request carries:

```json
{
 "user_id":"uuid",

 "tenant_id":"uuid",

 "role":"admin"
}
```

Flow:

```text
JWT

↓

Middleware

↓

Tenant Context

↓

Services

↓

Database Queries
```

---

# 13. Backend Project Structure Preview

```text
backend/

├── app/

│

├── api/

├── core/

├── modules/

├── database/

├── workers/

├── integrations/

├── ai/

├── tests/

└── migrations/
```

---

# 14. Background Processing

Required for:

* Audio processing
* Embeddings
* Reports
* Webhooks
* Long workflows

Architecture:

```text
FastAPI

↓

Queue

↓

Worker

↓

Database
```

---

# 15. Event Driven Architecture

Events:

```text
CallStarted

CallEnded

DocumentUploaded

EmbeddingCreated

PaymentCompleted
```

Flow:

```text
Service

↓

Event Bus

↓

Subscribers
```

---

# 16. Error Handling Strategy

Standard response:

```json
{
 "error":{
   "code":"AGENT_NOT_FOUND",
   "message":"Agent does not exist",
   "request_id":"uuid"
 }
}
```

---

# 17. Observability Integration

Backend emits:

* Logs
* Metrics
* Traces
* Audit events

Tools:

```text
OpenTelemetry

Prometheus

Grafana
```

---

# 18. Security Architecture

Includes:

* JWT validation
* RBAC
* RLS
* Rate limiting
* Secret management
* API validation

---

# 19. Deployment Architecture

Production:

```text
Users

 |

Load Balancer

 |

FastAPI Containers

 |

Workers

 |

PostgreSQL

 |

Redis
```

---

# 20. Scaling Strategy

Scale independently:

```text
API Servers

+

Agent Workers

+

Background Workers

+

Realtime Workers
```

---

# 21. Backend Development Principles

Follow:

```text
Clean Architecture

Domain Driven Design

Dependency Injection

Typed Python

Async Programming

Test Driven Development
```

---

# 22. Related Documents

| Document                           | Purpose           |
| ---------------------------------- | ----------------- |
| 02_FastAPI_Service_Architecture.md | API design        |
| 03_Project_Folder_Structure.md     | Code organization |
| 04_API_Layer_Design.md             | REST architecture |
| 05_Service_Layer_Design.md         | Business logic    |

---

# 23. Conclusion

The Backend Architecture provides the foundation for a production-grade AI Voice Agent SaaS platform.

It connects:

* FastAPI APIs
* Supabase database
* Redis realtime state
* LiveKit voice infrastructure
* LangGraph agent runtime
* External integrations

---

**End of Document**

# Project Folder Structure Guide

**Document Version:** 1.0
**Project:** AI Voice Agent SaaS Platform
**Phase:** 06 – Backend Architecture
**Section:** Project Folder Structure
**Purpose:** Master Architecture Guide
**Status:** Living Document
**Last Updated:** 2026-07-23

---

# 1. Purpose

This guide defines the **official repository architecture** for the AI Voice Agent SaaS platform.

It is the authoritative reference for:

* Repository organization
* Folder responsibilities
* Module boundaries
* Dependency rules
* Import policies
* Naming conventions
* Code ownership
* Development standards

Every engineer working on the project should follow this guide.

---

# 2. Why This Guide Exists

Large software systems become difficult to maintain when:

* Files are placed inconsistently
* Business logic is duplicated
* Modules become tightly coupled
* Responsibilities are unclear
* Architecture drifts over time

This guide prevents those problems by defining a single, consistent structure for the entire codebase.

---

# 3. Architecture Goals

The repository is designed to support:

* Enterprise SaaS
* Multi-tenancy
* AI Voice Agents
* LiveKit realtime communication
* Twilio telephony
* LangGraph orchestration
* LangChain RAG
* Supabase/PostgreSQL
* Redis
* pgvector
* Event-driven processing
* Horizontal scaling
* High test coverage
* Long-term maintainability

---

# 4. Design Principles

The repository follows these principles:

### Single Responsibility

Every directory has one purpose.

---

### High Cohesion

Related code stays together.

---

### Low Coupling

Modules communicate through interfaces instead of direct implementation dependencies whenever practical.

---

### Clear Ownership

Every feature belongs to one module.

---

### Predictable Navigation

Developers should be able to locate code without guessing.

---

### Scalability

The repository should support years of growth without requiring major restructuring.

---

# 5. Repository Philosophy

The repository is organized around **business domains**, not frameworks.

Instead of grouping code by technical type alone:

```text
controllers/
services/
repositories/
models/
```

we group it around domains:

```text
agent/
voice/
conversation/
billing/
workflow/
knowledge/
analytics/
```

Each domain owns its API, business logic, persistence, events, tests, and related assets.

---

# 6. Architectural Layers

The platform is divided into the following layers:

```text
Presentation Layer

↓

Application Layer

↓

Domain Layer

↓

Infrastructure Layer

↓

Persistence Layer
```

Each layer has clearly defined responsibilities and dependency rules.

---

# 7. Technology Stack

| Layer           | Technology           |
| --------------- | -------------------- |
| Backend         | FastAPI              |
| Language        | Python               |
| ORM             | SQLAlchemy           |
| Database        | Supabase PostgreSQL  |
| Cache           | Redis                |
| Voice           | LiveKit              |
| Telephony       | Twilio               |
| AI              | OpenAI               |
| Agent Framework | LangGraph            |
| RAG             | LangChain            |
| Vector Search   | pgvector             |
| Background Jobs | Celery / Redis Queue |
| Storage         | Supabase Storage     |
| Observability   | OpenTelemetry        |

---

# 8. Repository Overview

The project consists of several top-level repositories or workspaces.

```text
platform/

├── backend/
├── frontend/
├── infrastructure/
├── deployment/
├── docs/
├── scripts/
├── tools/
├── examples/
└── tests/
```

Each top-level directory is documented independently.

---

# 9. Documentation Structure

This folder contains the complete repository specification.

Each document focuses on one area of the architecture.

Examples include:

* Backend root
* API directory
* Core directory
* AI runtime
* LiveKit integration
* LangGraph runtime
* Workers
* Testing
* Configuration
* Docker
* CI/CD
* Coding standards

---

# 10. Audience

This guide is intended for:

* Software architects
* Backend engineers
* Frontend engineers
* DevOps engineers
* AI engineers
* QA engineers
* Technical leads

---

# 11. Scope

This guide covers:

* Repository layout
* Directory responsibilities
* Public interfaces
* Module organization
* Dependency boundaries
* Naming standards
* Import rules
* Development conventions

It does **not** replace:

* API specifications
* Database schema documentation
* Deployment guides
* Security documentation

Those are maintained separately.

---

# 12. Relationship to Other Documents

This guide complements:

```text
05_Database_Schema/
06_Backend_Architecture/
07_AI_Runtime/
08_Frontend_Architecture/
09_Deployment/
10_Observability/
```

Together, these documents define the complete platform architecture.

---

# 13. Reading Order

For new engineers, the recommended order is:

1. Architecture Principles
2. Repository Layout
3. Backend Root
4. App Directory
5. API Directory
6. Core Directory
7. Modules Directory
8. AI Runtime
9. LiveKit
10. LangGraph
11. Integrations
12. Testing
13. Coding Standards

---

# 14. Engineering Rules

All contributors should:

* Follow documented folder responsibilities.
* Keep modules cohesive.
* Avoid circular dependencies.
* Maintain backward compatibility where practical.
* Add tests for new functionality.
* Update documentation when architecture changes.

---

# 15. Change Management

Repository structure changes should be treated as architectural decisions.

Every significant structural change should include:

* Rationale
* Impact assessment
* Migration plan
* Documentation updates

---

# 16. Future Evolution

The repository is expected to evolve.

Future additions may include:

* New AI providers
* Additional telephony vendors
* Marketplace plugins
* Multi-region deployment
* Event sourcing
* Dedicated enterprise modules

The architecture should absorb these changes without major reorganization.

---

# 17. Success Criteria

A successful repository architecture allows engineers to:

* Find code quickly.
* Understand responsibilities easily.
* Add features safely.
* Scale the platform confidently.
* Maintain consistent engineering practices.

---

# 18. Conclusion

This guide is the architectural contract for the AI Voice Agent SaaS platform.

All future implementation work should align with the principles and structure defined throughout this documentation set.

---

## Next Document

**01_Architecture_Principles.md** establishes the engineering philosophy, architectural constraints, dependency direction, and core design decisions that govern the entire codebase.

---

**End of Document**

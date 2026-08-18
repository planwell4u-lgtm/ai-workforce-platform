# DOCUMENTATION_INDEX

**Project:** Voice Agent SaaS Platform

**Version:** 2.0

**Status:** Active

**Last Updated:** 2026-07-24

---

# Purpose

This document serves as the master index for all project documentation.

Its objectives are to:

- Provide a single entry point for all documentation
- Help developers quickly locate information
- Help AI assistants navigate the repository
- Prevent duplicate documentation
- Maintain documentation consistency

This document should be updated whenever new documentation is added, moved, renamed, or archived.

---

# Documentation Structure

```
docs/

├── 00_CONTROL/
├── 01_ARCHITECTURE/
├── 02_ADR/
├── 03_DATABASE/
├── 04_BACKEND/
├── 05_FRONTEND/
├── 06_VOICE_PLATFORM/
├── 07_AI_PLATFORM/
├── 08_RAG/
├── 09_MEMORY/
├── 10_AUTOMATION/
├── 11_SECURITY/
├── 12_DEPLOYMENT/
├── 13_OBSERVABILITY/
├── 14_OPERATIONS/
├── 15_TESTING/
├── 16_EXAMPLES/
└── archive/
```

---

# 00_CONTROL

Project governance and continuity.

| Document | Description |
|-----------|-------------|
| 00_README.md | Overview of the control layer |
| AI_CONTEXT.md | AI operating instructions |
| PROJECT_MASTER_ROADMAP.md | Long-term roadmap |
| PROJECT_STATE.md | Current project status |
| SESSION_LOG.md | Session history |
| PROJECT_DECISIONS.md | Engineering decisions |
| CODING_STANDARDS.md | Development standards |
| DOCUMENTATION_INDEX.md | Master documentation index |
| IMPLEMENTATION_PROGRESS.md | Implementation tracking |
| PROJECT_GLOSSARY.md | Standard terminology |
| TECH_DEBT.md | Technical debt register |
| KNOWN_LIMITATIONS.md | Current limitations |
| RISKS.md | Risk register |
| AI_PROMPTS.md | Reusable AI prompts |
| CHANGELOG.md | Project change history |
| CONTRIBUTORS.md | Contribution guide |
| VERSION.md | Version information |

---

# 01_ARCHITECTURE

System architecture and design.

Examples:

- System Overview
- Context Diagram
- High-Level Architecture
- Component Architecture
- Deployment Architecture
- Multi-Tenant Architecture
- Service Boundaries
- Data Flow
- Event Flow
- Sequence Diagrams

---

# 02_ADR

Architecture Decision Records.

Examples:

- ADR-001 Technology Stack
- ADR-002 Multi-Tenancy
- ADR-003 Database Strategy
- ADR-004 Authentication
- ADR-005 Voice Platform
- ADR-006 AI Runtime
- ADR-007 RAG Architecture
- ADR-008 Observability

---

# 03_DATABASE

Database architecture and design.

Contents include:

- ERDs
- Logical data model
- Physical data model
- Schemas
- Tables
- Relationships
- Constraints
- Indexes
- Partitioning
- Retention
- Backup strategy
- Migration strategy

---

# 04_BACKEND

Backend architecture.

Topics include:

- FastAPI
- Services
- Repositories
- Middleware
- APIs
- Background jobs
- Dependency injection
- Configuration

---

# 05_FRONTEND

Frontend architecture.

Topics include:

- Next.js
- React
- Routing
- Components
- State management
- Authentication
- Dashboard
- UI standards

---

# 06_VOICE_PLATFORM

Voice platform documentation.

Topics include:

- Twilio
- LiveKit
- SIP
- Call lifecycle
- Audio pipeline
- Recording
- Call transfer
- Dispatch
- Call events

---

# 07_AI_PLATFORM

Artificial Intelligence platform.

Topics include:

- LLM orchestration
- Prompt management
- Agent runtime
- LangChain
- LangGraph
- Tool calling
- AI Skills
- MCP integration

---

# 08_RAG

Knowledge and retrieval.

Topics include:

- Document ingestion
- Chunking
- Embeddings
- Vector search
- Retrieval
- Ranking
- Knowledge versioning

---

# 09_MEMORY

Conversation memory.

Topics include:

- Short-term memory
- Long-term memory
- Session memory
- User preferences
- Conversation history
- Memory lifecycle

---

# 10_AUTOMATION

Automation and workflows.

Topics include:

- Workflow engine
- Scheduling
- Triggers
- Actions
- Integrations
- Business automation

---

# 11_SECURITY

Security documentation.

Topics include:

- Authentication
- Authorization
- RBAC
- Secrets
- Encryption
- Threat model
- Compliance
- Audit logging

---

# 12_DEPLOYMENT

Deployment documentation.

Topics include:

- Docker
- Kubernetes
- Infrastructure
- CI/CD
- Environment configuration
- Scaling
- Disaster recovery

---

# 13_OBSERVABILITY

Monitoring and diagnostics.

Topics include:

- Logging
- Metrics
- Tracing
- Dashboards
- Alerting
- Health checks

---

# 14_OPERATIONS

Operational procedures.

Topics include:

- Runbooks
- Maintenance
- Incident response
- Backup
- Restore
- Release management

---

# 15_TESTING

Testing strategy.

Topics include:

- Unit tests
- Integration tests
- End-to-end tests
- Performance tests
- Load tests
- Security testing

---

# 16_EXAMPLES

Reference implementations.

Examples include:

- API examples
- LangGraph workflows
- Prompt templates
- MCP integrations
- Deployment examples
- Golden examples

---

# archive

Archived documentation.

Typical contents:

- Version 1 blueprint
- Deprecated designs
- Superseded ADRs
- Legacy diagrams
- Historical specifications

Archived documents remain available for reference but are not considered the active implementation guide.

---

# Documentation Lifecycle

Each document should have the following metadata:

- Title
- Version
- Status
- Last Updated
- Owner (optional)
- Related Documents

Recommended statuses:

- Draft
- In Review
- Approved
- Active
- Deprecated
- Archived

---

# Naming Standards

File names should:

- Use descriptive names
- Avoid spaces
- Use underscores where appropriate
- Include numeric prefixes when ordering is important

Example:

```
01_System_Overview.md
02_Component_Architecture.md
03_Data_Flow.md
```

---

# Cross-Referencing

Whenever possible, documents should reference related documents.

Examples:

- Architecture documents should reference relevant ADRs.
- ADRs should reference affected architecture documents.
- Database documentation should reference API documentation where appropriate.
- Security documentation should reference deployment and authentication documents.

---

# Documentation Review

Documentation should be reviewed when:

- Major architecture changes occur
- New features are introduced
- ADRs are approved
- Technology stack changes
- Project phases are completed

---

# Source of Truth

The documentation within this repository is the authoritative source of project knowledge.

Chat history, personal notes, or AI memory should never be considered authoritative when they conflict with the repository documentation.

---

# Maintenance Responsibility

Every contributor is responsible for maintaining documentation related to the changes they introduce.

No feature is considered complete until its associated documentation has been updated.
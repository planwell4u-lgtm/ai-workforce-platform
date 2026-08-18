# Database Architecture

**Document ID:** DB-ARCH-001  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

The database architecture defines the data storage foundation for the AI Voice Agent SaaS platform.

The system requires a scalable, secure, multi-tenant database architecture capable of supporting:

- SaaS customer organizations
- User identity management
- AI agent configuration
- Voice call processing
- Conversation history
- Agent runtime state
- Knowledge bases
- RAG pipelines
- Memory systems
- Workflow execution
- Billing and usage tracking
- Audit logging
- Analytics

The primary database technology is:

**PostgreSQL**

PostgreSQL is selected because it provides:

- Strong relational modeling
- ACID transactions
- JSONB support
- Full-text search
- Extensions ecosystem
- Vector similarity search through pgvector
- Row-Level Security (RLS)
- Enterprise scalability

---

# 2. Database Architecture Goals

The database architecture must satisfy the following requirements:

## 2.1 Multi-Tenant SaaS Isolation

The platform supports multiple customers running independent AI voice agents.

Requirements:

- Tenant data isolation
- Secure access boundaries
- Shared infrastructure
- Tenant-aware queries
- Row-Level Security policies

Architecture model:


Single PostgreSQL Cluster

    |
    |
    +----------------+
    |                |
Tenant A        Tenant B

Users           Users
Agents          Agents
Calls           Calls
Knowledge       Knowledge

The platform uses:

**Shared Database + Shared Schema + Tenant ID isolation**

---

# 3. High-Level Database Architecture

                Applications

                     |
                     |
            API Gateway Layer

                     |
                     |
          Backend Services

                     |
                     |
            PostgreSQL Cluster

    +----------------+----------------+

    |                |                |

 Core Schema     Agent Schema     Voice Schema


    |                |                |

Identity Runtime Data Call Data

    |
    |
Knowledge Schema

    |
    |
RAG / Embeddings


    |
    |
Analytics Schema

---

# 4. Database Technology Stack

## Primary Database

| Component | Technology |
|---|---|
| Database Engine | PostgreSQL |
| Version Target | PostgreSQL 16+ |
| Extension Support | Enabled |
| Deployment | Cloud Managed / Kubernetes |
| Connection Pooling | PgBouncer |
| Migration Tool | Alembic |
| ORM | SQLAlchemy 2.x |

---

# 5. PostgreSQL Extensions

Required extensions:

## UUID Generation

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

Purpose:

Generate distributed unique identifiers
Avoid sequential ID exposure
Vector Search
CREATE EXTENSION IF NOT EXISTS vector;

Purpose:

Store embeddings
Semantic search
RAG retrieval

Example:

Document
    |
    |
Embedding Vector
    |
    |
Similarity Search
    |
    |
LLM Context
Full Text Search
CREATE EXTENSION IF NOT EXISTS pg_trgm;

Purpose:

Text matching
Fuzzy search
Customer lookup
Cryptographic Functions
CREATE EXTENSION IF NOT EXISTS pgcrypto;

Purpose:

Encryption helpers
Secure identifiers
Hash functions
6. Database Logical Domains

The database is divided into logical domains.

03_DATABASE

|
+-- Core Domain
|
+-- Identity Domain
|
+-- Tenant Domain
|
+-- Agent Domain
|
+-- Voice Domain
|
+-- Conversation Domain
|
+-- Knowledge Domain
|
+-- Memory Domain
|
+-- Workflow Domain
|
+-- Billing Domain
|
+-- Analytics Domain
|
+-- Audit Domain

7. Schema Organization

The PostgreSQL database uses multiple schemas.

Schema Layout
postgres

|
+-- public

|
+-- core

|
+-- identity

|
+-- tenant

|
+-- agent

|
+-- voice

|
+-- conversation

|
+-- knowledge

|
+-- memory

|
+-- workflow

|
+-- billing

|
+-- analytics

|
+-- audit

8. Schema Responsibilities
core

Platform-wide entities.

Contains:

System configuration
Feature flags
Global settings
Common reference tables
identity

Authentication and authorization.

Contains:

Users
Roles
Permissions
Sessions
API keys
tenant

Customer organization management.

Contains:

Organizations
Workspaces
Tenant settings
Subscription relationships
agent

AI agent definitions.

Contains:

Agent profiles
Agent versions
Agent prompts
Agent tools
Agent configurations
voice

Telephony and voice infrastructure.

Contains:

Phone numbers
SIP connections
Call routing
Voice providers
Call sessions
conversation

Conversation lifecycle data.

Contains:

Conversations
Messages
Transcripts
Events
Transfers
knowledge

RAG knowledge system.

Contains:

Knowledge bases
Documents
Chunks
Embeddings
Retrieval metadata
memory

AI memory storage.

Contains:

Short-term memory
Long-term memory
User memory
Agent memory
workflow

Agent automation.

Contains:

Workflows
Nodes
Executions
Tasks
billing

Commercial operations.

Contains:

Plans
Usage
Invoices
Payments
analytics

Reporting data.

Contains:

Metrics
Aggregations
Usage statistics
audit

Compliance tracking.

Contains:

Audit logs
Security events
Data changes
9. Data Flow Architecture
Customer

 |
 |
Web Dashboard

 |
 |
FastAPI Backend

 |
 |
Service Layer

 |
 |
Database Repository Layer

 |
 |
PostgreSQL


10. Database Access Pattern

Applications must NOT directly access tables.

Required pattern:

API

 |

Service Layer

 |

Repository Layer

 |

Database


Example:

AgentService

      |

AgentRepository

      |

agent.agents table


Benefits:

Better testing
Security control
Easier migrations
Database abstraction
11. Multi-Tenant Data Model

All tenant-owned tables must include:

tenant_id UUID NOT NULL

Example:

CREATE TABLE agent.agents
(
    id UUID PRIMARY KEY,

    tenant_id UUID NOT NULL,

    name TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT now()
);

12. Row Level Security

All tenant tables require RLS.

Example:

ALTER TABLE agent.agents
ENABLE ROW LEVEL SECURITY;


CREATE POLICY tenant_isolation_policy
ON agent.agents

USING
(
tenant_id = current_setting('app.tenant_id')::uuid
);

13. Data Classification
Classification	Examples
Public	Documentation
Internal	Configuration
Confidential	Customer data
Restricted	Credentials, tokens
14. Backup Strategy

Production database backups:

Daily

Full backup

Hourly

Incremental backup

Continuous

Point-In-Time Recovery (PITR)

Requirements:

Backup encryption
Restore testing
Retention policy
15. Database Scaling Strategy
Phase 1

Single PostgreSQL instance

Supports:

MVP
Early customers
Phase 2

Read replicas

Primary DB

 |
 +---- Read Replica 1

 |
 +---- Read Replica 2

Phase 3

Partitioning

Large tables:

call_events
transcripts
embeddings
audit_logs
16. High Volume Tables

Expected large tables:

Table	Growth
call_sessions	High
transcripts	Very High
conversation_messages	Very High
embeddings	High
audit_logs	High
usage_events	High
17. Database Security Requirements

Required:

Encryption at rest
TLS connections
Secret management
Least privilege roles
Database auditing
RLS enforcement
18. Database Roles

Recommended roles:

postgres_admin

database_migrator

application_service

readonly_reporting

analytics_worker

backup_operator

19. Migration Strategy

All schema changes must use migrations.

Tool:

Alembic

Migration flow:

Developer

 |

Migration File

 |

Review

 |

CI Validation

 |

Production Deployment

20. Database Documentation Standards

Every database change must include:

Schema update
ERD update
Migration script
API impact review
ADR if architectural change
21. Related Documents

Next documents:

02_POSTGRESQL_DESIGN_STANDARDS.md

03_SCHEMA_ORGANIZATION.md

04_MULTI_TENANT_DATA_MODEL.md

05_CORE_ENTITY_MODEL.md
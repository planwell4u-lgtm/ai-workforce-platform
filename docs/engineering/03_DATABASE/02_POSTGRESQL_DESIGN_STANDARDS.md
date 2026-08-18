# PostgreSQL Design Standards

**Document ID:** DB-STD-002  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the PostgreSQL database design standards for the AI Voice Agent SaaS platform.

The purpose of these standards is to ensure:

- Consistent schema design
- Maintainable database structures
- High performance
- Strong security boundaries
- Production scalability
- Easier developer collaboration

All database objects must follow these standards.

---

# 2. Database Design Principles

The database design follows these core principles:

## 2.1 Domain-Driven Schema Design

Database objects must be organized by business domain.

Example:


agent.agents

voice.call_sessions

conversation.messages

knowledge.documents


Avoid:


public.all_data
public.misc_tables


---

## 2.2 Explicit Data Ownership

Every table must have a clear ownership domain.

Example:


agent.agents

Owner:
Agent Management Service


---

## 2.3 Normalization First

Default design:

- Third Normal Form (3NF)
- Avoid duplicate data
- Use foreign keys
- Maintain referential integrity


Denormalization is allowed only when:

- Performance requirements justify it
- Documented through ADR
- Has synchronization strategy

---

# 3. Naming Conventions

## 3.1 Schema Naming

Format:


lowercase


Examples:


agent

voice

conversation

billing


---

## 3.2 Table Naming

Rules:

- lowercase
- snake_case
- plural nouns

Correct:


agents

call_sessions

conversation_messages


Incorrect:


Agent

AgentTable

tbl_agents


---

## 3.3 Column Naming

Format:


snake_case


Examples:


created_at

tenant_id

agent_version


---

# 4. Primary Key Standards

Every table must have a primary key.

Standard:

```sql
id UUID PRIMARY KEY

Example:

CREATE TABLE agent.agents
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);
5. UUID Standards

UUIDs are required for all public-facing entities.

Reasons:

Prevent ID enumeration
Support distributed systems
Easier data migration
Better SaaS isolation

Example:

agent_id:

9f5e1b21-7f31-4b4f-a9a7-9d3e8c7f12aa
6. Timestamp Standards

All tables require:

created_at

updated_at

Example:

created_at TIMESTAMP WITH TIME ZONE
DEFAULT now(),

updated_at TIMESTAMP WITH TIME ZONE
DEFAULT now()
7. Soft Delete Pattern

Production tables should avoid hard deletion.

Standard columns:

deleted_at TIMESTAMP WITH TIME ZONE

Example:

deleted_at NULL

Active records:

deleted_at IS NULL

Deleted records:

deleted_at IS NOT NULL

Benefits:

Auditability
Recovery
Compliance support
8. Tenant Isolation Standards

All tenant-owned tables require:

tenant_id UUID NOT NULL

Example:

CREATE TABLE voice.call_sessions
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

call_sid TEXT NOT NULL
);
9. Foreign Key Standards

Foreign keys are mandatory.

Example:

CREATE TABLE agent.agent_tools
(
id UUID PRIMARY KEY,

agent_id UUID NOT NULL,

CONSTRAINT fk_agent
FOREIGN KEY(agent_id)
REFERENCES agent.agents(id)
);
10. Constraint Standards

All important business rules must exist at database level.

Examples:

Required Fields
NOT NULL
Unique Values
UNIQUE
Valid Ranges
CHECK

Example:

CHECK(status IN
(
'active',
'inactive'
))
11. Indexing Standards

Indexes must be created based on query patterns.

Required indexes:

Foreign Keys

Example:

CREATE INDEX idx_agents_tenant_id
ON agent.agents(tenant_id);
Search Columns

Example:

CREATE INDEX idx_users_email
ON identity.users(email);
Time-Series Data

Example:

CREATE INDEX idx_calls_created_at
ON voice.call_sessions(created_at);
12. Composite Index Standards

Composite indexes must follow query order.

Example:

Query:

WHERE tenant_id = ?
AND status = ?

Index:

CREATE INDEX idx_calls_tenant_status
ON voice.call_sessions
(
tenant_id,
status
);
13. JSONB Usage Standards

JSONB is allowed for:

Flexible metadata
Provider payloads
AI configuration
External API responses

Example:

metadata JSONB

Allowed:

Twilio webhook payload

LLM configuration

Agent settings

Not allowed:

Core business fields

Bad:

{
"name":"John",
"email":"test@test.com"
}

These should be columns.

14. Enum Standards

Avoid PostgreSQL ENUM types.

Preferred:

Reference tables.

Example:

agent_statuses

call_statuses

subscription_plans

Reason:

Easier migrations
Dynamic updates
Better SaaS flexibility
15. Audit Columns

Important tables require:

created_by

updated_by

Example:

created_by UUID

updated_by UUID

Used for:

Compliance
User tracking
Change history
16. Data Types Standards
IDs

Use:

UUID
Text

Use:

TEXT

Avoid:

VARCHAR(255)

unless a strict limit exists.

Money

Never use:

FLOAT

Use:

NUMERIC(12,2)
Boolean

Use:

BOOLEAN
Dates

Always use:

TIMESTAMP WITH TIME ZONE
17. Large Data Storage Rules

Do not store large files inside PostgreSQL.

Examples:

Avoid:

audio recording blobs

video files

large documents

Store:

Object Storage

+
Database metadata

Example:

S3 / Cloud Storage

        |

audio_url

        |

voice.call_recordings
18. Vector Database Standards

pgvector is used for AI embeddings.

Example:

embedding vector(1536)

Used for:

RAG retrieval
Semantic search
Memory retrieval
19. Transaction Standards

Database transactions are required for:

Financial operations
State changes
Multi-table updates

Example:

Call completion:

Update call

+

Store transcript

+

Create usage event


must be atomic.

20. Migration Standards

Every database change requires:

Migration File

+

Rollback Plan

+

Testing

+

Documentation Update
21. Performance Standards

Developers must monitor:

Query execution time
Missing indexes
Slow queries
Connection usage
Table growth

Tools:

pg_stat_statements
EXPLAIN ANALYZE
Database monitoring dashboards
22. Security Standards

Required:

Separate database users
Least privilege access
No application superuser
Encrypted connections
Secrets outside code
23. Production Checklist

Before merging database changes:

[ ] Naming conventions followed

[ ] Primary key added

[ ] Tenant isolation reviewed

[ ] Indexes reviewed

[ ] Migration created

[ ] Rollback tested

[ ] Documentation updated

[ ] ERD updated
24. Related Documents

Next:

03_SCHEMA_ORGANIZATION.md

04_MULTI_TENANT_DATA_MODEL.md

05_CORE_ENTITY_MODEL.md
# Database Development Guidelines

**Document ID:** DB-DEVELOPMENT-030  
**Version:** 2.0  
**Status:** Production Development Standard  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database development standards for engineers building and maintaining the AI Voice Agent SaaS platform.

The guidelines ensure:

- Consistent database design
- Maintainable schemas
- Safe migrations
- High performance
- Secure data handling
- Production reliability

---

# 2. Development Principles

Database changes must follow:


Design

|

Review

|

Migration

|

Testing

|

Deployment

|

Monitoring


---

# 3. Database Development Workflow

Standard workflow:


Developer

|

Create Migration

|

Local Testing

|

Code Review

|

CI Validation

|

Staging Deployment

|

Production Release


---

# 4. Local Development Environment

Recommended stack:


Docker PostgreSQL

Migration Tool

Seed Data

Testing Framework


---

Example:

```yaml
services:

  postgres:
    image: postgres:16
5. Schema Development Rules
5.1 Domain Ownership

Each schema belongs to a domain.

Example:

agent

Owned by:

Agent Platform Team


voice

Owned by:

Voice Infrastructure Team

5.2 Avoid Cross-Domain Coupling

Avoid:

billing

directly modifying

voice tables


Prefer:

Events

    |

Integration Layer

    |

Billing

6. Table Design Standards

Every major table should include:

id UUID PRIMARY KEY,

created_at TIMESTAMPTZ DEFAULT now(),

updated_at TIMESTAMPTZ DEFAULT now()

Tenant-owned tables require:

tenant_id UUID NOT NULL
7. Naming Standards

Use:

snake_case

Examples:

Good:

conversation_messages

agent_configs

voice_calls

Bad:

ConversationMessages

AgentConfig
8. Primary Key Standards

Use UUIDs:

id UUID PRIMARY KEY

Benefits:

Distributed systems support
Safer public identifiers
Service independence
9. Foreign Key Standards

Foreign keys should be explicit.

Example:

agent_id UUID REFERENCES agent.agents(id)

Use meaningful names:

Good:

conversation_id
tenant_id
agent_id

Avoid:

parent_id
object_id
10. Index Guidelines

Indexes should support:

Frequent queries
Tenant filtering
Foreign keys
Sorting
Searching

Required:

CREATE INDEX idx_table_tenant

ON table_name(tenant_id);

Avoid:

Excessive indexes
Duplicate indexes
Unused indexes
11. JSONB Usage Guidelines

Use JSONB for:

AI metadata
Configuration
External payloads
Dynamic attributes

Example:

{
 "voice":"female",
 "language":"en"
}

Avoid JSONB for:

Core relationships
Frequently queried fields
Financial data
12. Transaction Guidelines

Transactions must:

Be short
Avoid long locks
Handle failures

Example:

BEGIN;

INSERT INTO orders;

UPDATE inventory;

COMMIT;
13. Query Development Rules

Always:

Use prepared statements
Review query plans
Add indexes when needed
Limit returned data

Before merging:

Run:

EXPLAIN ANALYZE
14. Migration Guidelines

Every migration requires:

Description

Author

Risk Level

Rollback Plan

Testing Notes


Example:

Migration:

Add workflow execution table


Risk:

Medium


Rollback:

Drop table

15. Data Migration Guidelines

Large migrations require:

Batch processing
Progress tracking
Monitoring

Avoid:

UPDATE million_rows;

Prefer:

Process 1000 rows

Repeat

16. Production Change Rules

Never:

Modify production manually
Run unknown SQL
Skip migrations

All changes require:

Review
Testing
Approval
17. Database Security Rules

Developers must:

Protect credentials
Avoid exposing sensitive data
Follow RLS requirements
Use least privilege access
18. AI Data Guidelines

AI-related data requires special handling.

Examples:

Memory

Embeddings

Conversation History

Knowledge Documents


Requirements:

Retention policies
Access controls
Privacy protection
19. Voice Data Guidelines

Voice platform data includes:

Call metadata
Transcripts
Events
Recordings references

Requirements:

Tenant isolation
Encryption
Lifecycle management
20. Testing Requirements

Before merge:

Required:

Migration Test

Schema Validation

Query Test

Security Test

Performance Check

21. Code Review Checklist

Reviewers verify:

✓ Naming standards followed

✓ Tenant isolation implemented

✓ Indexes considered

✓ Migration tested

✓ Security reviewed

✓ Documentation updated

22. Documentation Requirements

Database changes must update:

Schema documentation
ER diagrams
ADRs
Migration notes
23. Production Readiness Checklist

Before release:

✓ Migration approved

✓ Backup available

✓ Rollback plan ready

✓ Monitoring configured

✓ Performance tested

✓ Security validated

24. Related Documents

Database Architecture:

01_DATABASE_ARCHITECTURE.md

Standards:

02_POSTGRESQL_DESIGN_STANDARDS.md

Migrations:

22_DATABASE_MIGRATION_STRATEGY.md

Security:

25_DATABASE_SECURITY_HARDENING.md

Testing:

26_DATABASE_TESTING_STRATEGY.md
End of Document
# 01 Schema Example
# Database Schema Example

**Version:** 2.0

---

# 1. Overview

This document demonstrates a production-ready PostgreSQL schema for the Voice Agent SaaS platform.

The example illustrates the recommended schema organization, naming conventions, relationships, indexing strategy, and multi-tenant design principles used throughout the platform.

The schema supports:

- Multi-tenancy
- AI agents
- Voice conversations
- Knowledge management
- Memory
- Automation
- Audit logging
- Analytics

---

# 2. Database Architecture

```
                    PostgreSQL

                         │

        ┌────────────────┼────────────────┐

        ▼                ▼                ▼

    Identity         Agent Core       Voice Platform

        ▼                ▼                ▼

 Authentication    Agent Runtime    Conversations

        ▼                ▼                ▼

      Memory            RAG          Automation

        ▼                ▼                ▼

      Billing         Analytics      Audit Logs
```

---

# 3. Schema Organization

Example logical schemas:

```
identity
agent
voice
memory
rag
automation
billing
analytics
audit
system
```

Each schema groups related database objects and simplifies maintenance.

---

# 4. Entity Relationship Overview

```
Tenant

   │

   ├──────── Users

   │

   ├──────── Agents

   │             │

   │             ▼

   │      Conversations

   │             │

   │             ▼

   │        Messages

   │             │

   │             ▼

   │          Memory

   │

   └──────── Knowledge Base
```

All business entities belong to a tenant.

---

# 5. Example Tables

### tenants

```sql
CREATE TABLE identity.tenants (

    id UUID PRIMARY KEY,

    name TEXT NOT NULL,

    status TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL
);
```

---

### users

```sql
CREATE TABLE identity.users (

    id UUID PRIMARY KEY,

    tenant_id UUID NOT NULL,

    email TEXT NOT NULL,

    full_name TEXT,

    created_at TIMESTAMPTZ NOT NULL,

    FOREIGN KEY (tenant_id)

        REFERENCES identity.tenants(id)
);
```

---

### agents

```sql
CREATE TABLE agent.agents (

    id UUID PRIMARY KEY,

    tenant_id UUID NOT NULL,

    name TEXT NOT NULL,

    status TEXT,

    model TEXT,

    created_at TIMESTAMPTZ NOT NULL
);
```

---

### conversations

```sql
CREATE TABLE voice.conversations (

    id UUID PRIMARY KEY,

    tenant_id UUID NOT NULL,

    agent_id UUID,

    started_at TIMESTAMPTZ,

    ended_at TIMESTAMPTZ,

    status TEXT
);
```

---

### messages

```sql
CREATE TABLE voice.messages (

    id UUID PRIMARY KEY,

    conversation_id UUID,

    role TEXT,

    content TEXT,

    created_at TIMESTAMPTZ
);
```

---

# 6. Relationships

```
Tenant

   │

   ▼

Users

Agents

Knowledge

Conversations

Automation

Audit

Analytics
```

Foreign keys should enforce referential integrity wherever appropriate.

---

# 7. Index Strategy

Recommended indexes:

```
PRIMARY KEY

UNIQUE

FOREIGN KEY

Composite Index

Partial Index

GIN

GiST

Vector Index
```

Indexes should support the platform's most common query patterns.

---

# 8. Multi-Tenant Design

Every business table should include:

```
tenant_id UUID NOT NULL
```

Benefits:

- Tenant isolation
- Efficient filtering
- Partitioning support
- Simplified authorization

---

# 9. Naming Standards

Use:

```
snake_case

plural table names

singular column names
```

Examples:

```
users

agents

conversation_messages

knowledge_documents
```

Avoid abbreviations unless they are industry standard.

---

# 10. Audit Columns

Standard audit fields:

```sql
created_at

updated_at

created_by

updated_by

deleted_at
```

Soft deletion is preferred for business-critical entities.

---

# 11. Constraints

Examples:

- Primary keys
- Foreign keys
- Unique constraints
- Check constraints
- NOT NULL
- Default values

Constraints help preserve data integrity.

---

# 12. Partitioning Example

```
messages

     │

Year

     │

Month

     │

Daily Partitions
```

Large append-only tables should be partitioned where appropriate.

---

# 13. Security

The schema should support:

- Row-Level Security (RLS)
- Tenant isolation
- Least privilege
- Role-based access
- Encryption for sensitive fields
- Audit logging

---

# 14. Performance Considerations

Optimize for:

- Read-heavy workloads
- Conversation history
- Vector search
- Reporting
- Batch inserts
- Background processing

Monitor execution plans regularly.

---

# 15. Backup Considerations

Critical entities:

- Tenants
- Users
- Agents
- Conversations
- Knowledge
- Memory
- Billing
- Audit

Backup strategies should align with business recovery objectives.

---

# 16. Testing

Validate:

- Schema creation
- Constraints
- Foreign keys
- Index usage
- Tenant isolation
- Cascade behavior
- Performance
- Migration compatibility

---

# 17. Best Practices

Always:

- Normalize transactional data
- Use UUID primary keys
- Include audit fields
- Enforce tenant isolation
- Create appropriate indexes
- Validate constraints
- Document schema changes

Avoid:

- Cross-tenant relationships
- Excessive denormalization
- Missing indexes
- Nullable foreign keys without justification
- Circular dependencies
- Uncontrolled schema changes

---

# 18. Example End-to-End Flow

```
Tenant Created

        │

Create User

        │

Create Agent

        │

Start Conversation

        │

Store Messages

        │

Update Memory

        │

Audit Activity
```

---

# 19. Future Enhancements

Potential improvements include:

- Automated partition management
- Temporal tables
- Logical replication
- Cross-region replication
- Advanced indexing
- Data archiving
- Online schema evolution
- AI-assisted query optimization

---

# 20. Summary

The example schema demonstrates the foundational database structure for the Voice Agent SaaS platform. By applying consistent naming conventions, multi-tenant design, strong referential integrity, indexing strategies, and security controls, the platform provides a scalable, maintainable, and production-ready data layer.
# Database Index & Performance Strategy

**Document Version:** 1.0
**Project:** AI Voice Agent SaaS Platform
**Phase:** 05 - Database Schema
**Database Platform:** PostgreSQL + Supabase + Redis + pgvector
**Architecture:** Production Scale Database Optimization
**Status:** Draft
**Last Updated:** 2026-07-23

---

# 1. Overview

This document defines the database performance strategy for the AI Voice Agent SaaS platform.

The platform handles:

* Real-time voice calls
* AI agent execution
* Conversation history
* RAG retrieval
* Billing calculations
* Analytics workloads
* Multi-tenant data isolation

The database design must support:

* Low latency
* High concurrency
* Large data volumes
* Secure tenant isolation

---

# 2. Performance Architecture

```text
Application

     |

     v

API Layer

     |

 -------------------------

 |           |            |

PostgreSQL Redis       pgvector

Primary    Cache       AI Search

Database

     |

     v

Analytics Pipeline
```

---

# 3. Database Optimization Areas

```text
Performance

├── Indexing

├── Query Optimization

├── Partitioning

├── Connection Pooling

├── Caching

├── Vector Optimization

└── Data Lifecycle
```

---

# 4. Indexing Strategy

Indexes improve lookup speed.

Every production table requires:

* Primary key index
* Tenant filtering index
* Foreign key index
* Time-based indexes where needed

---

# 5. Tenant-Based Indexing

Because the platform is multi-tenant:

Most queries start with:

```sql
WHERE tenant_id = ?
```

Therefore:

Recommended:

```sql
CREATE INDEX idx_table_tenant

ON table_name(tenant_id);
```

---

# 6. Composite Index Strategy

For frequent queries:

Example:

```sql
SELECT *

FROM calls

WHERE tenant_id = ?

AND status = ?

ORDER BY created_at DESC;
```

Index:

```sql
CREATE INDEX idx_calls_tenant_status_date

ON calls(

tenant_id,

status,

created_at DESC

);
```

---

# 7. Voice Call Indexes

High-frequency queries:

* Active calls
* Recent calls
* Customer call history

Recommended:

```sql
CREATE INDEX idx_calls_customer

ON calls(customer_id);


CREATE INDEX idx_calls_created

ON calls(created_at DESC);
```

---

# 8. Conversation Indexes

Conversation lookup:

```sql
CREATE INDEX idx_conversations_session

ON conversations(session_id);


CREATE INDEX idx_conversations_customer

ON conversations(customer_id);
```

---

# 9. Agent Runtime Indexes

Agent queries:

* Agent configuration
* Active agents
* Tenant agents

Recommended:

```sql
CREATE INDEX idx_agents_tenant

ON agents(tenant_id);


CREATE INDEX idx_agents_status

ON agents(status);
```

---

# 10. RAG Vector Index Strategy

The platform uses:

```text
PostgreSQL

+

pgvector
```

---

# 11. Vector Index Types

## IVFFlat

Good for:

* Large datasets
* Faster approximate search

Example:

```sql
CREATE INDEX embeddings_ivf

ON embeddings

USING ivfflat

(embedding vector_cosine_ops);
```

---

## HNSW

Recommended for:

* High accuracy
* Real-time retrieval

Example:

```sql
CREATE INDEX embeddings_hnsw

ON embeddings

USING hnsw

(embedding vector_cosine_ops);
```

---

# 12. Vector Search Optimization

Tune:

```text
Chunk Size

Embedding Model

Similarity Threshold

Top K Results

Metadata Filtering
```

---

Example:

```text
Retrieve:

Top 5 chunks

Similarity > 0.75
```

---

# 13. PostgreSQL Partitioning

Large tables should be partitioned.

Recommended candidates:

```text
calls

conversation_messages

audit_logs

analytics_events

usage_records
```

---

# 14. Time-Based Partitioning

Example:

```text
calls

├── calls_2026_01

├── calls_2026_02

├── calls_2026_03
```

---

Benefits:

* Faster queries
* Easier cleanup
* Better maintenance

---

# 15. Audit Log Partitioning

Audit logs grow continuously.

Recommended:

```sql
PARTITION BY RANGE(created_at)
```

---

Example:

```text
audit_logs

2026

 ├── January

 ├── February

 └── March
```

---

# 16. Connection Pooling

Production requires connection management.

Recommended:

```text
Application

↓

PgBouncer

↓

PostgreSQL
```

---

Benefits:

* Lower connection overhead
* Higher concurrency
* Better stability

---

# 17. Redis Caching Strategy

Redis stores temporary data.

Use cases:

```text
Active Calls

Agent State

Session Data

API Cache

Rate Limits

Realtime Metrics
```

---

# 18. Cache Pattern

Recommended:

```text
Request

↓

Check Redis

↓

Found?

YES → Return

NO

↓

Query PostgreSQL

↓

Store Cache
```

---

# 19. Cache Expiration

Example TTL:

```text
Agent State

1 Hour


Presence

5 Minutes


API Cache

10 Minutes


Temporary Context

30 Minutes
```

---

# 20. Query Optimization Rules

Avoid:

```sql
SELECT *
```

Use:

```sql
SELECT required_columns
```

---

Always:

* Analyze query plans
* Monitor slow queries
* Use prepared statements
* Avoid unnecessary joins

---

# 21. PostgreSQL Monitoring

Monitor:

```text
Query Duration

Index Usage

Locks

Connections

Cache Hit Ratio

Database Size
```

---

# 22. Slow Query Detection

Enable:

```sql
pg_stat_statements
```

Analyze:

```sql
SELECT *

FROM pg_stat_statements

ORDER BY total_exec_time DESC;
```

---

# 23. Data Lifecycle Management

Large data requires retention policies.

Example:

```text
Raw Call Audio

90 Days


Analytics Events

1 Year


Audit Logs

7 Years
```

---

# 24. Backup Strategy

Required:

* Daily backups
* Point-in-time recovery
* Disaster recovery plan
* Backup testing

---

# 25. Production Scaling Strategy

Growth path:

```text
Stage 1

Single PostgreSQL Instance


↓

Stage 2

Read Replicas


↓

Stage 3

Partitioned Database


↓

Stage 4

Dedicated Tenant Databases
```

---

# 26. Security Performance

Security should not reduce performance.

Use:

* Proper RLS indexes
* Tenant indexes
* Connection pooling
* Query optimization

---

# 27. Recommended Index Checklist

Every table:

✓ Primary Key

✓ Tenant ID Index

✓ Foreign Key Index

✓ Created Date Index

✓ Status Index (if queried)

✓ Composite Index (if required)

---

# 28. Related Documents

| Document                          | Purpose             |
| --------------------------------- | ------------------- |
| 22_Search_Vector_Index_Schema.md  | Vector optimization |
| 23_Realtime_State_Schema.md       | Redis state         |
| 24_Tenant_Organization_Schema.md  | Multi-tenancy       |
| 29_Database_Migration_Strategy.md | Migration planning  |

---

# 29. Conclusion

The Database Index & Performance Strategy ensures the AI Voice Agent SaaS platform can scale from early customers to enterprise workloads.

It provides:

* Fast queries
* Efficient AI retrieval
* Reliable realtime operations
* Scalable multi-tenant architecture

---

**End of Document**

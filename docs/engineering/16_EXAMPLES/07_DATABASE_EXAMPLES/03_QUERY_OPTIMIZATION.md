# 03 Query Optimization
# Query Optimization Example

**Version:** 2.0

---

# 1. Overview

This document demonstrates production-ready SQL query optimization practices for the Voice Agent SaaS platform.

As the platform scales, database queries become critical to application performance. Proper indexing, query planning, schema design, and monitoring ensure fast response times across high-volume workloads.

Optimization areas include:

- API queries
- Conversation history retrieval
- Agent execution data
- Knowledge retrieval
- Analytics queries
- Billing operations
- Background processing

---

# 2. Objectives

The query optimization strategy should:

- Reduce query latency
- Improve database resource usage
- Prevent inefficient scans
- Support high concurrency
- Maintain predictable performance
- Scale with growing data volume

---

# 3. Query Execution Lifecycle

```
Application Request

        │

        ▼

        SQL Query

        │

        ▼

    Query Planner

        │

        ▼

 Execution Plan

        │

        ▼

 Index / Table Access

        │

        ▼

   Result Returned
```

---

# 4. Query Analysis

Before optimization:

Use:

```sql
EXPLAIN ANALYZE
```

Example:

```sql
EXPLAIN ANALYZE

SELECT *

FROM voice.messages

WHERE conversation_id = 'abc';
```

Analyze:

- Sequential scans
- Index usage
- Execution time
- Rows examined
- Memory usage

---

# 5. Index Optimization

## Without Index

Example:

```sql
SELECT *

FROM voice.messages

WHERE conversation_id = '123';
```

Possible execution:

```
Full Table Scan

↓

Check Every Row

↓

Return Results
```

---

## With Index

```sql
CREATE INDEX idx_messages_conversation

ON voice.messages(conversation_id);
```

Execution:

```
Index Lookup

↓

Matching Rows

↓

Return Results
```

---

# 6. Composite Indexes

For multiple conditions:

Example query:

```sql
SELECT *

FROM voice.conversations

WHERE tenant_id='tenant_1'

AND status='active';
```

Recommended:

```sql
CREATE INDEX idx_conversations_tenant_status

ON voice.conversations(
    tenant_id,
    status
);
```

Column order should follow query patterns.

---

# 7. Covering Indexes

A covering index contains all required columns.

Example:

```sql
CREATE INDEX idx_agent_lookup

ON agent.agents(
    tenant_id,
    name,
    status
);
```

Benefits:

- Avoid table lookup
- Reduce disk access
- Improve read performance

---

# 8. Query Optimization Example

## Before

```sql
SELECT *

FROM voice.messages

WHERE tenant_id='tenant_1'

ORDER BY created_at DESC;
```

Problems:

- Large data scan
- Sorting overhead
- Excessive columns

---

## After

```sql
SELECT

id,

content,

created_at

FROM voice.messages

WHERE tenant_id='tenant_1'

ORDER BY created_at DESC

LIMIT 50;
```

Improvements:

- Reduced data transfer
- Limited result size
- Better index usage

---

# 9. Pagination Optimization

Avoid:

```sql
LIMIT 50 OFFSET 100000;
```

Large offsets become expensive.

Prefer cursor pagination:

```sql
WHERE id < last_seen_id

ORDER BY id DESC

LIMIT 50;
```

Benefits:

- Constant performance
- Better scalability
- Lower database load

---

# 10. Join Optimization

Example:

```sql
SELECT

u.email,

a.name

FROM users u

JOIN agents a

ON u.id = a.owner_id;
```

Optimize by:

- Indexing join columns
- Selecting required columns only
- Avoiding unnecessary joins

---

# 11. N+1 Query Prevention

Problem:

```
Fetch Users

      │

Loop Users

      │

Query Agent For Each User
```

Creates many queries.

Solution:

```
Single Optimized Query

      │

Return Complete Dataset
```

Use:

- Joins
- Batch loading
- ORM eager loading

---

# 12. JSONB Optimization

For JSONB queries:

Example:

```sql
SELECT *

FROM agent.agents

WHERE configuration->>'language'='en';
```

Create GIN index:

```sql
CREATE INDEX idx_agent_configuration

ON agent.agents

USING GIN(configuration);
```

---

# 13. Vector Query Optimization

For RAG workloads:

Optimize:

- Vector dimensions
- Index type
- Similarity metric
- Metadata filtering
- Chunk size

Example:

```
Query Vector

      │

Tenant Filter

      │

Vector Index Search

      │

Top-K Results
```

---

# 14. Partitioning Strategy

Large tables:

Examples:

- messages
- call_events
- audit_logs
- analytics_events

Partition by:

- Date
- Tenant
- Region

Example:

```
messages

 ├── 2026_01

 ├── 2026_02

 └── 2026_03
```

---

# 15. Connection Optimization

Database performance depends on:

- Connection pooling
- Query timeout
- Transaction duration
- Idle connection cleanup

Recommended:

```
Application

      │

Connection Pool

      │

PostgreSQL
```

---

# 16. Caching Strategy

Use caching for:

- Frequently accessed configuration
- Agent settings
- Permissions
- Static metadata

Example:

```
Request

   │

Redis Cache

   │

Cache Hit?

 ┌─┴─┐

Yes No

 │   │

Return Query DB
```

---

# 17. Monitoring

Track:

- Slow queries
- Query execution time
- Index usage
- Cache hit ratio
- Database CPU
- Lock contention
- Connection usage

---

# 18. Performance Targets

| Metric | Target |
|--------|-------:|
| Simple lookup | < 10 ms |
| Indexed query | < 50 ms |
| API database query | < 100 ms |
| Complex reporting | < seconds |
| Vector retrieval | < 300 ms |

---

# 19. Testing

Validate:

- Query plans
- Index effectiveness
- Large datasets
- Concurrent workloads
- Pagination performance
- Migration impact
- Production-like traffic

---

# 20. Best Practices

Always:

- Analyze queries before optimizing
- Use appropriate indexes
- Select only required columns
- Monitor slow queries
- Use pagination
- Optimize joins
- Review execution plans

Avoid:

- Using SELECT *
- Missing indexes
- Excessive joins
- Large OFFSET pagination
- Long-running transactions
- Ignoring query statistics

---

# 21. Example Optimization Workflow

```
Slow Query Detected

        │

Analyze Execution Plan

        │

Identify Bottleneck

        │

Add Index / Rewrite Query

        │

Benchmark Improvement

        │

Deploy Optimization

        │

Monitor Results
```

---

# 22. Future Enhancements

Potential improvements include:

- Automated query tuning
- AI-assisted indexing recommendations
- Workload-based optimization
- Database performance dashboards
- Automatic partition management
- Predictive scaling

---

# 23. Summary

Query optimization ensures the Voice Agent SaaS platform maintains fast, predictable database performance as data volume increases. Through proper indexing, execution plan analysis, optimized queries, caching strategies, and continuous monitoring, the database layer can support enterprise-scale workloads efficiently.
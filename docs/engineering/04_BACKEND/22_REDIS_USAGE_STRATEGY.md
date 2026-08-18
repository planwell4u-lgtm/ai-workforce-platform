# 22. Redis Usage Strategy

**Version:** 2.0  
**Status:** Production Ready  
**Owner:** Platform Engineering

---

# 1. Purpose

Redis provides high-performance in-memory data storage capabilities across the Voice Agent SaaS platform.

The Redis strategy defines where Redis should be used, where it should not be used, and how it supports scalability, low latency, and distributed backend operations.

Redis is used as a performance layer and coordination system, not as the primary source of truth for business data.

---

# 2. Redis Design Goals

Redis provides:

- Low-latency data access
- Caching
- Session management
- Distributed coordination
- Rate limiting
- Temporary state storage
- Queue support
- Real-time features

---

# 3. Redis Architecture

```text
                    Backend Services

                           │

                           ▼

                     Redis Cluster

        ┌──────────────────┼──────────────────┐

        ▼                  ▼                  ▼

     Cache Layer      Session Layer     Coordination Layer

        │                  │                  │

        ▼                  ▼                  ▼

 PostgreSQL          User Sessions      Distributed Locks
```

---

# 4. Redis Is NOT Primary Storage

Redis should not store permanent business records.

Do not store:

- Users
- Tenants
- Billing records
- Payments
- Invoices
- Knowledge documents
- Compliance records
- Audit history

These belong in PostgreSQL or dedicated storage systems.

---

# 5. Redis Use Cases

The platform uses Redis for:

- Application caching
- Session storage
- Rate limiting
- Distributed locks
- Temporary workflow state
- Job queues
- Real-time counters
- Presence tracking
- API throttling

---

# 6. Caching Strategy

Redis reduces database load by caching frequently accessed data.

Examples:

```text
Database Query

↓

Redis Cache

↓

Application Response
```

Common cached data:

- Tenant configuration
- Agent configuration
- User preferences
- Feature flags
- API responses
- Provider configuration

---

# 7. Cache Patterns

## Cache-Aside Pattern

Recommended approach:

```text
Application

↓

Check Redis

↓

Found?

YES → Return Data

NO

↓

Query Database

↓

Store in Redis

↓

Return Data
```

---

# 8. Cache Expiration

Every cache entry should have a TTL.

Examples:

| Data | TTL |
|---|---|
| User session | Hours |
| Agent configuration | Minutes |
| API response | Seconds |
| Feature flags | Minutes |
| Temporary workflow state | Minutes |

---

# 9. Cache Invalidation

Cache invalidation occurs when:

- Data changes
- Configuration updates
- User permissions change
- Tenant settings change

Strategies:

- Delete cache key
- Update cache value
- Short TTL expiration
- Event-driven invalidation

---

# 10. Session Management

Redis may store:

- Login sessions
- Temporary authentication state
- OAuth states
- MFA verification state
- User presence

Example:

```text
User Login

↓

Session Created

↓

Stored in Redis

↓

Validated on Requests
```

---

# 11. Rate Limiting

Redis supports distributed rate limiting.

Examples:

API limits:

```
100 requests / minute / user
```

Voice limits:

```
10 concurrent calls / tenant
```

Implementation patterns:

- Token bucket
- Sliding window
- Fixed window counters

---

# 12. Distributed Locks

Redis provides coordination between multiple workers.

Example:

Prevent duplicate invoice generation:

```text
Worker A

↓

Acquire Lock

↓

Generate Invoice


Worker B

↓

Lock Exists

↓

Wait
```

Common use cases:

- Billing jobs
- Scheduled tasks
- Data synchronization
- Resource updates

---

# 13. Real-Time State

Redis can store temporary real-time state.

Examples:

Voice sessions:

```
call_id

agent_id

connection_state

last_activity
```

Workflow execution:

```
workflow_id

current_step

status
```

---

# 14. Agent Runtime Usage

Redis supports AI agent runtime operations:

Examples:

- Active session state
- Conversation context cache
- Tool execution state
- Temporary agent variables
- Runtime coordination

Long-term memory remains in the Memory Service.

---

# 15. RAG Performance Optimization

Redis may improve RAG latency through:

- Query caching
- Retrieval result caching
- Embedding lookup caching
- Frequently accessed document metadata

Example:

```text
User Question

↓

Redis Cache

↓

Existing Result?

↓

Return

OR

↓

Execute RAG Search
```

---

# 16. Background Worker Support

Redis may support:

- Job queues
- Task status
- Worker coordination
- Retry tracking

Example:

```text
Job Created

↓

Redis Queue

↓

Worker Picks Job

↓

Process

↓

Update Status
```

---

# 17. Redis Data Structures

Recommended structures:

## Strings

Use for:

- Cache values
- Tokens
- Counters

---

## Hashes

Use for:

- Sessions
- Objects
- Runtime state

---

## Lists

Use for:

- Simple queues

---

## Sets

Use for:

- Membership tracking
- Unique collections

---

## Sorted Sets

Use for:

- Priority queues
- Leaderboards
- Time-based scheduling

---

## Streams

Use for:

- Event streams
- Message processing
- Worker communication

---

# 18. Redis Key Naming

Keys should follow a standard format.

Example:

```
{environment}:{service}:{resource}:{id}
```

Examples:

```
prod:user:session:123

prod:agent:config:456

prod:workflow:state:789
```

---

# 19. Redis Cluster Strategy

Production deployments should support:

- Redis Cluster
- Replication
- Automatic failover
- Persistence configuration
- Monitoring

---

# 20. Persistence Strategy

Redis supports:

## RDB Snapshots

Good for:

- Backups
- Recovery

---

## AOF Logging

Good for:

- Data durability
- Write recovery

---

Critical business data should still remain outside Redis.

---

# 21. Security

Redis security requirements:

- Authentication enabled
- TLS encryption
- Private network access
- Firewall restrictions
- Access control
- Secret rotation
- Audit logging

---

# 22. Monitoring

Important metrics:

- Memory usage
- Cache hit ratio
- Evictions
- Connected clients
- Command latency
- Key count
- Replication health
- CPU usage
- Network throughput

---

# 23. Failure Handling

If Redis becomes unavailable:

Applications should:

- Fall back to database where possible
- Disable non-critical caching
- Continue essential operations
- Retry connections
- Trigger alerts

Redis failure should not cause complete platform failure.

---

# 24. Integration Points

Redis integrates with:

- Backend API
- Authentication Service
- Workflow Service
- Background Workers
- Message Queue
- Agent Runtime
- Memory Service
- RAG Service
- Rate Limiting Middleware
- Observability Platform

---

# 25. Future Enhancements

Planned capabilities:

- Redis Cluster auto-scaling
- Advanced caching analytics
- AI-driven cache optimization
- Global distributed caching
- Real-time analytics pipelines
- Edge caching

---

# 26. Design Principles

Redis usage follows:

- Cache first, not source of truth
- Explicit expiration
- Predictable key management
- Secure access
- Graceful degradation
- Horizontal scalability
- Minimal persistence dependency
- Observable operations

---

# 27. Summary

Redis acts as a high-performance acceleration layer for the Voice Agent SaaS platform. It improves latency through caching, enables distributed coordination, supports real-time state management, and assists background processing while keeping PostgreSQL as the authoritative system of record. Proper Redis usage ensures the backend remains fast, scalable, and resilient without introducing data consistency risks.
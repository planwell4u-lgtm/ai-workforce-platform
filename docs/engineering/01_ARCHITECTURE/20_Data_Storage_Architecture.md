# DATA STORAGE ARCHITECTURE

**Project:** Voice Agent SaaS Platform  
**Document:** Data Storage Architecture  
**Version:** 2.0  
**Status:** Draft  
**Last Updated:** 2026-07-24


---

# 1. Purpose

This document defines the overall data storage architecture of the Voice Agent SaaS Platform.

Unlike traditional SaaS applications that primarily rely on a relational database, an AI-powered voice platform requires multiple specialized storage systems, each optimized for a different type of data.

This document explains:

- Why each storage technology exists
- What data each system owns
- How data flows between storage systems
- Data lifecycle
- Storage responsibilities
- Synchronization strategy
- Performance considerations

It serves as the master reference for all storage-related architectural decisions.


---

# 2. Storage Philosophy

The platform follows the principle:

> **Use the right storage technology for the right type of data.**

No single database is optimized for every workload.

Instead, the platform combines specialized storage technologies to maximize:

- Performance
- Reliability
- Scalability
- Maintainability
- AI capabilities


---

# 3. Storage Landscape

```
                          Voice Agent SaaS Platform

                                      │

        ┌───────────────┬───────────────┬───────────────┬───────────────┐

        ▼               ▼               ▼               ▼

   PostgreSQL        Redis          pgvector      Object Storage

 Structured Data   Fast State    Semantic Search     Large Files

 Users             Cache         Embeddings          Documents

 Agents            Sessions      Knowledge           Audio

 Billing           Queues        Chunks              Recordings

 Calls             Locks         Similarity          Images

 Configuration     Rate Limits   Retrieval           Exports
```


---

# 4. Storage Technologies

| Storage | Primary Purpose |
|----------|-----------------|
| PostgreSQL | Primary relational database |
| pgvector | Semantic vector search |
| Redis | Cache, ephemeral state, queues |
| Object Storage | Documents, recordings, media |
| LiveKit Redis | Cluster coordination (platform infrastructure) |


---

# 5. PostgreSQL

## Purpose

PostgreSQL is the platform's **System of Record**.

All authoritative business data is stored here.

---

## Responsibilities

- Organizations
- Tenants
- Users
- Authentication metadata
- Agents
- Voice configuration
- Calls
- Conversations
- Billing
- API keys
- Integrations
- Audit logs
- Analytics metadata
- Workflow definitions

---

## Characteristics

- ACID compliant
- Transactional
- Strong consistency
- Relational integrity
- Multi-tenant architecture
- Long-term persistence

---

## PostgreSQL Does NOT Store

- Audio streams
- Large recordings
- Embeddings
- Temporary runtime state
- High-speed cache


---

# 6. pgvector

## Purpose

pgvector extends PostgreSQL with vector search capabilities.

It enables semantic retrieval for Retrieval-Augmented Generation (RAG).

---

## Stores

- Embedding vectors
- Chunk references
- Similarity indexes
- Embedding metadata

---

## Example

```
Document

↓

Chunk

↓

Embedding

↓

pgvector
```

---

## Used By

- Knowledge Service
- RAG Service
- AI Runtime
- Search APIs

---

## pgvector Does NOT Store

- Original documents
- Business entities
- Runtime state

Those remain in PostgreSQL and Object Storage.


---

# 7. Redis

Redis is used for extremely fast, short-lived data.

---

## Responsibilities

### Cache

Examples

- Agent configuration
- Tenant configuration
- API responses
- Feature flags

---

### Session State

Examples

- Active voice sessions
- Temporary conversation state
- Active websocket users

---

### Distributed Locks

Examples

- Workflow execution
- Scheduled jobs
- Synchronization

---

### Queues

Examples

- Background jobs
- Event processing
- Async notifications

---

### Rate Limiting

Examples

- Login attempts
- API quotas
- Voice API protection

---

## Redis Does NOT Store

- Permanent conversations
- Billing
- Users
- Long-term business records


---

# 8. Object Storage

Object Storage stores binary assets.

Examples

- Uploaded PDFs
- Images
- Audio files
- Call recordings
- Generated reports
- Training datasets

---

Metadata for these files remains in PostgreSQL.


---

# 9. LiveKit Redis

LiveKit internally uses Redis for cluster coordination.

Responsibilities include

- Node discovery
- Room coordination
- Distributed state
- Presence information

This Redis instance is infrastructure-related and independent of the application's caching strategy.


---

# 10. Storage Ownership

| Data | Owner |
|------|-------|
| Users | PostgreSQL |
| Organizations | PostgreSQL |
| Agents | PostgreSQL |
| Voice Config | PostgreSQL |
| Calls | PostgreSQL |
| Conversations | PostgreSQL |
| Documents | Object Storage |
| Recordings | Object Storage |
| Images | Object Storage |
| Embeddings | pgvector |
| Runtime Cache | Redis |
| Active Sessions | Redis |
| Background Queues | Redis |


---

# 11. Document Processing Flow

```
Upload PDF

↓

Object Storage

↓

Document Processor

↓

Chunking

↓

Embedding Generation

↓

pgvector

↓

Metadata

↓

PostgreSQL
```


---

# 12. Voice Conversation Flow

```
Incoming Call

↓

LiveKit

↓

Speech-to-Text

↓

AI Runtime

↓

Conversation State

↓

Redis

↓

Conversation Complete

↓

Persist

↓

PostgreSQL
```


---

# 13. Knowledge Retrieval Flow

```
User Question

↓

Embedding

↓

pgvector Search

↓

Relevant Chunks

↓

AI Runtime

↓

LLM

↓

Voice Response
```


---

# 14. Agent Configuration Flow

```
Agent Request

↓

Redis Cache

↓

Cache Hit?

 ├── Yes → Return Configuration

 └── No

        ↓

   PostgreSQL

        ↓

   Cache Result

        ↓

   Return Configuration
```


---

# 15. Recording Storage Flow

```
Voice Session

↓

Recording

↓

Object Storage

↓

Recording Metadata

↓

PostgreSQL
```


---

# 16. Conversation Lifecycle

```
Conversation Starts

↓

Redis Session

↓

Memory Updates

↓

Tool Execution

↓

Conversation Ends

↓

Persist Conversation

↓

PostgreSQL

↓

Generate Embeddings

↓

pgvector
```


---

# 17. Data Synchronization

Each storage system has a clearly defined ownership boundary.

Synchronization occurs through:

- Backend services
- Domain events
- Background workers
- Event-driven pipelines

No storage system writes directly into another.

All coordination is performed by application services.


---

# 18. Data Retention Strategy

| Data Type | Storage |
|------------|----------|
| Business Records | PostgreSQL |
| Runtime State | Redis |
| Embeddings | pgvector |
| Uploaded Files | Object Storage |
| Voice Recordings | Object Storage |
| Audit Logs | PostgreSQL |
| Analytics Events | PostgreSQL / Data Warehouse (future) |


---

# 19. Scalability Strategy

The storage architecture scales independently.

### PostgreSQL

- Read replicas
- Partitioning
- Connection pooling

### Redis

- Redis Cluster
- High availability
- Automatic failover

### pgvector

- HNSW indexes
- IVFFlat indexes
- Horizontal database scaling

### Object Storage

- Virtually unlimited storage
- CDN integration
- Lifecycle policies


---

# 20. Security

Every storage system follows the platform security model.

Controls include:

- Encryption at rest
- Encryption in transit
- Tenant isolation
- Role-based access control
- Audit logging
- Secret management
- Backup and disaster recovery


---

# 21. Design Principles

The storage architecture follows these principles:

- Single source of truth
- Separation of responsibilities
- Event-driven synchronization
- Stateless services
- Independent scalability
- High availability
- Secure by design
- Multi-tenant isolation


---

# 22. Related Documentation

- 03_DATABASE
- 04_BACKEND
- 06_VOICE_PLATFORM
- 07_AI_RUNTIME
- 08_RAG
- 09_MEMORY
- 10_AUTOMATION
- 12_DEPLOYMENT


---

# 23. Summary

The Voice Agent SaaS Platform uses a multi-storage architecture in which each technology is responsible for a specific workload.

- **PostgreSQL** is the authoritative system for structured business data.
- **pgvector** powers semantic search and Retrieval-Augmented Generation.
- **Redis** provides high-speed caching, runtime state management, distributed coordination, and asynchronous messaging.
- **Object Storage** stores documents, recordings, and other large binary assets.
- **LiveKit Redis** supports media cluster coordination.

Together, these systems provide a scalable, resilient, and AI-optimized data foundation that supports enterprise-grade voice agents, real-time conversations, intelligent retrieval, and long-term business operations.

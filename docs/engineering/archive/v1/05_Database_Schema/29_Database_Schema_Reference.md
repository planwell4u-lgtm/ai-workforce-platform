# Database Schema Reference

**Document Version:** 1.0
**Project:** AI Voice Agent SaaS Platform
**Phase:** 05 - Database Schema
**Database Platform:** Supabase PostgreSQL + Redis + pgvector
**Purpose:** Master Database Catalog
**Status:** Draft
**Last Updated:** 2026-07-23

---

# 1. Overview

This document is the master reference for the complete database architecture of the AI Voice Agent SaaS platform.

It provides:

* Complete schema inventory
* Table ownership
* Entity relationships
* Data ownership rules
* Storage strategy
* Security boundaries

---

# 2. Database Architecture Overview

```text
AI Voice Agent Platform Database

                    PostgreSQL

 ------------------------------------------------

 Core Business

 ├── Tenants
 ├── Users
 ├── Organizations
 ├── Agents
 ├── Customers
 ├── Calls
 ├── Conversations


 AI Runtime

 ├── Agent Sessions
 ├── Workflows
 ├── Tools
 ├── Memory


 Knowledge Intelligence

 ├── Documents
 ├── Chunks
 ├── Embeddings


 Operations

 ├── Notifications
 ├── Integrations
 ├── Analytics
 ├── Billing


 Security

 ├── Audit Logs
 ├── Roles
 └── Permissions


                    Redis

 ------------------------------------------------

 ├── Active Calls
 ├── Session State
 ├── Agent State
 ├── Cache
 └── Realtime Metrics
```

---

# 3. Complete Schema Inventory

| Schema              | Purpose                       |
| ------------------- | ----------------------------- |
| Core Schema         | Users, tenants, organizations |
| Agent Schema        | AI agent configuration        |
| Voice Schema        | Calls and conversations       |
| Workflow Schema     | Agent execution               |
| Memory Schema       | AI memory                     |
| Knowledge Schema    | RAG documents                 |
| Billing Schema      | Subscription and usage        |
| Notification Schema | Events and messages           |
| Storage Schema      | Files and recordings          |
| Analytics Schema    | Reports and metrics           |
| Integration Schema  | External services             |
| Vector Schema       | Semantic search               |
| Realtime Schema     | Runtime state                 |
| Security Schema     | Access control                |

---

# 4. Core Tables

## Tenant Management

Tables:

```text
tenants

organizations

workspaces

teams

tenant_settings

tenant_features
```

Purpose:

* SaaS isolation
* Enterprise hierarchy
* Configuration management

---

# 5. Authentication Tables

Tables:

```text
users

roles

permissions

user_roles

sessions
```

Purpose:

* Identity
* Authorization
* Access control

---

# 6. AI Agent Tables

Tables:

```text
agents

agent_versions

agent_prompts

agent_tools

agent_settings

agent_memory_config
```

Purpose:

* Agent lifecycle
* Configuration
* Behavior control

---

# 7. Voice Communication Tables

Tables:

```text
calls

call_participants

call_events

call_recordings

transcripts

transcript_segments
```

Purpose:

* PSTN calls
* LiveKit sessions
* Voice history

---

# 8. Conversation Tables

Tables:

```text
conversations

messages

message_embeddings

conversation_metadata
```

Purpose:

* Chat history
* AI context
* Conversation analysis

---

# 9. Workflow Tables

Tables:

```text
workflows

workflow_versions

workflow_runs

workflow_steps

workflow_logs
```

Purpose:

* LangGraph execution
* Automation flows

---

# 10. Tool Execution Tables

Tables:

```text
tools

tool_definitions

tool_executions

tool_results
```

Purpose:

* AI function calling
* External actions

---

# 11. Memory System Tables

Tables:

```text
memory_items

memory_embeddings

memory_events

memory_access_logs
```

Purpose:

* Long-term AI memory
* User personalization
* Retrieval

---

# 12. RAG Knowledge Tables

Tables:

```text
knowledge_bases

documents

document_chunks

embeddings

retrieval_logs
```

Purpose:

* Enterprise knowledge
* Semantic search

---

# 13. Billing Tables

Tables:

```text
subscriptions

plans

usage_records

invoices

payments

credit_balances
```

Purpose:

* SaaS monetization
* Usage tracking

---

# 14. Notification Tables

Tables:

```text
events

event_subscriptions

notifications

templates

webhook_endpoints

delivery_logs
```

Purpose:

* Async communication
* External notifications

---

# 15. Storage Tables

Tables:

```text
storage_files

storage_buckets

file_versions

file_access_logs

media_processing_jobs
```

Purpose:

* Documents
* Audio
* Attachments

---

# 16. Analytics Tables

Tables:

```text
analytics_events

call_metrics

agent_metrics

customer_metrics

usage_metrics

revenue_metrics

reports
```

Purpose:

* Business intelligence
* Platform analytics

---

# 17. Integration Tables

Tables:

```text
integration_providers

integrations

integration_credentials

oauth_connections

api_endpoints

sync_jobs
```

Purpose:

* Twilio
* LiveKit
* OpenAI
* CRM systems

---

# 18. Vector Search Tables

Tables:

```text
knowledge_bases

documents

document_chunks

embeddings

search_queries

retrieval_logs
```

Purpose:

* RAG retrieval
* Semantic search

---

# 19. Realtime Tables

Tables:

```text
active_sessions

livekit_rooms

agent_sessions

state_snapshots

realtime_metrics
```

Redis:

```text
active_call:{id}

conversation:{id}:state

workflow:{id}:state

presence:{id}
```

---

# 20. Database Ownership Rules

Every resource belongs to:

```text
Tenant

↓

Organization

↓

Workspace

↓

Resource
```

Example:

```text
Tenant

 |

Agent

 |

Call

 |

Conversation

 |

Recording
```

---

# 21. Global Database Rules

All tenant-owned tables require:

```sql
tenant_id UUID NOT NULL
```

All tables require:

```text
created_at

updated_at
```

where applicable.

---

# 22. Naming Convention

Tables:

```text
snake_case plural
```

Examples:

```text
agents

call_events

workflow_runs
```

---

Columns:

```text
snake_case
```

Examples:

```text
created_at

tenant_id

agent_id
```

---

# 23. Primary Keys

Standard:

```sql
UUID
```

Example:

```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
```

---

# 24. Foreign Keys

Example:

```sql
agent_id UUID REFERENCES agents(id)
```

Rules:

* Maintain referential integrity
* Prevent orphan records

---

# 25. Soft Delete Strategy

For important records:

Use:

```sql
deleted_at TIMESTAMP
```

Example:

```text
Agents

Customers

Documents
```

---

# 26. Audit Strategy

Track:

```text
Who

What

When

Where

Before

After
```

Using:

```text
audit_logs
```

---

# 27. Production Database Stack

Recommended:

```text
Supabase PostgreSQL

+

pgvector

+

Redis

+

Object Storage
```

---

# 28. Development Workflow

```text
Design Schema

↓

Create Migration

↓

Update ERD

↓

Apply Migration

↓

Test API

↓

Deploy
```

---

# 29. Database Documentation Map

```text
05_Database_Schema/

├── Core

├── Agent

├── Voice

├── Workflow

├── Memory

├── RAG

├── Billing

├── Notifications

├── Storage

├── Analytics

├── Integrations

├── Vector

├── Realtime

└── Security
```

---

# 30. Future Database Evolution

Planned:

* Read replicas
* Data warehouse
* Event sourcing
* Multi-region databases
* Tenant dedicated databases

---

# 31. Final Architecture Summary

The database architecture supports:

✓ Multi-tenant SaaS

✓ AI voice agents

✓ LiveKit realtime communication

✓ Twilio telephony

✓ LangGraph workflows

✓ RAG knowledge systems

✓ Long-term AI memory

✓ Billing automation

✓ Enterprise security

✓ Production scalability

---

# 32. Related Documents

| Document                                  | Purpose      |
| ----------------------------------------- | ------------ |
| 25_Database_Index_Performance_Strategy.md | Optimization |
| 26_Database_Backup_Disaster_Recovery.md   | Recovery     |
| 27_Database_Migration_Strategy.md         | Migration    |
| 28_Database_Security_RLS_Strategy.md      | Security     |

---

# 33. Conclusion

The Database Schema Reference is the central map of the AI Voice Agent SaaS database architecture.

It connects all database domains into one scalable, secure, production-ready design.

---

**End of Document**

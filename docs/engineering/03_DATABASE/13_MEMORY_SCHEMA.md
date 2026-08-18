# Memory Schema

**Document ID:** DB-MEMORY-012  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for the AI Agent Memory System.

The memory domain provides persistent intelligence for AI agents by storing information learned from interactions, users, and operational experiences.

The memory system enables agents to:

- Remember previous conversations
- Store user preferences
- Maintain customer context
- Improve future responses
- Retrieve historical information
- Build long-term relationships

---

# 2. Memory Architecture

High-level architecture:

             Conversation

                  |

          Memory Extraction

                  |

         Memory Processing

                  |

    +-------------+-------------+

    |                           |

Short-Term Long-Term

Memory Memory

    |                           |

 Redis                   PostgreSQL

    |

Active Context

                  |

          Agent Runtime

---

# 3. Memory Design Principles

## 3.1 Memory Is Tenant-Owned

All stored memories belong to a tenant.

Example:


Customer Company

   |

Customer Memory

   |

AI Agent Usage


---

## 3.2 Memory Requires Classification

Every memory item must define:

- Type
- Scope
- Importance
- Expiration
- Source

---

## 3.3 Privacy First

Memory storage must support:

- Deletion requests
- Retention policies
- Access controls
- Audit history

---

# 4. Memory Schema

Schema:


memory


---

# 5. Memory Tables Overview


memory.memories

memory.memory_types

memory.user_memories

memory.agent_memories

memory.conversation_memories

memory.memory_embeddings

memory.memory_access_logs

memory.memory_versions


---

# 6. Memory Entity

Table:


memory.memories


Purpose:

Base entity for all memory records.

---

Structure:

```sql
CREATE TABLE memory.memories
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID NOT NULL,

    memory_type TEXT NOT NULL,

    content TEXT NOT NULL,

    importance_score FLOAT,

    status TEXT DEFAULT 'active',

    created_at TIMESTAMPTZ DEFAULT now(),

    updated_at TIMESTAMPTZ DEFAULT now()
);
7. Memory Types

Supported memory categories:

Type	Purpose
user	Customer preferences
agent	Agent learned information
conversation	Previous interaction context
business	Company knowledge
operational	Workflow history
8. Memory Lifecycle
Created

   |

Validated

   |

Stored

   |

Retrieved

   |

Updated

   |

Archived

9. User Memory

Table:

memory.user_memories

Purpose:

Stores information about individual customers.

Examples:

Customer prefers morning appointments

Customer owns three vehicles

Customer requested Spanish support


Structure:

CREATE TABLE memory.user_memories
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

user_id UUID NOT NULL,

memory_id UUID NOT NULL,

created_at TIMESTAMPTZ DEFAULT now()
);
10. Agent Memory

Table:

memory.agent_memories

Purpose:

Stores information associated with AI agents.

Examples:

Successful response patterns

Frequently used workflows

Business-specific behavior


Structure:

CREATE TABLE memory.agent_memories
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

agent_id UUID NOT NULL,

memory_id UUID NOT NULL,

created_at TIMESTAMPTZ DEFAULT now()
);
11. Conversation Memory

Table:

memory.conversation_memories

Purpose:

Stores important information extracted from conversations.

Example:

Conversation:

Customer:

"I prefer email communication."


Extracted memory:

Preferred contact method = Email


Structure:

CREATE TABLE memory.conversation_memories
(
id UUID PRIMARY KEY,

conversation_id UUID NOT NULL,

memory_id UUID NOT NULL,

created_at TIMESTAMPTZ DEFAULT now()
);
12. Memory Extraction Pipeline

Process:

Conversation Completed

        |

AI Extraction Model

        |

Identify Important Facts

        |

Validate Memory

        |

Store Memory

        |

Generate Embedding

        |

Future Retrieval

13. Memory Embeddings

Table:

memory.memory_embeddings

Purpose:

Stores vector representation of memories.

Structure:

CREATE TABLE memory.memory_embeddings
(
id UUID PRIMARY KEY,

memory_id UUID NOT NULL,

embedding VECTOR(1536),

model_name TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
14. Memory Retrieval

Runtime flow:

New Conversation

       |

Agent Runtime

       |

Memory Search

       |

Retrieve Relevant Memories

       |

Add Context

       |

Generate Response

15. Memory Search Example

User:

What appointment time did John prefer?

System:

Search Memory

       |

Find:

John prefers mornings

       |

Provide Context

       |

Agent Response

16. Memory Importance Scoring

Each memory may include:

importance_score

Example:

Score	Meaning
0.9	Critical preference
0.5	Useful information
0.1	Temporary information
17. Memory Expiration

Optional fields:

expires_at TIMESTAMPTZ

Used for:

Temporary preferences
Session information
Time-sensitive context
18. Memory Access Logs

Table:

memory.memory_access_logs

Purpose:

Tracks memory usage.

Events:

MEMORY_CREATED

MEMORY_RETRIEVED

MEMORY_UPDATED

MEMORY_DELETED


Structure:

CREATE TABLE memory.memory_access_logs
(
id UUID PRIMARY KEY,

memory_id UUID NOT NULL,

agent_id UUID,

action TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
19. Memory Versioning

Table:

memory.memory_versions

Purpose:

Maintains history of memory changes.

Example:

Preference:

Morning appointment


Updated:


Afternoon appointment

20. Agent Runtime Integration

Memory loading:

Incoming Request

       |

Identify User

       |

Search Memory

       |

Load Relevant Context

       |

Initialize Agent

       |

Respond

21. Knowledge vs Memory

Difference:

Knowledge	Memory
Company information	Individual context
Documents	Experiences
Static	Dynamic
Admin managed	AI generated
22. Storage Strategy
PostgreSQL

Stores:

Permanent memories
Metadata
Embeddings
Audit records
Redis

Stores:

Active session memory
Current conversation state
Temporary context

Architecture:

Agent Runtime

      |

+-------------+

|             |

Redis     PostgreSQL

Fast      Permanent

23. Multi-Tenant Requirements

Required:

tenant_id UUID NOT NULL

RLS enabled:

memory.*
24. Performance Requirements

High growth tables:

Table	Growth
memories	High
embeddings	High
access_logs	Very High
25. Index Requirements

Tenant search:

CREATE INDEX idx_memory_tenant
ON memory.memories(tenant_id);

User memory lookup:

CREATE INDEX idx_user_memory
ON memory.user_memories(user_id);

Vector search:

CREATE INDEX idx_memory_embedding
ON memory.memory_embeddings

USING ivfflat
(embedding vector_cosine_ops);
26. Security Requirements

Required:

Tenant isolation
User consent handling
Memory deletion support
Access auditing
Sensitive data filtering
27. Future Extensions

Possible additions:

memory.importance_model_scores

memory.memory_clusters

memory.agent_learning

memory.feedback_scores

memory.personalization_profiles

memory.semantic_cache

28. Related Documents

Next:

13_WORKFLOW_SCHEMA.md

14_INTEGRATION_SCHEMA.md

15_BILLING_SCHEMA.md
End of Document
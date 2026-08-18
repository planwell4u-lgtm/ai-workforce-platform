# RAG Schema

**Document ID:** DB-RAG-012  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for the Retrieval-Augmented Generation (RAG) system used by the AI Voice Agent SaaS platform.

The RAG subsystem enables AI agents to retrieve relevant information from tenant knowledge sources and provide context-aware responses.

The RAG layer manages:

- Retrieval pipelines
- Vector search
- Embeddings
- Search strategies
- Retrieved context
- Reranking
- Retrieval evaluation
- Semantic caching
- Agent knowledge routing

---

# 2. RAG Architecture

High-level flow:

             User Request

                  |

            Agent Runtime

                  |

             RAG Pipeline

                  |

    +-------------+-------------+

    |             |             |

Query        Retrieval       Ranking

Processing Engine Engine

    |             |             |

    +-------------+-------------+

                  |

          Context Assembly

                  |

               LLM

                  |

            Final Response

---

# 3. RAG Design Principles

## 3.1 Retrieval Before Generation

The AI model should receive relevant external context before generating responses.

Flow:


Question

|

Retrieve Knowledge

|

Build Context

|

Generate Answer


---

## 3.2 Tenant-Isolated Retrieval

Every retrieval operation must enforce tenant boundaries.

Required:

```sql
tenant_id UUID NOT NULL
3.3 Model Independence

The RAG system supports:

OpenAI embeddings
Local embedding models
Custom models
Future providers
4. RAG Schema

Schema:

rag
5. RAG Tables Overview
rag.pipelines

rag.pipeline_steps

rag.queries

rag.retrieval_sessions

rag.retrieval_results

rag.contexts

rag.reranking_results

rag.semantic_cache

rag.evaluations

rag.agent_knowledge_routes

6. RAG Pipeline

Table:

rag.pipelines

Purpose:

Defines retrieval workflows.

Examples:

Customer Support RAG

Medical Assistant RAG

Sales Agent RAG


Structure:

CREATE TABLE rag.pipelines
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID NOT NULL,

    name TEXT NOT NULL,

    description TEXT,

    configuration JSONB,

    status TEXT DEFAULT 'active',

    created_at TIMESTAMPTZ DEFAULT now()
);
7. Pipeline Lifecycle
Created

 |

Configured

 |

Testing

 |

Active

 |

Archived

8. Pipeline Steps

Table:

rag.pipeline_steps

Purpose:

Defines execution stages.

Example:

Query Rewrite

      |

Vector Search

      |

Metadata Filter

      |

Reranking

      |

Context Builder


Structure:

CREATE TABLE rag.pipeline_steps
(
id UUID PRIMARY KEY,

pipeline_id UUID NOT NULL,

step_type TEXT NOT NULL,

configuration JSONB,

execution_order INTEGER

);
9. Query Processing

Table:

rag.queries

Purpose:

Stores user retrieval requests.

Examples:

"What is your refund policy?"

"Schedule a service appointment"


Structure:

CREATE TABLE rag.queries
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

agent_id UUID,

conversation_id UUID,

query_text TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
10. Retrieval Sessions

Table:

rag.retrieval_sessions

Purpose:

Tracks one complete retrieval execution.

Example:

Customer Question

      |

Retrieval Session

      |

Search Results

      |

Context Generated


Structure:

CREATE TABLE rag.retrieval_sessions
(
id UUID PRIMARY KEY,

query_id UUID NOT NULL,

pipeline_id UUID,

status TEXT,

latency_ms INTEGER,

created_at TIMESTAMPTZ DEFAULT now()
);
11. Retrieval Results

Table:

rag.retrieval_results

Purpose:

Stores documents returned from search.

Example:

Query:

How do I cancel?


Results:

Document A - Refund Policy

Document B - Terms


Structure:

CREATE TABLE rag.retrieval_results
(
id UUID PRIMARY KEY,

retrieval_session_id UUID NOT NULL,

chunk_id UUID NOT NULL,

similarity_score FLOAT,

rank_position INTEGER,

created_at TIMESTAMPTZ DEFAULT now()
);
12. Retrieval Strategies

Supported:

Strategy	Description
vector	Semantic similarity
keyword	Traditional search
hybrid	Vector + keyword
metadata	Filter based
graph	Relationship search
13. Context Assembly

Table:

rag.contexts

Purpose:

Stores the final context provided to the LLM.

Example:

Retrieved Chunks

        +

Conversation History

        +

Memory

        |

LLM Context


Structure:

CREATE TABLE rag.contexts
(
id UUID PRIMARY KEY,

retrieval_session_id UUID NOT NULL,

context_text TEXT,

token_count INTEGER,

created_at TIMESTAMPTZ DEFAULT now()
);
14. Reranking

Table:

rag.reranking_results

Purpose:

Stores ranking improvements after initial retrieval.

Example:

Vector Search:

100 results


Reranker:

Top 5 results


Structure:

CREATE TABLE rag.reranking_results
(
id UUID PRIMARY KEY,

retrieval_session_id UUID NOT NULL,

chunk_id UUID NOT NULL,

rerank_score FLOAT,

final_position INTEGER
);
15. Semantic Cache

Table:

rag.semantic_cache

Purpose:

Stores previous successful retrieval responses.

Benefits:

Lower latency
Lower AI cost
Faster responses

Structure:

CREATE TABLE rag.semantic_cache
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

query_embedding VECTOR(1536),

response TEXT,

expires_at TIMESTAMPTZ,

created_at TIMESTAMPTZ DEFAULT now()
);
16. Agent Knowledge Routing

Table:

rag.agent_knowledge_routes

Purpose:

Controls which knowledge sources agents can access.

Example:

Sales Agent

   |

Sales Knowledge Base


Support Agent

   |

Support Documentation


Structure:

CREATE TABLE rag.agent_knowledge_routes
(
id UUID PRIMARY KEY,

agent_id UUID NOT NULL,

knowledge_base_id UUID NOT NULL,

priority INTEGER DEFAULT 1
);
17. RAG Evaluation

Table:

rag.evaluations

Purpose:

Measures retrieval quality.

Metrics:

Retrieval Accuracy

Context Relevance

Answer Grounding

Hallucination Rate

Latency


Structure:

CREATE TABLE rag.evaluations
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

retrieval_session_id UUID,

metric_name TEXT,

score NUMERIC,

created_at TIMESTAMPTZ DEFAULT now()
);
18. RAG Runtime Flow

Example:

Customer Question

        |

Conversation Service

        |

Agent Runtime

        |

RAG Pipeline

        |

Vector Database

        |

Context Injection

        |

LLM Generation

19. Integration With Knowledge Schema

Relationship:

Knowledge Base

      |

Documents

      |

Chunks

      |

Embeddings

      |

RAG Retrieval

20. Integration With Memory

RAG context may include:

Knowledge

+

Conversation History

+

User Memory

+

Runtime State

21. Storage Strategy
PostgreSQL + pgvector

Stores:

Embeddings
Retrieval metadata
Search history
Redis

Stores:

Semantic cache
Temporary retrieval state
Hot queries
22. Performance Requirements

High-volume tables:

Table	Growth
retrieval_results	Very High
queries	Very High
evaluations	Medium
23. Index Requirements

Tenant lookup:

CREATE INDEX idx_rag_queries_tenant
ON rag.queries(tenant_id);

Retrieval lookup:

CREATE INDEX idx_retrieval_session
ON rag.retrieval_results(retrieval_session_id);

Vector index:

CREATE INDEX idx_rag_cache_vector

ON rag.semantic_cache

USING ivfflat
(query_embedding vector_cosine_ops);
24. Security Requirements

Required:

Tenant isolation
Knowledge access permissions
Sensitive context filtering
Retrieval audit logs
Data retention policies
25. Future Extensions

Possible additions:

rag.graph_rag

rag.agent_reasoning_context

rag.multimodal_embeddings

rag.feedback_learning

rag.query_optimizer

rag.retrieval_models

26. Related Documents

Next:

13_MEMORY_SCHEMA.md

14_WORKFLOW_SCHEMA.md  (existing)

15_INTEGRATION_SCHEMA.md
End of Document
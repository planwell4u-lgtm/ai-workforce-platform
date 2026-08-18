# Knowledge Schema

**Document ID:** DB-KNOWLEDGE-011  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for the AI Knowledge Management and Retrieval-Augmented Generation (RAG) system.

The knowledge domain provides the foundation for AI agents to access tenant-specific information.

The system supports:

- Knowledge base management
- Document ingestion
- Document processing
- Text chunking
- Embedding generation
- Vector similarity search
- Retrieval tracking
- Knowledge versioning
- AI context enrichment

---

# 2. Knowledge Architecture

High-level RAG flow:

            Customer Data

                 |

          Knowledge Upload

                 |

          Document Processing

                 |

             Chunking

                 |

         Embedding Generation

                 |

          Vector Storage

                 |

         Similarity Retrieval

                 |

             LLM Context

                 |

          Agent Response

---

# 3. Knowledge Design Principles

## 3.1 Tenant-Owned Knowledge

All knowledge belongs to a tenant.

Example:


Company A

|

Knowledge Base

|

Documents

|

Embeddings


---

## 3.2 Source Independence

The system supports multiple sources:

- Uploaded files
- Websites
- APIs
- Databases
- Cloud storage
- CRM systems

---

## 3.3 Versioned Knowledge

Documents must support:

- Updates
- History
- Reprocessing
- Rollback

---

# 4. Knowledge Schema

Schema:


knowledge


---

# 5. Knowledge Tables Overview


knowledge.knowledge_bases

knowledge.documents

knowledge.document_versions

knowledge.document_chunks

knowledge.embeddings

knowledge.ingestion_jobs

knowledge.retrieval_logs

knowledge.sources


---

# 6. Knowledge Base Entity

Table:


knowledge.knowledge_bases


Purpose:

Represents a collection of information available to AI agents.

Examples:


Customer FAQ

Product Documentation

Internal Policies

Support Articles


---

Structure:

```sql
CREATE TABLE knowledge.knowledge_bases
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID NOT NULL,

    name TEXT NOT NULL,

    description TEXT,

    status TEXT DEFAULT 'active',

    created_at TIMESTAMPTZ DEFAULT now(),

    updated_at TIMESTAMPTZ DEFAULT now()
);
7. Knowledge Base Lifecycle
Created

   |

Active

   |

Updated

   |

Archived

8. Knowledge Sources

Table:

knowledge.sources

Purpose:

Defines where knowledge originates.

Supported sources:

Source	Example
upload	PDF, DOCX, TXT
website	Web crawler
api	External API
database	SQL source
cloud	Storage provider

Structure:

CREATE TABLE knowledge.sources
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

source_type TEXT NOT NULL,

configuration JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
9. Document Entity

Table:

knowledge.documents

Purpose:

Stores knowledge documents.

Examples:

Product Manual.pdf

Employee Handbook.docx

FAQ Article


Structure:

CREATE TABLE knowledge.documents
(
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

tenant_id UUID NOT NULL,

knowledge_base_id UUID NOT NULL,

name TEXT NOT NULL,

file_type TEXT,

status TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
10. Document Lifecycle
Uploaded

   |

Processing

   |

Indexed

   |

Available

   |

Archived

11. Document Versioning

Table:

knowledge.document_versions

Purpose:

Tracks document changes.

Example:

Product Manual v1

        |

Product Manual v2


Structure:

CREATE TABLE knowledge.document_versions
(
id UUID PRIMARY KEY,

document_id UUID NOT NULL,

version_number INTEGER NOT NULL,

storage_url TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
12. Document Processing Pipeline
Upload File

    |

Extract Text

    |

Clean Content

    |

Split Into Chunks

    |

Generate Embeddings

    |

Store Vectors

    |

Enable Retrieval

13. Document Chunks

Table:

knowledge.document_chunks

Purpose:

Stores searchable text segments.

Example:

Original:

500 page manual

Becomes:

Chunk 1

Chunk 2

Chunk 3

...


Structure:

CREATE TABLE knowledge.document_chunks
(
id UUID PRIMARY KEY,

document_id UUID NOT NULL,

content TEXT NOT NULL,

chunk_index INTEGER,

metadata JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
14. Chunking Strategy

Default strategy:

Document

    |

Paragraph Split

    |

Token Window

    |

Overlap

    |

Chunk Storage


Recommended:

Chunk Size:

500-1000 tokens


Overlap:

50-150 tokens

15. Embedding Storage

Table:

knowledge.embeddings

Purpose:

Stores vector representations.

Technology:

PostgreSQL + pgvector

Structure:

CREATE TABLE knowledge.embeddings
(
id UUID PRIMARY KEY,

chunk_id UUID NOT NULL,

embedding VECTOR(1536),

model_name TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
16. Vector Search

Example query:

SELECT *

FROM knowledge.embeddings

ORDER BY embedding <-> query_vector

LIMIT 10;

Used for:

Semantic search
RAG retrieval
Agent answers
17. Agent Knowledge Assignment

Relationship:

Knowledge Base

        |

Agent

        |

Runtime Retrieval


Future mapping table:

agent.agent_knowledge_bases
18. Retrieval Logs

Table:

knowledge.retrieval_logs

Purpose:

Tracks AI knowledge usage.

Example:

User Question

      |

Retrieved Documents

      |

Generated Answer


Structure:

CREATE TABLE knowledge.retrieval_logs
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

agent_id UUID,

query TEXT,

results JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
19. Ingestion Jobs

Table:

knowledge.ingestion_jobs

Purpose:

Tracks processing tasks.

Lifecycle:

Queued

 |

Processing

 |

Completed

 |

Failed


Structure:

CREATE TABLE knowledge.ingestion_jobs
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

document_id UUID,

status TEXT,

started_at TIMESTAMPTZ,

completed_at TIMESTAMPTZ
);
20. Integration With Agent Runtime

Runtime flow:

User Question

      |

Agent Runtime

      |

Knowledge Retrieval

      |

Vector Search

      |

Relevant Context

      |

LLM Response

21. Multi-Tenant Requirements

All tenant-owned tables require:

tenant_id UUID NOT NULL

Required:

knowledge.*

Row Level Security enabled.

22. Performance Requirements

High-volume tables:

Table	Growth
document_chunks	High
embeddings	Very High
retrieval_logs	High
23. Index Requirements

Tenant lookup:

CREATE INDEX idx_documents_tenant
ON knowledge.documents(tenant_id);

Chunk lookup:

CREATE INDEX idx_chunks_document
ON knowledge.document_chunks(document_id);

Vector index:

CREATE INDEX idx_embedding_vector

ON knowledge.embeddings

USING ivfflat (embedding vector_cosine_ops);
24. Security Requirements

Required:

Document access control
Tenant isolation
Encrypted storage references
Sensitive document protection
Audit logging
25. Data Retention

Policies:

Active Documents

Retained


Deleted Documents

Soft Delete


Expired Data

Archived

26. Future Extensions

Possible additions:

knowledge.graph_entities

knowledge.relationships

knowledge.feedback

knowledge.semantic_cache

knowledge.ai_annotations

knowledge.document_quality_scores

27. Related Documents

Next:

12_MEMORY_SCHEMA.md

13_WORKFLOW_SCHEMA.md

14_INTEGRATION_SCHEMA.md
End of Document
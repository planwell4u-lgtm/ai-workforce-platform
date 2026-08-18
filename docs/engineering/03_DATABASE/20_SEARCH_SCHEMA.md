# Search Schema

**Document ID:** DB-SEARCH-020  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for the global search subsystem of the AI Voice Agent SaaS platform.

The search system provides fast discovery across:

- Agents
- Users
- Conversations
- Knowledge documents
- Customers
- Calls
- Workflows
- Integrations
- Audit records

The search layer supports:

- Full-text search
- Semantic search
- Fuzzy matching
- Filtering
- Tenant-aware indexing
- Unified search experience

---

# 2. Search Architecture

High-level model:

             User Query

                 |

          Search Service

                 |

    +------------+------------+

    |                         |

PostgreSQL FTS Vector Search

    |                         |

    +------------+------------+

                 |

         Search Aggregator

                 |

          Search Results

---

# 3. Search Design Principles

## 3.1 Unified Search

Users should search multiple domains from one interface.

Example:


"John Smith"

Returns:

Customer

Conversation

Call Record

Invoice

Agent Notes


---

## 3.2 Tenant Isolation

Every search operation must enforce tenant boundaries.

Required:

```sql
tenant_id UUID NOT NULL
3.3 Multiple Search Strategies

The system supports:

Exact matching
Full-text search
Fuzzy matching
Semantic search
Metadata filtering
4. Search Schema

Schema:

search
5. Search Tables Overview
search.indexes

search.documents

search.records

search.queries

search.results

search.filters

search.synonyms

search.analytics

6. Search Index Registry

Table:

search.indexes

Purpose:

Defines searchable entities.

Examples:

agents

customers

conversations

knowledge_documents

calls


Structure:

CREATE TABLE search.indexes
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID NOT NULL,

    entity_type TEXT NOT NULL,

    status TEXT DEFAULT 'active',

    created_at TIMESTAMPTZ DEFAULT now()
);
7. Search Documents

Table:

search.documents

Purpose:

Stores searchable text content.

Examples:

Conversation transcript

Knowledge article

Agent description

Customer notes


Structure:

CREATE TABLE search.documents
(
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

tenant_id UUID NOT NULL,

entity_type TEXT NOT NULL,

entity_id UUID NOT NULL,

title TEXT,

content TEXT,

metadata JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
8. Search Records

Table:

search.records

Purpose:

Unified searchable entity registry.

Example:

Agent:
Customer Support Agent


Conversation:
Call #12345


Structure:

CREATE TABLE search.records
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

entity_type TEXT NOT NULL,

entity_id UUID NOT NULL,

display_name TEXT,

search_vector TSVECTOR,

created_at TIMESTAMPTZ DEFAULT now()
);
9. PostgreSQL Full Text Search

The system uses:

tsvector
tsquery

Example:

SELECT *

FROM search.records

WHERE search_vector @@ plainto_tsquery('appointment');
10. Search Queries

Table:

search.queries

Purpose:

Tracks user search activity.

Structure:

CREATE TABLE search.queries
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

user_id UUID,

query_text TEXT,

filters JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
11. Search Results

Table:

search.results

Purpose:

Stores returned results.

Structure:

CREATE TABLE search.results
(
id UUID PRIMARY KEY,

query_id UUID NOT NULL,

entity_type TEXT,

entity_id UUID,

ranking_score FLOAT,

created_at TIMESTAMPTZ DEFAULT now()
);
12. Search Ranking

Ranking factors:

Factor	Weight
Exact match	High
Text relevance	Medium
Recent activity	Medium
User permissions	Required
Semantic similarity	High
13. Semantic Search Integration

Search integrates with:

rag

knowledge

memory


Flow:

Query

 |

Embedding Generation

 |

Vector Search

 |

Ranking

 |

Results

14. Fuzzy Search

Used for:

Names
Phone numbers
Customer lookup
Typo correction

Technology:

pg_trgm

Example:

SELECT *

FROM customers

WHERE name % 'Jon Smith';
15. Search Filters

Table:

search.filters

Purpose:

Stores reusable search filters.

Examples:

Active Agents

Failed Calls

Recent Conversations


Structure:

CREATE TABLE search.filters
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

name TEXT,

configuration JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
16. Search Synonyms

Table:

search.synonyms

Purpose:

Improves search understanding.

Example:

appointment

=

booking

=

schedule


Structure:

CREATE TABLE search.synonyms
(
id UUID PRIMARY KEY,

tenant_id UUID,

term TEXT,

synonyms JSONB
);
17. Search Analytics

Table:

search.analytics

Purpose:

Measures search quality.

Metrics:

Search frequency

No-result searches

Popular queries

Response latency


Structure:

CREATE TABLE search.analytics
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

query_text TEXT,

result_count INTEGER,

latency_ms INTEGER,

created_at TIMESTAMPTZ DEFAULT now()
);
18. Permission Filtering

Search must apply:

Tenant permissions
User roles
Resource ownership
Data visibility rules

Example:

User searches:

"Customer Transcript"


System checks:

Can user access conversation?

19. Multi-Tenant Requirements

Tenant-owned tables:

search.documents

search.records

search.queries

search.analytics


Require:

tenant_id UUID NOT NULL
20. Performance Requirements

High-volume tables:

Table	Growth
records	Very High
documents	Very High
queries	High
results	High
21. Index Requirements

Full text:

CREATE INDEX idx_search_vector

ON search.records

USING GIN(search_vector);

Tenant filtering:

CREATE INDEX idx_search_tenant

ON search.records(tenant_id);

Entity lookup:

CREATE INDEX idx_search_entity

ON search.records(entity_type, entity_id);
22. Security Requirements

Required:

Permission-aware search
Tenant isolation
Sensitive data filtering
Audit search activity
23. Future Extensions

Possible additions:

search.ai_query_parser

search.semantic_ranking

search.personalized_results

search.search_agents

search.voice_search

24. Related Documents

Previous:

19_NOTIFICATION_SCHEMA.md

Next:

21_CONFIGURATION_SCHEMA.md
End of Document
# ADR-0006: RAG and Vector Storage Strategy Decision

**Project:** Voice Agent SaaS Platform  
**Document:** Retrieval Augmented Generation and Vector Storage Architecture  
**ADR Number:** ADR-0006  
**Version:** 2.0  
**Status:** Accepted  
**Date:** 2026-07-24


---

# 1. Decision Summary

The Voice Agent SaaS Platform will implement a Retrieval Augmented Generation (RAG) architecture to provide AI agents with accurate, tenant-specific knowledge.

The approved RAG foundation is:


| Capability | Technology |
|---|---|
| Primary database | PostgreSQL |
| Vector storage | PostgreSQL + pgvector |
| Document processing | Dedicated ingestion pipeline |
| Embedding generation | Configurable embedding providers |
| Retrieval layer | RAG Retrieval Service |
| Search strategy | Hybrid semantic + metadata filtering |
| Storage for original files | S3-compatible object storage |


The RAG system will provide:

- Business knowledge retrieval
- Document understanding
- Semantic search
- Agent context enrichment
- Tenant-isolated knowledge access


---

# 2. Context


AI agents require access to business-specific information.

Examples:



Company policies

Product documentation

Pricing information

FAQs

Service procedures

Customer records

Internal knowledge



A standalone LLM does not know private business information.

The platform requires a knowledge architecture that allows each tenant to provide their own information.


---

# 3. Problem Statement


The platform must solve:


## Knowledge Accuracy

Agents must answer using trusted business information.


---

## Tenant Isolation

One company's knowledge must never be accessible by another tenant.


---

## Retrieval Performance

Relevant information must be found quickly during conversations.


---

## Knowledge Management

Businesses need to:

- Upload documents
- Update information
- Remove outdated knowledge
- Monitor usage


---

# 4. RAG Architecture Goals


The RAG system must provide:


## Accuracy

Retrieved information should be:

- Relevant
- Recent
- Tenant-specific


---

## Scalability

Support:

- Thousands of documents
- Multiple tenants
- Large knowledge bases


---

## AI Integration

Support:

- Voice agents
- Chat agents
- Workflow agents


---

## Security

Support:

- Permission control
- Tenant isolation
- Audit logging


---

# 5. Options Considered


---

# Option 1: No RAG


Architecture:



User

|

LLM

|

Response



## Advantages

- Simple
- Low infrastructure


## Disadvantages

- No private knowledge
- Hallucination risk
- Poor business accuracy


## Decision

Rejected.


---

# Option 2: Dedicated Vector Database


Examples:



Pinecone

Weaviate

Milvus



## Advantages

- Specialized vector performance
- Independent scaling


## Disadvantages

- Additional infrastructure
- Additional operational complexity
- Data synchronization challenges


## Decision

Rejected initially.


---

# Option 3: PostgreSQL + pgvector


Architecture:



Documents

|

Chunks

|

Embeddings

|

PostgreSQL + pgvector

|

RAG Retrieval

|

LLM Context



## Advantages

- Single database platform
- Transaction consistency
- Tenant metadata integration
- Simpler operations
- PostgreSQL ecosystem


## Disadvantages

- Requires optimization at very large scale


## Decision

Accepted.


---

# 6. Final RAG Architecture


The platform will implement:


             User Request


                  |


                  v


          RAG Retrieval Service


                  |


    --------------------------------


    |                              |

Metadata Search Vector Search

    |                              |


    --------------------------------


                  |


                  v


         Relevant Knowledge


                  |


                  v


              LLM Context


                  |


                  v


             AI Response


---

# 7. Knowledge Data Flow


Document ingestion:



Document Upload

  |

File Storage

  |

Text Extraction

  |

Document Chunking

  |

Embedding Generation

  |

Vector Storage

  |

Available for Retrieval



---

# 8. Document Storage Strategy


Original files are stored in object storage.


Examples:



PDF

DOCX

TXT

HTML

CSV

Images



Storage:



S3 Compatible Storage



Database stores:


- Document metadata
- File location
- Tenant ownership
- Processing status


---

# 9. Document Processing Pipeline


The ingestion pipeline performs:


## Extraction


Convert documents into usable text.


---

## Cleaning


Remove:

- Formatting noise
- Duplicate content
- Invalid characters


---

## Chunking


Documents are divided into smaller sections.


Example:



Document

|

Chunk 1

Chunk 2

Chunk 3



---

## Embedding Generation


Each chunk receives a vector representation.


Example:



Text

|

Embedding Model

|

Vector



---

# 10. Chunking Strategy


The platform will use configurable chunking.


Factors:


- Document type
- Content length
- Structure
- Retrieval requirements


Chunk metadata includes:



document_id

tenant_id

chunk_number

source

created_at



---

# 11. Embedding Strategy


Embeddings represent meaning rather than exact words.


Used for:


- Semantic search
- Similarity matching
- Knowledge retrieval


The platform supports configurable embedding providers.


---

# 12. Retrieval Strategy


The retrieval layer uses:


## Semantic Search


Finds information based on meaning.


---

## Metadata Filtering


Filters by:


- Tenant
- Agent
- Knowledge source
- Permissions


---

## Hybrid Retrieval


Combines:



Keyword Search

Vector Search



---

# 13. RAG Runtime Flow


During conversation:



User Question

  |

Intent Understanding

  |

Knowledge Retrieval

  |

Context Injection

  |

LLM Generation

  |

Response



---

# 14. Multi-Tenant Knowledge Isolation


Every knowledge object requires:



tenant_id



Example:



knowledge_documents

id

tenant_id

name

status



Retrieval must always include tenant filtering.


---

# 15. Agent Knowledge Assignment


Agents can access assigned knowledge sources.


Example:



Reception Agent

   |

Clinic FAQ Knowledge

   |

Appointment Policies



---

# 16. Memory vs Knowledge Separation


The platform separates:


## Knowledge


Business information.


Examples:

- Policies
- Documents
- FAQs


Storage:


PostgreSQL + pgvector



---

## Memory


Previous interactions.


Examples:

- Customer preferences
- Conversation history


Storage:


Redis

PostgreSQL



---

# 17. Performance Strategy


Optimization includes:


## Vector Indexing


Use pgvector indexes for similarity search.


---

## Metadata Indexing


Index:

- tenant_id
- document_id
- timestamps


---

## Retrieval Limits


Control:

- Number of retrieved chunks
- Context size
- Response latency


---

# 18. Observability Requirements


Track:


## Ingestion Metrics

- Documents processed
- Processing failures
- Processing time


## Retrieval Metrics

- Search latency
- Retrieved chunks
- Relevance scores


## AI Metrics

- Answer quality
- Citation accuracy
- Hallucination rate


---

# 19. Security Considerations


The RAG system requires:


- Tenant isolation
- Access control
- Document permissions
- Secure file storage
- Audit logging


---

# 20. Implementation Rules


## Rule 1

Every knowledge object must belong to a tenant.


---

## Rule 2

Vector search must include authorization filtering.


---

## Rule 3

Original documents are stored outside PostgreSQL.


---

## Rule 4

Embeddings cannot exist without source metadata.


---

## Rule 5

Knowledge updates must trigger re-indexing.


---

# 21. Future Evolution


Future improvements:


- Dedicated vector database
- Advanced reranking models
- Knowledge graphs
- Multimodal retrieval
- Real-time indexing


Major changes require a new ADR.


---

# 22. Related Documents


Architecture:


- 11_RAG_Architecture.md
- 12_Memory_Architecture.md
- 13_Agent_Architecture.md
- ADR-0005_AI_Runtime_Architecture.md


Implementation:


- Knowledge Database Schema
- Embedding Pipeline Design
- Document Processing Service
- Search API Specification


---

# Final Statement


The Voice Agent SaaS Platform will use PostgreSQL with pgvector as the foundation for Retrieval Augmented Generation.

This decision provides:

- Tenant-aware knowledge retrieval
- AI accuracy improvement
- Operational simplicity
- Strong integration with the AI Runtime
- Future scalability path

The RAG system becomes the knowledge layer that enables specialized AI employees to operate reliably across multiple industries.

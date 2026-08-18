# ADR-004: RAG Implementation Strategy

## Status

Accepted

## Context

Agents need access to internal documentation, FAQs, and database structures to answer queries accurately without hallucination.

## Decision

We will implement Retrieval-Augmented Generation (RAG) using:
- **pgvector** as the vector database (leveraging existing PostgreSQL infrastructure).
- **OpenAI text-embedding-3-small** / **Cohere Embed** for document embeddings.
- **Hybrid Search:** Combining semantic similarity scores with keyword BM25 retrieval.

## Consequences

- Reuses existing PostgreSQL database instances (no new database type to maintain).
- Need to implement document chunking, indexing pipeline, and query expansion logic.

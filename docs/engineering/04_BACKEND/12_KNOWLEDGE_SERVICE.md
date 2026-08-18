# 12. Knowledge Service

**Version:** 2.0  
**Status:** Production Ready  
**Owner:** Platform Engineering

---

# 1. Purpose

The Knowledge Service is responsible for managing all knowledge assets that AI agents use during conversations.

It provides:

- Document management
- Knowledge organization
- Chunk storage
- Embedding references
- Versioning
- Retrieval metadata
- Source tracking
- Synchronization status

The Knowledge Service does **not** perform vector search itself.

Vector search is delegated to the Retrieval Service.

---

# 2. Responsibilities

The Knowledge Service manages:

- Knowledge Bases
- Documents
- Files
- Metadata
- Chunks
- Categories
- Tags
- Versions
- Publishing
- Archive lifecycle

---

# 3. High-Level Architecture

```text
                 +-----------------------+
                 | SaaS Dashboard        |
                 +----------+------------+
                            |
                            |
                   Upload Documents
                            |
                            ▼
              +---------------------------+
              | Knowledge Service         |
              +------------+--------------+
                           |
        +------------------+------------------+
        |                  |                  |
        ▼                  ▼                  ▼
 Knowledge DB        Object Storage      Chunk Generator
        |                  |                  |
        +------------------+------------------+
                           |
                           ▼
                 Embedding Pipeline
                           |
                           ▼
                    Retrieval Service
```

---

# 4. Primary Responsibilities

## Knowledge Base Management

Supports:

- Create
- Edit
- Archive
- Delete
- Clone
- Import
- Export

---

## Document Management

Supported formats:

- PDF
- DOCX
- TXT
- Markdown
- HTML
- CSV
- JSON
- XML

---

## Metadata Management

Every document stores:

- Title
- Description
- Owner
- Language
- Category
- Source
- Upload date
- Tags
- Tenant
- Agent visibility

---

## Chunk Management

Each document becomes:

```
Document

    ↓

Chunks

    ↓

Embeddings

    ↓

Indexed
```

---

# 5. Core Database Tables

The Knowledge Service owns:

```
knowledge_bases

knowledge_documents

knowledge_document_versions

knowledge_chunks

knowledge_categories

knowledge_tags

knowledge_document_tags

knowledge_sources

knowledge_sync_jobs

knowledge_import_jobs

knowledge_exports

knowledge_permissions

knowledge_audit
```

---

# 6. Knowledge Base

Represents a logical collection of documents.

Example:

```
Sales KB

Support KB

HR KB

Medical KB

Legal KB

Internal Wiki
```

---

Suggested fields

| Field | Description |
|--------|-------------|
| id | UUID |
| tenant_id | Owner |
| name | KB name |
| description | Description |
| visibility | Private/Public |
| default_language | Primary language |
| created_at | Timestamp |
| updated_at | Timestamp |

---

# 7. Documents

A document belongs to one Knowledge Base.

```
Knowledge Base

      │

      ├── Product Manual.pdf

      ├── FAQ.docx

      ├── Pricing.pdf

      ├── Refund Policy.md

      └── Company Handbook.pdf
```

---

Typical fields

- id
- knowledge_base_id
- filename
- title
- description
- mime_type
- language
- storage_path
- checksum
- uploaded_by
- status

---

# 8. Versioning

Every document supports versions.

```
Employee Handbook

Version 1

Version 2

Version 3

Version 4
```

Old versions remain available.

---

Example

```
knowledge_document_versions

Version

Checksum

Storage path

Created by

Created at

Published

Archived
```

---

# 9. Categories

Categories organize documents.

Example

```
Policies

Products

Sales

Support

Technical

Compliance

Finance

HR
```

---

# 10. Tags

Documents may have multiple tags.

Example

```
pricing

refund

billing

shipping

api

authentication

voice

sip

livekit
```

---

# 11. Chunk Storage

Each processed document becomes chunks.

```
Document

↓

Chunk 1

Chunk 2

Chunk 3

Chunk 4

↓

Embedding
```

Chunks contain:

- text
- order
- page
- token count
- embedding id

---

# 12. Chunk Metadata

Typical metadata

```
Chunk ID

Document ID

Page

Section

Paragraph

Heading

Token Count

Language

Hash

Created At
```

---

# 13. Sources

Knowledge may originate from multiple sources.

Supported sources

- Upload
- Website Crawl
- Git Repository
- API
- Database
- SharePoint
- Confluence
- Notion
- Google Drive
- Dropbox

---

# 14. Import Jobs

Large imports run asynchronously.

Lifecycle

```
Queued

↓

Downloading

↓

Parsing

↓

Chunking

↓

Embedding

↓

Completed
```

---

# 15. Synchronization

External sources periodically synchronize.

Tracks

- last sync
- next sync
- failures
- retries
- deleted files
- updated files

---

# 16. Publishing Workflow

```
Draft

↓

Processing

↓

Ready

↓

Published

↓

Archived
```

Agents only search Published documents.

---

# 17. Permissions

Visibility levels

```
Tenant

↓

Knowledge Base

↓

Document

↓

Section
```

Supported permissions

- Owner
- Editor
- Viewer
- Agent
- API

---

# 18. Audit Trail

Every operation is logged.

Examples

- Document uploaded
- Document deleted
- Version published
- Metadata changed
- Permission updated
- Import completed
- Sync executed

---

# 19. Performance Considerations

Recommended indexes

```
tenant_id

knowledge_base_id

document_id

status

category

language

created_at

updated_at
```

Frequently queried fields should always be indexed.

---

# 20. Storage Strategy

Large files are **not** stored inside PostgreSQL.

Instead:

```
Document Metadata
        │
        ▼
 PostgreSQL

File Binary
        │
        ▼
Object Storage
(S3 / Supabase Storage / GCS)
```

---

# 21. Security

Every request validates

- Tenant ownership
- User permissions
- API scopes
- Object storage authorization

No cross-tenant access is permitted.

---

# 22. Integration Points

The Knowledge Service integrates with:

- Authentication Service
- Tenant Service
- Agent Service
- Storage Service
- Embedding Service
- Retrieval Service
- Audit Service
- Event Bus

---

# 23. Future Enhancements

Planned capabilities

- Auto document summarization
- AI metadata generation
- Duplicate detection
- Semantic document clustering
- Incremental embedding updates
- OCR processing
- Image caption extraction
- Video transcript ingestion
- Audio transcript ingestion
- Automatic language detection
- Knowledge quality scoring

---

# 24. Design Principles

The Knowledge Service follows these principles:

- Multi-tenant by design
- Immutable document versions
- Metadata separated from binary storage
- Event-driven processing
- Horizontal scalability
- Asynchronous ingestion
- Fine-grained permissions
- Complete auditability
- Retrieval-service independence
- Cloud-native storage architecture

---

# 25. Summary

The Knowledge Service is the authoritative system for managing enterprise knowledge used by AI agents. It handles document lifecycle, organization, metadata, versioning, permissions, and ingestion while delegating embedding generation and semantic retrieval to specialized downstream services. This separation enables scalable, maintainable, and production-ready knowledge management for multi-tenant AI platforms.
# API Layer Design

**Module:** 04_BACKEND

**Document:** 04_API_LAYER_DESIGN

**Version:** 2.0

**Status:** Production Ready

---

# Purpose

This document defines the architecture, design principles, standards, and implementation guidelines for the REST API layer of the Voice Agent SaaS Platform.

The API Layer serves as the public interface between clients and the backend services. It is responsible for receiving requests, validating input, authenticating users, authorizing access, invoking business services, and returning standardized responses.

The API layer must remain thin and contain no business logic.

---

# Objectives

The API layer is designed to provide:

- Consistent REST APIs
- Secure request handling
- Versioned endpoints
- Predictable responses
- Stateless communication
- Enterprise-grade scalability
- Standardized validation
- Comprehensive documentation
- Backward compatibility

---

# High-Level Architecture

```
                Client
                   │
                   ▼
             HTTP Request
                   │
                   ▼
             API Gateway
                   │
                   ▼
            Authentication
                   │
                   ▼
            Authorization
                   │
                   ▼
          Request Validation
                   │
                   ▼
            API Controller
                   │
                   ▼
             Business Service
                   │
                   ▼
             Response Model
                   │
                   ▼
             HTTP Response
```

---

# API Responsibilities

The API layer is responsible for:

- Route registration
- Request validation
- Authentication
- Authorization
- Tenant resolution
- DTO conversion
- Service invocation
- Response serialization
- HTTP status codes
- Error translation
- OpenAPI generation

The API layer must never contain:

- Business rules
- Database queries
- SQL
- AI logic
- Workflow execution
- Repository access

---

# REST Design Principles

The platform follows RESTful conventions.

### Resource-Oriented URLs

```
/agents

/users

/conversations

/calls

/workflows

/knowledge
```

Avoid action-based URLs whenever possible.

Preferred:

```
POST /agents
```

Avoid:

```
POST /createAgent
```

---

# API Versioning

Every endpoint belongs to an API version.

Example

```
/api/v1/agents

/api/v1/users

/api/v1/workflows
```

Future versions

```
/api/v2/
```

Versioning strategy is documented separately in:

```
30_API_VERSIONING.md
```

---

# HTTP Methods

## GET

Retrieve resources.

```
GET /agents

GET /agents/{id}
```

Safe and idempotent.

---

## POST

Create resources.

```
POST /agents
```

---

## PUT

Replace an existing resource.

```
PUT /agents/{id}
```

---

## PATCH

Partial update.

```
PATCH /agents/{id}
```

---

## DELETE

Delete or archive resources.

```
DELETE /agents/{id}
```

---

# URL Standards

Good examples

```
/agents

/users

/workflows

/calls/{id}

/knowledge/documents
```

Avoid

```
/GetUsers

/CreateWorkflow

/delete_call
```

Use lowercase.

Use plural nouns.

Avoid verbs.

---

# Request Lifecycle

```
HTTP Request

↓

Router

↓

Authentication

↓

Authorization

↓

Validation

↓

Controller

↓

Service

↓

Repository

↓

Database

↓

Response DTO

↓

JSON Response
```

---

# Request Validation

Validation is handled using Pydantic models.

Validation includes:

- Required fields
- Types
- Length
- Format
- Regex
- Enum values
- Custom validators

Invalid requests return HTTP 422.

---

# Authentication

Supported authentication methods

- JWT
- OAuth2
- API Keys
- Service Accounts

Unauthenticated requests return

```
401 Unauthorized
```

---

# Authorization

Authorization uses RBAC.

Examples

```
Admin

Owner

Manager

Supervisor

Agent

Viewer
```

Forbidden operations return

```
403 Forbidden
```

---

# Tenant Resolution

Every request resolves the tenant context before accessing services.

```
Request

↓

Tenant Resolver

↓

Current Tenant

↓

Business Service
```

No request proceeds without tenant resolution unless explicitly public.

---

# Controller Responsibilities

Controllers should:

- Receive request
- Validate DTO
- Invoke service
- Return response

Controllers should never:

- Execute SQL
- Perform business calculations
- Access Redis
- Publish events
- Call external APIs directly

---

# Response Format

Successful responses follow a consistent structure.

```json
{
  "success": true,
  "data": {},
  "meta": {
    "request_id": "...",
    "timestamp": "..."
  }
}
```

---

# Error Response

Standard error format

```json
{
  "success": false,
  "error": {
    "code": "AGENT_NOT_FOUND",
    "message": "Requested agent does not exist."
  },
  "meta": {
    "request_id": "...",
    "timestamp": "..."
  }
}
```

Never expose internal exception details.

---

# Pagination

Large collections use pagination.

Example

```
GET /agents?page=1&page_size=25
```

Response

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 25,
    "total_items": 540,
    "total_pages": 22
  }
}
```

---

# Filtering

Example

```
GET /agents?status=active
```

Multiple filters

```
GET /calls?status=completed&agent_id=123
```

---

# Sorting

```
GET /calls?sort=created_at
```

Descending

```
GET /calls?sort=-created_at
```

---

# Searching

```
GET /knowledge/search?q=insurance
```

Search implementation belongs in the service layer.

---

# Idempotency

Critical POST endpoints should support an idempotency key.

Header

```
Idempotency-Key
```

Used for:

- Billing
- Payments
- Call creation
- Workflow execution
- External integrations

---

# File Uploads

Uploads use multipart requests.

Supported resources

- Knowledge documents
- Voice recordings
- CSV imports
- Images
- Attachments

Files are stored outside the application server.

---

# API Documentation

Every endpoint must include:

- Summary
- Description
- Tags
- Parameters
- Request schema
- Response schema
- Error responses
- Security requirements
- Examples

OpenAPI documentation is generated automatically.

---

# Rate Limiting

Rate limits are applied based on:

- Tenant
- User
- API Key
- IP Address

Example

```
100 requests/minute
```

Exceeded limits return

```
429 Too Many Requests
```

---

# Observability

Every request records:

- Request ID
- Correlation ID
- Tenant ID
- User ID
- Client IP
- Duration
- Response Status
- Endpoint
- HTTP Method

---

# Security Headers

Responses include standard security headers such as:

- Strict-Transport-Security
- Content-Security-Policy
- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy

---

# Performance Guidelines

Controllers should:

- Return DTOs only
- Avoid unnecessary serialization
- Stream large responses when appropriate
- Never block on long-running tasks
- Delegate background work to workers

---

# API Folder Structure

```
api/

├── v1/
│   ├── auth.py
│   ├── users.py
│   ├── tenants.py
│   ├── agents.py
│   ├── voice.py
│   ├── calls.py
│   ├── conversations.py
│   ├── knowledge.py
│   ├── rag.py
│   ├── memory.py
│   ├── workflows.py
│   ├── integrations.py
│   ├── billing.py
│   └── notifications.py
│
└── dependencies.py
```

---

# Related Documents

- 01_BACKEND_ARCHITECTURE.md
- 02_FASTAPI_APPLICATION_STRUCTURE.md
- 03_BACKEND_SERVICE_DESIGN.md
- 05_AUTHENTICATION_AUTHORIZATION.md
- 30_API_VERSIONING.md

---

# Summary

The API layer provides a secure, standardized, and versioned interface to the Voice Agent SaaS Platform. It is intentionally thin, focusing on HTTP concerns while delegating all business logic to the service layer. Consistent routing, validation, authentication, authorization, and response formats ensure maintainability, scalability, and an excellent developer experience for both internal teams and external API consumers.
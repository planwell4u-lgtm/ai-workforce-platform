# 20 Data Fetching Strategy

**Version:** 2.0  
**Status:** Production Architecture  
**Owner:** Frontend Engineering

---

# 1. Purpose

This document defines the frontend data fetching architecture for the Voice Agent SaaS Platform.

The data fetching strategy provides a consistent approach for communicating with backend services, managing server state, caching data, handling synchronization, and optimizing application performance.

The architecture supports:

- REST API communication
- Real-time updates
- Server state management
- Cache management
- Pagination
- Optimistic updates
- Error recovery

---

# 2. Data Fetching Goals

The frontend data layer provides:

- Predictable API communication
- Efficient caching
- Reduced network requests
- Consistent loading states
- Reliable synchronization
- Scalable application growth

---

# 3. Data Architecture Overview

```
                    React Components

                            │

                            ▼

                    Feature Hooks

                            │

        ┌───────────────────┼───────────────────┐

        ▼                   ▼                   ▼

 TanStack Query        Zustand Store       API Client

        │                   │                   │

        └───────────────────┼───────────────────┘

                            │

                            ▼

                    FastAPI Backend

                            │

                            ▼

                    Database Services
```

---

# 4. Data Categories

Frontend data is divided into three categories.

---

# Server State

Data owned by backend systems.

Examples:

- Agents
- Calls
- Conversations
- Knowledge documents
- Workflows
- Billing information

Managed by:

```
TanStack Query
```

---

# Client State

Temporary UI state.

Examples:

- Modal visibility
- Selected filters
- Theme
- Form drafts

Managed by:

```
Zustand
```

---

# Realtime State

Live changing information.

Examples:

- Call status
- Agent state
- Transcripts
- Workflow execution

Managed by:

```
WebSocket Store
```

---

# 5. Technology Stack

| Purpose | Technology |
|---|---|
| API State | TanStack Query |
| HTTP Client | Fetch / Axios Wrapper |
| Client State | Zustand |
| Validation | Zod |
| Realtime | WebSocket + LiveKit |
| Type Safety | TypeScript |

---

# 6. API Client Architecture

All backend communication goes through a centralized API client.

Structure:

```
src/

lib/

api/

├── client.ts

├── endpoints.ts

├── interceptors.ts

└── errors.ts
```

---

# 7. API Client Responsibilities

The API client handles:

- Base URL configuration
- Authentication headers
- Request formatting
- Response parsing
- Error normalization
- Request tracing

---

# 8. Request Flow

```
Component

↓

Feature Hook

↓

API Client

↓

FastAPI Endpoint

↓

Backend Service

↓

Database
```

---

# 9. Feature-Based Data Architecture

Data logic is organized by domain.

Example:

```
features/

agents/

├── api.ts

├── hooks.ts

├── types.ts

└── schemas.ts
```

---

# 10. Query Architecture

Queries retrieve backend data.

Example:

```
useAgents()

        ↓

TanStack Query

        ↓

GET /agents

        ↓

Agent Service
```

---

# 11. Query Key Strategy

Query keys follow a predictable structure.

Example:

```ts
[
  "agents",
  tenantId,
  filters
]
```

Benefits:

- Cache separation
- Easier invalidation
- Better debugging

---

# 12. Cache Management

Caching reduces unnecessary requests.

Cached data:

- Agent lists
- User profiles
- Knowledge sources
- Configuration data

---

Cache strategy:

```
Request

↓

Check Cache

↓

Return Cached Data

↓

Background Refresh
```

---

# 13. Cache Invalidation

Data is invalidated after mutations.

Example:

```
Create Agent

↓

Invalidate:

agents.list

↓

Fetch Updated Data
```

---

# 14. Mutation Architecture

Mutations handle data changes.

Examples:

- Create agent
- Update workflow
- Upload document
- Delete memory

Flow:

```
User Action

↓

Mutation Hook

↓

API Request

↓

Backend Update

↓

Cache Update
```

---

# 15. Optimistic Updates

For fast user experience.

Example:

```
User Changes Setting

↓

Update UI Immediately

↓

Send Request

↓

Confirm Change

↓

Rollback If Failed
```

---

# 16. Loading State Architecture

All async operations provide:

- Initial loading
- Background loading
- Submitting state
- Refresh state

Example:

```
Loading Agents...

Displaying Cached Data

Refreshing...
```

---

# 17. Error State Architecture

Errors are standardized.

Types:

```
Network Error

Authentication Error

Permission Error

Validation Error

Server Error
```

---

# 18. Pagination Strategy

Large datasets use pagination.

Examples:

- Calls
- Conversations
- Documents
- Audit logs

Supported methods:

```
Offset Pagination

Cursor Pagination
```

---

# 19. Infinite Loading

For large lists:

```
Load First Page

↓

Scroll

↓

Load Next Page

↓

Append Results
```

---

# 20. Search and Filtering

Search requests should support:

- Debouncing
- Server-side filtering
- Query synchronization

Example:

```
Search Input

↓

Debounce

↓

API Request

↓

Update Results
```

---

# 21. Realtime Synchronization

Realtime updates synchronize with server state.

Example:

```
WebSocket Event

↓

Update Store

↓

Invalidate Query

↓

Refresh Data
```

---

# 22. Data Prefetching

The application preloads expected data.

Examples:

- Dashboard widgets
- Agent details
- Workflow editor data

Flow:

```
User Intent

↓

Prefetch

↓

Instant Navigation
```

---

# 23. Server Component Data Fetching

Next.js Server Components may fetch:

- Initial page data
- Static configuration
- SEO content

Client Components handle:

- Interactive data
- User actions
- Realtime updates

---

# 24. Authentication Integration

Every API request includes:

```
Authorization Header

Tenant Context

Request ID
```

---

# 25. Multi-Tenant Data Handling

Frontend requests always operate within:

```
User

↓

Tenant

↓

Workspace

↓

Resource
```

Tenant isolation remains enforced by backend services.

---

# 26. Data Fetching Security

The frontend must:

- Avoid exposing secrets
- Validate responses
- Handle expired sessions
- Protect sensitive information

---

# 27. Performance Optimization

Strategies:

- Query caching
- Request deduplication
- Pagination
- Prefetching
- Lazy loading
- Background refresh

---

# 28. Testing Strategy

## Unit Testing

Test:

- Query hooks
- API functions
- Data transformations

---

## Integration Testing

Test:

- API communication
- Cache behavior
- Error states

---

## End-to-End Testing

Example:

```
Open Dashboard

↓

Load Agents

↓

Update Agent

↓

Verify Refresh
```

---

# 29. Data Fetching Standards

All frontend data access should:

- Use centralized API clients
- Use TanStack Query for server state
- Separate UI state from server state
- Handle loading and errors
- Support realtime synchronization
- Maintain type safety

---

# 30. Future Expansion

The architecture supports:

- GraphQL integration
- Offline support
- Edge caching
- Advanced synchronization
- Mobile clients

---

# 31. Summary

The Data Fetching Strategy defines how the Voice Agent SaaS Platform frontend communicates with backend services.

By separating server state, client state, and realtime state while using caching, synchronization, and type-safe API patterns, the frontend achieves scalability, reliability, and high performance. 
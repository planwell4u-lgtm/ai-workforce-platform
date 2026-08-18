# 06 State Management Architecture

**Version:** 2.0  
**Status:** Production Architecture  
**Owner:** Frontend Engineering

---

# 1. Purpose

This document defines the state management architecture for the Voice Agent SaaS Platform frontend.

The state management strategy establishes how application data is:

- Stored
- Retrieved
- Updated
- Cached
- Synchronized
- Shared across components

The architecture separates different types of state to maintain scalability and performance.

---

# 2. State Management Goals

The frontend state architecture provides:

- Predictable state handling
- Minimal unnecessary re-renders
- Clear ownership of data
- Efficient API synchronization
- Real-time updates
- Maintainable application logic

---

# 3. State Management Philosophy

The application follows:

```
Use the right state tool for the right problem
```

Not all data belongs in global state.

State is classified into:

```
Server State

        ↓

Client Application State

        ↓

Component Local State

        ↓

URL State
```

---

# 4. State Architecture Overview

```
                    Application State

                           │

        ┌──────────────────┼──────────────────┐

        ▼                  ▼                  ▼

 Server State        Client State       Local State

        │                  │                  │

        ▼                  ▼                  ▼

TanStack Query       Zustand            React State


                           │

                           ▼

                    UI Components
```

---

# 5. State Categories

The frontend manages four categories of state.

---

# 5.1 Server State

Server state represents backend-owned data.

Examples:

- Users
- Tenants
- AI agents
- Conversations
- Calls
- Knowledge bases
- Billing information

Technology:

```
TanStack Query
```

---

# 5.2 Client Application State

Client state represents frontend-controlled application data.

Examples:

- Sidebar state
- Theme preference
- UI preferences
- Active workspace
- Builder configuration

Technology:

```
Zustand
```

---

# 5.3 Component Local State

Temporary state owned by individual components.

Examples:

- Modal open state
- Form input values
- Dropdown selection
- Temporary UI interaction

Technology:

```
React useState
```

---

# 5.4 URL State

State represented in the URL.

Examples:

- Search filters
- Pagination
- Selected tabs
- Sorting

Benefits:

- Shareable URLs
- Browser navigation support
- Better user experience

---

# 6. TanStack Query Architecture

TanStack Query manages communication with backend services.

Responsibilities:

- Data fetching
- Cache management
- Background updates
- Request deduplication
- Retry handling
- Synchronization

---

Architecture:

```
React Component

        │

        ▼

Query Hook

        │

        ▼

API Service

        │

        ▼

FastAPI Backend
```

---

# 7. Query Organization

Queries are organized by domain.

Example:

```
features/

agents/

├── queries/

│   ├── useAgents.ts

│   └── useAgent.ts
```

---

Example:

```typescript
useAgent(agentId)
```

Provides:

- Agent data
- Loading state
- Error handling
- Cache management

---

# 8. Query Key Strategy

Query keys must follow a consistent pattern.

Example:

```typescript
[
 "agents",
 agentId
]
```

Examples:

```
agents

agents:list

agents:123

conversations:123

knowledge:sources
```

---

# 9. Cache Strategy

Caching depends on data type.

## Static Data

Examples:

- Configuration
- Templates

Strategy:

Long cache duration

---

## Dynamic Data

Examples:

- Calls
- Active sessions

Strategy:

Short cache duration

---

## Real-Time Data

Examples:

- Voice sessions
- Live events

Strategy:

WebSocket updates

---

# 10. Zustand Architecture

Zustand manages client-side application state.

Used for:

- UI state
- Temporary workflows
- Complex interactions

---

Example stores:

```
stores/

├── auth-store.ts

├── ui-store.ts

├── agent-builder-store.ts

├── voice-session-store.ts

└── workspace-store.ts
```

---

# 11. Global State Rules

Global state should contain only shared application concerns.

Good examples:

```
Current Tenant

Theme

User Preferences

Active Voice Session
```

---

Avoid storing:

```
API Response Data

Tables

Lists

Server Resources
```

These belong in:

```
TanStack Query
```

---

# 12. Agent Builder State Architecture

The AI Agent Builder requires complex temporary state.

Example:

```
Agent Builder

        │

        ├── Identity

        ├── Instructions

        ├── Voice

        ├── Tools

        ├── Knowledge

        └── Workflow
```

Managed by:

```
Zustand
```

until saved.

---

# 13. Voice Session State

Real-time voice state requires special handling.

Examples:

- Connection status
- Active participant
- Audio state
- Transcript state
- Agent status

Architecture:

```
LiveKit Events

        ↓

Voice Store

        ↓

React Components
```

---

# 14. Authentication State

Authentication state includes:

- Current user
- Tenant
- Permissions
- Session status

Managed through:

```
Auth Provider

+

Secure Session Handling
```

---

# 15. Form State Management

Forms use:

```
React Hook Form

+

Zod Validation
```

Responsibilities:

- Input state
- Validation
- Submission handling
- Error display

---

Example:

```
Agent Configuration Form

        ↓

Validation Schema

        ↓

API Mutation

        ↓

Query Refresh
```

---

# 16. Mutation Architecture

Changes to backend data use mutations.

Examples:

- Create agent
- Update settings
- Upload documents
- Start workflow

Flow:

```
User Action

↓

Mutation

↓

Backend API

↓

Cache Update

↓

UI Refresh
```

---

# 17. Real-Time State Synchronization

Real-time updates use:

- WebSockets
- LiveKit events
- Server events

Example:

```
Call Started

↓

Backend Event

↓

WebSocket

↓

Frontend Store

↓

UI Update
```

---

# 18. State Persistence

Persistent state includes:

- User preferences
- Theme
- Workspace selection

Storage options:

- Cookies
- Secure browser storage
- Backend persistence

Sensitive data must not be stored in local storage.

---

# 19. Error Handling Strategy

State systems handle:

## Loading

```
isLoading
```

## Errors

```
error
```

## Empty Data

```
empty state
```

## Retry

```
refetch
```

---

# 20. Performance Guidelines

State management should:

- Keep stores small
- Avoid unnecessary subscriptions
- Normalize complex state
- Prefer server state caching
- Avoid duplicate data storage

---

# 21. Testing Strategy

State should be tested through:

## Query Tests

Verify:

- Fetching
- Caching
- Error handling

---

## Store Tests

Verify:

- State updates
- Actions
- Reset behavior

---

## Integration Tests

Verify:

- Complete user workflows

---

# 22. State Management Rules

The frontend follows:

- Server data belongs to TanStack Query
- UI state belongs to Zustand
- Temporary state belongs to components
- URL state belongs in routing
- Real-time state follows event architecture

---

# 23. Summary

The State Management Architecture provides a scalable approach for managing frontend data across the Voice Agent SaaS Platform.

By separating server state, client state, component state, and URL state, the frontend remains predictable, performant, and ready to support complex SaaS workflows, AI agent configuration, and real-time voice experiences.
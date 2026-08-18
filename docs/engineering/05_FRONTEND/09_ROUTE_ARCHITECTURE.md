# 09 Frontend Routing Architecture

**Version:** 2.0  
**Status:** Production Architecture  
**Owner:** Frontend Engineering

---

# 1. Purpose

This document defines the routing architecture for the Voice Agent SaaS Platform frontend.

The routing system establishes:

- Application navigation structure
- Route organization
- Authentication boundaries
- Tenant-aware routing
- Dynamic resource routing
- Loading and error handling
- Scalable page organization

The architecture uses the Next.js App Router.

---

# 2. Routing Goals

The routing architecture provides:

- Clear navigation structure
- Secure route protection
- Scalable application growth
- Better user experience
- Deep linking support
- Consistent URL patterns

---

# 3. Routing Architecture Overview

```
                    Browser Request

                           │

                           ▼

                   Next.js Router

                           │

             ┌─────────────┼─────────────┐

             ▼             ▼             ▼

        Public Routes  Auth Routes  Protected Routes

             │             │             │

             └─────────────┼─────────────┘

                           │

                           ▼

                    Application Pages

                           │

                           ▼

                    Feature Components
```

---

# 4. Next.js App Router

The application uses:

```
Next.js App Router
```

Benefits:

- Nested layouts
- Server components
- Streaming
- Route groups
- Better organization
- Built-in loading/error handling

---

# 5. Route Organization

The frontend routes are organized by application domain.

Recommended:

```
app/

├── (marketing)/

├── (auth)/

├── (dashboard)/

├── api/

├── layout.tsx

├── loading.tsx

├── error.tsx

└── not-found.tsx
```

---

# 6. Public Routes

Public routes do not require authentication.

Examples:

```
/

 /pricing

 /features

 /documentation

 /login

 /register
```

Used for:

- Marketing pages
- Account creation
- Public resources

---

# 7. Authentication Routes

Authentication routes handle user identity flows.

Structure:

```
app/

(auth)/

├── login/

│   └── page.tsx


├── register/

│   └── page.tsx


├── forgot-password/

│   └── page.tsx


└── verify-email/

    └── page.tsx
```

---

# 8. Protected Dashboard Routes

Main SaaS application routes are protected.

Structure:

```
app/

(dashboard)/

├── dashboard/

├── agents/

├── calls/

├── conversations/

├── knowledge/

├── workflows/

├── integrations/

├── billing/

└── settings/
```

---

# 9. Dashboard Layout Architecture

Protected routes share a common layout.

```
Dashboard Layout

        │

        ├── Sidebar

        ├── Header

        ├── Tenant Selector

        ├── User Menu

        └── Page Content
```

---

# 10. Agent Routing

AI agents are a primary product resource.

Route structure:

```
/agents

/agents/new

/agents/[agentId]

/agents/[agentId]/settings

/agents/[agentId]/knowledge

/agents/[agentId]/testing
```

---

Example:

```
/agents/123/settings
```

represents:

```
Agent ID:

123

Section:

Settings
```

---

# 11. Call Management Routing

Voice calls require dedicated routes.

Structure:

```
/calls

/calls/[callId]

/calls/[callId]/transcript

/calls/[callId]/recording
```

Used for:

- Call history
- Live monitoring
- Transcript review
- Analytics

---

# 12. Conversation Routing

Conversation management:

```
/conversations

/conversations/[conversationId]
```

Supports:

- Chat history
- Voice transcripts
- Agent interactions

---

# 13. Knowledge Base Routing

Knowledge management routes:

```
/knowledge

/knowledge/sources

/knowledge/documents

/knowledge/search
```

Supports:

- Document uploads
- RAG configuration
- Search testing

---

# 14. Workflow Builder Routing

Workflow interfaces:

```
/workflows

/workflows/new

/workflows/[workflowId]

/workflows/[workflowId]/editor
```

Used for:

- Agent workflows
- Automation
- Tool orchestration

---

# 15. Billing Routing

Billing pages:

```
/billing

/billing/plans

/billing/usage

/billing/invoices
```

---

# 16. Settings Routing

Settings are organized by category.

```
/settings

/settings/profile

/settings/security

/settings/team

/settings/api-keys

/settings/integrations
```

---

# 17. Dynamic Routes

Dynamic resources use Next.js parameters.

Example:

```
[agentId]
```

Maps to:

```
params.agentId
```

---

Example:

```
app/agents/[agentId]/page.tsx
```

---

# 18. Tenant-Aware Routing

The platform supports multi-tenant operations.

Possible structures:

## Option A

Tenant from session:

```
/agents
```

Backend determines tenant.

---

## Option B

Tenant in URL:

```
/workspace/[tenantId]/agents
```

---

Recommended:

Use session-based tenant context with optional workspace URLs for enterprise environments.

---

# 19. Navigation Architecture

Navigation is role-aware.

Example:

```
Sidebar

├── Dashboard

├── Agents

├── Calls

├── Knowledge

├── Workflows

├── Analytics

├── Billing

└── Settings
```

---

# 20. Route Permissions

Routes should define required permissions.

Example:

```
/billing

Requires:

billing.view
```

---

Permission flow:

```
Route Request

↓

Authentication Check

↓

Permission Check

↓

Allow Access
```

---

# 21. Loading Architecture

Each major route can define:

```
loading.tsx
```

Example:

```
agents/

├── page.tsx

├── loading.tsx

└── error.tsx
```

---

Loading states provide:

- Skeleton UI
- Better perceived performance
- Smooth transitions

---

# 22. Error Handling

Routes support:

```
error.tsx
```

Responsibilities:

- Catch rendering errors
- Display recovery UI
- Log failures

---

# 23. Not Found Handling

Global:

```
app/not-found.tsx
```

Used for:

- Invalid routes
- Missing resources
- Deleted entities

---

# 24. URL Design Standards

URLs should be:

- Human readable
- Predictable
- Stable

Good:

```
/agents/123/settings
```

Avoid:

```
/page?id=123&type=settings
```

---

# 25. Route Metadata

Routes should define:

- Page titles
- Descriptions
- Open Graph data

Example:

```
Agent Settings

↓

Voice Agent Configuration
```

---

# 26. Route Performance Strategy

Routing performance uses:

- Server components
- Prefetching
- Streaming
- Dynamic imports
- Lazy loading

---

# 27. Testing Strategy

Routing tests include:

## Unit Tests

- Route helpers
- Permission checks

---

## Integration Tests

- Navigation flows

---

## End-to-End Tests

Example:

```
Login

↓

Open Agents

↓

Create Agent

↓

Configure Voice

↓

Publish
```

---

# 28. Routing Security Rules

Routes must:

- Validate authentication
- Validate permissions
- Avoid exposing sensitive data
- Handle unauthorized access

---

# 29. Future Expansion

The routing architecture supports:

- Mobile applications
- Enterprise workspaces
- White-label portals
- Additional AI modules
- Plugin interfaces

---

# 30. Summary

The Frontend Routing Architecture defines how users navigate and interact with the Voice Agent SaaS Platform.

Using Next.js App Router patterns, protected route groups, tenant-aware design, and domain-based navigation, the frontend provides a scalable foundation for enterprise AI SaaS experiences.
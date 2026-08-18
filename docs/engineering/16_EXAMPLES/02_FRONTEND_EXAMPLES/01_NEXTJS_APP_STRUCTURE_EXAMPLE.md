# 01 Nextjs App Structure Example
# Next.js App Structure Example

**Version:** 2.0

---

# 1. Overview

This document defines the recommended project structure for frontend applications built with **Next.js App Router** in the Voice Agent SaaS platform.

The objective is to provide a scalable, maintainable, and production-ready architecture that supports:

- Multi-tenant SaaS
- Authentication
- AI Agent Management
- Voice Platform
- Real-time updates
- Workflow Builder
- RAG Knowledge Base
- Memory Management
- Administration
- Billing
- Monitoring

This serves as the reference architecture for all frontend applications.

---

# 2. Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | Next.js 15+ (App Router) |
| Language | TypeScript |
| UI Library | React 19 |
| Styling | Tailwind CSS |
| Components | shadcn/ui |
| State | Zustand |
| Server State | TanStack Query |
| Forms | React Hook Form |
| Validation | Zod |
| Authentication | JWT / OAuth2 |
| Charts | Recharts |
| Real-time | WebSocket / LiveKit |
| Testing | Vitest + Playwright |

---

# 3. High-Level Architecture

```
Browser
   │
   ▼
Next.js App Router
   │
   ├───────────────┐
   │               │
Server Components  Client Components
   │               │
   └───────┬───────┘
           ▼
      API Client Layer
           │
           ▼
      Backend Services
```

---

# 4. Recommended Directory Structure

```text
frontend/

├── app/
│   ├── (auth)/
│   ├── (dashboard)/
│   ├── agents/
│   ├── calls/
│   ├── workflows/
│   ├── knowledge/
│   ├── memory/
│   ├── analytics/
│   ├── billing/
│   ├── settings/
│   ├── admin/
│   ├── api/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── loading.tsx
│   ├── error.tsx
│   └── not-found.tsx
│
├── components/
│   ├── ui/
│   ├── layout/
│   ├── common/
│   ├── forms/
│   ├── tables/
│   ├── charts/
│   ├── voice/
│   ├── agents/
│   ├── workflows/
│   └── knowledge/
│
├── features/
│   ├── auth/
│   ├── agents/
│   ├── calls/
│   ├── workflows/
│   ├── memory/
│   ├── rag/
│   └── billing/
│
├── hooks/
├── lib/
├── services/
├── stores/
├── types/
├── utils/
├── styles/
├── public/
└── tests/
```

---

# 5. App Router Organization

Use route groups to organize features.

```text
app/

(auth)
    login/
    register/
    forgot-password/

(dashboard)
    dashboard/
    agents/
    calls/
    workflows/
    knowledge/
    memory/
    analytics/
    billing/
    settings/
```

Benefits:

- Shared layouts
- Cleaner routing
- Logical separation
- Better maintainability

---

# 6. Component Organization

Components should be grouped by responsibility.

```text
components/

ui/
    button.tsx
    input.tsx
    dialog.tsx

layout/
    sidebar.tsx
    navbar.tsx
    footer.tsx

voice/
    call-controls.tsx
    transcript.tsx

agents/
    agent-card.tsx
    agent-editor.tsx
```

Guidelines:

- Reusable UI belongs in `ui/`
- Feature-specific components stay within their domain
- Avoid deeply nested component trees

---

# 7. Feature-Based Organization

Each feature should encapsulate its own logic.

Example:

```text
features/

agents/

    api/

    hooks/

    components/

    schemas/

    types/

    utils/
```

Advantages:

- Clear ownership
- Reduced coupling
- Easier testing
- Better scalability

---

# 8. Shared Libraries

Recommended contents of `lib/`:

```text
lib/

api-client.ts

auth.ts

logger.ts

permissions.ts

date.ts

constants.ts

env.ts
```

These modules should remain framework-independent where possible.

---

# 9. Service Layer

API communication should be centralized.

```text
services/

agent-service.ts

call-service.ts

workflow-service.ts

knowledge-service.ts

billing-service.ts
```

Responsibilities:

- HTTP requests
- Response mapping
- Error handling
- Authentication headers
- Retry logic

---

# 10. State Management

Separate state by purpose.

| State Type | Recommended Solution |
|------------|----------------------|
| UI State | Zustand |
| Server State | TanStack Query |
| Form State | React Hook Form |
| URL State | Next.js Router |

Avoid duplicating server state inside client stores.

---

# 11. Authentication Structure

```text
(auth)

login/

logout/

forgot-password/

reset-password/

verify-email/
```

Authentication should support:

- JWT
- Refresh tokens
- Role-based navigation
- Tenant-aware routing

---

# 12. Layout Hierarchy

```
Root Layout

      │

Authentication Layout

      │

Dashboard Layout

      │

Feature Layout

      │

Page

      │

Components
```

Shared navigation, themes, and providers should be defined in layouts.

---

# 13. Environment Configuration

Example:

```text
.env.local

NEXT_PUBLIC_API_URL=

NEXT_PUBLIC_WS_URL=

NEXT_PUBLIC_LIVEKIT_URL=
```

Never expose secrets through `NEXT_PUBLIC_*` variables.

---

# 14. Testing Structure

```text
tests/

unit/

integration/

e2e/

fixtures/
```

Recommended tools:

- Vitest
- React Testing Library
- Playwright

---

# 15. Performance Guidelines

Use:

- Server Components by default
- Client Components only when necessary
- Dynamic imports for large modules
- Image optimization
- Route-based code splitting
- Streaming and Suspense where appropriate

---

# 16. Security Considerations

Frontend should:

- Never store secrets
- Sanitize user input
- Protect against XSS
- Validate permissions
- Handle token expiration
- Use secure cookies when applicable

---

# 17. Coding Standards

Recommended practices:

- Strict TypeScript
- Functional components
- Named exports
- ESLint + Prettier
- Feature-first organization
- Small reusable components
- Clear file naming conventions

---

# 18. Example Feature Flow

```
User

 │

 ▼

Dashboard

 │

 ▼

Agent List

 │

 ▼

Agent Details

 │

 ▼

Agent Editor

 │

 ▼

API Client

 │

 ▼

Backend
```

---

# 19. Best Practices

Always:

- Keep components small
- Co-locate related files
- Reuse shared UI
- Centralize API logic
- Separate client and server concerns
- Prefer composition over inheritance

Avoid:

- Large monolithic pages
- Business logic inside components
- Direct API calls from UI elements
- Global state for local concerns
- Circular dependencies

---

# 20. Summary

This Next.js App Structure provides a scalable foundation for the Voice Agent SaaS frontend. By combining feature-based organization, the App Router, shared UI components, centralized services, and modern React patterns, the frontend remains maintainable, testable, and ready for enterprise-scale development.
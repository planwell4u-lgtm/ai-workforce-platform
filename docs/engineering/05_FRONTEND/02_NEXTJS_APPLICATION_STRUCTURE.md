# 02 Next.js Application Structure

**Version:** 2.0  
**Status:** Production Architecture  
**Owner:** Frontend Engineering

---

# 1. Purpose

This document defines the Next.js application structure for the Voice Agent SaaS Platform frontend.

The goal is to establish a scalable application organization that supports:

- Enterprise SaaS dashboards
- AI agent management
- Real-time voice interfaces
- Multi-tenant applications
- Feature-based development
- Long-term maintainability

The frontend uses the Next.js App Router architecture with React Server Components and Client Components.

---

# 2. Application Architecture Goals

The Next.js application structure provides:

- Clear separation of responsibilities
- Scalable routing architecture
- Feature ownership
- Reusable components
- Secure authentication boundaries
- Optimized rendering strategy
- Production deployment readiness

---

# 3. Next.js Architecture Overview

The application follows:

```
                    Browser

                       │

                       ▼

                Next.js Application

                       │

        ┌──────────────┼──────────────┐

        ▼              ▼              ▼

     App Router     Components     Features

        │              │              │

        ▼              ▼              ▼

     Pages          UI System     Business Logic

                       │

                       ▼

                API Integration Layer

                       │

                       ▼

                Backend Platform
```

---

# 4. Recommended Project Structure

Production structure:

```
frontend/

├── app/
│
│   ├── (auth)/
│   │
│   ├── (dashboard)/
│   │
│   ├── api/
│   │
│   ├── layout.tsx
│   │
│   ├── loading.tsx
│   │
│   ├── error.tsx
│   │
│   └── not-found.tsx
│
├── components/
│
│   ├── ui/
│   │
│   ├── layouts/
│   │
│   └── shared/
│
├── features/
│
│   ├── agents/
│   │
│   ├── voice/
│   │
│   ├── conversations/
│   │
│   ├── knowledge/
│   │
│   ├── workflows/
│   │
│   └── billing/
│
├── services/
│
│   ├── api/
│   │
│   ├── websocket/
│   │
│   └── livekit/
│
├── stores/
│
├── hooks/
│
├── schemas/
│
├── types/
│
├── utils/
│
├── config/
│
├── providers/
│
├── styles/
│
├── public/
│
├── tests/
│
└── package.json
```

---

# 5. App Router Structure

The application uses Next.js App Router.

Example:

```
app/

├── layout.tsx

├── page.tsx

├── dashboard/

│   └── page.tsx

├── agents/

│   ├── page.tsx

│   ├── new/

│   │   └── page.tsx

│   └── [agentId]/

│       └── page.tsx
```

---

# 6. Route Groups

Route groups organize application sections without affecting URLs.

Example:

```
app/

├── (auth)/

│   ├── login/

│   └── register/


├── (dashboard)/

│   ├── dashboard/

│   ├── agents/

│   ├── calls/

│   └── settings/
```

Benefits:

- Separate layouts
- Cleaner organization
- Authentication boundaries

---

# 7. Layout Architecture

Layouts define shared application structures.

Example:

```
Root Layout

        │

        ▼

Dashboard Layout

        │

        ▼

Feature Page

        │

        ▼

Components
```

---

## Root Layout

Responsibilities:

- Global styles
- Providers
- Fonts
- Metadata

---

## Dashboard Layout

Responsibilities:

- Navigation
- Sidebar
- Header
- Tenant context
- User menu

---

# 8. Server Components Strategy

Server Components are the default.

Used for:

- Initial page rendering
- Data fetching
- Static content
- SEO metadata

Example:

```tsx
export default async function Page() {

  const agents = await getAgents();

  return (
    <AgentList data={agents}/>
  );
}
```

---

# 9. Client Components Strategy

Client Components are used only when required.

Examples:

- Interactive forms
- Voice controls
- Real-time updates
- Browser APIs
- Animations

Example:

```tsx
"use client"

export function VoiceButton(){

}
```

---

# 10. Component Boundary Rules

Recommended approach:

```
Server Component

        │

        ▼

Client Component

        │

        ▼

Interactive Logic
```

Avoid converting entire pages into Client Components.

---

# 11. Feature-Based Organization

Business features own their logic.

Example:

```
features/

agents/

├── components/

├── hooks/

├── services/

├── schemas/

├── types/

└── utils/
```

Benefits:

- Easier scaling
- Clear ownership
- Reduced coupling

---

# 12. Component Organization

Components are divided into three categories.

---

## UI Components

Reusable primitives.

Examples:

- Button
- Modal
- Table
- Input

Location:

```
components/ui
```

---

## Shared Components

Application-wide components.

Examples:

- Header
- Sidebar
- Navigation
- Empty states

Location:

```
components/shared
```

---

## Feature Components

Domain-specific components.

Examples:

- Agent Builder
- Voice Console
- Workflow Editor

Location:

```
features/
```

---

# 13. Provider Architecture

Global providers are centralized.

Example:

```
providers/

├── QueryProvider.tsx

├── AuthProvider.tsx

├── ThemeProvider.tsx

└── LiveKitProvider.tsx
```

---

Providers handle:

- Application state
- Authentication
- Theme
- API clients
- Real-time connections

---

# 14. Middleware Architecture

Next.js middleware handles:

- Authentication checks
- Route protection
- Tenant routing
- Request processing

Example:

```
Request

↓

Middleware

↓

Authentication

↓

Route Access
```

---

# 15. Authentication Route Structure

Example:

```
app/

(auth)/

├── login/

├── register/

└── forgot-password/
```

Protected application:

```
(dashboard)/

├── agents

├── calls

├── knowledge

└── settings
```

---

# 16. Loading States

Every major route should define:

```
loading.tsx
```

Used for:

- Data loading
- Skeleton screens
- Better UX

---

# 17. Error Handling

Routes should define:

```
error.tsx
```

Responsibilities:

- Display friendly errors
- Recover from failures
- Log issues

---

# 18. Metadata Architecture

Pages should define metadata.

Examples:

- Title
- Description
- Open Graph information
- SEO properties

---

# 19. Environment Configuration

Environment variables:

```
.env.local

.env.development

.env.production
```

Examples:

```
NEXT_PUBLIC_API_URL

NEXT_PUBLIC_LIVEKIT_URL

AUTH_SECRET
```

Sensitive values must never be exposed publicly.

---

# 20. API Route Usage

Next.js API routes should only be used when required.

Examples:

- Frontend-specific endpoints
- Proxy requests
- Secure server actions

Primary business APIs remain in:

```
FastAPI Backend
```

---

# 21. Deployment Structure

Production flow:

```
Developer

↓

Git Repository

↓

CI/CD Pipeline

↓

Next.js Build

↓

Container Image

↓

Deployment Platform

↓

Users
```

---

# 22. Performance Considerations

The application uses:

- Server Components
- Streaming
- Dynamic imports
- Route optimization
- Image optimization
- Bundle analysis

---

# 23. Security Considerations

Frontend structure supports:

- Protected routes
- Secure sessions
- Permission-aware UI
- Input validation
- Dependency security

---

# 24. Development Principles

The Next.js application follows:

- App Router best practices
- Server-first rendering
- Feature ownership
- Component reuse
- Type safety
- Minimal client-side JavaScript
- Secure data handling

---

# 25. Summary

The Next.js Application Structure defines the foundation of the Voice Agent SaaS frontend.

By using the App Router architecture, feature-based organization, server-first rendering, reusable components, and secure integration patterns, the frontend can support complex SaaS workflows, AI agent builders, and real-time voice experiences at enterprise scale.
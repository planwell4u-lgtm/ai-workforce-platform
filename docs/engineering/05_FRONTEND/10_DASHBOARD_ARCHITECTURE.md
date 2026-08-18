# 10 Dashboard Architecture

**Version:** 2.0  
**Status:** Production Architecture  
**Owner:** Frontend Engineering

---

# 1. Purpose

This document defines the dashboard architecture for the Voice Agent SaaS Platform frontend.

The dashboard is the primary application workspace where users manage:

- AI agents
- Voice operations
- Conversations
- Knowledge systems
- Workflows
- Analytics
- Billing
- Organization settings

The dashboard provides a unified control center for SaaS customers.

---

# 2. Dashboard Architecture Goals

The dashboard architecture provides:

- Enterprise SaaS experience
- Multi-tenant workspace management
- Role-based navigation
- Real-time operational visibility
- Scalable feature integration
- Consistent user experience

---

# 3. Dashboard Architecture Overview

```
                         User

                           │

                           ▼

                    Dashboard Shell

                           │

        ┌──────────────────┼──────────────────┐

        ▼                  ▼                  ▼

   Navigation          Workspace          User Context

        │                  │                  │

        ▼                  ▼                  ▼

 Feature Modules     Tenant Data       Permissions


                           │

                           ▼

                    Feature Pages
```

---

# 4. Dashboard Technology Stack

The dashboard uses:

| Layer | Technology |
|---|---|
| Framework | Next.js App Router |
| UI | React 19 |
| Styling | Tailwind CSS |
| Components | shadcn/ui |
| State | Zustand |
| Data Fetching | TanStack Query |
| Charts | Chart Library |
| Real-Time | WebSockets + LiveKit |

---

# 5. Dashboard Layout Architecture

The dashboard follows a shell-based architecture.

```
Dashboard Layout

├── Sidebar

├── Top Navigation

├── Workspace Selector

├── Notification Center

├── User Menu

└── Page Content
```

---

# 6. Dashboard Route Structure

Recommended:

```
app/

(dashboard)/

├── dashboard/

│   └── page.tsx

├── agents/

├── calls/

├── conversations/

├── knowledge/

├── workflows/

├── analytics/

├── billing/

└── settings/
```

---

# 7. Dashboard Shell Components

Structure:

```
components/

layouts/

└── DashboardShell.tsx
```

Responsibilities:

- Application layout
- Navigation rendering
- Workspace context
- Global providers
- Responsive behavior

---

# 8. Sidebar Architecture

The sidebar provides feature navigation.

Example:

```
Sidebar

├── Dashboard

├── Agents

├── Calls

├── Conversations

├── Knowledge

├── Workflows

├── Analytics

├── Billing

└── Settings
```

---

# 9. Role-Based Navigation

Navigation is permission aware.

Example:

```
Owner

├── Everything


Admin

├── Agents

├── Users

├── Billing


Viewer

├── Read Only Access
```

---

# 10. Workspace Architecture

A workspace represents a tenant operating environment.

Context includes:

```
Workspace

├── Tenant

├── Users

├── Agents

├── Usage

└── Settings
```

---

# 11. Workspace Selector

Enterprise users may manage multiple workspaces.

Flow:

```
User Menu

↓

Workspace Selector

↓

Change Workspace

↓

Reload Context

↓

Refresh Data
```

---

# 12. Dashboard Home Architecture

The dashboard landing page provides:

- System overview
- Usage metrics
- Recent activity
- Agent status
- Quick actions

Example:

```
Dashboard Home

├── Overview Cards

├── Active Agents

├── Recent Calls

├── Usage Statistics

└── System Events
```

---

# 13. Dashboard Metrics

Common metrics:

## Agent Metrics

- Total agents
- Active agents
- Agent executions

---

## Voice Metrics

- Calls completed
- Call duration
- Success rate

---

## Knowledge Metrics

- Documents indexed
- Searches performed

---

## Usage Metrics

- Minutes consumed
- API usage
- Storage usage

---

# 14. Real-Time Dashboard Updates

Dashboard supports live updates.

Examples:

- Active calls
- Agent status
- Processing jobs
- Notifications

Flow:

```
Backend Event

↓

WebSocket

↓

Dashboard Store

↓

Component Update
```

---

# 15. Dashboard Cards

Cards display summarized information.

Examples:

```
Agent Status Card

Call Activity Card

Usage Card

System Health Card
```

Each card supports:

- Loading state
- Empty state
- Error state
- Refresh action

---

# 16. Dashboard Data Architecture

Data flow:

```
Dashboard Component

↓

Feature Hook

↓

TanStack Query

↓

API Service

↓

FastAPI Backend
```

---

# 17. Dashboard State Management

Dashboard-specific state includes:

- Selected workspace
- Date filters
- Dashboard preferences
- Widget visibility

Managed by:

```
Zustand
```

---

# 18. Dashboard Widgets

Widgets are modular.

Example:

```
widgets/

├── AgentOverview.tsx

├── CallStatistics.tsx

├── UsageSummary.tsx

└── ActivityTimeline.tsx
```

---

# 19. Dashboard Customization

Future support:

- Custom layouts
- Widget selection
- Saved views
- Role-based dashboards

---

# 20. Responsive Dashboard Design

Desktop:

```
Sidebar + Multi-column Layout
```

Tablet:

```
Collapsed Navigation
```

Mobile:

```
Drawer Navigation

Single Column Content
```

---

# 21. Dashboard Search

Global search may support:

- Agents
- Calls
- Conversations
- Knowledge documents
- Settings

Architecture:

```
Search Input

↓

Search Service

↓

Backend Search API

↓

Results Display
```

---

# 22. Notification Center

Dashboard notifications include:

- Agent events
- Call completion
- Processing status
- Billing alerts

Flow:

```
Backend

↓

Notification Service

↓

WebSocket

↓

Notification Center
```

---

# 23. Dashboard Security

Dashboard enforces:

- Authentication
- Authorization
- Tenant isolation
- Permission checks

Security authority remains:

```
Backend
```

---

# 24. Performance Strategy

Dashboard performance uses:

- Server components
- Lazy loaded widgets
- Query caching
- Component memoization
- Virtualized tables

---

# 25. Testing Strategy

Dashboard testing includes:

## Component Tests

Verify:

- Widgets
- Cards
- Navigation

---

## Integration Tests

Verify:

- Data loading
- Permissions
- Workspace switching

---

## End-to-End Tests

Example:

```
Login

↓

Open Dashboard

↓

View Agent Metrics

↓

Navigate Agent Builder
```

---

# 26. Future Expansion

The dashboard architecture supports:

- Enterprise analytics
- Custom dashboards
- AI insights
- Team collaboration
- White-label portals

---

# 27. Summary

The Dashboard Architecture defines the central workspace of the Voice Agent SaaS Platform.

By combining modular widgets, tenant-aware navigation, real-time updates, permission-based access, and scalable frontend patterns, the dashboard provides the operational foundation for managing AI voice agents and SaaS workflows.
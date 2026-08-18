# 03 State Management Example
# State Management Example

**Version:** 2.0

---

# 1. Overview

This document defines the recommended state management architecture for the Voice Agent SaaS frontend.

The objective is to maintain a predictable, scalable, and high-performance frontend by clearly separating different categories of state.

The architecture combines modern React patterns with specialized state management libraries, ensuring each type of state is managed by the most appropriate solution.

---

# 2. State Architecture

```
                    Browser
                       │
                       ▼
                 React Components
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Local UI State   Global UI State  Server State
        │              │              │
      React         Zustand     TanStack Query
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                  Backend APIs
```

---

# 3. State Categories

| State Type | Technology | Examples |
|------------|------------|----------|
| Local Component State | React `useState` | Modal open, input values |
| Shared UI State | Zustand | Sidebar, theme, selected agent |
| Server State | TanStack Query | Agents, calls, workflows |
| Form State | React Hook Form | Login, agent editor |
| URL State | Next.js Router | Search, filters, pagination |

---

# 4. Recommended Directory Structure

```text
frontend/

stores/

    auth-store.ts

    ui-store.ts

    call-store.ts

    notification-store.ts

hooks/

    use-agents.ts

    use-calls.ts

    use-workflows.ts

services/

    api-client.ts

    agent-service.ts

    call-service.ts

providers/

    query-provider.tsx
```

---

# 5. Local Component State

Use React state for temporary UI interactions.

Examples:

- Dialog visibility
- Dropdown selection
- Accordion expansion
- Active tab
- Input focus
- Hover state

Example:

```tsx
const [open, setOpen] = useState(false)
```

Keep local state close to where it is used.

---

# 6. Global UI State

Use Zustand for shared UI state.

Examples:

- Sidebar state
- Theme selection
- Current tenant
- Active workspace
- Notification panel
- Selected voice device

Example:

```tsx
import { create } from "zustand"

interface UIStore {
  sidebarOpen: boolean
  toggleSidebar: () => void
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  toggleSidebar: () =>
    set((state) => ({
      sidebarOpen: !state.sidebarOpen,
    })),
}))
```

Avoid storing server data in Zustand.

---

# 7. Server State

Server state should be managed using TanStack Query.

Examples:

- Agent list
- Conversations
- Knowledge base
- Memory entries
- Billing data
- Analytics

Example:

```tsx
export function useAgents() {
  return useQuery({
    queryKey: ["agents"],
    queryFn: getAgents,
  })
}
```

Benefits:

- Automatic caching
- Background refetching
- Request deduplication
- Retry handling
- Optimistic updates

---

# 8. Form State

Use React Hook Form for all complex forms.

Example:

```tsx
const form = useForm({
  defaultValues: {
    name: "",
    description: "",
  },
})
```

Combine with Zod for validation.

---

# 9. URL State

State reflected in the URL should use the Next.js router.

Examples:

```
?page=2

?search=voice

?status=active

?tab=settings
```

Benefits:

- Shareable links
- Browser history support
- Bookmarking
- Refresh persistence

---

# 10. Authentication State

Authentication store should contain only client-side session information.

Example:

```tsx
interface AuthState {
  user?: User
  tenantId?: string
  isAuthenticated: boolean
}
```

Never store:

- Passwords
- API secrets
- Refresh tokens in local storage

Prefer secure HTTP-only cookies for sensitive tokens.

---

# 11. State Flow

```
User Action

      │

Component

      │

Custom Hook

      │

API Service

      │

Backend

      │

TanStack Query Cache

      │

React Components
```

Business logic should remain outside UI components.

---

# 12. Optimistic Updates

Example workflow:

```
Update Agent

      │

Update UI Immediately

      │

Send API Request

      │

Success?

   ┌──┴──┐
   │     │
 Yes     No
   │     │
 Keep   Roll Back
```

Use optimistic updates for responsive user experiences.

---

# 13. Cache Invalidation

Invalidate relevant queries after mutations.

Example:

```tsx
queryClient.invalidateQueries({
  queryKey: ["agents"],
})
```

Avoid invalidating unrelated caches.

---

# 14. Real-Time Updates

For WebSocket or LiveKit events:

```
WebSocket Event

      │

Event Handler

      │

Update Query Cache

      │

React Re-render
```

Prefer updating the query cache instead of maintaining duplicate state.

---

# 15. Derived State

Avoid storing values that can be computed.

Instead of:

```tsx
const [activeCount, setActiveCount]
```

Prefer:

```tsx
const activeCount = agents.filter(
  (a) => a.status === "active"
).length
```

Derived state reduces synchronization issues.

---

# 16. Error Handling

Each server query should expose:

- Loading state
- Success state
- Error state
- Retry capability

Example:

```tsx
const {
  data,
  isLoading,
  error,
} = useAgents()
```

Display appropriate UI for each state.

---

# 17. Performance Considerations

Optimize state management by:

- Keeping state minimal
- Splitting large stores
- Memoizing expensive calculations
- Using selectors with Zustand
- Avoiding unnecessary re-renders
- Lazy loading feature stores

---

# 18. Testing

State management tests should verify:

- Store initialization
- State updates
- Hook behavior
- Query caching
- Cache invalidation
- Optimistic updates
- Error recovery

Recommended tools:

- Vitest
- React Testing Library
- MSW (Mock Service Worker)

---

# 19. Best Practices

Always:

- Keep local state local
- Use Zustand only for shared UI state
- Use TanStack Query for server state
- Keep stores focused
- Use typed interfaces
- Prefer derived state
- Invalidate caches selectively

Avoid:

- Duplicating server data
- Global state for temporary UI
- Large monolithic stores
- Direct API calls inside components
- Storing secrets in client state

---

# 20. Example End-to-End Flow

```
User Clicks "Create Agent"

        │

React Hook Form

        │

Validation (Zod)

        │

Mutation (TanStack Query)

        │

Backend API

        │

Database

        │

Success Response

        │

Invalidate "agents" Query

        │

Updated Agent List Rendered
```

---

# 21. Summary

The recommended state management architecture separates concerns by using React for local state, Zustand for shared UI state, TanStack Query for server state, React Hook Form for forms, and the Next.js router for URL state. This approach minimizes complexity, improves performance, and provides a scalable foundation for the Voice Agent SaaS frontend.
# 04 Api Client Example
# API Client Example

**Version:** 2.0

---

# 1. Overview

This document defines the standard API client architecture for the Voice Agent SaaS frontend.

The API client provides a centralized, type-safe, and reusable layer for all communication between the Next.js frontend and backend services.

Objectives:

- Centralize HTTP communication
- Provide consistent error handling
- Automatically manage authentication
- Support request retries
- Simplify API consumption
- Improve maintainability
- Enable testing and mocking

All frontend features should communicate with backend services through this API client layer.

---

# 2. Architecture

```
React Components

       │

Feature Hooks

       │

Feature Services

       │

API Client

       │

Authentication

       │

HTTP Transport

       │

Backend API
```

The API client acts as the single gateway for all backend communication.

---

# 3. Recommended Directory Structure

```text
frontend/

lib/

    api-client.ts

    api-error.ts

    auth.ts

services/

    agent-service.ts

    call-service.ts

    workflow-service.ts

    knowledge-service.ts

    memory-service.ts

    billing-service.ts

types/

hooks/
```

---

# 4. API Client Responsibilities

The API client should provide:

- Base URL configuration
- Authentication headers
- Request timeout
- JSON serialization
- Error handling
- Token refresh
- Request cancellation
- Logging hooks
- Retry support

Business logic should remain in feature services.

---

# 5. Base Client Example

```typescript
const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_URL;

export async function apiClient(
    path: string,
    options: RequestInit = {}
) {
    const response = await fetch(
        `${API_BASE_URL}${path}`,
        {
            ...options,
            headers: {
                "Content-Type":
                    "application/json",
                ...options.headers,
            },
        }
    );

    if (!response.ok) {
        throw new Error(
            "Request failed"
        );
    }

    return response.json();
}
```

This base client should be reused throughout the application.

---

# 6. Authentication

Authentication headers should be added automatically.

Example:

```http
Authorization: Bearer <access_token>
```

The API client should retrieve the token from the authentication layer rather than requiring each service to manage headers manually.

---

# 7. Request Flow

```
React Component

      │

Feature Hook

      │

Feature Service

      │

API Client

      │

Backend

      │

JSON Response

      │

TanStack Query

      │

UI Update
```

---

# 8. Feature Service Example

```typescript
import { apiClient } from "@/lib/api-client";

export async function getAgents() {

    return apiClient(
        "/agents"
    );

}
```

Feature services should contain endpoint-specific operations while delegating transport concerns to the API client.

---

# 9. CRUD Example

```typescript
export const AgentService = {

    list() {
        return apiClient("/agents");
    },

    get(id: string) {
        return apiClient(
            `/agents/${id}`
        );
    },

    create(data: AgentCreate) {

        return apiClient("/agents", {

            method: "POST",

            body: JSON.stringify(data),

        });

    },

    update(id, data) {

        return apiClient(

            `/agents/${id}`,

            {

                method: "PUT",

                body: JSON.stringify(data),

            }

        );

    },

    delete(id) {

        return apiClient(

            `/agents/${id}`,

            {

                method: "DELETE",

            }

        );

    }

};
```

---

# 10. Error Handling

Errors should be normalized into a consistent format.

Example:

```typescript
class ApiError extends Error {

    constructor(

        public status: number,

        message: string

    ) {

        super(message);

    }

}
```

Expose meaningful information such as:

- HTTP status
- Error code
- User-friendly message
- Validation details

---

# 11. Automatic Token Refresh

Recommended flow:

```
Request

   │

401 Unauthorized

   │

Refresh Token

   │

Success?

┌──┴──┐
│     │
Yes   No
│     │
Retry Logout
```

The refresh process should be transparent to feature services whenever possible.

---

# 12. Request Timeout

All requests should have configurable timeouts.

Recommended defaults:

| Endpoint Type | Timeout |
|--------------|--------:|
| Standard API | 30 seconds |
| File Upload | 120 seconds |
| AI Processing | 300 seconds |
| Streaming | Unlimited / Managed Separately |

Long-running operations should provide progress updates where appropriate.

---

# 13. Request Cancellation

Use `AbortController` for cancellable requests.

Example:

```typescript
const controller = new AbortController();

fetch(url, {

    signal: controller.signal

});
```

Useful for:

- Search
- Autocomplete
- Navigation
- Component unmount

---

# 14. Retry Strategy

Retry only transient failures.

Recommended retries:

| Error | Retry |
|--------|------|
| Network failure | Yes |
| 429 Too Many Requests | Yes |
| 503 Service Unavailable | Yes |
| 500 Internal Error | Limited |
| 400 Bad Request | No |
| 401 Unauthorized | Refresh then retry |

Use exponential backoff to reduce server load.

---

# 15. Type Safety

Every request and response should use TypeScript interfaces.

Example:

```typescript
interface Agent {

    id: string;

    name: string;

    status: string;

}
```

Avoid using `any`.

---

# 16. Logging

Development logging may include:

- Method
- URL
- Duration
- Status
- Correlation ID

Sensitive information must never be logged.

---

# 17. Testing

The API client should be tested for:

- Successful requests
- Authentication headers
- Token refresh
- Timeouts
- Retries
- Error mapping
- Request cancellation

Use mocked network responses for repeatable tests.

---

# 18. Best Practices

Always:

- Centralize HTTP logic
- Keep services small
- Use typed models
- Handle errors consistently
- Support retries
- Cancel unnecessary requests
- Keep authentication transparent

Avoid:

- Direct `fetch()` calls inside components
- Duplicate request logic
- Hard-coded URLs
- Unhandled promise rejections
- Storing secrets in the client

---

# 19. Example End-to-End Flow

```
User Opens Agent List

        │

TanStack Query

        │

Agent Service

        │

API Client

        │

Authentication

        │

Backend API

        │

JSON Response

        │

Cache Updated

        │

UI Rendered
```

---

# 20. Summary

A centralized API client provides a consistent and maintainable approach to backend communication across the Voice Agent SaaS frontend. By encapsulating authentication, retries, error handling, timeouts, and transport concerns, feature modules remain clean, testable, and focused solely on business functionality.
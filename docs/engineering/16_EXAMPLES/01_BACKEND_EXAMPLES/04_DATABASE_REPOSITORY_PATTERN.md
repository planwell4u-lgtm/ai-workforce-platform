# 04 Database Repository Pattern
# Authentication Flow Example

**Version:** 2.0

---

# 1. Overview

This document provides a production-ready example of the authentication and authorization flow used throughout the Voice Agent SaaS platform.

The authentication architecture is designed to provide:

- Secure user authentication
- Multi-tenant isolation
- JWT-based authorization
- Role-Based Access Control (RBAC)
- API security
- Service-to-service authentication
- Auditability
- Scalability

This document serves as the reference implementation for all backend services.

---

# 2. Authentication Architecture

```
                    User
                      │
                      ▼
                 Login Request
                      │
                      ▼
            Authentication Service
                      │
         Verify Credentials / MFA
                      │
                      ▼
                Generate JWT
                      │
                      ▼
                 Return Tokens
                      │
────────────────────────────────────────
                      │
               Authenticated Request
                      │
                      ▼
               API Gateway
                      │
              JWT Verification
                      │
              Token Validation
                      │
             Tenant Resolution
                      │
            Permission Validation
                      │
                      ▼
              FastAPI Endpoint
                      │
                      ▼
              Service Layer
```

---

# 3. Authentication Components

| Component | Responsibility |
|-----------|----------------|
| Identity Provider | User authentication |
| JWT Service | Token generation |
| API Gateway | Token verification |
| FastAPI Dependency | Current user resolution |
| Authorization Service | Permission validation |
| Audit Service | Security logging |

---

# 4. Login Flow

```
Client
   │
POST /login
   │
Validate Credentials
   │
Generate Access Token
   │
Generate Refresh Token
   │
Store Refresh Token
   │
Return Tokens
```

---

# 5. Login Request

```http
POST /api/v1/auth/login
```

Example:

```json
{
    "email": "admin@example.com",
    "password": "********"
}
```

---

# 6. Login Response

```json
{
    "access_token": "<jwt-token>",
    "refresh_token": "<refresh-token>",
    "token_type": "Bearer",
    "expires_in": 3600
}
```

---

# 7. JWT Payload Example

```json
{
    "sub": "user_123",
    "tenant_id": "tenant_001",
    "email": "admin@example.com",
    "roles": [
        "Admin"
    ],
    "permissions": [
        "agents:read",
        "agents:create",
        "calls:manage"
    ],
    "iat": 1750000000,
    "exp": 1750003600
}
```

---

# 8. Authorization Header

Every authenticated request must include:

```http
Authorization: Bearer <access_token>
```

---

# 9. FastAPI Dependency Example

```python
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()


async def get_current_user(
    credentials=Depends(security)
):

    token = credentials.credentials

    # Validate JWT

    # Decode payload

    # Load user

    return current_user
```

---

# 10. Route Protection Example

```python
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


@router.get("/agents")
async def list_agents(

    current_user=Depends(
        get_current_user
    )

):
    return []
```

---

# 11. Tenant Resolution

Every authenticated request resolves:

```
JWT

↓

User

↓

Tenant

↓

Permissions

↓

Request Context
```

The tenant identifier is passed through the request lifecycle to ensure complete tenant isolation.

---

# 12. Permission Validation

Example:

```python
def require_permission(
    permission: str
):

    def validator(user):

        if permission not in user.permissions:

            raise PermissionError()

        return user

    return validator
```

Usage:

```python
Depends(
    require_permission(
        "agents:create"
    )
)
```

---

# 13. Refresh Token Flow

```
Access Token Expired

        │

Refresh Request

        │

Validate Refresh Token

        │

Generate New Access Token

        │

Return New Token
```

Endpoint:

```http
POST /api/v1/auth/refresh
```

---

# 14. Logout Flow

```
Logout Request

      │

Invalidate Refresh Token

      │

Revoke Session

      │

Audit Event

      │

Return Success
```

---

# 15. Service-to-Service Authentication

Internal services authenticate using:

- Service JWT
- Mutual TLS (mTLS)
- API Keys (where appropriate)

Example:

```
AI Runtime

↓

Signed JWT

↓

Knowledge Service

↓

Validate Signature

↓

Authorize Request
```

---

# 16. Error Responses

Unauthorized:

```http
401 Unauthorized
```

```json
{
    "detail": "Invalid authentication credentials"
}
```

Forbidden:

```http
403 Forbidden
```

```json
{
    "detail": "Permission denied"
}
```

---

# 17. Security Best Practices

Access tokens should:

- Have short lifetimes (15–60 minutes)
- Be signed using strong algorithms
- Include minimal claims
- Never contain sensitive data

Refresh tokens should:

- Be securely stored
- Be revocable
- Rotate after use
- Have longer expiration periods

Passwords must:

- Be hashed using Argon2 or bcrypt
- Never be logged
- Never be returned by APIs

---

# 18. Audit Logging

Authentication events must be logged.

Examples:

- Login succeeded
- Login failed
- Password changed
- Token refreshed
- Logout
- Permission denied
- Account locked

Example log:

```json
{
    "event": "user_login",
    "user_id": "user_123",
    "tenant_id": "tenant_001",
    "ip_address": "203.0.113.10",
    "timestamp": "2026-07-31T10:30:00Z"
}
```

---

# 19. Testing

Authentication tests should verify:

- Successful login
- Invalid credentials
- Expired tokens
- Invalid signatures
- Permission enforcement
- Tenant isolation
- Refresh token rotation
- Logout behavior

---

# 20. Summary

The authentication flow ensures that every request is securely authenticated, authorized, and scoped to the correct tenant before business logic is executed.

This pattern should be consistently implemented across all backend services to provide secure, scalable, and maintainable authentication throughout the Voice Agent SaaS platform.
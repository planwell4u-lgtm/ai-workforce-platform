# User Service

**Module:** 04_BACKEND

**Document:** 07_USER_SERVICE

**Version:** 2.0

**Status:** Production Ready

---

# Purpose

The User Service is responsible for managing the complete lifecycle of platform users.

Every authenticated user belongs to a tenant and is assigned one or more roles that determine access to platform resources.

The service manages user identities, profiles, roles, permissions, preferences, sessions, and account status while enforcing strict tenant isolation.

---

# Responsibilities

The User Service manages:

- User registration
- User invitations
- User profiles
- User activation
- User suspension
- User deletion
- Password management
- Role assignment
- Permission assignment
- Session management
- User preferences
- API access
- Audit events

---

# Architecture

```
                    API

                     │

                     ▼

               User Service

     ┌───────────────┼────────────────┐

     ▼               ▼                ▼

 Repository    Authentication    Event Bus

     │

     ▼

 PostgreSQL
```

---

# Service Dependencies

The User Service depends on:

- User Repository
- Tenant Service
- Authentication Service
- Notification Service
- Audit Service
- Event Publisher
- Redis Cache

---

# Database Tables

Primary

```
users

user_profiles

user_roles

user_permissions

user_sessions

user_preferences

user_api_keys
```

Supporting

```
tenants

roles

permissions

audit_logs
```

---

# Public Responsibilities

The service exposes operations for:

```
Create User

Invite User

Update User

Deactivate User

Suspend User

Delete User

Reset Password

Assign Role

Remove Role

Assign Permission

Update Preferences

Rotate API Keys

Get User

List Users
```

---

# User Lifecycle

```
Create User

↓

Validate Tenant

↓

Create Identity

↓

Assign Default Role

↓

Create User Profile

↓

Send Welcome Email

↓

Publish UserCreated Event

↓

User Active
```

---

# User States

```
Pending

Active

Suspended

Locked

Archived

Deleted
```

Only Active users may authenticate.

---

# User Profile

Each user maintains:

- First Name
- Last Name
- Display Name
- Email
- Phone Number
- Avatar
- Language
- Time Zone
- Theme Preference
- Notification Preferences

---

# Role Management

A user may have multiple roles.

Examples

```
Tenant Owner

Tenant Admin

Manager

Supervisor

Developer

Support

Billing Manager

Viewer
```

Role assignment follows RBAC rules.

---

# Permission Management

Permissions may be inherited from roles or assigned directly.

Examples

```
agent:create

agent:update

agent:delete

call:view

workflow:execute

knowledge:upload

billing:view
```

---

# Session Management

Each authenticated session stores:

- Session ID
- Login Time
- Last Activity
- Device
- Browser
- IP Address
- Refresh Token
- Expiration

Users may revoke individual sessions.

---

# API Key Management

Users may create personal API keys.

Each key includes:

- Name
- Scope
- Expiration
- Status
- Last Used
- Created By

---

# Security Responsibilities

The service enforces:

- Tenant isolation
- Password policy
- Role validation
- Permission validation
- Session validation
- Account lockout
- Audit logging

---

# Password Management

Supported operations

```
Change Password

Reset Password

Forgot Password

Force Password Reset
```

Passwords are hashed using Argon2id.

---

# Notification Integration

The service triggers notifications for:

- Welcome Email
- Password Reset
- Account Activation
- Invitation
- Role Change
- Account Suspension
- Security Alerts

---

# Events Published

```
UserCreated

UserUpdated

UserActivated

UserSuspended

UserDeleted

PasswordChanged

RoleAssigned

RoleRemoved

UserLoggedIn

UserLoggedOut
```

---

# Events Consumed

```
TenantCreated

TenantSuspended

SubscriptionExpired

PaymentSucceeded

PaymentFailed
```

---

# Cache Strategy

Frequently accessed data is cached.

Examples

```
User Profile

Permissions

Roles

Preferences

Session Information
```

Cache is invalidated after updates.

---

# Error Handling

Domain exceptions include:

```
UserNotFound

UserAlreadyExists

InvalidCredentials

PasswordPolicyViolation

RoleNotFound

PermissionDenied

SessionExpired
```

---

# Performance Guidelines

The service should:

- Cache user permissions
- Batch permission lookups
- Use indexed email searches
- Minimize joins
- Avoid repeated role resolution

---

# Audit Logging

The following actions are recorded:

- User creation
- Login
- Logout
- Password changes
- Role assignments
- Permission changes
- Profile updates
- API key creation
- Session revocation
- Account suspension

---

# Testing Requirements

The User Service must include tests for:

- User lifecycle
- Authentication
- Authorization
- Password reset
- Session management
- Role assignment
- Permission validation
- Tenant isolation
- Event publishing
- Cache invalidation

---

# Related Documents

- 05_AUTHENTICATION_AUTHORIZATION.md
- 06_TENANT_SERVICE.md
- 08_AGENT_SERVICE.md
- 26_BACKEND_SECURITY.md
- 03_DATABASE/06_USER_IDENTITY_SCHEMA.md

---

# Summary

The User Service manages all aspects of user identity within the Voice Agent SaaS Platform. It provides secure account management, role and permission administration, session handling, and profile management while ensuring tenant isolation and enterprise-grade security. As the foundation of user identity, it integrates closely with authentication, authorization, billing, notifications, and audit services.
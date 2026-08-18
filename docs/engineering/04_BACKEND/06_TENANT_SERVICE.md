# Tenant Service

**Module:** 04_BACKEND

**Document:** 06_TENANT_SERVICE

**Version:** 2.0

**Status:** Production Ready

---

# Purpose

The Tenant Service is responsible for managing the complete lifecycle of a tenant within the Voice Agent SaaS Platform.

Every customer organization is represented as a tenant. The Tenant Service ensures complete logical isolation of data, users, AI agents, billing, voice resources, integrations, and analytics.

It is the foundation of the platform's multi-tenant architecture.

---

# Responsibilities

The Tenant Service is responsible for:

- Tenant creation
- Tenant onboarding
- Tenant configuration
- Tenant activation
- Tenant suspension
- Tenant deletion
- Tenant settings
- Subscription assignment
- Feature flags
- Usage limits
- Branding
- Regional settings
- Compliance settings

---

# Architecture

```
                    API

                     │

                     ▼

              Tenant Service

      ┌──────────────┼───────────────┐

      ▼              ▼               ▼

 Repository     Billing Service   Event Bus

      │

      ▼

 PostgreSQL
```

---

# Service Dependencies

The Tenant Service depends on:

- Tenant Repository
- User Service
- Billing Service
- Notification Service
- Integration Service
- Event Publisher
- Redis Cache

---

# Database Tables

Primary tables

```
tenants

tenant_settings

tenant_domains

tenant_features

tenant_limits

tenant_api_keys

tenant_integrations
```

Supporting tables

```
users

subscriptions

audit_logs

billing_accounts
```

---

# Public Responsibilities

The service exposes functionality for:

```
Create Tenant

Update Tenant

Delete Tenant

Suspend Tenant

Reactivate Tenant

Archive Tenant

Get Tenant

List Tenants

Update Settings

Update Limits

Update Branding

Update Features

Rotate API Keys
```

---

# Tenant Lifecycle

```
Create Tenant

↓

Provision Database Records

↓

Create Owner Account

↓

Create Default Roles

↓

Create Default Agent Templates

↓

Create Storage

↓

Initialize Billing

↓

Publish TenantCreated Event

↓

Tenant Ready
```

---

# Tenant States

```
Pending

Active

Suspended

Archived

Deleted
```

Only **Active** tenants may access production services.

---

# Tenant Configuration

Each tenant maintains configuration including:

- Company name
- Timezone
- Language
- Currency
- Region
- Branding
- Logo
- Theme
- Contact details
- Default voice settings
- AI model preferences

---

# Feature Flags

Features can be enabled or disabled per tenant.

Examples

```
Voice Calls

Outbound Dialing

SMS

Knowledge Base

Memory

Workflow Builder

Custom Tools

API Access

Webhooks

Analytics

Billing

Human Handoff
```

---

# Usage Limits

Each tenant has configurable limits.

Examples

```
Maximum Users

Maximum Agents

Maximum Calls

Storage Limit

Monthly Minutes

Knowledge Documents

Concurrent Calls

API Requests

Workflow Executions
```

Limits are enforced by the service before resource creation.

---

# Subscription Integration

The Tenant Service integrates with Billing.

Subscription plans determine:

- Enabled features
- Usage quotas
- Storage
- AI model availability
- Voice providers
- Support level

---

# Branding

Each tenant may customize:

- Company logo
- Dashboard theme
- Brand colors
- Email templates
- Notification templates
- Voice greeting defaults

---

# API Key Management

Tenant-level API keys support:

- External integrations
- Automation
- SDK access
- Webhooks

Each key has:

- Name
- Scope
- Expiration
- Status
- Last Used
- Permissions

---

# Security Responsibilities

The service enforces:

- Tenant ownership
- Tenant isolation
- Permission validation
- Audit logging
- API key validation

Cross-tenant operations are prohibited unless performed by platform administrators.

---

# Cache Strategy

Frequently accessed tenant information is cached.

Examples

```
Tenant Settings

Subscription

Features

Limits

Branding
```

Cache is invalidated immediately after updates.

---

# Events Published

```
TenantCreated

TenantUpdated

TenantActivated

TenantSuspended

TenantDeleted

TenantArchived

TenantLimitsChanged

TenantFeaturesChanged

TenantBrandingUpdated
```

---

# Events Consumed

```
SubscriptionChanged

InvoicePaid

InvoiceFailed

PaymentSucceeded

PaymentFailed
```

---

# Integrations

The Tenant Service communicates with:

- Billing Service
- Notification Service
- Storage Service
- Authentication Service
- Analytics Service

---

# Error Handling

Domain exceptions include:

```
TenantNotFound

TenantAlreadyExists

TenantAlreadySuspended

TenantLimitExceeded

SubscriptionRequired

InvalidTenantState
```

Raw database exceptions are never exposed.

---

# Performance Considerations

The service should:

- Cache tenant metadata
- Minimize joins
- Batch updates
- Use indexed tenant lookups
- Avoid repeated configuration loading

---

# Audit Logging

The following actions are audited:

- Tenant creation
- Tenant updates
- Branding changes
- Subscription changes
- API key creation
- API key revocation
- Feature changes
- Limit changes
- Suspension
- Reactivation
- Deletion

---

# Testing Requirements

The Tenant Service must include tests for:

- Tenant lifecycle
- Permission validation
- Feature flags
- Usage limits
- Subscription changes
- Tenant isolation
- Cache invalidation
- Event publishing
- Failure recovery

---

# Related Documents

- 05_AUTHENTICATION_AUTHORIZATION.md
- 07_USER_SERVICE.md
- 17_BILLING_SERVICE.md
- 26_BACKEND_SECURITY.md
- 03_DATABASE/04_MULTI_TENANT_DATA_MODEL.md

---

# Summary

The Tenant Service is the central authority for managing customer organizations within the Voice Agent SaaS Platform. It provisions tenants, enforces subscription limits, maintains configuration and branding, manages feature availability, and guarantees strict tenant isolation. All backend services rely on the Tenant Service to provide the tenant context that underpins secure and scalable multi-tenant operation.
# Data Classification Policy

Defines storage, retention, and access guidelines based on data sensitivity levels.

## Classifications

### 1. Restricted (PII & Credentials)
- **Examples:** Hashed passwords, email addresses, external integration tokens.
- **Handling:** Must be encrypted at rest and in transit. Access limited via RBAC.

### 2. Confidential (Internal Business Logic)
- **Examples:** Proprietary codebase, system logs, internal roadmap plans.
- **Handling:** Access limited to authenticated employee accounts.

### 3. Public
- **Examples:** Product features marketing site, public API documentation.
- **Handling:** Readable by everyone.

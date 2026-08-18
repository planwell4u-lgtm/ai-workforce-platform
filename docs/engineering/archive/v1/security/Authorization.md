# Authorization Design

Detailed specification of access control paradigms.

## RBAC (Role-Based Access Control)

Roles define coarse-grained permissions:

- **Admin:** Complete access to billing, users, agents, and logs.
- **Developer:** Read/write access to agents and configurations. No billing modifications.
- **Viewer:** Read-only access to configurations and metrics.

## ABAC / Row-Level Security

- Conversation records are protected by database row-level security (RLS) policies matching `user_id` against the authenticated session token context.

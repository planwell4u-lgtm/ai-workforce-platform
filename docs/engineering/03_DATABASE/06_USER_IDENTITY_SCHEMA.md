# User Identity Schema

**Document ID:** DB-IDENTITY-006  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the user identity and access management database design for the AI Voice Agent SaaS platform.

The identity domain manages:

- User accounts
- Authentication identities
- Organization memberships
- Roles
- Permissions
- Sessions
- API credentials
- Security controls

The identity system provides secure access management across all tenant environments.

---

# 2. Identity Architecture

High-level model:

                User

                 |

          Authentication

                 |

          Identity Account

                 |

         Organization Membership

                 |

              Role

                 |

          Permissions

---

# 3. Identity Design Principles

## 3.1 Separation of Identity and Tenant Data

Users are platform identities.

Organizations define ownership.

Example:


User

belongs to

Organization

through

Membership


---

## 3.2 Role-Based Access Control

Authorization uses:


User

Membership

Role

Permission


---

## 3.3 Secure Credential Handling

Passwords, tokens, and secrets must:

- Never be stored in plain text
- Use secure hashing
- Use encryption where required
- Support rotation

---

# 4. Identity Schema

Schema:


identity


---

# 5. Identity Tables Overview


identity.users

identity.credentials

identity.oauth_accounts

identity.sessions

identity.roles

identity.permissions

identity.role_permissions

identity.memberships

identity.api_keys

identity.login_events


---

# 6. Users Table

Table:


identity.users


Purpose:

Stores platform user profiles.

---

## Structure

```sql
CREATE TABLE identity.users
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    email TEXT UNIQUE NOT NULL,

    first_name TEXT,

    last_name TEXT,

    status TEXT DEFAULT 'active',

    created_at TIMESTAMPTZ DEFAULT now(),

    updated_at TIMESTAMPTZ DEFAULT now()
);
User States

Supported:

active

pending

suspended

deleted

7. User Identity Flow

Authentication flow:

User Login

      |

Authentication Provider

      |

Validate Identity

      |

Create Session

      |

Load Memberships

      |

Authorize Request

8. Credentials Table

Table:

identity.credentials

Purpose:

Stores authentication credentials.

Supported methods:

Password

OAuth

SSO

API Authentication


Example:

CREATE TABLE identity.credentials
(
id UUID PRIMARY KEY,

user_id UUID NOT NULL,

password_hash TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
9. Password Security Standards

Passwords must use:

Recommended:

Argon2id

or

bcrypt

Never:

MD5

SHA1

Plain Text

10. OAuth Accounts

Table:

identity.oauth_accounts

Purpose:

External identity providers.

Examples:

Google

Microsoft

GitHub

Enterprise SSO


Structure:

CREATE TABLE identity.oauth_accounts
(
id UUID PRIMARY KEY,

user_id UUID NOT NULL,

provider TEXT NOT NULL,

provider_user_id TEXT NOT NULL

);
11. Organization Membership Model

A user does not directly own tenant resources.

Relationship:

User

 |

Membership

 |

Organization


Table:

identity.memberships

Example:

CREATE TABLE identity.memberships
(
id UUID PRIMARY KEY,

user_id UUID NOT NULL,

tenant_id UUID NOT NULL,

role_id UUID NOT NULL,

created_at TIMESTAMPTZ DEFAULT now()
);
12. Membership States
active

invited

suspended

removed

13. Roles Table

Table:

identity.roles

Purpose:

Defines access levels.

Default roles:

Role	Description
Owner	Complete tenant control
Admin	Manage tenant resources
Developer	API and integrations
Operator	Daily operations
Viewer	Read-only access
14. Permissions Table

Table:

identity.permissions

Purpose:

Fine-grained authorization.

Examples:

agent.create

agent.update

agent.delete

call.view

billing.manage

user.invite

15. Role Permission Mapping

Table:

identity.role_permissions

Relationship:

Role

 |

Permissions


Example:

CREATE TABLE identity.role_permissions
(
role_id UUID,

permission_id UUID
);
16. Authorization Model

Permission check flow:

API Request

      |

Identify User

      |

Find Membership

      |

Find Role

      |

Load Permissions

      |

Allow / Deny

17. Sessions Table

Table:

identity.sessions

Purpose:

Tracks authenticated sessions.

Fields:

id

user_id

token_hash

expires_at

created_at

last_activity_at


Security requirements:

Store hashed tokens
Support revocation
Track device information
18. API Keys Table

Table:

identity.api_keys

Purpose:

Machine-to-machine authentication.

Used by:

Developers
External integrations
Automation systems

Example:

sk_live_xxxxxxxxx


Database storage:

key_hash

prefix

last_used_at

expires_at

19. Login Events

Table:

identity.login_events

Purpose:

Security auditing.

Tracks:

Login attempts
Failed logins
IP metadata
Device information

Example:

User Login

 |

Success

 |

Audit Event

20. Tenant Isolation Rules

Identity tables follow tenant rules.

Tenant-owned tables:

identity.memberships

identity.api_keys

identity.sessions


Global tables:

identity.users

identity.permissions

21. Security Requirements

Required:

MFA support
Session expiration
Token rotation
Login monitoring
Audit logging
Brute-force protection
22. Data Retention

Recommended:

Data	Retention
Sessions	30-90 days
Login events	1+ year
Deleted users	According to policy
API keys	Until revoked
23. Integration Points

Identity integrates with:

Authentication Service

Tenant Service

Authorization Middleware

Audit Service

Billing Service

24. Future Enhancements

Possible additions:

identity.mfa_devices

identity.passkeys

identity.sso_connections

identity.access_policies

identity.device_sessions

25. Related Documents

Next:

07_AGENT_SCHEMA.md

08_AGENT_RUNTIME_SCHEMA.md

09_VOICE_CALL_SCHEMA.md
End of Document
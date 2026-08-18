# Database Migration Strategy

**Document Version:** 1.0
**Project:** AI Voice Agent SaaS Platform
**Phase:** 05 - Database Schema
**Database Platform:** Supabase PostgreSQL
**Migration Tools:** Alembic + Supabase Migration System
**Architecture:** Version Controlled Database Evolution
**Status:** Draft
**Last Updated:** 2026-07-23

---

# 1. Overview

This document defines the database migration strategy for the AI Voice Agent SaaS platform.

Database migrations manage controlled changes to:

* Tables
* Columns
* Indexes
* Constraints
* Functions
* Policies
* Extensions

The migration system ensures:

* Safe schema evolution
* Version tracking
* Automated deployment
* Rollback capability

---

# 2. Migration Architecture

```text
Developer

    |

    v

Migration File

    |

    v

Git Repository

    |

    v

CI/CD Pipeline

    |

    v

Supabase PostgreSQL

    |

    v

Production Database
```

---

# 3. Migration Responsibilities

```text
Migration System

├── Schema Creation

├── Schema Updates

├── Data Transformation

├── Index Management

├── Security Policies

└── Rollback Handling
```

---

# 4. Migration Tools

Recommended stack:

```text
Backend:

Python FastAPI


ORM:

SQLAlchemy


Migration:

Alembic


Database:

Supabase PostgreSQL
```

---

# 5. Migration Folder Structure

Recommended:

```text
backend/

├── app/

├── migrations/

│   ├── versions/

│   │

│   ├── env.py

│   │

│   └── script.py.mako

│

└── alembic.ini
```

---

# 6. Migration Naming Convention

Format:

```text
<timestamp>_<description>.py
```

Examples:

```text
20260723_create_tenant_tables.py

20260724_add_agent_settings.py

20260725_create_vector_indexes.py
```

---

# 7. Initial Database Migration

The first migration creates:

```text
Core Tables

├── tenants

├── users

├── organizations

├── agents

├── calls

├── conversations

└── billing
```

---

# 8. Migration Lifecycle

```text
Create Migration

        |

        v

Review Code

        |

        v

Run Locally

        |

        v

Test Environment

        |

        v

Production Deployment
```

---

# 9. Creating Migration

Example:

```bash
alembic revision \
--autogenerate \
-m "create agent tables"
```

---

# 10. Applying Migration

Development:

```bash
alembic upgrade head
```

Production:

```bash
alembic upgrade head
```

---

# 11. Migration Version Table

Alembic maintains:

```text
alembic_version
```

Example:

```text
current_version:

a82f91d
```

---

# 12. Migration Rollback

Rollback command:

```bash
alembic downgrade -1
```

Example:

```text
Migration 3

↓

Migration 2
```

---

# 13. Migration Safety Rules

Never:

* Modify existing production migrations
* Delete applied migrations
* Manually change production schema

Always:

* Create new migration
* Review SQL
* Test rollback

---

# 14. Database Migration Environments

Three environments:

```text
Development

↓

Staging

↓

Production
```

---

# 15. Development Database

Purpose:

* Rapid iteration
* Testing
* Schema experiments

Example:

```text
Local PostgreSQL

or

Supabase Development Project
```

---

# 16. Staging Database

Purpose:

* Production-like testing
* Migration validation
* Performance testing

---

# 17. Production Database

Rules:

* Automated migrations only
* Approval required
* Backup before migration

---

# 18. CI/CD Migration Flow

```text
Pull Request

↓

Run Migration Test

↓

Create Temporary Database

↓

Apply Migration

↓

Run Tests

↓

Deploy
```

---

# 19. Database Migration Pipeline

```text
GitHub Actions

        |

        v

Build Backend

        |

        v

Run Alembic

        |

        v

Apply Schema Changes

        |

        v

Restart Services
```

---

# 20. Data Migration Strategy

Schema changes may require data movement.

Example:

Old:

```sql
full_name
```

New:

```sql
first_name

last_name
```

Process:

```text
Add Columns

↓

Copy Data

↓

Verify

↓

Remove Old Columns
```

---

# 21. Zero Downtime Migration

For production systems:

Use:

```text
Expand

↓

Migrate

↓

Contract
```

---

Example:

```text
Version 1

users.name


Version 2

users.first_name


Version 3

remove users.name
```

---

# 22. Large Table Migration

For:

* Calls
* Messages
* Analytics
* Audit Logs

Use:

* Batch updates
* Background jobs
* Partitioning

---

# 23. Migration Testing

Every migration should test:

```text
✓ Upgrade

✓ Downgrade

✓ Data integrity

✓ Performance

✓ Security policies
```

---

# 24. Supabase Migration Strategy

Supabase supports:

```text
supabase/migrations/

├── 001_initial.sql

├── 002_add_agents.sql

└── 003_add_vectors.sql
```

---

# 25. Choosing Migration Approach

Recommended:

```text
Application Schema:

Alembic


Supabase Features:

Supabase CLI migrations


Production:

Controlled CI/CD execution
```

---

# 26. Database Schema Documentation

Every migration should update:

* ERD diagrams
* Schema documentation
* API contracts
* Architecture documents

---

# 27. Emergency Migration Procedure

If urgent:

```text
Create Patch Migration

↓

Backup Database

↓

Apply Change

↓

Monitor

↓

Document
```

---

# 28. Migration Audit Trail

Track:

* Migration version
* Developer
* Timestamp
* Environment
* Result

---

# 29. Future Extensions

Support:

* Automated schema validation
* Database branching
* Migration previews
* Blue/green database deployments
* Tenant-specific migrations

---

# 30. Related Documents

| Document                                  | Purpose        |
| ----------------------------------------- | -------------- |
| 25_Database_Index_Performance_Strategy.md | Performance    |
| 26_Database_Backup_Disaster_Recovery.md   | Recovery       |
| 29_Database_Schema_Reference.md           | Schema catalog |
| 35_CI_CD                                  | Deployment     |

---

# 31. Conclusion

The Database Migration Strategy provides a safe and scalable method for evolving the AI Voice Agent SaaS database.

It enables:

* Controlled schema changes
* Production safety
* Automated deployment
* Database reliability

---

**End of Document**

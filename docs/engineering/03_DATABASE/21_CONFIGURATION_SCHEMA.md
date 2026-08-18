# Configuration Schema

**Document ID:** DB-CONFIG-021  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for configuration management across the AI Voice Agent SaaS platform.

The configuration subsystem manages dynamic settings that control:

- Tenant behavior
- AI agent configuration
- Feature availability
- System preferences
- Integration settings
- Runtime parameters
- Environment configuration

The configuration layer allows the platform to modify behavior without requiring application redeployment.

---

# 2. Configuration Architecture

High-level model:

             Configuration Request

                     |

              Configuration Service

                     |

      +--------------+--------------+

      |              |              |

   Tenant        Agent          System

   Config        Config         Config

      |              |              |

      +--------------+--------------+

                     |

              Runtime Services

---

# 3. Configuration Design Principles

## 3.1 Dynamic Configuration

Configuration values can change at runtime.

Examples:


Agent Voice

Business Hours

Feature Flags

API Limits

Workflow Settings


---

## 3.2 Hierarchical Configuration

Configuration follows inheritance:


System Default

    |

Tenant Override

    |

Agent Override

    |

Runtime Override


---

## 3.3 Version Controlled

Important configuration changes must maintain history.

---

# 4. Configuration Schema

Schema:


configuration


---

# 5. Configuration Tables Overview


configuration.settings

configuration.values

configuration.schemas

configuration.versions

configuration.feature_flags

configuration.environments

configuration.overrides

configuration.secrets

configuration.change_history


---

# 6. Configuration Settings

Table:


configuration.settings


Purpose:

Defines available configuration keys.

---

Examples:


agent.voice

agent.temperature

billing.currency

call.recording.enabled


---

Structure:

```sql
CREATE TABLE configuration.settings
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    key TEXT NOT NULL UNIQUE,

    description TEXT,

    data_type TEXT NOT NULL,

    default_value JSONB,

    created_at TIMESTAMPTZ DEFAULT now()
);
7. Configuration Values

Table:

configuration.values

Purpose:

Stores actual configuration values.

Structure:

CREATE TABLE configuration.values
(
id UUID PRIMARY KEY,

tenant_id UUID,

setting_id UUID NOT NULL,

value JSONB,

scope TEXT,

created_at TIMESTAMPTZ DEFAULT now(),

updated_at TIMESTAMPTZ DEFAULT now()
);
8. Configuration Scope

Supported scopes:

Scope	Purpose
system	Platform-wide
tenant	Customer organization
agent	Individual AI agent
workflow	Automation
user	User preference
runtime	Temporary value
9. Configuration Schemas

Table:

configuration.schemas

Purpose:

Defines validation rules.

Example:

{
 "type":"object",
 "properties":{
   "temperature":{
     "type":"number"
   }
 }
}

Structure:

CREATE TABLE configuration.schemas
(
id UUID PRIMARY KEY,

setting_id UUID NOT NULL,

schema_definition JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
10. Configuration Versions

Table:

configuration.versions

Purpose:

Tracks configuration history.

Example:

Agent Prompt Version 1

        |

Agent Prompt Version 2


Structure:

CREATE TABLE configuration.versions
(
id UUID PRIMARY KEY,

configuration_id UUID NOT NULL,

version_number INTEGER,

previous_value JSONB,

new_value JSONB,

changed_by UUID,

created_at TIMESTAMPTZ DEFAULT now()
);
11. Feature Flags

Table:

configuration.feature_flags

Purpose:

Controls feature rollout.

Examples:

new_agent_builder

advanced_rag

voice_cloning

beta_tools


Structure:

CREATE TABLE configuration.feature_flags
(
id UUID PRIMARY KEY,

tenant_id UUID,

flag_name TEXT,

enabled BOOLEAN DEFAULT false,

configuration JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
12. Feature Flag Lifecycle
Created

 |

Internal Testing

 |

Beta

 |

General Availability

 |

Deprecated

13. Environment Configuration

Table:

configuration.environments

Purpose:

Stores environment-specific settings.

Examples:

development

staging

production


Structure:

CREATE TABLE configuration.environments
(
id UUID PRIMARY KEY,

environment_name TEXT,

configuration JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
14. Configuration Overrides

Table:

configuration.overrides

Purpose:

Supports custom behavior.

Example:

Default:

GPT Model A


Tenant Override:

GPT Model B


Structure:

CREATE TABLE configuration.overrides
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

setting_id UUID NOT NULL,

override_value JSONB,

priority INTEGER DEFAULT 1
);
15. Secret References

Table:

configuration.secrets

Purpose:

Stores references to secret providers.

Secrets are NOT stored directly.

Supported:

Hashicorp Vault
Cloud Secret Manager
AWS Secrets Manager

Structure:

CREATE TABLE configuration.secrets
(
id UUID PRIMARY KEY,

tenant_id UUID,

secret_name TEXT,

secret_reference TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
16. Configuration Change History

Table:

configuration.change_history

Purpose:

Tracks configuration modifications.

Structure:

CREATE TABLE configuration.change_history
(
id UUID PRIMARY KEY,

tenant_id UUID,

setting_id UUID,

old_value JSONB,

new_value JSONB,

changed_by UUID,

created_at TIMESTAMPTZ DEFAULT now()
);
17. Agent Runtime Integration

Configuration lookup:

Agent Starts

     |

Load Configuration

     |

Resolve Overrides

     |

Build Runtime Settings

     |

Execute Agent

18. Workflow Integration

Workflow engine uses configuration for:

Retry policies
Timeout values
Action settings
Approval rules
19. Voice Platform Integration

Examples:

Call Recording Enabled

Voice Provider Settings

Transfer Rules

SIP Configuration

20. Multi-Tenant Requirements

Tenant-owned tables:

configuration.values

configuration.feature_flags

configuration.overrides

configuration.secrets


Require:

tenant_id UUID NOT NULL
21. Performance Requirements

High-volume tables:

Table	Growth
values	High
change_history	High
feature_flags	Medium
22. Index Requirements

Tenant lookup:

CREATE INDEX idx_configuration_tenant

ON configuration.values(tenant_id);

Setting lookup:

CREATE INDEX idx_configuration_setting

ON configuration.values(setting_id);
23. Security Requirements

Required:

Encryption
Secret isolation
Role-based access
Change auditing
Tenant separation
24. Future Extensions

Possible additions:

configuration.ai_policy

configuration.model_registry

configuration.prompt_registry

configuration.experiment_flags

configuration.remote_config

configuration.policy_engine

25. Related Documents

Previous:

20_SEARCH_SCHEMA.md

Related:

07_AGENT_SCHEMA.md

08_AGENT_RUNTIME_SCHEMA.md

14_WORKFLOW_SCHEMA.md

18_AUDIT_SCHEMA.md
End of Document
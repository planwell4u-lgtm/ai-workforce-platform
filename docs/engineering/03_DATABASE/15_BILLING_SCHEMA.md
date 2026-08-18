# Billing Schema

**Document ID:** DB-BILLING-015  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for subscription billing, usage metering, invoices, payments, and financial operations in the AI Voice Agent SaaS platform.

The billing domain manages:

- Customer subscriptions
- Pricing plans
- Usage tracking
- AI consumption costs
- Voice minutes
- Invoices
- Payments
- Credits
- Billing history

The system supports a multi-tenant SaaS billing model.

---

# 2. Billing Architecture

High-level model:

             Tenant

                |

          Subscription

                |

            Plan

                |

          Usage Events

                |

         Usage Metering

                |

           Invoice

                |

           Payment

---

# 3. Billing Design Principles

## 3.1 Usage-Based Billing

The platform tracks consumption from:

- Voice minutes
- AI model usage
- TTS characters
- STT processing
- Storage
- API usage
- Integrations

---

## 3.2 Immutable Financial Records

Financial records should never be modified.

Changes create:

- Adjustments
- Credits
- New invoice versions

---

## 3.3 Provider Independence

The schema supports:

- Stripe
- Paddle
- Custom billing providers

---

# 4. Billing Schema

Schema:


billing


---

# 5. Billing Tables Overview


billing.plans

billing.plan_features

billing.subscriptions

billing.subscription_items

billing.usage_events

billing.usage_records

billing.invoices

billing.invoice_items

billing.payments

billing.transactions

billing.credits


---

# 6. Pricing Plans

Table:


billing.plans


Purpose:

Defines available SaaS plans.

Examples:


Starter

Professional

Enterprise


---

Structure:

```sql
CREATE TABLE billing.plans
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name TEXT NOT NULL,

    description TEXT,

    price_monthly NUMERIC,

    currency TEXT DEFAULT 'USD',

    billing_interval TEXT,

    status TEXT DEFAULT 'active',

    created_at TIMESTAMPTZ DEFAULT now()
);
7. Plan Features

Table:

billing.plan_features

Purpose:

Defines included capabilities.

Examples:

Feature	Limit
Voice Minutes	5000
Agents	10
Knowledge Bases	20
Users	50

Structure:

CREATE TABLE billing.plan_features
(
id UUID PRIMARY KEY,

plan_id UUID NOT NULL,

feature_name TEXT NOT NULL,

limit_value NUMERIC,

created_at TIMESTAMPTZ DEFAULT now()
);
8. Subscription Model

Table:

billing.subscriptions

Purpose:

Links tenants to billing plans.

Example:

Acme Company

       |

Professional Plan


Structure:

CREATE TABLE billing.subscriptions
(
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

tenant_id UUID NOT NULL,

plan_id UUID NOT NULL,

status TEXT,

started_at TIMESTAMPTZ,

ended_at TIMESTAMPTZ,

created_at TIMESTAMPTZ DEFAULT now()
);
9. Subscription States
trialing

active

past_due

paused

cancelled

expired
10. Subscription Items

Table:

billing.subscription_items

Purpose:

Stores additional purchased services.

Examples:

Extra Voice Minutes

Additional Agents

Extra Storage

Premium Support


Structure:

CREATE TABLE billing.subscription_items
(
id UUID PRIMARY KEY,

subscription_id UUID NOT NULL,

item_name TEXT,

quantity INTEGER,

price NUMERIC

);
11. Usage Metering

Table:

billing.usage_events

Purpose:

Records every billable activity.

Examples:

Voice Call Started

AI Token Consumed

TTS Generated

Recording Stored


Structure:

CREATE TABLE billing.usage_events
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

event_type TEXT NOT NULL,

quantity NUMERIC,

metadata JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
12. Usage Event Types

Supported:

Event	Measurement
voice_minutes	Minutes
llm_tokens	Tokens
stt_seconds	Seconds
tts_characters	Characters
storage_bytes	Bytes
api_requests	Requests
13. Usage Records

Table:

billing.usage_records

Purpose:

Aggregated usage for billing periods.

Example:

July 2026

Voice:

25,000 minutes

Tokens:

20M


Structure:

CREATE TABLE billing.usage_records
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

period_start DATE,

period_end DATE,

usage_type TEXT,

total_quantity NUMERIC

);
14. Invoice Model

Table:

billing.invoices

Purpose:

Stores generated invoices.

Structure:

CREATE TABLE billing.invoices
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

invoice_number TEXT UNIQUE,

status TEXT,

subtotal NUMERIC,

tax NUMERIC,

total NUMERIC,

currency TEXT,

issued_at TIMESTAMPTZ,

due_at TIMESTAMPTZ
);
15. Invoice Status
draft

issued

paid

overdue

void

refunded
16. Invoice Items

Table:

billing.invoice_items

Purpose:

Line items on invoices.

Examples:

Professional Plan

10,000 Voice Minutes

Extra Storage


Structure:

CREATE TABLE billing.invoice_items
(
id UUID PRIMARY KEY,

invoice_id UUID NOT NULL,

description TEXT,

quantity NUMERIC,

unit_price NUMERIC,

amount NUMERIC

);
17. Payment Records

Table:

billing.payments

Purpose:

Tracks customer payments.

Structure:

CREATE TABLE billing.payments
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

invoice_id UUID,

provider TEXT,

provider_payment_id TEXT,

amount NUMERIC,

status TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
18. Transaction Ledger

Table:

billing.transactions

Purpose:

Immutable financial ledger.

Transaction types:

charge

refund

credit

adjustment


Structure:

CREATE TABLE billing.transactions
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

transaction_type TEXT,

amount NUMERIC,

currency TEXT,

reference_id UUID,

created_at TIMESTAMPTZ DEFAULT now()
);
19. Credit System

Table:

billing.credits

Purpose:

Manages prepaid credits.

Examples:

Enterprise Credit Balance

Promotional Credits

Usage Credits


Structure:

CREATE TABLE billing.credits
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

balance NUMERIC,

currency TEXT,

updated_at TIMESTAMPTZ DEFAULT now()
);
20. Billing Flow

Example:

Voice Call

    |

Usage Event

    |

Usage Aggregation

    |

Invoice Generation

    |

Payment Processing

    |

Ledger Entry

21. Integration With Voice System

Voice usage:

Call Completed

      |

Calculate Duration

      |

Create Usage Event

      |

Update Billing Meter

22. Integration With AI Runtime

AI usage:

LLM Request

      |

Token Count

      |

Usage Event

      |

Billing Calculation

23. Multi-Tenant Requirements

Tenant-owned tables:

subscriptions

usage_events

usage_records

invoices

payments

transactions

credits

Require:

tenant_id UUID NOT NULL
24. Security Requirements

Required:

Financial data encryption
Payment token protection
Audit logging
Restricted access
Compliance controls
25. Performance Requirements

High-volume tables:

Table	Growth
usage_events	Very High
transactions	High
invoice_items	Medium
26. Index Requirements

Tenant billing:

CREATE INDEX idx_billing_tenant
ON billing.subscriptions(tenant_id);

Usage lookup:

CREATE INDEX idx_usage_events_tenant
ON billing.usage_events(tenant_id);

Invoice lookup:

CREATE INDEX idx_invoice_tenant
ON billing.invoices(tenant_id);
27. Future Extensions

Possible additions:

billing.tax_rules

billing.discount_codes

billing.usage_forecasting

billing.cost_allocation

billing.enterprise_contracts

billing.revenue_analytics

28. Related Documents

Next:

16_ANALYTICS_SCHEMA.md

17_AUDIT_SCHEMA.md

18_NOTIFICATION_SCHEMA.md
End of Document
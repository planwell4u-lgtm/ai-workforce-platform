# Analytics Schema

**Document ID:** DB-ANALYTICS-016  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for analytics, reporting, metrics, and business intelligence capabilities in the AI Voice Agent SaaS platform.

The analytics domain transforms operational data into measurable insights across:

- Voice operations
- AI agent performance
- Customer interactions
- Revenue metrics
- Usage patterns
- System performance

The analytics layer supports:

- Dashboards
- Reports
- KPIs
- Trend analysis
- Machine learning evaluation
- Business intelligence

---

# 2. Analytics Architecture

High-level flow:


Operational Databases

    |

Event Collection

    |

Analytics Pipeline

    |

Aggregation Layer

    |

Analytics Database

    |

Dashboards / Reports


---

# 3. Analytics Design Principles

## 3.1 Separate Operational and Analytics Data

Operational schemas:


voice

conversation

agent_runtime

billing


Analytics schema:


analytics


---

## 3.2 Event-Driven Analytics

Analytics data is generated from:

- Call events
- Conversation events
- Usage events
- Billing events
- Runtime events

---

## 3.3 Historical Preservation

Analytics data should support:

- Time-based analysis
- Trend comparison
- Historical reporting
- Forecasting

---

# 4. Analytics Schema

Schema:


analytics


---

# 5. Analytics Tables Overview


analytics.events

analytics.call_metrics

analytics.agent_metrics

analytics.conversation_metrics

analytics.usage_metrics

analytics.revenue_metrics

analytics.daily_statistics

analytics.reports

analytics.dashboards


---

# 6. Analytics Events

Table:


analytics.events


Purpose:

Central analytics event stream.

---

Examples:


CALL_COMPLETED

AGENT_RESPONSE_GENERATED

CUSTOMER_SATISFACTION_RECORDED

TOKEN_USAGE_RECORDED

PAYMENT_COMPLETED


---

Structure:

```sql
CREATE TABLE analytics.events
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID NOT NULL,

    event_type TEXT NOT NULL,

    source TEXT NOT NULL,

    payload JSONB,

    created_at TIMESTAMPTZ DEFAULT now()
);
7. Call Metrics

Table:

analytics.call_metrics

Purpose:

Stores voice performance metrics.

Metrics:

Call duration
Wait time
Transfer rate
Completion rate
Failed calls

Structure:

CREATE TABLE analytics.call_metrics
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

call_session_id UUID NOT NULL,

duration_seconds INTEGER,

status TEXT,

transferred BOOLEAN,

created_at TIMESTAMPTZ DEFAULT now()
);
8. Agent Performance Metrics

Table:

analytics.agent_metrics

Purpose:

Measures AI agent effectiveness.

Metrics:

Response latency

Task completion

Tool success rate

Escalation rate

Accuracy score


Structure:

CREATE TABLE analytics.agent_metrics
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

agent_id UUID NOT NULL,

metric_name TEXT,

metric_value NUMERIC,

created_at TIMESTAMPTZ DEFAULT now()
);
9. Agent Quality Metrics

Tracked measurements:

Metric	Description
resolution_rate	Problems solved
transfer_rate	Human escalation
response_time	AI latency
satisfaction_score	Customer rating
error_rate	Failures
10. Conversation Metrics

Table:

analytics.conversation_metrics

Purpose:

Measures conversation quality.

Metrics:

Message count
Sentiment
Intent accuracy
Resolution status
Duration

Structure:

CREATE TABLE analytics.conversation_metrics
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

conversation_id UUID NOT NULL,

message_count INTEGER,

sentiment_score NUMERIC,

resolution_status TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
11. Usage Analytics

Table:

analytics.usage_metrics

Purpose:

Tracks resource consumption.

Examples:

Voice Minutes

LLM Tokens

TTS Characters

Storage Usage

API Requests


Structure:

CREATE TABLE analytics.usage_metrics
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

metric_type TEXT,

quantity NUMERIC,

period DATE
);
12. Revenue Analytics

Table:

analytics.revenue_metrics

Purpose:

Business financial analytics.

Metrics:

Monthly Revenue

Recurring Revenue

Customer Lifetime Value

Churn

Expansion Revenue


Structure:

CREATE TABLE analytics.revenue_metrics
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

metric_type TEXT,

amount NUMERIC,

period DATE
);
13. Daily Statistics

Table:

analytics.daily_statistics

Purpose:

Precomputed dashboard values.

Example:

Date:

2026-07-24


Calls:

12000


AI Minutes:

35000


Revenue:

$8500


Structure:

CREATE TABLE analytics.daily_statistics
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

stat_date DATE,

metric_name TEXT,

metric_value NUMERIC
);
14. Analytics Aggregation Pipeline

Process:

Operational Event

        |

Event Collector

        |

Analytics Processor

        |

Aggregation

        |

Analytics Tables

        |

Dashboard

15. Dashboard Model

Table:

analytics.dashboards

Purpose:

Stores dashboard definitions.

Example:

Voice Operations Dashboard

Agent Performance Dashboard

Billing Dashboard


Structure:

CREATE TABLE analytics.dashboards
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

name TEXT,

configuration JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
16. Reports

Table:

analytics.reports

Purpose:

Stores generated reports.

Examples:

Weekly Call Report

Monthly Revenue Report

Agent Quality Report


Structure:

CREATE TABLE analytics.reports
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

report_type TEXT,

parameters JSONB,

generated_at TIMESTAMPTZ
);
17. AI Evaluation Analytics

The system tracks:

Prompt Performance

Model Accuracy

Hallucination Rate

Tool Usage

Response Quality

18. Voice Analytics Integration

Flow:

Call Completed

      |

Call Metrics Generated

      |

Analytics Event

      |

Dashboard Update

19. Agent Runtime Analytics

Flow:

Agent Execution

      |

Runtime Events

      |

Performance Metrics

      |

AI Evaluation

20. Multi-Tenant Requirements

Tenant-owned tables:

analytics.events

analytics.call_metrics

analytics.agent_metrics

analytics.conversation_metrics

analytics.usage_metrics

analytics.revenue_metrics


Require:

tenant_id UUID NOT NULL
21. Data Retention

Analytics retention:

Raw Events:

30-180 days


Aggregated Metrics:

Long term

22. Partitioning Strategy

Large tables:

analytics.events

analytics.call_metrics

analytics.conversation_metrics


Partition by:

created_at

tenant_id

23. Index Requirements

Tenant analytics:

CREATE INDEX idx_analytics_tenant
ON analytics.events(tenant_id);

Time queries:

CREATE INDEX idx_analytics_date
ON analytics.events(created_at);
24. Security Requirements

Required:

Tenant isolation
Dashboard permissions
Data anonymization
Audit access
Export controls
25. Future Extensions

Possible additions:

analytics.ml_predictions

analytics.customer_segments

analytics.agent_benchmarks

analytics.forecasting

analytics.anomaly_detection

analytics.cost_analysis

26. Related Documents

Next:

17_AUDIT_SCHEMA.md

18_NOTIFICATION_SCHEMA.md

19_SEARCH_SCHEMA.md
End of Document
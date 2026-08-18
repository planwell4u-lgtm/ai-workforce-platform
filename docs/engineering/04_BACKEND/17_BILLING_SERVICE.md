# 17. Billing Service

**Version:** 2.0  
**Status:** Production Ready  
**Owner:** Platform Engineering

---

# 1. Purpose

The Billing Service manages the complete financial lifecycle of customer accounts within the Voice Agent SaaS platform.

It is responsible for subscription management, usage metering, invoicing, payment processing, taxation, credits, refunds, and financial reporting.

The Billing Service is designed to support multiple pricing models while maintaining complete tenant isolation and auditability.

---

# 2. Responsibilities

The Billing Service manages:

- Subscription plans
- Usage metering
- Customer billing
- Payment processing
- Invoice generation
- Credits
- Refunds
- Taxes
- Promotions
- Financial reporting
- Billing notifications
- Payment reconciliation

---

# 3. High-Level Architecture

```text
                Customer Dashboard
                        │
                        ▼
                 Billing Service
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
 Subscription      Usage Engine    Invoice Engine
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                Payment Provider
                        │
                        ▼
                     Stripe
                  (or others)
```

---

# 4. Billing Lifecycle

```text
Customer Signup

↓

Select Plan

↓

Subscription Created

↓

Usage Recorded

↓

Invoice Generated

↓

Payment Processed

↓

Receipt Issued

↓

Renewal
```

---

# 5. Subscription Plans

Each tenant subscribes to a billing plan.

Example plans:

- Free
- Starter
- Professional
- Business
- Enterprise
- Custom

Each plan defines:

- Monthly price
- Annual price
- Included usage
- Feature limits
- User limits
- Agent limits
- Storage limits
- API limits

---

# 6. Supported Billing Models

The platform supports:

- Fixed monthly subscription
- Fixed annual subscription
- Usage-based billing
- Per-user pricing
- Per-agent pricing
- Per-minute voice billing
- Per-message billing
- Hybrid billing
- Enterprise contracts

---

# 7. Usage Metering

The Billing Service records billable usage.

Examples:

- Voice minutes
- AI tokens
- API requests
- Active agents
- Storage usage
- Knowledge uploads
- SMS messages
- Emails sent
- Phone numbers
- Recording storage

---

# 8. Usage Collection

Usage events originate from:

- Voice Platform
- Agent Runtime
- API Gateway
- Storage Service
- Notification Service
- Workflow Service

Example:

```text
Call Completed

↓

Duration Calculated

↓

Usage Event

↓

Billing Service

↓

Monthly Usage
```

---

# 9. Subscription States

```text
Trial

↓

Active

↓

Past Due

↓

Suspended

↓

Cancelled

↓

Expired
```

---

# 10. Invoice Generation

Invoices contain:

- Subscription charges
- Usage charges
- Discounts
- Taxes
- Credits
- Previous balance
- Total amount
- Payment status

Invoices are generated automatically according to the billing cycle.

---

# 11. Payment Processing

Supported operations:

- Initial payment
- Subscription renewal
- One-time payment
- Refund
- Credit application
- Failed payment retry

Payment processing is delegated to an external payment provider.

---

# 12. Payment Providers

Supported providers include:

- Stripe
- Paddle
- PayPal (future)
- Custom enterprise gateways

The provider layer should remain abstracted through the Integration Service.

---

# 13. Discounts & Promotions

Supported promotion types:

- Percentage discount
- Fixed discount
- Trial extension
- Coupon codes
- Promotional credits
- Referral rewards

---

# 14. Credits

Credits may be issued for:

- Service outages
- Promotional campaigns
- Manual adjustments
- Customer support resolutions
- Referral bonuses

Credits are automatically applied to future invoices.

---

# 15. Refunds

Refunds support:

- Full refund
- Partial refund
- Manual refund
- Automated refund
- Payment reversal

Every refund must generate an audit record.

---

# 16. Tax Management

The Billing Service supports:

- VAT
- GST
- Sales tax
- Tax exemptions
- Regional tax rules
- Tax-inclusive pricing
- Tax-exclusive pricing

Tax calculations may be delegated to the payment provider where appropriate.

---

# 17. Database Tables

The Billing Service owns:

```text
billing_accounts

subscription_plans

subscriptions

subscription_features

usage_records

billing_cycles

invoices

invoice_items

payments

payment_methods

refunds

credits

discounts

coupons

tax_records

billing_events

billing_audit_logs
```

---

# 18. Payment Events

Typical events include:

- Subscription Created
- Subscription Renewed
- Payment Authorized
- Payment Captured
- Payment Failed
- Invoice Generated
- Invoice Paid
- Refund Issued
- Credit Applied

These events are published to the platform event bus.

---

# 19. Security

Security requirements include:

- PCI-compliant payment processing
- Encrypted payment metadata
- No storage of card numbers
- Tokenized payment methods
- Role-based billing permissions
- Audit logging
- Secure webhook verification

---

# 20. Monitoring

Key metrics include:

- Monthly recurring revenue (MRR)
- Annual recurring revenue (ARR)
- Active subscriptions
- Churn rate
- Failed payments
- Invoice generation time
- Payment success rate
- Credit usage
- Refund volume

---

# 21. Failure Handling

If billing operations fail:

- Retry transient payment failures
- Queue invoice generation
- Notify administrators
- Record audit events
- Preserve financial consistency
- Prevent duplicate charges through idempotency

---

# 22. Integration Points

The Billing Service integrates with:

- Authentication Service
- Tenant Service
- Integration Service
- Notification Service
- Workflow Service
- Event Bus
- Payment Providers
- Accounting Systems
- Observability Platform

---

# 23. Future Enhancements

Planned capabilities include:

- Multi-currency billing
- Regional pricing
- Usage forecasting
- AI-powered cost optimization
- Revenue analytics
- Self-service billing portal
- Enterprise invoicing
- Purchase orders
- Cost allocation by department

---

# 24. Design Principles

The Billing Service follows these principles:

- Financial accuracy
- Immutable financial records
- Idempotent payment operations
- Tenant isolation
- Secure payment processing
- Event-driven architecture
- Horizontal scalability
- Complete auditability
- Provider independence
- Regulatory compliance

---

# 25. Example Billing Flow

```text
Customer Makes Voice Call

↓

Call Ends

↓

Usage Event Created

↓

Billing Service Records Minutes

↓

Monthly Invoice Generated

↓

Stripe Charges Customer

↓

Payment Successful

↓

Receipt Sent

↓

Billing Event Published
```

---

# 26. Summary

The Billing Service is the financial backbone of the Voice Agent SaaS platform. It manages subscriptions, usage metering, invoicing, payments, taxes, credits, and financial events while ensuring accuracy, security, and compliance. Through integration with external payment providers and the platform's event-driven architecture, it delivers scalable and reliable billing for organizations of all sizes.
# 03 Sales Agent
# Sales Agent Example

**Version:** 2.0

---

# 1. Overview

This document provides a production-ready example of an AI-powered Sales Voice Agent for the Voice Agent SaaS platform.

The Sales Agent is designed to engage prospective customers, qualify leads, answer product-related questions, recommend suitable solutions, schedule follow-up meetings, and transfer high-value opportunities to human sales representatives.

Typical use cases include:

- Inbound sales inquiries
- Product information
- Lead qualification
- Pricing discussions
- Feature recommendations
- Demo scheduling
- Follow-up calls
- Human sales transfer

---

# 2. Architecture

```
Incoming Call

      │

      ▼

LiveKit Voice Session

      │

      ▼

Sales Agent Runtime

      │

 ┌────┼───────────┐

 ▼    ▼           ▼

STT   LLM         TTS

      │

      ▼

CRM / Product Catalog

      │

      ▼

Calendar Service

      │

      ▼

Human Sales Team
```

---

# 3. Objectives

The Sales Agent should:

- Welcome prospects
- Understand business needs
- Qualify sales opportunities
- Recommend products
- Explain pricing
- Handle objections
- Schedule demos
- Capture lead information
- Transfer qualified leads

---

# 4. Supported Intents

Examples include:

- Product inquiry
- Pricing request
- Feature comparison
- Demo request
- Sales consultation
- Existing customer upgrade
- Partnership inquiry
- Speak with sales representative

---

# 5. Conversation Flow

```
Incoming Call

      │

Greeting

      │

Identify Needs

      │

Lead Qualification

      │

Recommend Solution

      │

Questions?

      │

Demo Required?

 ┌────┴────┐

 │         │

No        Yes

 │         │

Close   Schedule Demo

 │         │

Goodbye Human Follow-up
```

---

# 6. Example System Prompt

```text
You are an AI Sales Consultant.

Your goals are:

- Understand customer requirements.
- Recommend the most appropriate solution.
- Explain features clearly.
- Never pressure customers.
- Capture lead information accurately.
- Schedule demonstrations when appropriate.
- Transfer high-value opportunities to a human sales representative.
```

---

# 7. Greeting Example

```
Agent:

Hello, and thank you for contacting us.

I'm your AI sales assistant.

I'd be happy to answer your questions and help you find the right solution.

What are you looking for today?
```

---

# 8. Lead Qualification

Example questions:

- What type of business do you operate?
- How many users will need access?
- What challenges are you trying to solve?
- Are you currently using another solution?
- When are you planning to implement a new system?

Example flow:

```
Prospect

      │

Business Type

      │

Company Size

      │

Requirements

      │

Budget

      │

Timeline

      │

Qualified Lead
```

---

# 9. Product Recommendation

The agent should use product information to recommend suitable offerings.

Example:

```
Customer:

We need an AI receptionist.

↓

Agent:

Based on your requirements, our Voice Receptionist solution would be a strong fit.

It supports inbound calls, appointment scheduling, call routing, and integration with your existing systems.
```

Recommendations should be based on verified product data.

---

# 10. Pricing Discussions

The Sales Agent may:

- Explain pricing plans
- Compare available packages
- Describe included features
- Estimate costs based on usage

The agent should avoid making pricing commitments beyond approved information.

---

# 11. CRM Integration

The agent may perform:

- Lead creation
- Contact updates
- Opportunity creation
- Activity logging
- Follow-up reminders

Example workflow:

```
Conversation

      │

Capture Lead

      │

Create CRM Record

      │

Assign Sales Owner

      │

Schedule Follow-up
```

---

# 12. Demo Scheduling

If the customer requests a demonstration:

```
Demo Requested

      │

Check Calendar

      │

Available Slots

      │

Customer Selects Time

      │

Create Meeting

      │

Send Confirmation
```

Calendar integrations may include:

- Google Calendar
- Microsoft Outlook
- Internal scheduling systems

---

# 13. Handling Objections

Examples:

Customer:

```
Your solution seems expensive.
```

Agent:

```
I understand cost is an important consideration.

Would it help if I explained the differences between our plans or discussed the features included in each option?
```

The agent should remain informative rather than argumentative.

---

# 14. Human Transfer

Transfer conditions:

- Enterprise opportunity
- Custom pricing request
- Contract negotiation
- Procurement discussion
- Customer request
- Low confidence response

Transfer workflow:

```
Qualified Opportunity

        │

Transfer Context

        │

Available Sales Representative

        │

Live Conversation
```

Conversation notes should accompany the transfer.

---

# 15. Security

The Sales Agent must:

- Protect customer information
- Validate access before exposing account details
- Respect tenant isolation
- Avoid collecting unnecessary personal data
- Log sales activities securely

---

# 16. Performance Targets

| Metric | Target |
|--------|-------:|
| Greeting latency | < 1 second |
| STT latency | < 500 ms |
| AI response | < 2 seconds |
| CRM lookup | < 1 second |
| Calendar lookup | < 2 seconds |
| Total response | < 3 seconds |

---

# 17. Observability

Monitor:

- Lead conversion rate
- Demo bookings
- Call duration
- Product recommendations
- Human transfers
- CRM synchronization
- AI response latency
- Customer satisfaction

---

# 18. Testing

Validate:

- Lead qualification
- Product recommendations
- Pricing responses
- CRM integration
- Calendar booking
- Human transfer
- API failures
- Conversation quality
- Permission enforcement

---

# 19. Best Practices

Always:

- Listen before recommending
- Ask qualifying questions
- Use verified product information
- Capture complete lead details
- Summarize agreed next steps
- Escalate enterprise opportunities

Avoid:

- High-pressure sales tactics
- Guessing pricing
- Promising unavailable features
- Skipping lead qualification
- Ignoring customer concerns

---

# 20. Example End-to-End Workflow

```
Prospect Calls

        │

Greeting

        │

Needs Assessment

        │

Lead Qualification

        │

Recommend Solution

        │

Answer Questions

        │

Book Demo

        │

Create CRM Lead

        │

Transfer (Optional)

        │

Goodbye

        │

Call Ends
```

---

# 21. Summary

The Sales Agent demonstrates how AI voice assistants can automate the early stages of the sales process by qualifying leads, recommending products, integrating with CRM and scheduling systems, and handing qualified opportunities to human sales teams. This approach improves response times, increases consistency, and allows sales representatives to focus on high-value engagements.
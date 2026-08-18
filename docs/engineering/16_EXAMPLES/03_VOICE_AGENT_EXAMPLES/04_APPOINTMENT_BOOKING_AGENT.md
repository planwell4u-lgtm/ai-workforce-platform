# 04 Appointment Booking Agent
# Appointment Booking Agent Example

**Version:** 2.0

---

# 1. Overview

This document provides a production-ready example of an AI-powered Appointment Booking Voice Agent for the Voice Agent SaaS platform.

The Appointment Booking Agent is designed to automate appointment scheduling by interacting with callers, checking availability, booking appointments, rescheduling or canceling existing bookings, and sending confirmations.

Typical use cases include:

- Medical clinics
- Hospitals
- Dental practices
- Beauty salons
- Professional services
- Legal offices
- Financial advisors
- Government offices
- Educational institutions

---

# 2. Architecture

```
Incoming Call

      │

      ▼

LiveKit Voice Session

      │

      ▼

Appointment Agent

      │

 ┌────┼───────────┐

 ▼    ▼           ▼

STT   LLM         TTS

      │

      ▼

Scheduling Service

      │

      ▼

Calendar System

      │

      ▼

Notification Service
```

---

# 3. Primary Responsibilities

The Appointment Booking Agent should:

- Greet callers
- Understand booking requests
- Collect appointment details
- Check calendar availability
- Book appointments
- Reschedule appointments
- Cancel appointments
- Send confirmations
- Escalate when necessary

---

# 4. Supported Intents

Examples include:

- Book appointment
- Reschedule appointment
- Cancel appointment
- Check availability
- Office hours
- Service information
- Speak with staff

---

# 5. Conversation Flow

```
Incoming Call

      │

Greeting

      │

Identify Request

      │

Collect Details

      │

Check Availability

      │

Available?

 ┌────┴─────┐

 │          │

No         Yes

 │          │

Suggest    Confirm

Another    Booking

 │          │

Finish     Send Confirmation
```

---

# 6. Example System Prompt

```text
You are an AI Appointment Booking Assistant.

Your responsibilities are:

- Help callers schedule appointments.
- Confirm all booking details before finalizing.
- Never book unavailable time slots.
- Offer alternative times when needed.
- Be polite, clear, and efficient.
- Transfer callers to staff if required.
```

---

# 7. Greeting Example

```
Agent:

Hello, thank you for calling.

I'm your AI appointment assistant.

I'd be happy to help you schedule, change, or cancel an appointment.

How may I assist you today?
```

---

# 8. Information Collection

Before booking, collect:

- Customer name
- Phone number
- Email address (optional)
- Requested service
- Preferred date
- Preferred time
- Additional notes (optional)

Example:

```
Agent:

What service would you like to book?

↓

Customer:

General consultation.

↓

Agent:

What day would you prefer?
```

---

# 9. Availability Check

Workflow:

```
Requested Date

      │

Query Calendar

      │

Available?

 ┌────┴────┐

 │         │

Yes       No

 │         │

Reserve   Offer Alternatives
```

Availability should be verified in real time.

---

# 10. Booking Confirmation

Before creating the appointment:

```
Agent:

I'd like to confirm your appointment.

General consultation

Tuesday, August 11

10:30 AM

Is everything correct?
```

Only create the booking after confirmation.

---

# 11. Booking Creation

```
Confirmed

     │

Create Appointment

     │

Generate Booking ID

     │

Update Calendar

     │

Send Confirmation

     │

Complete
```

Example confirmation:

```
Your appointment has been successfully booked.

Your confirmation number is AP-10425.
```

---

# 12. Rescheduling

Workflow:

```
Existing Appointment

        │

Verify Identity

        │

Retrieve Booking

        │

Select New Time

        │

Update Calendar

        │

Send Confirmation
```

---

# 13. Cancellation

Workflow:

```
Cancellation Request

        │

Verify Booking

        │

Confirm Cancellation

        │

Release Time Slot

        │

Send Confirmation
```

Example:

```
Your appointment has been cancelled successfully.

We'd be happy to help you schedule another appointment whenever you're ready.
```

---

# 14. Calendar Integrations

Supported integrations may include:

- Google Calendar
- Microsoft Outlook
- Microsoft Exchange
- CalDAV
- Internal scheduling platform

All updates should remain synchronized across systems.

---

# 15. Notification Service

After booking:

```
Appointment Created

        │

Email Confirmation

        │

SMS Confirmation

        │

Calendar Invite

        │

Reminder Scheduling
```

Optional reminders:

- 24 hours before
- 2 hours before
- 30 minutes before

---

# 16. Human Escalation

Transfer when:

- Customer requests staff
- Calendar service unavailable
- Complex scheduling request
- Double-booking conflict
- Special accommodations required

Workflow:

```
Transfer Request

        │

Share Booking Context

        │

Human Staff
```

---

# 17. Security

The Appointment Booking Agent should:

- Verify identity before modifying bookings
- Protect customer information
- Validate tenant ownership
- Log appointment activity
- Avoid exposing calendar details beyond authorized information

---

# 18. Performance Targets

| Metric | Target |
|--------|-------:|
| Greeting latency | < 1 second |
| STT latency | < 500 ms |
| Calendar lookup | < 1 second |
| Booking creation | < 2 seconds |
| Confirmation delivery | < 5 seconds |
| Total response | < 3 seconds |

---

# 19. Testing

Validate:

- Appointment creation
- Calendar synchronization
- Availability lookup
- Rescheduling
- Cancellation
- Notification delivery
- Human transfer
- Duplicate booking prevention
- Error recovery

---

# 20. Best Practices

Always:

- Confirm booking details
- Check real-time availability
- Prevent double bookings
- Offer alternative time slots
- Send confirmations
- Keep conversations concise
- Escalate complex requests

Avoid:

- Booking unavailable slots
- Skipping confirmation
- Exposing confidential calendar information
- Guessing availability
- Creating duplicate appointments

---

# 21. Example End-to-End Workflow

```
Customer Calls

        │

Greeting

        │

Collect Booking Details

        │

Check Calendar

        │

Offer Available Times

        │

Customer Selects Time

        │

Confirm Details

        │

Create Appointment

        │

Send Confirmation

        │

Schedule Reminder

        │

Goodbye

        │

Call Ends
```

---

# 22. Summary

The Appointment Booking Agent automates the complete appointment lifecycle, from scheduling and confirmation to rescheduling and cancellation. By integrating with calendar systems and notification services, it delivers a seamless, reliable, and production-ready booking experience while reducing manual workload for staff.
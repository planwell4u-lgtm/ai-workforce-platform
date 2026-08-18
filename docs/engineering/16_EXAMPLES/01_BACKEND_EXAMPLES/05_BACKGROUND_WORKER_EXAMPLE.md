# 05 Background Worker Example
# Background Worker Example

**Version:** 2.0

---

# 1. Overview

This document provides a production-ready example of implementing background workers in the Voice Agent SaaS platform.

Background workers execute asynchronous tasks outside the request-response lifecycle, improving API responsiveness and enabling reliable processing of long-running or resource-intensive operations.

Typical use cases include:

- AI processing
- Call transcription
- RAG document indexing
- Embedding generation
- Email notifications
- Webhook delivery
- Report generation
- File processing
- Data synchronization
- Scheduled maintenance

---

# 2. Architecture

```
                 Client
                    │
                    ▼
             FastAPI Service
                    │
         Validate Request
                    │
          Store Database Record
                    │
                    ▼
            Publish Background Job
                    │
     ┌──────────────┴──────────────┐
     ▼                             ▼
 Redis Queue                 Job Scheduler
     │
     ▼
 Background Worker
     │
     ▼
 Execute Task
     │
     ▼
 Update Database
     │
     ▼
 Publish Event / Notify Client
```

---

# 3. Recommended Technologies

| Component | Technology |
|-----------|------------|
| Queue Broker | Redis |
| Worker Framework | Celery / Dramatiq / RQ |
| Scheduler | Celery Beat / APScheduler |
| Database | PostgreSQL |
| Monitoring | Prometheus |
| Logging | Structured Logging |

---

# 4. Project Structure

```
app/

workers/

    __init__.py

    celery_app.py

    tasks/

        transcription.py

        embeddings.py

        notifications.py

        webhooks.py

        reports.py

services/

repositories/

models/

main.py
```

---

# 5. Queue Configuration Example

```python
from celery import Celery

celery = Celery(
    "voice_agent",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"]
)
```

---

# 6. Task Example

```python
from app.workers.celery_app import celery


@celery.task(
    bind=True,
    max_retries=5
)
def generate_embeddings(
    self,
    document_id: str
):

    print(
        f"Processing {document_id}"
    )

    return True
```

---

# 7. Publishing a Job

```python
generate_embeddings.delay(
    document_id
)
```

The API returns immediately while processing continues in the background.

---

# 8. Example Workflow

```
Upload Document

      │

Save Metadata

      │

Return HTTP 202

      │

Queue Job

      │

Worker Starts

      │

Extract Text

      │

Generate Embeddings

      │

Store Vectors

      │

Mark Complete

      │

Emit Event
```

---

# 9. Retry Strategy

Transient failures should automatically retry.

Example:

```python
raise self.retry(
    countdown=30
)
```

Recommended retry policy:

| Attempt | Delay |
|----------|------:|
| 1 | 30 sec |
| 2 | 60 sec |
| 3 | 120 sec |
| 4 | 300 sec |
| 5 | 600 sec |

---

# 10. Idempotency

Background tasks must be idempotent.

Example:

```
Job Received

↓

Check Already Processed?

↓

Yes → Exit

↓

No

↓

Continue Processing
```

Store processing status in the database to avoid duplicate execution.

---

# 11. Error Handling

Workers should:

- Log failures
- Retry transient errors
- Mark permanent failures
- Generate alerts for repeated failures
- Preserve error details for debugging

Example:

```python
try:

    process_document()

except TemporaryError:

    raise self.retry()

except Exception:

    logger.exception(
        "Background task failed"
    )

    raise
```

---

# 12. Logging

Every task should include structured logging.

Example:

```python
logger.info(

    "embedding_generation_started",

    extra={

        "job_id": job_id,

        "tenant_id": tenant_id,

        "document_id": document_id

    }

)
```

Include:

- Job ID
- Correlation ID
- Tenant ID
- Worker name
- Duration
- Retry count

---

# 13. Monitoring

Monitor:

- Queue depth
- Processing rate
- Processing duration
- Success rate
- Failure rate
- Retry count
- Worker availability

Recommended metrics:

```
worker_jobs_total

worker_jobs_failed

worker_job_duration_seconds

worker_retry_total

worker_queue_size
```

---

# 14. Scheduled Jobs

Examples:

- Cleanup expired sessions
- Archive old conversations
- Generate billing reports
- Rotate logs
- Refresh AI models
- Rebuild search indexes

Example scheduler:

```
Daily 02:00

↓

Cleanup Task

↓

Archive Records

↓

Vacuum Database

↓

Generate Report
```

---

# 15. Scaling Workers

Workers should scale horizontally.

```
Redis Queue

       │

 ┌─────┼─────┐

 ▼     ▼     ▼

Worker1 Worker2 Worker3

       │

 Parallel Processing
```

Scale based on:

- Queue size
- CPU utilization
- Memory usage
- Processing latency

---

# 16. Security

Workers should:

- Validate job payloads
- Verify tenant ownership
- Use least-privilege credentials
- Never execute arbitrary code
- Encrypt sensitive data
- Avoid logging secrets

---

# 17. Testing

Background worker tests should cover:

- Successful execution
- Retry behavior
- Permanent failure handling
- Idempotency
- Database updates
- Queue publishing
- Event generation
- Performance under load

---

# 18. Best Practices

Always:

- Keep tasks small
- Make tasks idempotent
- Use retries with exponential backoff
- Log structured events
- Monitor queue health
- Limit task execution time
- Handle failures gracefully

Avoid:

- Long database transactions
- Blocking network calls without timeouts
- Large job payloads
- Business logic inside queue configuration
- Infinite retries

---

# 19. Common Use Cases

Background workers are used for:

- Voice transcription
- AI summarization
- RAG indexing
- Memory consolidation
- Call recording processing
- Email delivery
- SMS notifications
- Webhook retries
- Analytics aggregation
- Billing calculations

---

# 20. Summary

Background workers enable reliable asynchronous processing across the Voice Agent SaaS platform. By offloading long-running operations from API requests, they improve responsiveness, scalability, and fault tolerance while supporting production-grade monitoring, retry handling, and horizontal scaling.
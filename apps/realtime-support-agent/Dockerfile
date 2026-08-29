FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY agent.py faq_context.py /app/

RUN pip install --no-cache-dir "livekit-agents[openai]>=1.5,<2"

CMD ["python", "agent.py", "start"]

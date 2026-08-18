FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml requirements.txt ./
COPY apps/backend/src ./apps/backend/src
COPY packages/agent/python/src ./packages/agent/python/src
COPY packages/conversation/python/src ./packages/conversation/python/src
COPY packages/data/python/src ./packages/data/python/src
COPY packages/integration/python/src ./packages/integration/python/src
COPY packages/voice/python/src ./packages/voice/python/src

RUN python -m pip install --upgrade pip \
    && python -m pip install .

EXPOSE 8080

CMD ["python", "-m", "ai_workforce_backend.server"]

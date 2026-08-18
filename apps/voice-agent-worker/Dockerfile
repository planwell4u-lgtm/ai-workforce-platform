FROM ai-workforce-backend:livekit-sandbox

RUN apt-get update \
    && apt-get install --yes --no-install-recommends espeak-ng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
CMD ["python", "apps/voice-agent-worker/worker.py"]

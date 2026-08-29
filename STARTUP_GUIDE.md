# Planwell local startup guide

Use this guide to start the local Planwell support application after a restart.
It starts two Docker containers:

| Service | Address | Purpose |
|---|---|---|
| Backend | `http://localhost:8080` | Authenticated support API and LiveKit token service |
| Frontend | `http://localhost:3000` | Planwell support web app |

This repository does not currently include an active Docker Compose file, so
start the two containers separately using the commands below.

## 1. Before starting

1. Open **Docker Desktop** and wait until it says Docker is running.
2. Open PowerShell in the project folder:

   ```powershell
   cd D:\project
   ```

3. Confirm your private `.env` file is still present. It must contain the
   Auth0, database, support-FAQ, Jira (if used), and LiveKit values already
   configured for this project. Do not paste this file into chat or commit it.

4. Confirm Docker is available:

   ```powershell
   docker version
   docker ps
   ```

## 2. Stop an older local run

Run this only if containers with these names already exist:

```powershell
docker stop planwell-backend planwell-frontend
docker rm planwell-backend planwell-frontend
```

If Docker says a container does not exist, that is fine.

## 3. Build the current application images

From `D:\project`, run:

```powershell
docker build -t planwell-backend:local -f apps/backend/Dockerfile .
docker build -t planwell-frontend:local -f apps/frontend/Dockerfile .
```

Wait for each command to finish successfully before moving on.

## 4. Start the backend

The backend needs the approved FAQ file mounted read-only inside its container.
Run this as one command from `D:\project`:

```powershell
docker run -d --name planwell-backend --env-file .env -e SUPPORT_FAQ_PATH=/app/approved-support-faqs.jsonl -v "${PWD}\packages\agent\knowledge\staging-demo\approved-support-faqs.jsonl:/app/approved-support-faqs.jsonl:ro" -p 8080:8080 planwell-backend:local
```

Check its health:

```powershell
Invoke-WebRequest http://localhost:8080/healthz | Select-Object -Expand Content
```

Expected result:

```json
{"status":"ok"}
```

If it does not start, inspect the backend messages:

```powershell
docker logs planwell-backend
```

## 5. Start the frontend

Run:

```powershell
docker run -d --name planwell-frontend --env-file .env -e API_BASE_URL=http://host.docker.internal:8080 -p 3000:3000 planwell-frontend:local
```

Then open [http://localhost:3000](http://localhost:3000) and sign in through
Auth0.

If the page does not open, inspect the frontend messages:

```powershell
docker logs planwell-frontend
```

## 6. Normal local checks

After signing in, verify these in order:

1. Ask an approved FAQ question, such as **How can I track my order?**
2. Ask an unsupported question, such as **What is your refund policy?** The
   app should offer human support rather than invent an answer.
3. Open **Admin** only if you need to review saved conversations or create an
   authorized Jira ticket.
4. Do not use a real customer’s personal, account, payment, or order data in
   a test.

## 7. Realtime agent FAQ rehearsal — separately gated

The isolated LiveKit agent `customer-support-realtime-v1` is already deployed.
The backend prefers the `LIVEKIT_ISOLATION_*` values in `.env` when they are
present, so restart the backend using steps 2–4 after changing those values.

To test the realtime agent:

1. Sign in at `http://localhost:3000`.
2. Select **Test Cloud voice agent**.
3. Enter a generic approved topic, such as `order tracking`.
4. Read the microphone notice and choose **Enable microphone and start Cloud
   agent** only when you explicitly consent to sharing live audio.
5. Confirm the agent answers only from the approved excerpt. Stop the voice
   session when finished.

The voice test does **not** enable phone routing, call recording, customer-data
access, tools, Jira escalation, or outbound calling.

## 8. Useful status commands

```powershell
docker ps
docker logs --tail 100 planwell-backend
docker logs --tail 100 planwell-frontend
docker stop planwell-backend planwell-frontend
```

## 9. Common problems

| Symptom | First check |
|---|---|
| Port `8080` or `3000` is busy | Run `docker ps`; stop the older Planwell container before starting a replacement. |
| Backend health check fails | Run `docker logs planwell-backend`; confirm `.env` and the mounted FAQ path are available. |
| Frontend cannot reach support service | Confirm backend health first, then confirm the frontend was started with `API_BASE_URL=http://host.docker.internal:8080`. |
| Sign-in fails | Confirm the Auth0 settings in `.env` and the allowed local callback/origin configuration. |
| Voice test does not start | Confirm the backend was restarted after the `LIVEKIT_ISOLATION_*` settings were added, then check the LiveKit agent status. |

## 10. Stop for the day

```powershell
docker stop planwell-backend planwell-frontend
```

Stopping the containers does not delete your database or the deployed LiveKit
agent. Start again later from step 4 if the images are already built, or from
step 3 after code changes.

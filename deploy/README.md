# Oracle cloud-pilot deployment and recovery

## Scope and boundaries

The Oracle pilot serves `https://planwell.online` through Caddy. The frontend
and backend remain on the Docker-internal network; the only public application
entrypoint is the HTTPS gateway. This procedure does not enable telephony,
recording, customer-data access, tools, escalation, or outbound calling.

The server checkout is `/home/opc/planwell` and the Compose files are in
`/home/opc/planwell/deploy`. Keep the server `.env` file local to the server
and out of source control.

## Prerequisites

- An approved SSH private key for the `opc` user.
- The target server address: `130.210.46.184`.
- The intended source changes reviewed and validated locally.

Confirm access before a deployment:

```powershell
ssh -i <private-key-path> -o BatchMode=yes -o IdentitiesOnly=yes opc@130.210.46.184 "pwd"
```

The expected result is `/home/opc`.

## Deploy a targeted change

Copy only the changed source file or files into the matching path below
`/home/opc/planwell`. For example, to publish an Access Management UI change:

```powershell
scp -i <private-key-path> apps/frontend/app/access-management/page.tsx `
  opc@130.210.46.184:/home/opc/planwell/apps/frontend/app/access-management/page.tsx
```

Rebuild and recreate only the affected service. Run these commands from the
server checkout:

```sh
cd /home/opc/planwell/deploy
sudo docker compose --env-file ../.env up --build -d --force-recreate frontend
```

For backend-only changes, replace `frontend` with `backend`.

## Verify after deployment

Confirm that the affected container is running:

```sh
sudo docker compose --env-file ../.env ps
```

Verify backend health through the same HTTPS gateway used by the application:

```sh
curl -fsS --max-time 10 \
  --resolve planwell.online:443:127.0.0.1 \
  https://planwell.online/api/healthz
```

The expected response is `{"status":"ok"}`.

Complete the relevant signed-in browser check. For access-control changes,
verify both of the following with a non-owner account:

- Support returns the approved FAQ answer.
- Access Management shows an access-denied screen and no owner controls.

## Recovery

- If a service does not become healthy after a targeted rebuild, inspect its
  Compose logs and restore the last known-good source before recreating only
  that service.
- If SSH fails, first retry the original instance key for `opc`. Do not create
  broad remote-command permissions as an access-recovery shortcut.
- If the original key is no longer authorized, use a separately approved,
  temporary serial-console recovery procedure to restore the key, then remove
  any temporary access artifact when finished.
- Record the deployment time, changed paths, health result, and browser
  validation outcome in the project status record.

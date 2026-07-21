# TeqFarm incident runbook

## Application unavailable

1. Check `docker compose ps` and `docker compose logs --tail=200 nginx backend db`.
2. Verify free disk space and `/health/`.
3. If PostgreSQL is unhealthy, stop writes, preserve volumes, and investigate before restarting repeatedly.
4. Restart only the failed service with `docker compose restart <service>`.

## Incorrect stock or bird balance

Do not edit balance columns directly. Preserve the relevant transactions, daily records, sales, and audit actor. Correct the source record or create an explicit adjustment through the API, then document the reason.

## Suspected account compromise

Deactivate the user, change affected credentials, rotate `DJANGO_SECRET_KEY` if token signing may be exposed, restart the backend, and review proxy/application logs.

## Restore

Restore into a temporary environment first, validate row counts and recent transactions, then schedule production restoration. Pair the SQL dump with its matching media archive.


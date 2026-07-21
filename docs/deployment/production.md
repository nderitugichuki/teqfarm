# Production deployment

## Requirements

- Linux host with Docker Engine and Docker Compose v2
- At least 2 CPU cores, 4 GB RAM, and monitored disk space
- A domain name and HTTPS termination at a load balancer or an HTTPS-enabled Nginx configuration
- Off-host encrypted backup storage

## Initial deployment

1. Clone the repository and create `.env` from `.env.example`.
2. Generate a long random `DJANGO_SECRET_KEY` and strong PostgreSQL password.
3. Set `DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS` to the production domain. Origins must include `https://`.
4. Keep `DJANGO_DEBUG=false`, `SECURE_SSL_REDIRECT=true`, and `POSTGRES_SSLMODE=prefer` unless the database requires stricter TLS.
5. Run `docker compose build` and `docker compose up -d`.
6. Create the first administrator:

   ```sh
   docker compose exec backend python manage.py createsuperuser
   ```

7. Verify `docker compose ps`, `/health/`, login, one daily-record transaction, and a database backup.

Complete [acceptance-checklist.md](acceptance-checklist.md) on staging before production sign-off.

## Updates

```sh
sh scripts/backup.sh
git pull --ff-only
docker compose build
docker compose up -d
docker compose ps
```

The backend entrypoint applies migrations and collects static files before Gunicorn starts. Deploy one backend replica during migrations; scale only after migrations complete.

## Backups

Run `sh scripts/backup.sh` at least daily. It creates a compressed PostgreSQL dump and media archive. Copy both off-host, encrypt them, enforce retention, and test `sh scripts/restore.sh` regularly on a non-production database.

Suggested retention: 7 daily, 5 weekly, and 12 monthly backups.

## HTTPS

The included gateway listens on HTTP port 80 so it can sit behind a managed TLS proxy. If Nginx terminates TLS directly, mount the certificate/key, add a port 443 server, redirect port 80, and keep `X-Forwarded-Proto` set correctly. Never expose the backend, PostgreSQL, or frontend containers directly.

## Operations

- Monitor container health, HTTP 5xx rate, disk usage, database size, and backup freshness.
- Review low-stock and health alerts daily.
- Apply OS and container updates monthly after testing.
- Disable departing users immediately; do not share accounts.
- Receipt and profile uploads are limited by type and size, but should also be scanned by infrastructure malware controls where available.

## Rollback

Application images can be rolled back to the previous Git revision. Database migrations may not be safely reversible; take a verified backup before every deployment and restore it when schema rollback is required.

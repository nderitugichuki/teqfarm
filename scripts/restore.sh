#!/bin/sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 backups/teqfarm-YYYYMMDD-HHMMSS.sql.gz" >&2
  exit 1
fi

gzip -dc "$1" | docker compose exec -T db sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
echo "Database restore completed. Restore the matching media archive separately if required."


#!/bin/sh
set -eu

backup_dir="${1:-./backups}"
timestamp="$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"

docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists' | gzip > "$backup_dir/teqfarm-$timestamp.sql.gz"
docker compose run --rm -T --no-deps -v "$(pwd)/$backup_dir:/backup" backend sh -c "tar -czf /backup/teqfarm-media-$timestamp.tar.gz -C /app/media ."

echo "Backup created: $backup_dir/teqfarm-$timestamp.sql.gz"


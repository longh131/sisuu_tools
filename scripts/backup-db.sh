#!/usr/bin/env bash
# Daily MySQL backup — keep last 7 days
# Usage: bash scripts/backup-db.sh
# Cron:  0 3 * * * /opt/seller-toolkit/scripts/backup-db.sh
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/seller-toolkit}"
BACKUP_DIR="${APP_DIR}/backups"
KEEP_DAYS=7
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CONTAINER="sisuu_mysql"

mkdir -p "$BACKUP_DIR"

source "${APP_DIR}/.env" 2>/dev/null || true
DB_NAME="${MYSQL_DATABASE:-sisuu_tools}"
DB_PASS="${MYSQL_ROOT_PASSWORD:-sisuu_root}"

echo "==> Backing up ${DB_NAME}..."
docker exec "$CONTAINER" \
    mysqldump -u root -p"${DB_PASS}" --single-transaction "$DB_NAME" \
    | gzip > "${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"

echo "==> Removing backups older than ${KEEP_DAYS} days..."
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +${KEEP_DAYS} -delete

echo "==> Done: ${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"

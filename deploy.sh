#!/usr/bin/env bash
# Seller Toolkit — production deploy (Ubuntu + Docker)
# Usage: bash /opt/sisuu_tools/deploy.sh
#        APP_DIR=/opt/sisuu_tools bash deploy.sh
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/sisuu_tools}"
COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)

cd "$APP_DIR"

if [ ! -f .env ]; then
    echo "[FAIL] .env not found in ${APP_DIR}"
    exit 1
fi

echo "[1/5] Pull latest code..."
git pull origin main

echo "[2/5] Build and start containers..."
# Skip `down` to reduce downtime; --build recreates changed services
"${COMPOSE[@]}" up -d --build --remove-orphans

echo "[3/5] Wait for web container healthy..."
for i in $(seq 1 40); do
    if "${COMPOSE[@]}" exec -T web curl -sf http://localhost:8000/health >/dev/null 2>&1; then
        echo "      web healthy after ${i} attempt(s)"
        break
    fi
    if [ "$i" -eq 40 ]; then
        echo "[FAIL] web health check timeout"
        "${COMPOSE[@]}" ps
        "${COMPOSE[@]}" logs --tail=50 web
        exit 1
    fi
    sleep 3
done

echo "[4/5] Database migration..."
# entrypoint also runs alembic on start; this confirms DB is reachable post-deploy
if "${COMPOSE[@]}" exec -T web alembic upgrade head; then
    echo "      migration OK"
else
    echo "[FAIL] alembic upgrade failed"
    exit 1
fi

echo "[5/5] Status"
"${COMPOSE[@]}" ps

if curl -sf https://sisuu.com/health >/dev/null 2>&1; then
    echo "[OK] https://sisuu.com/health"
else
    echo "[WARN] external health check failed (nginx/DNS may still be starting)"
fi

echo "[OK] Deploy complete."
echo "      First deploy with empty DB? Run once:"
echo "      ${COMPOSE[*]} exec -T web python scripts/seed_db.py"

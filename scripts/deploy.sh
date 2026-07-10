#!/usr/bin/env bash
# Seller Toolkit — production deployment script (Ubuntu 24.04)
# Usage: sudo bash scripts/deploy.sh
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/seller-toolkit}"
COMPOSE="docker compose -f docker-compose.yml -f docker-compose.prod.yml"

echo "==> Deploying Seller Toolkit in ${APP_DIR}"
cd "$APP_DIR"

if [ ! -f .env ]; then
    echo "ERROR: .env not found. Copy .env.example and configure production values."
    exit 1
fi

echo "==> Pulling latest code..."
git pull origin main

echo "==> Building and starting containers..."
$COMPOSE down
$COMPOSE up -d --build

echo "==> Waiting for web healthcheck..."
sleep 10
$COMPOSE ps

echo "==> Deployment complete."
echo "    Site: https://sisuu.com"
echo "    Health: curl -f https://sisuu.com/health"

#!/bin/sh
set -e

echo "==> Seller Toolkit — starting container"

echo "==> Running database migrations..."
alembic upgrade head

echo "==> Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1

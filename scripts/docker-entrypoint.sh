#!/bin/sh
set -e

echo "==> Seller Toolkit — starting container"

echo "==> Running database migrations..."
alembic upgrade head

echo "==> Syncing SEO blog posts..."
python scripts/sync_blog_posts.py || echo "[WARN] blog sync skipped (DB may be unavailable on first boot)"

echo "==> Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1

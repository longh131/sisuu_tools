#!/usr/bin/env bash
# First-time Let's Encrypt SSL setup for sisuu.com
# Run on Ubuntu server BEFORE starting nginx with SSL config.
#
# Usage:
#   sudo bash scripts/setup-ssl.sh your@email.com
set -euo pipefail

EMAIL="${1:-}"
if [ -z "$EMAIL" ]; then
    echo "Usage: sudo bash scripts/setup-ssl.sh your@email.com"
    exit 1
fi

echo "==> Installing certbot..."
apt-get update
apt-get install -y certbot

echo "==> Obtaining certificate (standalone mode — port 80 must be free)..."
certbot certonly --standalone \
    --preferred-challenges http \
    -d sisuu.com \
    -d www.sisuu.com \
    --email "$EMAIL" \
    --agree-tos \
    --non-interactive

echo "==> Setting up auto-renewal cron..."
(crontab -l 2>/dev/null; echo "0 4 * * * certbot renew --quiet --deploy-hook 'docker compose -f /opt/seller-toolkit/docker-compose.yml -f /opt/seller-toolkit/docker-compose.prod.yml restart nginx'") | crontab -

echo "==> SSL certificates ready at /etc/letsencrypt/live/sisuu.com/"
echo "    Now run: docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build"

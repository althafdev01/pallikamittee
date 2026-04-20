#!/usr/bin/env bash
# deploy/deploy.sh
# Run this script on the VPS to update the application after a git pull.
# Usage:  bash deploy/deploy.sh
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$APP_DIR/env"
PYTHON="$VENV/bin/python"
PIP="$VENV/bin/pip"

echo "==> Pulling latest code..."
git -C "$APP_DIR" pull

echo "==> Installing/updating Python dependencies..."
"$PIP" install -r "$APP_DIR/requirements.txt"

echo "==> Applying database migrations..."
"$PYTHON" "$APP_DIR/manage.py" migrate --noinput

echo "==> Collecting static files..."
"$PYTHON" "$APP_DIR/manage.py" collectstatic --noinput

echo "==> Restarting gunicorn..."
sudo systemctl restart pallikamitti

echo "==> Done. Check status with: sudo systemctl status pallikamitti"

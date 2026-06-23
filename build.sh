#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
echo "==> Build complete. Database migrations and seed data are managed manually."

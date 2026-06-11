#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
# Load existing data on first deploy (skips if data already present)
python manage.py loaddata data.json || echo "loaddata skipped or already loaded"

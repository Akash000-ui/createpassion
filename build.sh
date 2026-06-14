#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
# Only load fixture on first deploy (when DB has no users yet)
# tail -1 isolates our print() from any Django startup messages on stdout
USER_COUNT=$(python manage.py shell -c "from mainapp.models import UserProfile; print(UserProfile.objects.count())" 2>/dev/null | tail -1)
if [ "$USER_COUNT" = "0" ]; then
    echo "==> Empty DB detected, loading initial data..."
    PYTHONIOENCODING=utf-8 python manage.py loaddata data.json
    echo "==> Data loaded."
else
    echo "==> DB already has $USER_COUNT users, skipping loaddata."
fi

#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Seed a newly created demo database once. Normal redeploys keep existing data.
USER_COUNT=$(python manage.py shell -c "from mainapp.models import UserProfile; print(UserProfile.objects.count())" 2>/dev/null | tail -1)
if [ "$USER_COUNT" = "0" ]; then
    echo "==> Empty database detected. Loading demo data..."
    PYTHONIOENCODING=utf-8 python manage.py loaddata data.json
    echo "==> Demo data loaded."
else
    echo "==> Database already contains $USER_COUNT users. Skipping demo data."
fi

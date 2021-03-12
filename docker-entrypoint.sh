#!/bin/bash
source /app/venv/bin/activate

echo "Collect static files"
python3.9 /app/backend/manage.py collectstatic --noinput

echo "Apply migrations"
python3.9 /app/backend/manage.py migrate --noinput

echo "Create cron jobs"
python3.9 /app/backend/manage.py crontab add

echo "Start server"
python3.9 /app/backend/manage.py runserver 0.0.0.0:8000

#!/bin/bash
source /app/venv/bin/activate

echo "Collect static files"
python3.9 /app/backend/manage.py collectstatic --noinput

echo "Make database migrations"
python3.9 /app/backend/manage.py makemigrations

echo "Apply database migrations"
python3.9 /app/backend/manage.py migrate

echo "Create cron jobs"
python3.9 /app/backend/manage.py crontab add

echo "Start server"
python3.9 /app/backend/manage.py runserver 0.0.0.0:8000

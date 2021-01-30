#!/bin/bash
source venv/bin/activate

echo "Collect static files"
python3.9 backend/manage.py collectstatic --noinput

echo "Make database migrations"
python3.9 backend/manage.py makemigrations

echo "Apply database migrations"
python3.9 backend/manage.py migrate

echo "Start server"
python3.9 backend/manage.py runserver 0.0.0.0:8000

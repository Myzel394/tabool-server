#!/bin/bash
source venv/bin/activate

# Preparation
echo "Collect static files"
python3.9 backend/manage.py collectstatic --noinput

echo "Apply migrations"
python3.9 backend/manage.py migrate --noinput

# Server
echo "Start server"
python3.9 backend/manage.py runserver 0.0.0.0:8000

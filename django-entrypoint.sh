#!/bin/bash
source venv/bin/activate

# Cleanup
echo "Remove migrations"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

echo "Remove static_root folder"
rmdir ./backend/static_root/

# Preparation
echo "Collect static files"
python3.9 backend/manage.py collectstatic --noinput

echo "Make database migrations"
python3.9 backend/manage.py makemigrations --noinput

echo "Apply database migrations"
python3.9 backend/manage.py migrate --noinput

# Server
echo "Start server"
python3.9 backend/manage.py runserver 0.0.0.0:8000

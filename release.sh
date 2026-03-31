#!/usr/bin/env bash
set -o errexit

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating default superuser if not exists..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.production')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@rapid-cash.com', '123456+++')
    print('Superuser admin created!')
else:
    print('Superuser admin already exists.')
"

echo "Release commands completed!"

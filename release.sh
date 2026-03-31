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
if not User.objects.filter(username='kizy').exists():
    user = User.objects.create_superuser('kizy', 'kizy@rapid-cash.com', '789456+++')
    user.first_name = 'Admin'
    user.last_name = 'Kizy'
    user.save()
    print('Superuser kizy created!')
else:
    print('Superuser kizy already exists.')
"

echo "Unlocking kizy account if locked..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.production')
django.setup()
try:
    from axes.utils import reset
    reset(username='kizy')
    print('Kizy account unlocked!')
except Exception as e:
    print(f'Note: Could not unlock kizy: {e}')
"

echo "Release commands completed!"

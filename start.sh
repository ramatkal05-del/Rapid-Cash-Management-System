#!/bin/bash
set -e

echo "Starting Rapid Cash deployment..."

# Collect static files first
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Create/update admin user
echo "Creating/updating admin user kizy..."
python create_admin.py || echo "Warning: Could not create admin user"

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60

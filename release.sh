#!/usr/bin/env bash
set -o errexit

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating/updating admin user kizy..."
python create_admin.py

echo "Release commands completed!"

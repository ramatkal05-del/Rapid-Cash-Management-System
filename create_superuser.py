#!/usr/bin/env python
"""
Create default superuser for Rapid Cash.
Run this on Render console: python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.production')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Create superuser
username = 'admin'
email = 'admin@rapid-cash.com'
password = '123456+++'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser "{username}" created successfully!')
    print(f'Email: {email}')
    print(f'You can now login at https://rapid-cash-management.onrender.com/admin/')
else:
    print(f'User "{username}" already exists.')
    print('To reset password, run: python manage.py changepassword admin')

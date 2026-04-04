#!/usr/bin/env python
"""
Créer l'admin kizy avec mot de passe 789456+++
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.production')
django.setup()

from django.contrib.auth import get_user_model
from axes.utils import reset

User = get_user_model()

# Créer ou mettre à jour kizy
user, created = User.objects.get_or_create(
    username='kizy',
    defaults={
        'email': 'kizy@rapid-cash.com',
        'first_name': 'Admin',
        'last_name': 'Kizy',
        'is_staff': True,
        'is_superuser': True,
    }
)

# Toujours mettre à jour le mot de passe
user.set_password('789456+++')
user.is_staff = True
user.is_superuser = True
user.save()

print(f"{'Créé' if created else 'Mis à jour'}: kizy")

# Déverrouiller
reset(username='kizy')
print("✅ Compte kizy déverrouillé !")

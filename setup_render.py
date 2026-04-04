#!/usr/bin/env python
"""
Setup script pour Render - Créer admin et assigner une caisse
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.production')
django.setup()

from django.contrib.auth import get_user_model
from axes.utils import reset
from finance.models import Caisse
from core.models import Currency

User = get_user_model()

def setup_admin_and_caisse():
    # Créer les devises d'abord
    currencies_data = [
        {'code': 'USD', 'name': 'Dollar Américain', 'symbol': '$'},
        {'code': 'CDF', 'name': 'Franc Congolais', 'symbol': 'FC'},
        {'code': 'EUR', 'name': 'Euro', 'symbol': '€'},
        {'code': 'GBP', 'name': 'Livre Sterling', 'symbol': '£'},
    ]
    
    for curr in currencies_data:
        currency, created = Currency.objects.get_or_create(
            code=curr['code'],
            defaults={'name': curr['name'], 'symbol': curr['symbol']}
        )
        if created:
            print(f"✅ Devise créée: {curr['code']} - {curr['name']}")
    
    # Créer ou mettre à jour kizy
    user, created = User.objects.get_or_create(
        username='kizy',
        defaults={
            'email': 'kizy@rapid-cash.com',
            'first_name': 'Admin',
            'last_name': 'Kizy',
            'is_staff': True,
            'is_superuser': True,
            'role': 'ADMIN',
        }
    )
    
    # Toujours mettre à jour le mot de passe et les permissions
    user.set_password('789456+++')
    user.is_staff = True
    user.is_superuser = True
    user.role = 'ADMIN'
    user.save()
    
    print(f"✅ Admin {'créé' if created else 'mis à jour'}: kizy")
    
    # Déverrouiller le compte
    reset(username='kizy')
    print("✅ Compte kizy déverrouillé !")
    
    # Créer une caisse principale si elle n'existe pas
    caisse, caisse_created = Caisse.objects.get_or_create(
        name='Caisse Principale',
        defaults={
            'currency': 'USD',
            'balance': 100000.00,
            'manager': user,
            'location': 'Siège Principal',
            'is_active': True,
        }
    )
    
    if caisse_created:
        print(f"✅ Caisse créée: {caisse.name} (Balance: {caisse.balance} {caisse.currency})")
    else:
        print(f"ℹ️ Caisse existe déjà: {caisse.name}")
        # S'assurer que kizy est le manager
        caisse.manager = user
        caisse.save()
        print(f"✅ Caisse assignée à kizy")
    
    # Créer des caisses additionnelles
    currencies = ['CDF', 'EUR', 'GBP']
    for currency in currencies:
        caisse, created = Caisse.objects.get_or_create(
            name=f'Caisse {currency}',
            defaults={
                'currency': currency,
                'balance': 50000.00 if currency == 'CDF' else 10000.00,
                'manager': user,
                'location': 'Siège Principal',
                'is_active': True,
            }
        )
        if created:
            print(f"✅ Caisse créée: {caisse.name}")
    
    print("\n🎉 Setup terminé!")
    print(f"Identifiants admin:")
    print(f"  - Username: kizy")
    print(f"  - Password: 789456+++")
    print(f"  - Admin URL: /admin/")

if __name__ == "__main__":
    setup_admin_and_caisse()

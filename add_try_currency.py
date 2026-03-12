#!/usr/bin/env python
"""
Ajouter Turkish Lira (TRY) aux devises
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    import django
    django.setup()
    
    from core.models import Currency
    
    # Ajouter Turkish Lira
    currency_try, created_try = Currency.objects.get_or_create(
        code='TRY',
        defaults={
            'name': 'Turkish Lira',
            'symbol': '₺',
            'is_reference': False
        }
    )
    
    if created_try:
        print(f"✅ Devise ajoutée: {currency_try.code} - {currency_try.name} ({currency_try.symbol})")
    else:
        print(f"ℹ️ Devise existe déjà: {currency_try.code} - {currency_try.name}")
    
    # Ajouter British Pound Sterling
    currency_gbp, created_gbp = Currency.objects.get_or_create(
        code='GBP',
        defaults={
            'name': 'British Pound Sterling',
            'symbol': '£',
            'is_reference': False
        }
    )
    
    if created_gbp:
        print(f"✅ Devise ajoutée: {currency_gbp.code} - {currency_gbp.name} ({currency_gbp.symbol})")
    else:
        print(f"ℹ️ Devise existe déjà: {currency_gbp.code} - {currency_gbp.name}")
    
    # Afficher toutes les devises
    print("\n📋 Devises disponibles:")
    for c in Currency.objects.all().order_by('code'):
        ref = " (Référence)" if c.is_reference else ""
        print(f"   - {c.code}: {c.name} ({c.symbol}){ref}")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

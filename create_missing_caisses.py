#!/usr/bin/env python
"""
Script pour créer des caisses pour tous les utilisateurs qui n'en ont pas
"""

import os
import sys

def create_missing_caisses():
    """Créer des caisses pour les utilisateurs qui n'en ont pas"""
    
    print("🏦 CRÉATION DES CAISSES MANQUANTES")
    print("=" * 50)
    
    # Configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        from operations.models import Caisse
        from core.models import Currency
        
        User = get_user_model()
        
        print("\n👥 Vérification des utilisateurs:")
        
        # Trouver la devise USD
        usd_currency = Currency.objects.filter(code='USD').first()
        if not usd_currency:
            print("   ❌ Devise USD non trouvée")
            return
        
        created_caisses = []
        
        for user in User.objects.all():
            existing_caisse = Caisse.objects.filter(agent=user).first()
            
            if existing_caisse:
                print(f"   ✅ {user.username}: Déjà une caisse (#{existing_caisse.id})")
            else:
                # Créer une nouvelle caisse
                caisse = Caisse.objects.create(
                    agent=user,
                    currency=usd_currency,
                    balance=0.00,
                    is_active=True
                )
                created_caisses.append(caisse)
                print(f"   ➕ {user.username}: Caisse créée (#{caisse.id})")
        
        if created_caisses:
            print(f"\n✅ {len(created_caisses)} caisse(s) créée(s):")
            for caisse in created_caisses:
                print(f"   📄 {caisse.agent.username} - {caisse.currency.code} - Solde: {caisse.balance}")
        else:
            print("\n✅ Tous les utilisateurs ont déjà une caisse")
        
        print("\n🎯 RÉSULTAT:")
        print("   Tous les utilisateurs peuvent maintenant créer des opérations")
        print("   Le formulaire /operations/nouveau/ devrait fonctionner")
        
        print("\n🚀 TEST RECOMMANDÉ:")
        print("   1. python manage.py runserver")
        print("   2. Se connecter avec un utilisateur")
        print("   3. Accéder à: http://127.0.0.1:8000/operations/nouveau/")
        print("   4. Créer une opération")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_missing_caisses()

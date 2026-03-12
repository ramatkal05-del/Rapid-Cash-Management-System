#!/usr/bin/env python
"""
Diagnostic du POST 200 sur /operations/nouveau/
"""

import os

def diagnose_post_200():
    """Diagnostiquer pourquoi le POST retourne 200 au lieu de 302"""
    
    print("🔍 DIAGNOSTIC POST 200 SUR /operations/nouveau/")
    print("=" * 60)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        from operations.forms import OperationForm
        from operations.models import Caisse, FeeGrid
        from core.models import Currency
        from decimal import Decimal
        
        User = get_user_model()
        
        print("\n👤 UTILISATEUR CONNECTÉ:")
        # Simuler l'utilisateur qui fait la requête
        user = User.objects.first()
        if user:
            print(f"   Utilisateur: {user.username}")
            print(f"   Rôle: {user.get_role_display()}")
        
        print("\n🏦 VÉRIFICATION CAISSE:")
        caisse = Caisse.objects.filter(agent=user).first()
        if caisse:
            print(f"   ✅ Caisse: #{caisse.id} - {caisse.name}")
            print(f"   Solde: {caisse.balance} {caisse.currency.code}")
        else:
            print("   ❌ Pas de caisse assignée")
            # Essayer de trouver une caisse pour admin
            caisse = Caisse.objects.first()
            if caisse:
                print(f"   ⚠️ Caisse alternative: #{caisse.id}")
        
        print("\n💰 GRILLES DE FRAIS:")
        fee_grids = FeeGrid.objects.filter(currency=caisse.currency if caisse else None)
        if fee_grids.exists():
            print(f"   ✅ {fee_grids.count()} grilles trouvées")
        else:
            print("   ⚠️ Aucune grille de frais pour cette devise")
        
        print("\n📝 TEST FORMULAIRE AVEC DONNÉES TYPE:")
        
        # Test avec données réalistes
        if caisse:
            form_data = {
                'type': 'TRANSFER',
                'amount_orig': '300.00',
                'currency_orig': caisse.currency.id,
                'observation': 'Test diagnostic'
            }
            
            print(f"   Données: {form_data}")
            
            form = OperationForm(data=form_data, agent=user)
            
            if form.is_valid():
                print("   ✅ Formulaire VALIDE - Devrait créer l'opération")
                print("   ✅ Attendu: POST 302 (redirection)")
            else:
                print("   ❌ Formulaire INVALIDE - Explications:")
                for field, errors in form.errors.items():
                    print(f"      • {field}: {errors}")
                print("   ❌ Résultat: POST 200 (formulaire réaffiché)")
        
        print("\n🔍 CAUSES POSSIBLES DU POST 200:")
        print("   1. Type d'opération invalide (doit être TRANSFER ou WITHDRAWAL)")
        print("   2. Montant négatif ou zéro")
        print("   3. Devise incompatible avec la caisse")
        print("   4. Solde insuffisant pour le retrait")
        print("   5. Caisse non assignée à l'utilisateur")
        
        print("\n💡 SOLUTIONS:")
        print("   • Vérifier les données envoyées dans le formulaire")
        print("   • S'assurer que type=TRANSFER (pas SEND ou autre)")
        print("   • Vérifier que la devise correspond à la caisse")
        print("   • Vérifier le solde suffisant")
        
        print("\n📊 RÉSUMÉ:")
        print("   POST 200 = Formulaire invalide")
        print("   POST 302 = Succès (redirection)")
        print("   Vérifiez les messages d'erreur sur la page")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    diagnose_post_200()

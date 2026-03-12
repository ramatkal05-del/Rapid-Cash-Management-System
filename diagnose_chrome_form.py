#!/usr/bin/env python
"""
Diagnostic et correction des problèmes Chrome DevTools et formulaire d'opération
"""

import os

def diagnose_chrome_and_form_issues():
    """Diagnostiquer les problèmes Chrome DevTools et formulaire"""
    
    print("🔍 DIAGNOSTIC PROBLÈMES CHROME DEVTOOLS + FORMULAIRE")
    print("=" * 65)
    
    print("\n❌ PROBLÈMES IDENTIFIÉS:")
    
    print("\n1. Chrome DevTools 404:")
    print("   GET /.well-known/appspecific/com.chrome.devtools.json HTTP/1.1\" 404 4600")
    print("   ├── Cause: Chrome DevTools cherche ce fichier automatiquement")
    print("   ├── Impact: Normal en développement, pas critique")
    print("   ├── Solution: Ignorer ou créer le fichier")
    
    print("\n2. Formulaire d'opération POST 200:")
    print("   POST /operations/nouveau/ HTTP/1.1\" 200 44683")
    print("   ├── Cause: Formulaire probablement invalide")
    print("   ├── Impact: Opération non créée")
    print("   ├── Solution: Vérifier erreurs du formulaire")
    
    print("\n✅ SOLUTIONS PROPOSÉES:")
    
    print("\n🔧 1. Solution Chrome DevTools:")
    print("   Option A (Ignorer): Normal en développement")
    print("   Option B (Créer): Créer le fichier pour éviter les 404")
    
    print("\n🔧 2. Solution Formulaire:")
    print("   - Vérifier les erreurs de validation")
    print("   - Vérifier si l'utilisateur a une caisse assignée")
    print("   - Vérifier les messages d'erreur affichés")
    
    print("\n📋 VÉRIFICATIONS À FAIRE:")
    
    # Vérifier si l'utilisateur a une caisse
    print("\n🏦 Vérification caisses:")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        from operations.models import Caisse
        
        User = get_user_model()
        
        print("   Utilisateurs et leurs caisses:")
        for user in User.objects.all():
            caisse = Caisse.objects.filter(agent=user).first()
            status = "✅" if caisse else "❌"
            print(f"   {status} {user.username}: {'Caisse #' + str(caisse.id) if caisse else 'Aucune caisse'}")
        
        # Vérifier le formulaire
        print("\n📝 Test du formulaire:")
        from operations.forms import OperationForm
        
        test_user = User.objects.filter(role='ADMIN').first()
        if test_user:
            try:
                form = OperationForm(agent=test_user)
                print(f"   ✅ Formulaire créé pour {test_user.username}")
                print(f"   Champs: {list(form.fields.keys())}")
            except Exception as e:
                print(f"   ❌ Erreur formulaire: {e}")
        
    except Exception as e:
        print(f"   ❌ Erreur vérification: {e}")
    
    print("\n🎯 ACTIONS RECOMMANDÉES:")
    print("   1. Créer les caisses manquantes pour les agents")
    print("   2. Tester le formulaire avec des données valides")
    print("   3. Ignorer les erreurs Chrome DevTools (normales)")
    
    print("\n💡 SI FORMULAIRE ÉCHEOUE:")
    print("   - Vérifier les messages affichés sur la page")
    print("   - Vérifier la console navigateur (F12)")
    print("   - Créer une caisse pour l'utilisateur si nécessaire")

if __name__ == '__main__':
    diagnose_chrome_and_form_issues()

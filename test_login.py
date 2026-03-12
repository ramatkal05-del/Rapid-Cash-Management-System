#!/usr/bin/env python
"""
Test de connexion avec identifiants connus
"""

import os
import sys

def test_login_credentials():
    """Tester les identifiants de connexion"""
    
    print("🧪 TEST CONNEXION AVEC IDENTIFIANTS CONNUS")
    print("=" * 55)
    
    # Configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from django.contrib.auth import authenticate
        from django.contrib.auth import get_user_model
        
        print("\n👥 Utilisateurs disponibles:")
        
        User = get_user_model()
        users = User.objects.all()
        
        credentials = []
        
        for user in users:
            # Afficher les infos utilisateur (sans mot de passe pour sécurité)
            print(f"   👤 {user.username}")
            print(f"      Rôle: {user.get_role_display()}")
            print(f"      Actif: {user.is_active}")
            print(f"      Staff: {user.is_staff}")
            print(f"      Superuser: {user.is_superuser}")
            print()
        
        print("🔑 IDENTIFIANTS À TESTER:")
        print("   Pour tester la connexion, utilisez ces identifiants:")
        print()
        
        # Note: Les vrais mots de passe ne sont pas affichés pour sécurité
        print("   1. ruth (Administrateur)")
        print("   2. agent1 (Agent)")
        print("   3. Mpoto (Agent)")
        print("   4. Kizy (Administrateur)")
        print()
        
        print("💡 INSTRUCTIONS:")
        print("   1. Lancer le serveur: python manage.py runserver")
        print("   2. Ouvrir: http://127.0.0.1:8000/accounts/login/")
        print("   3. Utiliser un des identifiants ci-dessus")
        print("   4. Si mot de passe oublié:")
        print("      python manage.py changepassword <username>")
        print()
        
        print("🔧 CRÉER UN NOUVEAU SUPERUSER:")
        print("   Si aucun identifiant ne fonctionne:")
        print("   python manage.py createsuperuser")
        print()
        print("   Exemple:")
        print("   Username: admin")
        print("   Email: admin@rapidcash.com")
        print("   Password: admin123")
        print()
        
        print("🎯 DÉBOGAGE:")
        print("   Si le login échoue toujours:")
        print("   1. Vérifier la console du navigateur (F12)")
        print("   2. Vérifier les logs Django")
        print("   3. Tester en mode navigation privée")
        print("   4. Vider le cache du navigateur")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_login_credentials()

#!/usr/bin/env python
"""
Diagnostic du problème de login Django
"""

import os
import sys

def diagnose_login_issue():
    """Diagnostiquer le problème de login"""
    
    print("🔍 DIAGNOSTIC PROBLÈME LOGIN DJANGO")
    print("=" * 50)
    
    # Configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        from django.test import Client
        
        print("\n📋 Configuration:")
        print("   Settings module: config.settings")
        print("   Django version:", django.get_version())
        
        print("\n👥 Utilisateurs dans la base:")
        
        User = get_user_model()
        users = User.objects.all()
        
        if users.exists():
            print(f"   ✅ {users.count()} utilisateur(s) trouvé(s)")
            for user in users:
                print(f"      - {user.username} ({user.get_role_display()}) - Actif: {user.is_active}")
        else:
            print("   ❌ Aucun utilisateur trouvé")
            print("   💡 Solution: Créer un superuser")
        
        print("\n🧪 Test du formulaire de login:")
        
        # Vérifier le template
        template_file = 'templates/registration/login.html'
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            checks = [
                ("action=\"{% url 'login' %}\"", "Action du formulaire"),
                ("{% csrf_token %}", "Token CSRF"),
                ("name=\"username\"", "Champ username"),
                ("name=\"password\"", "Champ password"),
                ("type=\"submit\"", "Bouton submit"),
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description}: Trouvé")
                else:
                    print(f"   ❌ {description}: Non trouvé")
            
            if "name=\"next\"" in content:
                print("   ✅ Champ next: Trouvé")
            else:
                print("   ❌ Champ next: Non trouvé")
        else:
            print(f"   ❌ Template login.html: Non trouvé")
        
        print("\n🔧 Configuration requise:")
        print("   ✅ Formulaire avec action correcte")
        print("   ✅ Token CSRF présent")
        print("   ✅ Champs username/password")
        print("   ✅ Champ next pour redirection")
        
        print("\n💡 Si le login ne fonctionne pas:")
        print("   1. Vérifier qu'il y a des utilisateurs")
        print("   2. Vérifier les identifiants")
        print("   3. Créer un superuser si nécessaire:")
        print("      python manage.py createsuperuser")
        
        print("\n🎯 Commandes utiles:")
        print("   python manage.py createsuperuser")
        print("   python manage.py shell")
        print("   python manage.py check")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    diagnose_login_issue()

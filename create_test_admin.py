#!/usr/bin/env python
"""
Script pour créer un superuser de test pour Rapid Cash
"""

import os
import sys

def create_test_superuser():
    """Créer un superuser de test"""
    
    print("🔑 CRÉATION SUPERUSER DE TEST")
    print("=" * 40)
    
    # Configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        from django.core.management import execute_from_command_line
        
        User = get_user_model()
        
        print("\n👥 Vérification des utilisateurs existants:")
        
        # Vérifier si admin existe déjà
        if User.objects.filter(username='admin').exists():
            print("   ⚠️ L'utilisateur 'admin' existe déjà")
            
            # Proposer de réinitialiser le mot de passe
            print("\n🔄 Réinitialiser le mot de passe de 'admin':")
            print("   python manage.py changepassword admin")
        else:
            print("   ✅ L'utilisateur 'admin' n'existe pas")
            
            print("\n🔑 Création du superuser de test:")
            print("   Username: admin")
            print("   Email: admin@rapidcash.com")
            print("   Password: admin123")
            print()
            
            # Créer le superuser avec le modèle User personnalisé
            user = User.objects.create_superuser(
                username='admin',
                email='admin@rapidcash.com',
                password='admin123',
                first_name='Admin',
                last_name='Test'
            )
            
            print("   ✅ Superuser 'admin' créé avec succès!")
            print("   📝 Identifiants:")
            print("      Username: admin")
            print("      Password: admin123")
        
        print("\n📋 Liste complète des utilisateurs:")
        
        users = User.objects.all()
        for user in users:
            status = "🟢" if user.is_active else "🔴"
            superuser = "⭐" if user.is_superuser else "  "
            print(f"   {status} {superuser} {user.username} ({user.get_role_display()})")
        
        print("\n🚀 UTILISATION:")
        print("   1. Lancer le serveur:")
        print("      python manage.py runserver")
        print()
        print("   2. Se connecter:")
        print("      URL: http://127.0.0.1:8000/accounts/login/")
        print("      Username: admin")
        print("      Password: admin123")
        print()
        print("   3. Accéder au dashboard:")
        print("      http://127.0.0.1:8000/core/capital/")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_test_superuser()

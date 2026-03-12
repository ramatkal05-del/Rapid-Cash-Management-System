#!/usr/bin/env python
"""
Test et réparation de l'authentification agent
Usage: python fix_agent_login.py <username> <new_password>
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    import django
    django.setup()
    
    from django.contrib.auth import get_user_model, authenticate
    
    User = get_user_model()
    
    print("🔧 RÉPARATION LOGIN AGENT")
    print("=" * 50)
    
    if len(sys.argv) < 3:
        print("Usage: python fix_agent_login.py <username> <new_password>")
        print("\n📋 Agents disponibles:")
        agents = User.objects.filter(role='AGENT')
        for a in agents:
            print(f"   - {a.username} (Actif: {a.is_active})")
        sys.exit(1)
    
    username = sys.argv[1]
    new_password = sys.argv[2]
    
    try:
        user = User.objects.get(username=username)
        print(f"\n👤 Utilisateur trouvé: {username}")
        print(f"   Rôle: {user.role}")
        print(f"   Actif: {user.is_active}")
        print(f"   Email: {user.email}")
        
        # Vérifier le hash du mot de passe
        print(f"\n🔐 Hash actuel: {user.password[:30]}...")
        
        # Réinitialiser le mot de passe
        user.set_password(new_password)
        user.is_active = True
        user.save()
        
        print(f"✅ Mot de passe réinitialisé avec set_password()")
        print(f"🔐 Nouveau hash: {user.password[:30]}...")
        
        # Tester l'authentification
        test_user = authenticate(username=username, password=new_password)
        if test_user:
            print(f"\n✅ SUCCÈS! L'authentification fonctionne maintenant.")
            print(f"   Connectez-vous avec:")
            print(f"   Username: {username}")
            print(f"   Password: {new_password}")
        else:
            print(f"\n❌ ÉCHEC - L'authentification ne fonctionne toujours pas")
            print(f"   Problème possible: le backend d'authentification")
            
    except User.DoesNotExist:
        print(f"❌ Utilisateur '{username}' introuvable")
        
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

#!/usr/bin/env python
"""
Script pour déverrouiller un compte utilisateur verrouillé par Django Axes
Usage: python unlock_user.py <username>
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.production')
django.setup()

from django.contrib.auth import get_user_model
from axes.utils import reset

User = get_user_model()

def unlock_user(username):
    """Déverrouiller un utilisateur"""
    try:
        user = User.objects.get(username=username)
        
        # Réinitialiser les tentatives Axes pour cet utilisateur
        reset(username=username)
        
        print(f"✅ Utilisateur '{username}' déverrouillé avec succès!")
        print(f"   L'utilisateur peut maintenant se connecter.")
        return True
        
    except User.DoesNotExist:
        print(f"❌ Utilisateur '{username}' non trouvé.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python unlock_user.py <username>")
        print("Example: python unlock_user.py admin")
        sys.exit(1)
    
    username = sys.argv[1]
    unlock_user(username)

#!/usr/bin/env python
"""
Déverrouiller un compte utilisateur bloqué par Axes
Usage: python unlock_account.py <username>
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.production')
django.setup()

def unlock_user(username):
    try:
        from axes.utils import reset
        reset(username=username)
        print(f"✅ Compte '{username}' déverrouillé !")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        username = input("Nom d'utilisateur à déverrouiller: ")
    else:
        username = sys.argv[1]
    unlock_user(username)

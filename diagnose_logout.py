#!/usr/bin/env python
"""
Diagnostic du problème de logout Django
"""

import os
import sys

def diagnose_logout_issue():
    """Diagnostiquer le problème de logout"""
    
    print("🔍 DIAGNOSTIC PROBLÈME LOGOUT DJANGO")
    print("=" * 50)
    
    # Configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from django.urls import reverse
        from django.conf import settings
        
        print("\n📋 Configuration Django:")
        print(f"   LOGIN_URL: {settings.LOGIN_URL}")
        print(f"   LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
        print(f"   LOGOUT_REDIRECT_URL: {settings.LOGOUT_REDIRECT_URL}")
        
        print("\n🔍 Test des URLs de logout:")
        
        # Tester les URLs de logout
        logout_urls = [
            'logout',
            'accounts:logout',
            'admin:logout',
            'rest_framework:logout'
        ]
        
        for url_name in logout_urls:
            try:
                url = reverse(url_name)
                print(f"   ✅ {url_name}: {url}")
            except Exception as e:
                print(f"   ❌ {url_name}: {e}")
        
        print("\n📝 Templates utilisant logout:")
        
        # Vérifier les templates
        template_dir = 'templates'
        logout_templates = []
        
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if 'logout' in content and 'url' in content:
                            logout_templates.append(file_path)
                    except:
                        pass
        
        for template in logout_templates:
            print(f"   📄 {template}")
        
        print("\n💡 Cause probable du problème:")
        print("   ❌ L'URL 'logout' n'est pas définie dans les URLs")
        print("   ❌ Redirection vers une page inexistante")
        print("   ❌ Template utilise une URL non valide")
        
        print("\n🔧 Solutions possibles:")
        print("   1. Ajouter une vue de logout personnalisée")
        print("   2. Utiliser les URLs Django auth par défaut")
        print("   3. Corriger les templates")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    diagnose_logout_issue()

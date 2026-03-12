#!/usr/bin/env python
"""
Test du POST /core/profil/ pour voir l'erreur 500 exacte
"""

import os

def test_profile_post():
    """Test POST sur /core/profil/"""
    
    print("🧪 TEST POST /core/profil/")
    print("=" * 50)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from django.test import Client
        from django.contrib.auth import get_user_model
        from django.urls import reverse
        
        User = get_user_model()
        client = Client()
        
        # Récupérer un utilisateur
        user = User.objects.first()
        if not user:
            print("❌ Aucun utilisateur trouvé")
            return
        
        # Se connecter
        client.force_login(user)
        print(f"✅ Connecté en tant que: {user.username}")
        
        # Test GET
        print("\n📥 TEST GET /core/profil/:")
        response_get = client.get('/core/profil/')
        print(f"   Status: {response_get.status_code}")
        
        if response_get.status_code == 200:
            print(f"   ✅ GET fonctionne")
        else:
            print(f"   ❌ GET échoue: {response_get.content[:200]}")
        
        # Test POST
        print("\n📤 TEST POST /core/profil/:")
        
        post_data = {
            'first_name': 'Test',
            'last_name': 'Profil',
            'email': user.email or 'test@test.com',
            'phone': '1234567890'
        }
        
        response_post = client.post('/core/profil/', post_data)
        print(f"   Status: {response_post.status_code}")
        
        if response_post.status_code == 302:
            print(f"   ✅ POST réussi (redirect après succès)")
        elif response_post.status_code == 200:
            # Vérifier s'il y a des erreurs de formulaire
            if b'error' in response_post.content.lower() or b'erreur' in response_post.content.lower():
                print(f"   ⚠️ POST retourne 200 mais avec erreurs")
                # Chercher les erreurs dans le contenu
                content = response_post.content.decode('utf-8', errors='ignore')
                if 'errorlist' in content:
                    print(f"   Erreurs de formulaire détectées")
            else:
                print(f"   ✅ POST réussi (reste sur la page)")
        elif response_post.status_code == 500:
            print(f"   ❌ ERREUR 500 - Détails:")
            content = response_post.content.decode('utf-8', errors='ignore')
            # Chercher le traceback
            if 'Traceback' in content:
                import re
                traceback_match = re.search(r'Traceback.*?</div>', content, re.DOTALL)
                if traceback_match:
                    print(f"   {traceback_match.group(0)[:500]}")
                else:
                    print(f"   {content[:500]}")
            else:
                print(f"   {content[:500]}")
        else:
            print(f"   ⚠️ Status inattendu: {response_post.status_code}")
            print(f"   {response_post.content[:300]}")
        
        # Vérifier si l'utilisateur a été modifié
        user.refresh_from_db()
        print(f"\n📊 VÉRIFICATION:")
        print(f"   first_name après POST: {user.first_name}")
        print(f"   last_name après POST: {user.last_name}")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_profile_post()

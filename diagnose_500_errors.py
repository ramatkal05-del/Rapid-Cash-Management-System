#!/usr/bin/env python
"""
Diagnostic des erreurs 500 sur /core/paie/ et /core/taux-change/
"""

import os

def diagnose_errors():
    """Diagnostiquer les erreurs 500"""
    
    print("🔍 DIAGNOSTIC ERREURS 500")
    print("=" * 60)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from django.test import Client
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        client = Client()
        
        # Récupérer un admin
        admin = User.objects.filter(role='ADMIN').first()
        if not admin:
            print("❌ Aucun admin trouvé")
            return
        
        client.force_login(admin)
        print(f"✅ Connecté en tant que: {admin.username}")
        
        # Test 1: /core/paie/
        print("\n📊 TEST 1: GET /core/paie/")
        try:
            response = client.get('/core/paie/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 500:
                content = response.content.decode('utf-8', errors='ignore')
                print(f"   ❌ Erreur 500:")
                # Chercher le traceback
                if 'Traceback' in content:
                    import re
                    match = re.search(r'Traceback.*?</div>', content, re.DOTALL)
                    if match:
                        print(f"   {match.group(0)[:800]}")
                    else:
                        print(f"   {content[:800]}")
                else:
                    print(f"   {content[:800]}")
            elif response.status_code == 200:
                print(f"   ✅ OK")
            else:
                print(f"   ⚠️ Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 2: /core/paie/calculer/
        print("\n📊 TEST 2: GET /core/paie/calculer/")
        try:
            response = client.get('/core/paie/calculer/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 500:
                content = response.content.decode('utf-8', errors='ignore')
                print(f"   ❌ Erreur 500:")
                if 'Traceback' in content:
                    import re
                    match = re.search(r'Traceback.*?</div>', content, re.DOTALL)
                    if match:
                        print(f"   {match.group(0)[:800]}")
                    else:
                        print(f"   {content[:800]}")
                else:
                    print(f"   {content[:800]}")
            elif response.status_code in [302, 200]:
                print(f"   ✅ OK (redirect ou success)")
            else:
                print(f"   ⚠️ Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 3: /core/taux-change/
        print("\n📊 TEST 3: GET /core/taux-change/")
        try:
            response = client.get('/core/taux-change/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 500:
                content = response.content.decode('utf-8', errors='ignore')
                print(f"   ❌ Erreur 500:")
                if 'Traceback' in content:
                    import re
                    match = re.search(r'Traceback.*?</div>', content, re.DOTALL)
                    if match:
                        print(f"   {match.group(0)[:800]}")
                    else:
                        print(f"   {content[:800]}")
                else:
                    print(f"   {content[:800]}")
            elif response.status_code == 200:
                print(f"   ✅ OK")
            else:
                print(f"   ⚠️ Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            import traceback
            traceback.print_exc()
        
        # Vérifier les modèles
        print("\n🔧 VÉRIFICATION DES MODÈLES:")
        try:
            from core.models import PayPeriod, MonthlySalary
            print(f"   ✅ PayPeriod: {PayPeriod.objects.count()} périodes")
            print(f"   ✅ MonthlySalary: {MonthlySalary.objects.count()} salaires")
        except Exception as e:
            print(f"   ❌ Erreur modèles paie: {e}")
        
        try:
            from core.models import ExchangeRate, Currency
            print(f"   ✅ ExchangeRate: {ExchangeRate.objects.count()} taux")
            print(f"   ✅ Currency: {Currency.objects.count()} devises")
        except Exception as e:
            print(f"   ❌ Erreur modèles taux de change: {e}")
        
    except Exception as e:
        print(f"\n❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    diagnose_errors()

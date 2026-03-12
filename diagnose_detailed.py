#!/usr/bin/env python
"""
Diagnostic détaillé des erreurs avec logging complet
"""

import os
import sys

# Capture toutes les erreurs
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
    if admin:
        client.force_login(admin)
        print(f"✅ Connecté: {admin.username}")
    else:
        print("❌ Aucun admin trouvé")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("TEST 1: /core/paie/ (payroll_dashboard)")
    print("="*60)
    
    try:
        from core.views import payroll_dashboard
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/core/paie/')
        request.user = admin
        
        # Ajouter les attributs manquants pour les messages
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        response = payroll_dashboard(request)
        print(f"✅ Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ ERREUR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("TEST 2: /core/paie/calculer/ (calculate_salaries)")
    print("="*60)
    
    try:
        from core.views import calculate_salaries
        
        factory = RequestFactory()
        request = factory.get('/core/paie/calculer/')
        request.user = admin
        
        # Ajouter les attributs manquants pour les messages
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        response = calculate_salaries(request)
        print(f"✅ Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ ERREUR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("TEST 3: /core/taux-change/ (exchange_rates)")
    print("="*60)
    
    try:
        from core.views import exchange_rates
        
        factory = RequestFactory()
        request = factory.get('/core/taux-change/')
        request.user = admin
        
        response = exchange_rates(request)
        print(f"✅ Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ ERREUR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"❌ Erreur générale: {e}")
    import traceback
    traceback.print_exc()

#!/usr/bin/env python
"""
Script de test pour vérifier l'encodage UTF-8 dans le projet Django
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_utf8_encoding():
    """Tester l'encodage UTF-8 dans tout le projet"""
    
    print("🔍 TEST D'ENCODAGE UTF-8 - RAPID CASH")
    print("=" * 50)
    
    # 1. Test des settings Django
    print("\n📋 Configuration Django:")
    from django.conf import settings
    
    print(f"   LANGUAGE_CODE: {settings.LANGUAGE_CODE}")
    print(f"   DEFAULT_CHARSET: {getattr(settings, 'DEFAULT_CHARSET', 'Non défini')}")
    print(f"   FILE_CHARSET: {getattr(settings, 'FILE_CHARSET', 'Non défini')}")
    print(f"   USE_I18N: {settings.USE_I18N}")
    
    # 2. Test des modèles
    print("\n📊 Modèles Django:")
    from core.models import Currency, ExchangeRate
    from operations.models import Caisse, Operation
    from finance.models import Expense
    
    # Test création avec accents
    try:
        # Test Currency
        currency = Currency.objects.create(
            code='EUR',
            name='Euro',
            symbol='€'
        )
        print(f"   ✅ Currency: {currency.name}")
        
        # Test ExchangeRate
        ex_rate = ExchangeRate.objects.create(
            base_currency=currency,
            target_currency=currency,
            rate=1.0
        )
        print(f"   ✅ ExchangeRate: {ex_rate}")
        
        # Test Caisse
        caisse = Caisse.objects.create(
            name='Caisse principale',
            currency=currency
        )
        print(f"   ✅ Caisse: {caisse.name}")
        
        # Test Expense
        expense = Expense.objects.create(
            amount=100.00,
            currency=currency,
            reason='Dépense test',
            admin=None
        )
        print(f"   ✅ Expense: {expense.reason}")
        
        print("   🎉 Tous les modèles acceptent les accents!")
        
    except Exception as e:
        print(f"   ❌ Erreur modèles: {e}")
    
    # 3. Test des templates
    print("\n🎨 Templates:")
    template_dir = settings.TEMPLATES[0]['DIRS'][0]
    
    # Vérifier les meta tags UTF-8
    base_template = os.path.join(template_dir, 'base.html')
    if os.path.exists(base_template):
        with open(base_template, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'charset="UTF-8"' in content:
                print("   ✅ base.html contient charset=\"UTF-8\"")
            else:
                print("   ❌ base.html ne contient pas charset=\"UTF-8\"")
    
    # 4. Test des strings français
    print("\n🇫🇷 Test des caractères français:")
    
    test_strings = [
        "Dépenses",
        "Opérations", 
        "Nom de la caisse",
        "Taux de change",
        "Paiements partenaires",
        "éèàêëîïôöùûüÿç",
        "ÀÉÈÊËÎÏÔÖÙÛÜŸÇ"
    ]
    
    for test_string in test_strings:
        try:
            # Test encodage/décodage
            encoded = test_string.encode('utf-8')
            decoded = encoded.decode('utf-8')
            
            if decoded == test_string:
                print(f"   ✅ '{test_string}' - OK")
            else:
                print(f"   ❌ '{test_string}' - Erreur d'encodage")
                
        except Exception as e:
            print(f"   ❌ '{test_string}' - {e}")
    
    # 5. Test de l'admin
    print("\n🔧 Admin Django:")
    try:
        from django.test import Client
        client = Client()
        
        # Test de l'accès à l'admin
        response = client.get('/admin/')
        
        # Vérifier les headers
        content_type = response.get('Content-Type', '')
        if 'charset=utf-8' in content_type.lower():
            print("   ✅ Admin utilise UTF-8")
        else:
            print(f"   ❌ Admin Content-Type: {content_type}")
            
        # Vérifier le contenu
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if 'charset' in content.lower():
                print("   ✅ Page admin contient charset")
            else:
                print("   ❌ Page admin ne contient pas charset")
        
    except Exception as e:
        print(f"   ❌ Erreur admin: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 TEST TERMINÉ")
    
    # Nettoyage des données de test
    try:
        expense.delete()
        caisse.delete()
        ex_rate.delete()
        currency.delete()
        print("🧹 Données de test nettoyées")
    except:
        pass

if __name__ == '__main__':
    test_utf8_encoding()

#!/usr/bin/env python
"""
Setup script pour Render - Créer admin et assigner une caisse
With comprehensive error handling and logging
"""
import os
import sys
import traceback

# Setup Django first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.production')

try:
    import django
    django.setup()
except Exception as e:
    print(f"❌ Erreur Django setup: {e}")
    traceback.print_exc()
    sys.exit(1)

# Import Django models
try:
    from django.contrib.auth import get_user_model
    from axes.utils import reset
    from finance.models import Caisse
    from core.models import Currency
    User = get_user_model()
except Exception as e:
    print(f"❌ Erreur import models: {e}")
    traceback.print_exc()
    sys.exit(1)


def setup_currencies():
    """Setup currencies with error handling"""
    try:
        currencies_data = [
            {'code': 'USD', 'name': 'Dollar Américain', 'symbol': '$', 'is_reference': True},
            {'code': 'CDF', 'name': 'Franc Congolais', 'symbol': 'FC'},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€'},
            {'code': 'GBP', 'name': 'Livre Sterling', 'symbol': '£'},
            {'code': 'TL', 'name': 'Livre Turque', 'symbol': '₺'},
        ]
        
        currencies = {}
        for curr in currencies_data:
            try:
                currency, created = Currency.objects.get_or_create(
                    code=curr['code'],
                    defaults={
                        'name': curr['name'], 
                        'symbol': curr['symbol'],
                        'is_reference': curr.get('is_reference', False)
                    }
                )
                currencies[curr['code']] = currency
                if created:
                    print(f"✅ Devise créée: {curr['code']} - {curr['name']}")
                else:
                    print(f"ℹ️ Devise existe: {curr['code']}")
            except Exception as e:
                print(f"⚠️ Erreur création devise {curr['code']}: {e}")
                continue
        
        return currencies
    except Exception as e:
        print(f"❌ Erreur setup currencies: {e}")
        traceback.print_exc()
        return {}


def setup_exchange_rates(currencies):
    """Setup exchange rates with error handling"""
    try:
        from core.models import ExchangeRate
        
        exchange_rates = [
            {'base': 'USD', 'target': 'CDF', 'rate': 2800.00},
            {'base': 'USD', 'target': 'EUR', 'rate': 0.92},
            {'base': 'USD', 'target': 'GBP', 'rate': 0.79},
            {'base': 'USD', 'target': 'TL', 'rate': 32.50},
            {'base': 'EUR', 'target': 'CDF', 'rate': 3043.00},
            {'base': 'EUR', 'target': 'GBP', 'rate': 0.86},
            {'base': 'EUR', 'target': 'TL', 'rate': 35.30},
            {'base': 'GBP', 'target': 'CDF', 'rate': 3542.00},
            {'base': 'GBP', 'target': 'TL', 'rate': 41.00},
            {'base': 'TL', 'target': 'CDF', 'rate': 86.15},
        ]
        
        for rate_data in exchange_rates:
            try:
                base_curr = currencies.get(rate_data['base'])
                target_curr = currencies.get(rate_data['target'])
                if base_curr and target_curr:
                    rate_obj, created = ExchangeRate.objects.get_or_create(
                        base_currency=base_curr,
                        target_currency=target_curr,
                        defaults={'rate': rate_data['rate']}
                    )
                    if created:
                        print(f"✅ Taux créé: {rate_data['base']} → {rate_data['target']}: {rate_data['rate']}")
            except Exception as e:
                print(f"⚠️ Erreur taux {rate_data['base']}→{rate_data['target']}: {e}")
                continue
    except Exception as e:
        print(f"❌ Erreur setup exchange rates: {e}")
        traceback.print_exc()


def setup_admin_user():
    """Setup admin user with error handling"""
    try:
        user, created = User.objects.get_or_create(
            username='kizy',
            defaults={
                'email': 'kizy@rapid-cash.com',
                'first_name': 'Admin',
                'last_name': 'Kizy',
                'is_staff': True,
                'is_superuser': True,
                'role': 'ADMIN',
            }
        )
        
        user.set_password('789456+++')
        user.is_staff = True
        user.is_superuser = True
        user.role = 'ADMIN'
        user.save()
        
        print(f"✅ Admin {'créé' if created else 'mis à jour'}: kizy")
        
        try:
            reset(username='kizy')
            print("✅ Compte kizy déverrouillé !")
        except Exception as e:
            print(f"⚠️ Erreur déverrouillage compte: {e}")
        
        return user
    except Exception as e:
        print(f"❌ Erreur setup admin: {e}")
        traceback.print_exc()
        return None


def setup_caisses(admin_user, currencies):
    """Setup caisses with error handling"""
    if not admin_user:
        print("❌ Impossible créer caisses: admin user manquant")
        return
    
    try:
        usd_currency = currencies.get('USD')
        if usd_currency:
            try:
                caisse, created = Caisse.objects.get_or_create(
                    name='Caisse Principale',
                    defaults={
                        'currency': usd_currency,
                        'balance': 100000.00,
                        'manager': admin_user,
                        'location': 'Siège Principal',
                        'is_active': True,
                    }
                )
                if created:
                    print(f"✅ Caisse créée: {caisse.name}")
                else:
                    print(f"ℹ️ Caisse existe: {caisse.name}")
                    caisse.manager = admin_user
                    caisse.save()
            except Exception as e:
                print(f"⚠️ Erreur caisse principale: {e}")
        
        for curr_code in ['CDF', 'EUR', 'GBP']:
            currency = currencies.get(curr_code)
            if currency:
                try:
                    caisse, created = Caisse.objects.get_or_create(
                        name=f'Caisse {curr_code}',
                        defaults={
                            'currency': currency,
                            'balance': 50000.00 if curr_code == 'CDF' else 10000.00,
                            'manager': admin_user,
                            'location': 'Siège Principal',
                            'is_active': True,
                        }
                    )
                    if created:
                        print(f"✅ Caisse créée: {caisse.name}")
                except Exception as e:
                    print(f"⚠️ Erreur caisse {curr_code}: {e}")
                    continue
    except Exception as e:
        print(f"❌ Erreur setup caisses: {e}")
        traceback.print_exc()


def setup_admin_and_caisse():
    """Main setup function with comprehensive error handling"""
    print("🚀 Démarrage du setup Rapid Cash...")
    print("=" * 50)
    
    errors = []
    
    print("\n📊 Setup des devises...")
    currencies = setup_currencies()
    if not currencies:
        errors.append("Échec setup currencies")
    
    print("\n💱 Setup des taux de change...")
    setup_exchange_rates(currencies)
    
    print("\n👤 Setup admin user...")
    admin_user = setup_admin_user()
    if not admin_user:
        errors.append("Échec setup admin user")
    
    print("\n💰 Setup des caisses...")
    setup_caisses(admin_user, currencies)
    
    print("\n" + "=" * 50)
    if errors:
        print(f"⚠️  Setup terminé avec {len(errors)} erreur(s):")
        for err in errors:
            print(f"   - {err}")
    else:
        print("🎉 Setup terminé avec succès!")
    
    print(f"\nIdentifiants admin:")
    print(f"  - Username: kizy")
    print(f"  - Password: 789456+++")
    print(f"  - Admin URL: /admin/")
    
    return len(errors) == 0


if __name__ == "__main__":
    success = setup_admin_and_caisse()
    sys.exit(0 if success else 1)

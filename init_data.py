#!/usr/bin/env python
"""
Rapid Cash System Initialization Script
Sets up currencies, fee grid, and sample data according to the specification
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Currency, User
from operations.models import Caisse, Operation, FeeGrid
from finance.models import Expense

print("=" * 60)
print("RAPID CASH SYSTEM INITIALIZATION")
print("=" * 60)

# 1. Create currencies according to specification (section 11.1)
currencies_data = [
    {'code': 'USD', 'name': 'US Dollar', 'symbol': '$', 'is_reference': True},
    {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'is_reference': False},
    {'code': 'GBP', 'name': 'British Pound', 'symbol': '£', 'is_reference': False},
    {'code': 'CDF', 'name': 'Congolese Franc', 'symbol': 'CDF', 'is_reference': False},
    {'code': 'TRY', 'name': 'Turkish Lira', 'symbol': '₺', 'is_reference': False},
]

currencies = {}
for data in currencies_data:
    curr, created = Currency.objects.get_or_create(code=data['code'], defaults=data)
    currencies[data['code']] = curr
    status = "CREATED" if created else "EXISTS"
    print(f"Currency {data['code']}: {status}")

# 2. Create Fee Grid according to specification (section 5)
# Fee grid for USD - automatic calculation
fee_grid_data = [
    {'min': 0.10, 'max': 40.00, 'fee': 5.00},
    {'min': 40.10, 'max': 100.00, 'fee': 8.00},
    {'min': 100.10, 'max': 200.00, 'fee': 15.00},
    {'min': 200.10, 'max': 300.00, 'fee': 20.00},
    {'min': 300.10, 'max': 400.00, 'fee': 26.00},
    {'min': 400.10, 'max': 600.00, 'fee': 30.00},
    {'min': 600.10, 'max': 800.00, 'fee': 35.00},
    {'min': 800.10, 'max': 1000.00, 'fee': 40.00},
    {'min': 1000.10, 'max': 1500.00, 'fee': 45.00},
    {'min': 1500.10, 'max': 1800.00, 'fee': 64.00},
    {'min': 1800.10, 'max': 2000.00, 'fee': 80.00},
]

usd = currencies['USD']
for data in fee_grid_data:
    fee_grid, created = FeeGrid.objects.get_or_create(
        currency=usd,
        min_amount=data['min'],
        max_amount=data['max'],
        defaults={'fee_amount': data['fee']}
    )
    status = "CREATED" if created else "EXISTS"
    print(f"Fee Grid {data['min']}-{data['max']} USD: {status}")

print(f"\nTotal Fee Grids: {FeeGrid.objects.count()}")

# 3. Get or create admin user
admin, created = User.objects.get_or_create(
    username='Kizy',
    defaults={
        'role': 'ADMIN',
        'email': 'admin@rapircash.com',
        'phone': '+243999999999',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print(f"\nAdmin user created: Kizy / admin123")
else:
    print(f"\nAdmin user exists: Kizy")

# 4. Get or create agent users
agent1, created = User.objects.get_or_create(
    username='Mpoto',
    defaults={
        'role': 'AGENT',
        'email': 'mpoto@rapircash.com',
        'phone': '+243988888888',
        'commission_rate': 20.00
    }
)
if created:
    agent1.set_password('agent123')
    agent1.save()
    print(f"Agent created: Mpoto / agent123 (20% commission)")

agent2, created = User.objects.get_or_create(
    username='ramatkal01',
    defaults={
        'role': 'AGENT',
        'email': 'ramatkal@rapircash.com',
        'phone': '+243977777777',
        'commission_rate': 15.00
    }
)
if created:
    agent2.set_password('agent123')
    agent2.save()
    print(f"Agent created: ramatkal01 / agent123 (15% commission)")

# 5. Create Caisse for admin
admin_caisse, created = Caisse.objects.get_or_create(
    name='Caisse Principale',
    defaults={
        'agent': admin,
        'balance': 10000.00,
        'currency': usd
    }
)
if created:
    print(f"\nCaisse created: Caisse Principale (10,000 USD)")

# 6. Create sample operations for testing
agents = User.objects.filter(role='AGENT')
caisses = Caisse.objects.all()

if Operation.objects.count() == 0 and agents.exists() and caisses.exists():
    from django.utils import timezone
    from datetime import timedelta
    
    agent = agents.first()
    caisse = caisses.first()
    
    # Create sample operations
    sample_ops = [
        {'type': 'TRANSFER', 'amount': 150.00, 'fee': 15.00},
        {'type': 'TRANSFER', 'amount': 500.00, 'fee': 30.00},
        {'type': 'WITHDRAWAL', 'amount': 250.00, 'fee': 20.00},
        {'type': 'TRANSFER', 'amount': 1000.00, 'fee': 40.00},
    ]
    
    for i, op_data in enumerate(sample_ops):
        Operation.objects.create(
            transaction_number=f'TXN{1000+i}',
            agent=agent,
            caisse=caisse,
            type=op_data['type'],
            amount_orig=op_data['amount'],
            currency_orig=usd,
            amount_ref=op_data['amount'],
            currency_ref=usd,
            exchange_rate=1.0,
            fee_calculated=op_data['fee'],
            date_time=timezone.now() - timedelta(days=i)
        )
    print(f"\nSample operations created: {len(sample_ops)}")

# 7. Create sample expenses
if Expense.objects.count() == 0 and admin:
    Expense.objects.create(
        amount=50.00,
        currency=usd,
        reason='Ravitaillement caisse',
        category='Ravitaillement',
        destination='Caisse Principale',
        comment='Approvisionnement initial',
        admin=admin
    )
    Expense.objects.create(
        amount=25.00,
        currency=usd,
        reason='Crédit téléphone',
        category='Communication',
        destination='Agent Mpoto',
        comment='Crédit phone opérationnel',
        admin=admin
    )
    print("Sample expenses created: 2")

print("\n" + "=" * 60)
print("INITIALIZATION COMPLETE")
print("=" * 60)
print(f"\nCurrencies: {Currency.objects.count()}")
print(f"Fee Grids: {FeeGrid.objects.count()}")
print(f"Users: {User.objects.count()}")
print(f"Caisses: {Caisse.objects.count()}")
print(f"Operations: {Operation.objects.count()}")
print(f"Expenses: {Expense.objects.count()}")

print("\n" + "=" * 60)
print("LOGIN CREDENTIALS")
print("=" * 60)
print("Admin: Kizy / admin123")
print("Agent: Mpoto / agent123")
print("Agent: ramatkal01 / agent123")
print("=" * 60)

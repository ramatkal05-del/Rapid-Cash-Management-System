#!/usr/bin/env python
"""
Mise à jour de la grille de frais selon les nouvelles spécifications
"""

import os

def update_fee_grid():
    """Mettre à jour la grille de frais"""
    
    print("💰 MISE À JOUR GRILLE DE FRAIS")
    print("=" * 50)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from operations.models import FeeGrid
        from core.models import Currency
        from decimal import Decimal
        
        # Obtenir la devise USD
        usd = Currency.objects.filter(code='USD').first()
        if not usd:
            print("❌ Devise USD non trouvée")
            return
        
        print(f"\n📊 Devise: {usd.code} ({usd.name})")
        
        # Supprimer les anciennes grilles pour USD
        old_count = FeeGrid.objects.filter(currency=usd).count()
        FeeGrid.objects.filter(currency=usd).delete()
        print(f"🗑️  {old_count} ancienne(s) grille(s) supprimée(s)")
        
        # Nouvelle grille de frais
        fee_ranges = [
            # (min_amount, max_amount, fee_amount)
            (Decimal('0.10'), Decimal('40.00'), Decimal('5.00')),
            (Decimal('40.10'), Decimal('100.00'), Decimal('8.00')),
            (Decimal('100.10'), Decimal('200.00'), Decimal('15.00')),
            (Decimal('200.10'), Decimal('300.00'), Decimal('20.00')),
            (Decimal('300.10'), Decimal('400.00'), Decimal('26.00')),
            (Decimal('400.10'), Decimal('600.00'), Decimal('30.00')),
            (Decimal('600.10'), Decimal('800.00'), Decimal('35.00')),
            (Decimal('800.10'), Decimal('1000.00'), Decimal('40.00')),
            (Decimal('1000.10'), Decimal('1500.00'), Decimal('45.00')),
            (Decimal('1500.10'), Decimal('1800.00'), Decimal('64.00')),
            (Decimal('1800.10'), Decimal('2000.00'), Decimal('80.00')),
            (Decimal('2000.10'), Decimal('2500.00'), Decimal('95.00')),
            (Decimal('2500.10'), Decimal('3000.00'), Decimal('110.00')),
            (Decimal('3000.10'), Decimal('4000.00'), Decimal('135.00')),
            (Decimal('4000.10'), Decimal('5000.00'), Decimal('160.00')),
            (Decimal('5000.10'), Decimal('7000.00'), Decimal('200.00')),
            (Decimal('7000.10'), Decimal('10000.00'), Decimal('260.00')),
        ]
        
        print(f"\n📝 Création des {len(fee_ranges)} grilles de frais:\n")
        
        created_count = 0
        for min_amt, max_amt, fee_amt in fee_ranges:
            grid = FeeGrid.objects.create(
                min_amount=min_amt,
                max_amount=max_amt,
                fee_amount=fee_amt,
                currency=usd
            )
            created_count += 1
            print(f"   {created_count:2d}. {min_amt:>8.2f}$ - {max_amt:>8.2f}$  →  {fee_amt:>6.2f}$")
        
        print(f"\n✅ {created_count} grilles créées avec succès!")
        
        # Vérification
        print("\n🔍 VÉRIFICATION:")
        all_grids = FeeGrid.objects.filter(currency=usd).order_by('min_amount')
        print(f"   Total grilles: {all_grids.count()}")
        print(f"   Première: {all_grids.first().min_amount}$ - {all_grids.first().max_amount}$")
        print(f"   Dernière: {all_grids.last().min_amount}$ - {all_grids.last().max_amount}$")
        
        print("\n🎊 Grille de frais mise à jour avec succès!")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    update_fee_grid()

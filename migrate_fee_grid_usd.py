#!/usr/bin/env python
"""
Migration vers une grille de frais unique en USD
Supprime toutes les grilles non-USD existantes
"""

import os

def migrate_fee_grid():
    """Migrer vers une grille de frais unique USD"""
    
    print("🔄 MIGRATION VERS GRILLE DE FRAIS UNIQUE USD")
    print("=" * 55)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from operations.models import FeeGrid
        from core.models import Currency
        from decimal import Decimal
        
        # 1. Vérifier que USD existe
        usd = Currency.objects.filter(code='USD').first()
        if not usd:
            print("❌ ERREUR: Devise USD non trouvée!")
            print("   Créez d'abord la devise USD avec code='USD'")
            return
        
        print(f"✅ Devise USD trouvée: {usd.name}")
        
        # 2. Compter les grilles avant migration
        all_grids = FeeGrid.objects.all()
        usd_grids = FeeGrid.objects.filter(currency=usd)
        non_usd_grids = FeeGrid.objects.exclude(currency=usd)
        
        print(f"\n📊 AVANT MIGRATION:")
        print(f"   Total grilles: {all_grids.count()}")
        print(f"   Grilles USD: {usd_grids.count()}")
        print(f"   Grilles non-USD: {non_usd_grids.count()}")
        
        # 3. Afficher les grilles non-USD qui vont être supprimées
        if non_usd_grids.exists():
            print(f"\n⚠️  GRILLES NON-USD À SUPPRIMER:")
            for grid in non_usd_grids:
                print(f"   • {grid.min_amount} - {grid.max_amount} {grid.currency.code} → {grid.fee_amount}")
        
        # 4. Supprimer les grilles non-USD
        deleted_count = non_usd_grids.count()
        if deleted_count > 0:
            non_usd_grids.delete()
            print(f"\n🗑️  {deleted_count} grille(s) non-USD supprimée(s)")
        else:
            print(f"\n✅ Aucune grille non-USD à supprimer")
        
        # 5. Vérifier que les grilles USD utilisent bien USD
        usd_grids_after = FeeGrid.objects.all()
        print(f"\n📊 APRÈS MIGRATION:")
        print(f"   Total grilles: {usd_grids_after.count()}")
        print(f"   Toutes en USD: {usd_grids_after.filter(currency=usd).count() == usd_grids_after.count()}")
        
        # 6. Liste des grilles USD restantes
        print(f"\n📋 GRILLES USD FINALES:")
        for i, grid in enumerate(usd_grids_after.order_by('min_amount'), 1):
            print(f"   {i:2d}. {grid.min_amount:>8.2f}$ - {grid.max_amount:>8.2f}$ → {grid.fee_amount:>6.2f}$")
        
        print(f"\n✅ MIGRATION TERMINÉE AVEC SUCCÈS!")
        print(f"   Source unique de vérité: Grille de frais en USD uniquement")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    migrate_fee_grid()

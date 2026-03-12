from django.core.management.base import BaseCommand
from core.models import Currency
from operations.models import FeeGrid
from decimal import Decimal

class Command(BaseCommand):
    help = 'Initialise la grille tarifaire Rapid Cash'

    def handle(self, *args, **options):
        # 1. Obtenir ou créer la devise de référence USD
        usd, created = Currency.objects.get_or_create(
            code='USD',
            defaults={'name': 'US Dollar', 'symbol': '$', 'is_reference': True}
        )
        if not usd.is_reference:
            usd.is_reference = True
            usd.save()

        # 2. Définition des paliers
        tiers = [
            (0.10, 40.00, 5.00),
            (40.10, 100.00, 8.00),
            (100.10, 200.00, 15.00),
            (200.10, 300.00, 20.00),
            (300.10, 400.00, 26.00),
            (400.10, 600.00, 30.00),
            (600.10, 800.00, 35.00),
            (800.10, 1000.00, 40.00),
            (1000.10, 1500.00, 45.00),
            (1500.10, 1800.00, 64.00),
            (1800.10, 2000.00, 80.00),
        ]

        # Nettoyage de la grille existante si nécessaire (optionnel)
        # FeeGrid.objects.filter(currency=usd).delete()

        for min_a, max_a, fee in tiers:
            FeeGrid.objects.update_or_create(
                min_amount=Decimal(str(min_a)),
                max_amount=Decimal(str(max_a)),
                currency=usd,
                defaults={'fee_amount': Decimal(str(fee))}
            )
            self.stdout.write(self.style.SUCCESS(f'Palier {min_a} - {max_a} : {fee} USD ajouté/mis à jour.'))

        self.stdout.write(self.style.SUCCESS('Grille tarifaire initialisée avec succès.'))

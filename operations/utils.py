from decimal import Decimal
from .models import FeeGrid

def calculate_fee(amount, currency):
    """
    Calculates the fee based on the amount and currency using the FeeGrid tiered system.
    If no specific tier is found, it could return a default or raise an error.
    """
    try:
        tier = FeeGrid.objects.get(
            currency=currency,
            min_amount__lte=amount,
            max_amount__gte=amount
        )
        return tier.fee_amount
    except FeeGrid.DoesNotExist:
        # Fallback or default fee logic - for now return 0 or log warning
        return Decimal('0.00')

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from core.models import AuditLog, User, Currency, ExchangeRate
from operations.models import Operation, Caisse, FeeGrid
from finance.models import Expense, PartnerContract, PartnerPayment
import json


def get_client_ip(request):
    """Extract client IP from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def track_model_changes(sender, instance, created, **kwargs):
    """Track model changes using signals"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Try to get current user from thread local or fallback
    try:
        from threading import local
        _thread_local = local()
        user = getattr(_thread_local, 'current_user', None)
    except:
        user = None
    
    if created:
        AuditLog.log_create(user, instance, created=True)
    else:
        # For updates, we need the old instance
        pass  # Handled in pre_save


@receiver(pre_save, sender=Operation)
def operation_pre_save(sender, instance, **kwargs):
    """Track operation before save"""
    if instance.pk:
        try:
            instance._old_instance = Operation.objects.get(pk=instance.pk)
        except Operation.DoesNotExist:
            instance._old_instance = None
    else:
        instance._old_instance = None


@receiver(post_save, sender=Operation)
def operation_post_save(sender, instance, created, **kwargs):
    """Track operation after save"""
    from threading import local
    _thread_local = local()
    user = getattr(_thread_local, 'current_user', None)
    
    if created:
        AuditLog.objects.create(
            action=AuditLog.ActionType.TRANSACTION,
            user=user,
            model_name='operation',
            object_id=str(instance.pk),
            object_repr=f"Transaction {instance.transaction_number}",
            changes={
                'transaction_number': [None, instance.transaction_number],
                'amount_orig': [None, str(instance.amount_orig)],
                'amount_ref': [None, str(instance.amount_ref)],
                'fee_calculated': [None, str(instance.fee_calculated)],
                'type': [None, instance.type],
            }
        )
    else:
        old = getattr(instance, '_old_instance', None)
        if old:
            changes = {}
            for field in ['status', 'amount_orig', 'amount_ref', 'fee_calculated', 'observation']:
                old_val = getattr(old, field, None)
                new_val = getattr(instance, field, None)
                if str(old_val) != str(new_val):
                    changes[field] = [str(old_val), str(new_val)]
            
            if changes:
                AuditLog.objects.create(
                    action=AuditLog.ActionType.UPDATE,
                    user=user,
                    model_name='operation',
                    object_id=str(instance.pk),
                    object_repr=f"Transaction {instance.transaction_number}",
                    changes=changes
                )


@receiver(post_save, sender=Expense)
def expense_post_save(sender, instance, created, **kwargs):
    """Track expense after save"""
    from threading import local
    _thread_local = local()
    user = getattr(_thread_local, 'current_user', None)
    
    if created:
        AuditLog.objects.create(
            action=AuditLog.ActionType.EXPENSE,
            user=user,
            model_name='expense',
            object_id=str(instance.pk),
            object_repr=f"Dépense {instance.reason}",
            changes={
                'amount': [None, str(instance.amount)],
                'reason': [None, instance.reason],
                'category': [None, instance.category],
            }
        )


@receiver(post_save, sender=FeeGrid)
def fee_grid_post_save(sender, instance, created, **kwargs):
    """Track fee grid after save"""
    from threading import local
    _thread_local = local()
    user = getattr(_thread_local, 'current_user', None)
    
    action = AuditLog.ActionType.CREATE if created else AuditLog.ActionType.UPDATE
    changes = {}
    
    if created:
        changes = {
            'min_amount': [None, str(instance.min_amount)],
            'max_amount': [None, str(instance.max_amount)],
            'fee_amount': [None, str(instance.fee_amount)],
            'currency': [None, str(instance.currency)],
        }
    else:
        changes = {'fee_grid': 'updated'}
    
    AuditLog.objects.create(
        action=action,
        user=user,
        model_name='feegrid',
        object_id=str(instance.pk),
        object_repr=f"FeeGrid {instance.min_amount}-{instance.max_amount}",
        changes=changes
    )


@receiver(post_save, sender=Currency)
def currency_post_save(sender, instance, created, **kwargs):
    """Track currency after save"""
    from threading import local
    _thread_local = local()
    user = getattr(_thread_local, 'current_user', None)
    
    if created:
        AuditLog.objects.create(
            action=AuditLog.ActionType.CURRENCY,
            user=user,
            model_name='currency',
            object_id=str(instance.pk),
            object_repr=f"{instance.code} - {instance.name}",
            changes={
                'code': [None, instance.code],
                'name': [None, instance.name],
                'is_reference': [None, str(instance.is_reference)],
            }
        )


@receiver(post_save, sender=ExchangeRate)
def exchange_rate_post_save(sender, instance, created, **kwargs):
    """Track exchange rate after save"""
    from threading import local
    _thread_local = local()
    user = getattr(_thread_local, 'current_user', None)
    
    if created:
        AuditLog.objects.create(
            action=AuditLog.ActionType.EXCHANGE_RATE,
            user=user,
            model_name='exchangerate',
            object_id=str(instance.pk),
            object_repr=f"{instance.base_currency.code} -> {instance.target_currency.code}",
            changes={
                'rate': [None, str(instance.rate)],
            }
        )

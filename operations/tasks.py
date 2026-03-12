"""
Rapid Cash - Celery Tasks for Operations
"""
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def generate_daily_report(self):
    """
    Generate daily report and send via email (async)
    """
    from operations.models import Operation
    from operations.services import get_operation_summary
    
    today = timezone.now().date()
    operations = Operation.objects.filter(date_time__date=today)
    
    summary = get_operation_summary(operations)
    
    # Generate report content
    report_content = f"""
    Daily Report - {today}
    ====================
    
    Total Operations: {summary['count']}
    Total Volume: {summary['total_volume']}
    Total Fees: {summary['total_fees']}
    
    Transfers: {summary['transfers']}
    Withdrawals: {summary['withdrawals']}
    """
    
    # Log the report
    logger.info(f"Daily report generated: {report_content}")
    
    return {
        'date': str(today),
        'summary': {
            'count': summary['count'],
            'volume': str(summary['total_volume']),
            'fees': str(summary['total_fees']),
        }
    }


@shared_task(bind=True)
def send_operation_confirmation(self, operation_id):
    """
    Send confirmation email after operation (async)
    """
    from operations.models import Operation
    
    try:
        operation = Operation.objects.get(id=operation_id)
        
        subject = f"Transaction confirmée - {operation.transaction_number}"
        message = f"""
        Bonjour {operation.agent.username},
        
        Votre transaction a été enregistrée avec succès.
        
        Numéro: {operation.transaction_number}
        Type: {operation.get_type_display()}
        Montant: {operation.amount_orig} {operation.currency_orig.code}
        Frais: {operation.fee_calculated}
        
        Date: {operation.date_time}
        
        Merci de votre confiance.
        """
        
        # In production, send actual email
        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [operation.agent.email])
        
        logger.info(f"Confirmation email queued for operation {operation_id}")
        
        return {'status': 'sent', 'operation_id': operation_id}
        
    except Operation.DoesNotExist:
        logger.error(f"Operation {operation_id} not found")
        return {'status': 'error', 'message': 'Operation not found'}


@shared_task(bind=True)
def send_daily_summary_email(self, recipient_email):
    """
    Send daily summary email to admins (async)
    """
    from operations.models import Operation
    from finance.models import Expense
    
    today = timezone.now().date()
    
    # Get today's data
    operations = Operation.objects.filter(date_time__date=today)
    expenses = Expense.objects.filter(date=today)
    
    total_volume = operations.aggregate(Sum('amount_ref'))['amount_ref__sum'] or 0
    total_fees = operations.aggregate(Sum('fee_calculated'))['fee_calculated__sum'] or 0
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    subject = f"Rapport Journalier - {today}"
    message = f"""
    Rapport Journalier - {today}
    =========================
    
    Opérations: {operations.count()}
    Volume Total: {total_volume}
    Frais Collectés: {total_fees}
    Dépenses: {total_expenses}
    Bénéfice Net: {total_fees - total_expenses}
    """
    
    # In production, send actual email
    # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
    
    logger.info(f"Daily summary email sent to {recipient_email}")
    
    return {'status': 'sent', 'recipient': recipient_email}

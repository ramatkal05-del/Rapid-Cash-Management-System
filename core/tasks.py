"""
Rapid Cash - Celery Tasks for Core
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def cleanup_audit_logs(self, days=90):
    """
    Clean up old audit logs (older than specified days)
    Default: 90 days
    """
    from core.models import AuditLog
    
    cutoff_date = timezone.now() - timedelta(days=days)
    
    deleted_count, _ = AuditLog.objects.filter(
        timestamp__lt=cutoff_date
    ).delete()
    
    logger.info(f"Cleaned up {deleted_count} audit logs older than {days} days")
    
    return {
        'deleted_count': deleted_count,
        'cutoff_date': str(cutoff_date),
    }


@shared_task(bind=True)
def log_user_login(self, user_id, ip_address=None):
    """
    Log user login asynchronously
    """
    from core.models import AuditLog, User
    
    try:
        user = User.objects.get(id=user_id)
        AuditLog.log_action(
            user=user,
            action=AuditLog.ActionType.LOGIN,
            model_name='user',
            object_id=user_id,
            object_repr=str(user),
            ip_address=ip_address,
        )
        logger.info(f"User login logged: {user.username}")
        return {'status': 'success'}
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return {'status': 'error', 'message': 'User not found'}


@shared_task(bind=True)
def log_system_event(self, event_type, message, level='INFO'):
    """
    Log system event
    """
    from core.models import AuditLog
    
    logger.log(
        level=logging.INFO if level == 'INFO' else logging.ERROR,
        msg=f"System Event [{event_type}]: {message}"
    )
    
    return {'status': 'logged', 'event_type': event_type}

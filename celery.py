"""
Rapid Cash - Celery Configuration
Async tasks for PDF generation, emails, and background processing
"""
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('rapid_cash')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')


# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    # Generate daily reports at midnight
    'generate-daily-report': {
        'task': 'operations.tasks.generate_daily_report',
        'schedule': 0,  # Run at midnight
    },
    # Clean up old audit logs (older than 90 days)
    'cleanup-old-audit-logs': {
        'task': 'core.tasks.cleanup_audit_logs',
        'schedule': 86400,  # Run daily
    },
}

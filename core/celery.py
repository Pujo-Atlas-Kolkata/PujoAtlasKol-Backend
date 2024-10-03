import os
from celery import Celery
from decouple import config

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('DJANGO_SETTINGS_MODULE'))

# Initialize Celery
app = Celery('core')

# Load Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Ensure all Django apps are loaded
import django
django.setup()

# Autodiscover tasks from installed Django apps
app.autodiscover_tasks()

# Import tasks after Django setup
from core.task import update_pujo_scores, backup_logs_to_minio

# Register tasks explicitly
app.register_task(update_pujo_scores)
app.register_task(backup_logs_to_minio)

# Set additional configuration
app.conf.broker_connection_retry_on_startup = True
app.conf.task_time_limit = 300

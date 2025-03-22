from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_service.settings')

# Create a Celery instance
app = Celery('user_service')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Celery Beat Schedule
app.conf.beat_schedule = {
    # Task to reduce collections every day at midnight
    'reduce_collections_task': {
        'task': 'core.tasks.reduce_collections_task',
        'schedule': crontab(hour=0, minute=0),
    },
}
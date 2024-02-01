# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PawsCareConnect.settings')
app = Celery('PawsCareConnect')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'check-appointments-every-day': {
        'task': 'yourapp.tasks.check_appointments',
        'schedule': crontab(hour=0, minute=0),
    },
}

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

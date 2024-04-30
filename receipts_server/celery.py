from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'receipts_server.settings')

app = Celery('receipts_server', broker='redis://localhost:6379/0')

app.conf.result_backend = 'redis://localhost:6379/1'

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
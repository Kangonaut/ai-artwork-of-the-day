import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aotd_backend.settings')
app = Celery('aotd_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

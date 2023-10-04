import os
from celery import Celery
from celery.signals import setup_logging

# set the default Django settings module for the celery application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aotd_backend.settings')

# create the celery application
app = Celery('aotd_backend')

# all celery-related configuration keys should have a CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig
    from django.conf import settings

    dictConfig(settings.LOGGING)


# load task modules from all registered Django app configs
app.autodiscover_tasks()

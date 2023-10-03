from django.apps import AppConfig
import dotenv
import os


class WorkshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workshop'

    def ready(self):
        import workshop.signals.handlers  # noqa

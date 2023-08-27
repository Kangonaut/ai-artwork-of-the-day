from django.apps import AppConfig


class AiworkshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aiworkshop'

    def ready(self):
        import aiworkshop.signals.handlers  # noqa

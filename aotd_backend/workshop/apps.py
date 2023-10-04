from django.apps import AppConfig
import os
import openai


class WorkshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workshop'

    def ready(self):
        # load OpenAI API key
        openai.api_key = os.getenv('OPENAI_API_KEY')

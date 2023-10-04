from celery import shared_task
from django.core.files.base import ContentFile

import openai
import json
import base64
from datetime import datetime
import os
import logging

from . import models, ai, delivery_services

logger = logging.getLogger(__name__)


@shared_task()
def generate_artwork(user_id: int):
    # retrieve user
    user = models.CustomUser.objects.get(pk=user_id)
    logger.info(f'generating artwork for {user.username}')

    # load OpenAI API key
    openai.api_key = os.getenv('OPENAI_API_KEY')

    data: dict[str, any] = {
        'weather': 'cloudy with a little sun',
        'temperature': 'hot',
        'scenery': 'mountains',
        'animal': 'elephant',
        'style': 'hyper-realistic'
    }

    # build prompt
    json_data: str = json.dumps(data)
    chat_prompt_template: str = os.getenv('AOTD_CHAT_PROMPT_TEMPLATE')
    chat_prompt: str = chat_prompt_template.replace('<JSON-DATA>', json_data)

    # prompt chat AI
    image_prompt = ai.chat_ai.generate(
        prompt=chat_prompt
    )

    # prompt image AI
    base64_image = ai.image_ai.generate(prompt=image_prompt)
    image = base64.b64decode(base64_image)
    timestamp: str = datetime.now().isoformat()
    image_file = ContentFile(content=image, name=f'{timestamp}.png')

    # save artwork
    artwork = models.Artwork(
        user=user,
        data=data,
        image=image_file,
        image_prompt=image_prompt
    )
    artwork.save()
    logger.info(f'successfully saved artwork')

    # trigger delivery services
    logger.info(f'requesting artwork delivery')
    delivery_services.DeliveryManager.deliver(artwork)

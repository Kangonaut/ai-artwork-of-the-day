from celery import shared_task
from django.core.files.base import ContentFile

import openai
import json
import base64
from datetime import datetime

from . import models, ai


@shared_task()
def generate_artwork():
    # load OpenAI API key
    openai.api_key = models.BasicConfig.objects.get(pk='OPENAI_API_KEY').value

    data: dict[str, any] = {
        'weather': 'cloudy with a little sun',
        'temperature': 'hot',
        'scenery': 'mountains',
        'animal': 'elephant',
        'style': 'hyper-realistic'
    }

    # build prompt
    json_data: str = json.dumps(data)
    chat_prompt_template: str = models.BasicConfig.objects.get(key='AOTD_CHAT_PROMPT_TEMPLATE').value
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
    artwork = models.Artwork(data=data, image=image_file, image_prompt=image_prompt)
    artwork.save()

from celery import shared_task
import openai
import json
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
    image_url = ai.image_ai.generate(prompt=image_prompt)

    # save artwork
    artwork = models.Artwork(data=data, image_url=image_url, image_prompt=image_prompt)
    artwork.save()

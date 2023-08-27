from celery import shared_task
import openai
import json
from . import models, ai


@shared_task()
def generate_artwork():
    openai_api_key: str = models.BasicConfig.objects.get(pk='OPENAI_API_KEY').value
    openai.api_key = openai_api_key

    data: dict[str, any] = {
        'weather': 'cloudy with a little sun',
        'temperature': 'hot',
        'scenery': 'mountains',
        'animal': 'elephant',
        'style': 'hyper-realistic'
    }

    json_doc: str = json.dumps(data)

    image_prompt = ai.chat_ai.prompt('')

    image_response = openai.Image.create(
        prompt=image_prompt,
        n=1,
        size="256x256"
    )
    image_url: str = image_response['data'][0]['url']

    # save artwork
    artwork = models.Artwork(data=data, image_url=image_url, image_prompt=image_prompt)
    artwork.save()

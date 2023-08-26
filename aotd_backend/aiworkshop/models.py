from django.db import models


# Create your models here.

class BasicConfig(models.Model):
    key = models.CharField(max_length=255, null=False, primary_key=True)
    value = models.CharField(max_length=255, null=True)


class Artwork(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False, primary_key=True)
    data = models.JSONField(null=False)
    image_url = models.URLField(max_length=1_000, null=False)
    image_prompt = models.CharField(max_length=1_000)


# TODO: move code somewhere else
from django.db.models.signals import post_save
from django.dispatch import receiver

import openai
import json

from . import signals, models


@receiver(signals.artwork_request)
def generate_artwork(**kwargs):
    # TODO: start separate thread
    print('generating artwork')

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

    chat_response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        n=1,
        max_tokens=100,
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user',
             'content': f'write a prompt (only the prompt) for DALL-E according to the following JSON document: {json_doc}; the prompt should be short; prompt: '},
        ]
    )
    image_prompt: str = chat_response['choices'][0]['message']['content']

    image_response = openai.Image.create(
        prompt=image_prompt,
        n=1,
        size="256x256"
    )
    image_url: str = image_response['data'][0]['url']

    # save artwork
    artwork = models.Artwork(data=data, image_url=image_url, image_prompt=image_prompt)
    artwork.save()


@receiver(post_save, sender=models.Artwork)
def send_pushover(sender, instance, created: bool, **kwargs):
    # TODO: implement
    print('send Pushover message')

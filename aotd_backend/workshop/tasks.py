from django.core.files.base import ContentFile

from celery import shared_task
import openai
import json
import base64
from datetime import datetime
import os
import logging
from datetime import datetime, time

from . import models, ai, delivery_services

logger = logging.getLogger(__name__)


def get_last_run(task: str) -> models.CeleryTaskRun | None:
    return models.CeleryTaskRun.objects.filter(task=task).order_by('run_at').last()


@shared_task(bind=True, ignore_result=True)
def check_due_artworks(self):
    logger.info('looking for due artworks')

    # retrieve the last run
    last_run: models.CeleryTaskRun = get_last_run(self.name)

    # create a celery-task-run entry
    current_run = models.CeleryTaskRun(task=self.name)
    current_run.save()

    # retrieve all users that are due for an artwork
    # range_start = last run or start of day
    time_range_start: datetime = last_run.run_at if last_run else datetime.combine(datetime.now(), time.min)
    time_range_end: datetime = current_run.run_at
    users_settings = models.UserSettings.objects.filter(
        issue_time__gt=time_range_start,  # exclusive
        issue_time__lte=time_range_end,  # inclusive
    )

    # trigger artwork generation for those users
    logger.info(f'{users_settings.count()} due artworks found')
    for user_settings in users_settings:
        generate_artwork.delay(user_id=user_settings.user.id)


@shared_task(ignore_result=True)
def generate_artwork(user_id: int):
    # retrieve user
    user = models.CustomUser.objects.get(pk=user_id)
    logger.info(f'generating artwork for {user.username}')

    data: dict[str, any] = {
        'weather': 'sunny',
        'season': 'spring',
        'activity': 'exploring lost place ruin (old castle)',
        'style': 'cinematic shot'
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

from django.core.files.base import ContentFile

from celery import shared_task
import openai
import json
import base64
from datetime import datetime
import os
import logging
import caldav
import icalendar
from datetime import datetime, time

from . import models, delivery_services, data_sources
from .ai import language_ai, image_ai

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

    # get data from sources
    data_source_manager = data_sources.DataSourceManager(user=user)
    data = data_source_manager.retrieve_data(query=datetime.now())

    # generate image prompt
    image_prompt = language_ai.generate_artwork_description(data=data)
    logger.debug(f'image prompt: {image_prompt}')

    # generate artwork title
    title = language_ai.generate_artwork_title(image_prompt)

    # prompt image AI
    base64_image = image_ai.generate(prompt=image_prompt)
    image = base64.b64decode(base64_image)
    timestamp: str = datetime.now().isoformat()
    image_file = ContentFile(content=image, name=f'{timestamp}.png')

    # save artwork
    artwork = models.Artwork(
        user=user,
        data=data,
        image=image_file,
        image_prompt=image_prompt,
        title=title,
    )
    artwork.save()
    logger.info(f'successfully saved artwork')

    # trigger delivery services
    logger.info(f'requesting artwork delivery')
    delivery_services.DeliveryManager.deliver(artwork)

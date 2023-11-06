import json

import requests
import base64
import abc
import os
import logging
from PIL import Image
import io
from . import models


class DeliveryService(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def deliver(artwork: models.Artwork):
        pass


class _Pushover(DeliveryService):
    __LOGGER = logging.getLogger(__name__)

    @staticmethod
    def __get_settings(user: models.CustomUser) -> models.PushoverSettings | None:
        try:
            return models.PushoverSettings.objects.get(pk=user)
        except models.PushoverSettings.DoesNotExist:
            return None

    @staticmethod
    def __prepare_payload(artwork: models.Artwork, settings: models.PushoverSettings):
        with artwork.image.file.open() as image_file:
            original_image = Image.open(image_file)

            # resize image
            resized_image = original_image.resize(
                size=(
                    int(os.getenv("PUSHOVER_IMAGE_WIDTH")),
                    int(os.getenv("PUSHOVER_IMAGE_HEIGHT"))
                )
            )

            # convert Pillow image to jpeg
            buffered_image = io.BytesIO()
            resized_image.save(buffered_image, format="JPEG")

            # Base64 encode image
            base64_image: bytes = base64.b64encode(buffered_image.getvalue())

            pretty_json_data = json.dumps(artwork.data, indent=4)
            text: str = f"""AI Artwork of the Day!\nprompt: {artwork.image_prompt}\ndata: {pretty_json_data}"""

            user_key: str = settings.user_key
            application_api_key: str = os.getenv('PUSHOVER_APPLICATION_API_KEY')

            return {
                'message': text,
                'attachment_base64': base64_image,
                'user': user_key,
                'token': application_api_key
            }

    @staticmethod
    def deliver(artwork: models.Artwork):
        _Pushover.__LOGGER.info('starting delivery process')

        settings = _Pushover.__get_settings(artwork.user)
        if settings:
            _Pushover.__LOGGER.info('configured => continue')

            response = requests.post(
                url='https://api.pushover.net/1/messages.json',
                data=_Pushover.__prepare_payload(artwork, settings),
            )

            _Pushover.__LOGGER.info(
                'successful' if response.status_code == 200
                else f'Pushover request failed: {response.text}'
            )
            print('successful' if response.status_code == 200
                  else f'Pushover request failed: {response.text}')
        else:
            _Pushover.__LOGGER.info('not configured => abort')


class DeliveryManager(DeliveryService):
    DELIVERY_SERVICES: list[DeliveryService] = [
        _Pushover
    ]

    @staticmethod
    def deliver(artwork: models.Artwork):
        for service in DeliveryManager.DELIVERY_SERVICES:
            print(f'deliver using {service}')
            service.deliver(artwork)

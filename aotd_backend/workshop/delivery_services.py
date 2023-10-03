import requests
import base64
import abc
import os

import users.models
from . import models
from users.models import CustomUser


class DeliveryService(abc.ABC):
    @abc.abstractmethod
    def deliver(self, artwork: models.Artwork):
        pass


class DeliveryManager(DeliveryService):
    def deliver(self, artwork: models.Artwork):
        # TODO: determine which delivery services are configured for the user and trigger those that are
        pass


class _Pushover(DeliveryService):
    def deliver(self, artwork: models.Artwork):
        with artwork.image.file.open() as image_file:
            base64_image: bytes = base64.b64encode(image_file.read())

            text: str = f"""AI Artwork of the Day!\nprompt: {artwork.image_prompt}"""

            user_key: str = models.PushoverSettings.objects.get(pk=artwork.user).user_key
            application_api_key: str = os.getenv('PUSHOVER_APPLICATION_API_KEY')

            payload = {
                'message': text,
                'attachment_base64': base64_image,
                'user': user_key,
                'token': application_api_key
            }
            response = requests.post(
                url='https://api.pushover.net/1/messages.json',
                data=payload,
            )
            print(response.content)

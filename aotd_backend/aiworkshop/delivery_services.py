import requests
import base64

from . import models


class Pushover:
    @staticmethod
    def send_artwork(artwork: models.Artwork):
        with artwork.image.file.open() as image_file:
            base64_image: bytes = base64.b64encode(image_file.read())

            text: str = f"""AI Artwork of the Day!\nprompt: {artwork.image_prompt}"""

            user_key: str = models.BasicConfig.objects.get(key='PUSHOVER_USER_KEY').value
            application_api_key: str = models.BasicConfig.objects.get(key='PUSHOVER_APPLICATION_API_KEY').value

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

import openai
import os


class _ImageAi:
    def __init__(self, image_dimensions: tuple[int, int]):
        self.image_width, self.image_height = image_dimensions

    def generate(self, prompt: str) -> str:
        image_response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=f'{self.image_width}x{self.image_height}',
            response_format='b64_json'
        )
        return image_response['data'][0]['b64_json']


image_ai = _ImageAi(
    image_dimensions=(
        int(os.getenv('AOTD_IMAGE_WIDTH')),
        int(os.getenv('AOTD_IMAGE_HEIGHT'))
    ),
)

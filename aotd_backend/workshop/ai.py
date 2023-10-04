import os

import openai
import json


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


class _ChatAi:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt

    def generate(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            n=1,
            max_tokens=100,
            messages=[
                {'role': 'system', 'content': self.system_prompt},
                {'role': 'user',
                 'content': prompt},
            ]
        )
        return response['choices'][0]['message']['content']


image_ai = _ImageAi(
    image_dimensions=(
        int(os.getenv('AOTD_IMAGE_WIDTH')),
        int(os.getenv('AOTD_IMAGE_HEIGHT'))
    ),
)
chat_ai = _ChatAi(
    system_prompt='You are a helpful assistant.',
)

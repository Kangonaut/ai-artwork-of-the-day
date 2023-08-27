import openai
import json


class _ImageAi:
    def __init__(self, size: str):
        self.size = size

    def generate(self, prompt: str) -> str:
        image_response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=self.size,
        )
        return image_response['data'][0]['url']


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
    size="256x256",
)
chat_ai = _ChatAi(
    system_prompt='You are a helpful assistant.',
)

import openai
import json

class _ImageAi:
    pass


class _ChatAi:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt

    def prompt(self, prompt: str) -> str:
        data: dict[str, any] = {
            'weather': 'cloudy with a little sun',
            'temperature': 'hot',
            'scenery': 'mountains',
            'animal': 'elephant',
            'style': 'hyper-realistic'
        }

        json_doc: str = json.dumps(data)

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            n=1,
            max_tokens=100,
            messages=[
                {'role': 'system', 'content': self.system_prompt},
                {'role': 'user',
                 'content': f'write a prompt (only the prompt) for DALL-E according to the following JSON document: {json_doc}; the prompt should be short; prompt: '},
            ]
        )
        return response['choices'][0]['message']['content']


image_ai = _ImageAi()
chat_ai = _ChatAi(
    system_prompt='You are a helpful assistant.'
)

import os
import re
from langchain.chat_models import ChatOpenAI
from langchain.base_language import BaseLanguageModel
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

_ARTWORK_DESCRIPTION_EXAMPLES = [
    {
        "data": {
            "events": [
                "Kickoff Meeting",
                "DE10CBA3",
                "Cycling Tour",
                "Band Practice",
            ],
            "weather": {
                "general": "sunny",
                "is_dew": "False",
                "is_rain": "False",
                "is_snow": "False"
            },
            "daytime": "morning",
            "art_style": "photograph"
        },
        "image_prompt": "A photograph of a person on a bicycle, driving on a road in the woods, on a sunny morning.",
    }
]


class _LanguageAi:
    def __init__(self, language_model: BaseLanguageModel):
        self.__language_model: BaseLanguageModel = language_model

    def generate_artwork_description(self, data: dict[str, any]) -> str:
        example_prompt = ChatPromptTemplate.from_messages([
            ("human", "data: {data}"),
            ("ai", "image prompt: '{image_prompt}'")
        ])

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=_ARTWORK_DESCRIPTION_EXAMPLES,
        )

        final_prompt = ChatPromptTemplate.from_messages([
            ("system", """Please generate a prompt (in quotes) for an image generation AI that visualizes the provided data 
            (in JSON format)."""),
            few_shot_prompt,
            ("human", "data: {data}"),
            ("ai", "image prompt: ")
        ])

        chain = final_prompt | self.__language_model | StrOutputParser()
        response = chain.invoke({"data": data})

        print(f"response: {response}")

        # extract description quotes
        result = re.findall("['\"]([^'\"]+)['\"]", response)[0]

        return result

    def generate_artwork_title(self, artwork_description: str) -> str:
        pass


language_ai = _LanguageAi(
    language_model=ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("OPENAI_CHAT_MODEL_NAME"),
        temperature=os.getenv("OPENAI_CHAT_MODEL_TEMPERATURE"),
        max_tokens=os.getenv("OPENAI_CHAT_MODEL_MAX_TOKENS"),
    )
)

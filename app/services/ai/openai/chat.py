import evars
import openai

from services.ai.base import IChatModel


class OpenAIChatModel(IChatModel):
    def __init__(self) -> None:
        self._api_key = evars.OPENAI_API_KEY
        self._model = evars.AI_EMBEDDING_MODEL_NAME
        openai.api_key = evars.OPENAI_API_KEY

    def submit(self, messages: list[dict]) -> str:
        resp = openai.chat.completions.create(
            model=self._model,
            messages=messages
        )

        return resp.choices[0].message.content

import evars
import openai

from services.ai.base import IChatModel, IChatMessage


class OpenAIChatModel(IChatModel):
    def __init__(self) -> None:
        self._api_key = evars.OPENAI_API_KEY
        self._model = evars.AI_EMBEDDING_MODEL_NAME
        openai.api_key = evars.OPENAI_API_KEY

    def submit(self, messages: list[IChatMessage]) -> str:
        prep_messages = self._parse_messages(messages)

        resp = openai.chat.completions.create(
            model=self._model,
            messages=prep_messages
        )

        return resp.choices[0].message.content

    def _parse_messages(self, messages: list[IChatMessage]) -> list[dict]:
        return [
            {"role": msg.get_role(), "message": msg.get_message()}
            for msg in messages
        ]

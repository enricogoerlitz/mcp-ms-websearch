import openai
import numpy as np
import evars

from services.ai.base import IEmbeddingModel


class OpenAIEmbeddingModel(IEmbeddingModel):
    def __init__(self) -> None:
        self._api_key = evars.OPENAI_API_KEY
        self._model = evars.AI_EMBEDDING_MODEL_NAME
        openai.api_key = evars.OPENAI_API_KEY

    def embed(self, text: str) -> list[float]:
        embedding = self.embed_batch([text])

        return embedding[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        resp = openai.embeddings.create(
            input=texts,
            model=self._model
        )

        embeddings = np.array([record.embedding for record in resp.data], dtype=np.float32)

        return embeddings

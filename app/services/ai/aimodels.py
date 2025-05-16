import evars
import gvars

from services.ai.base import IChatModel, IEmbeddingModel
from services.ai.openai.chat import OpenAIChatModel
from services.ai.openai.embedding import OpenAIEmbeddingModel


class ChatModelFactory:
    @staticmethod
    def create(type: str) -> IChatModel:
        match type:
            case gvars.AI_CHAT_MODEL_PROVIDER_OPENAI:
                return OpenAIChatModel()
            case _:
                raise ValueError(f"Unsupported chat model type: {type}")


class EmbeddingModelFactory:
    @staticmethod
    def create(type: str) -> IChatModel:
        match type:
            case gvars.AI_EMBEDDING_MODEL_PROVIDER_OPENAI:
                return OpenAIEmbeddingModel()
            case _:
                raise ValueError(f"Unsupported chat model type: {type}")


chat_model: IChatModel = ChatModelFactory.create(evars.AI_CHAT_MODEL_PROVIDER)
embedding_model: IEmbeddingModel = EmbeddingModelFactory.create(evars.AI_EMBEDDING_MODEL_PROVIDER)

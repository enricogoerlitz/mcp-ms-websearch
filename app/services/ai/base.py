import numpy as np

from abc import ABC, abstractmethod


class IChatMessage(ABC):
    @abstractmethod
    def get_role(self) -> str: pass

    @abstractmethod
    def get_message(self) -> str: pass


class IChatModel(ABC):
    @abstractmethod
    def submit(self, messages: list[dict]) -> str: pass


class IEmbeddingModel(ABC):
    @abstractmethod
    def embed(self, text: str) -> np.ndarray: pass

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> np.ndarray[np.ndarray]: pass

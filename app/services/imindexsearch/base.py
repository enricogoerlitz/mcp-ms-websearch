import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class IndexDBDocument:
    id: int
    reference: str
    text: str
    embedding: np.ndarray


@dataclass(frozen=True)
class IndexDBDocumentResult(IndexDBDocument):
    distance: float


class IInMemoryIndexDB(ABC):
    @abstractmethod
    def add(self, reference: str, texts: str, embedding: np.ndarray) -> None: pass

    @abstractmethod
    def add_batch(self, reference: str, texts: list[str], embedding: np.ndarray[np.ndarray]) -> None: pass

    @abstractmethod
    def search(self, query: str, k: int = 5) -> list[IndexDBDocumentResult]: pass

from abc import ABC, abstractmethod


class IGoogleSearch(ABC):
    @abstractmethod
    def search(queries: list[str], max_count: int) -> list[str]: pass

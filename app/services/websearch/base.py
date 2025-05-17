from abc import ABC, abstractmethod
from services.websearch.request import WebSearchRequest
from services.websearch.response import WebSearchResponse


class IWebSearch(ABC):
    @abstractmethod
    def execute(self, req: WebSearchRequest) -> WebSearchResponse: pass

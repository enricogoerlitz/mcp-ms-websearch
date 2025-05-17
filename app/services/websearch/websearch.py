from services.websearch.base import IWebSearch
from services.websearch.v1.execute import WebSearchV1


class WebSearchFactory:
    @staticmethod
    def create(version: str) -> IWebSearch:
        match version:
            case "v1":
                return WebSearchV1()
            case _:
                raise ValueError(f"Unsupported websearch version: {version}")

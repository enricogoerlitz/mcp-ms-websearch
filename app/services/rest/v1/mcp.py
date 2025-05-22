from dataclasses import asdict
from logger import logger
from exc import httperrors
from services.websearch.request import WebSearchRequest
from services.websearch.websearch import WebSearchFactory


class WebSearchService:
    def __init__(self):
        self._version = "v1"

    def handle_mcp_invoke(self, req: WebSearchRequest) -> tuple[dict, int]:
        try:
            req.validate()
            websearch = WebSearchFactory.create(self._version)
            response = websearch.execute(req)
            return asdict(response), 200
        except Exception as e:
            logger.error(e, exc_info=True)
            return httperrors.UNEXPECTED_ERROR_RESULT


websearch_service = WebSearchService()

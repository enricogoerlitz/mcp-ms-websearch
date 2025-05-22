import pydantic
from dataclasses import asdict
from logger import logger
from exc import httperrors
from services.websearch.request import WebSearchRequest
from services.websearch.websearch import WebSearchFactory


class WebSearchService:
    def __init__(self):
        self._version = "v1"

    def handle_mcp_invoke(self, data: dict) -> tuple[dict, int]:
        try:
            req = WebSearchRequest(**data)
            req.validate()
            print(req)
            websearch = WebSearchFactory.create(self._version)
            response = websearch.execute(req)
            return asdict(response), 200
        except pydantic.ValidationError as e:
            logger.info(e)
            print("PYDANTIC")
            return httperrors.bad_request_pydantic_validation(e)
        except ValueError as e:
            logger.info(e)
            print("VALUE")
            return httperrors.bad_request(e)
        except Exception as e:
            logger.error(e, exc_info=True)
            return httperrors.UNEXPECTED_ERROR_RESULT


websearch_service = WebSearchService()

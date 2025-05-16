import gvars
import evars

from services.websearch.googlesearch.base import IGoogleSearch
from services.websearch.googlesearch.googlesearchpkg import GoogleSearchPKGImpl


class GoogleSearchFactory:
    @staticmethod
    def create(type: str) -> IGoogleSearch:
        match type:
            case gvars.GOOGLE_SEARCH_PROVIDER_GOOGLESEARCHPKG:
                return GoogleSearchPKGImpl()
            case _:
                raise ValueError(f"Unsupported googlesearch type: {type}")


google: IGoogleSearch = GoogleSearchFactory.create(evars.GOOGLE_SEARCH_PROVIDER)

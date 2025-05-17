import evars
import gvars

from services.webscraper.base import IWebScraper
from services.webscraper.default import DefaultWebScraper


class WebScraperFactory:
    @staticmethod
    def create(type: str) -> IWebScraper:
        match type:
            case gvars.WEBSCRAPER_TYPE_DEFAULT:
                return DefaultWebScraper()
            case _:
                raise ValueError(f"Unsupported googlesearch type: {type}")


webscraper: IWebScraper = WebScraperFactory.create(evars.WEBSCRAPER_TYPE)

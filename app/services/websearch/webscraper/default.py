import requests
import evars

from bs4 import BeautifulSoup
from services.websearch.webscraper.base import IWebScraper, WebPageResult
from services.websearch.webscraper import wsutils
from logger import logger


class DefaultWebScraper(IWebScraper):
    def scrape(self, url: str) -> WebPageResult:
        try:
            resp = requests.get(url, timeout=evars.HTTP_TIMEOUT)
        except Exception as e:
            msg = f"Error by handling url {url}: {str(e)}"
            logger.info(msg)
            return self._empty_result(url)

        if resp.status_code != 200:
            return self._empty_result(url)

        soup = BeautifulSoup(resp.text, features="html.parser")
        result = self._prepare_page_result(url, soup)

        return result

    def _prepare_page_result(self, url: str, soup: BeautifulSoup) -> WebPageResult:
        a_tags = [a_tag for a_tag in soup.find_all("a", href=True)]
        host_url = wsutils.get_host_url(url)
        links, doc_links = self._extract_links(host_url, a_tags)
        text = wsutils.compress_soup_text(soup)

        return WebPageResult(
            url=url,
            content=text,
            links=links,
            document_links=doc_links
        )

    def _extract_links(self, host_url: str, a_tags: list[dict]) -> tuple[list[str], list[str]]:
        doc_links = []
        links = []
        for a in a_tags:
            href: str = a["href"]
            if not href.startswith("http"):
                continue

            if ".pdf" in href:
                doc_links.append(self._prepare_pdf_link(host_url, href))
            else:
                links.append(href)

        return links, doc_links

    def _prepare_pdf_link(self, host_url: str, url: str) -> str:
        if not url.startswith("http"):
            return host_url + url
        return url

    def _empty_result(self, url: str) -> WebPageResult:
        return WebPageResult(
            url=url,
            content=None,
            links=None,
            document_links=None
        )

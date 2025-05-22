import googlesearch

from urllib.parse import urlparse
from services.googlesearch.base import IGoogleSearch


class GoogleSearchPKGImpl(IGoogleSearch):
    def search(self, queries: list[str], n: int) -> list[str]:
        search_links = [
            link for i, query in enumerate(queries)
            for link in self._search(query, n, i)
            if self._filter_condition(link)
        ]

        max_link_count = len(queries) * n
        self._unique_links(search_links, max_link_count)

        return search_links

    def _search(self, query: str, n: int, i: int) -> list[str]:
        return googlesearch.search(
            term=query.strip(),
            num_results=self._n_results(n, i)
        )

    def _unique_links(self, links: list[str], max_link_count: int) -> list[str]:
        seen = set()
        search_links = [
            link
            for link in links
            if not (urlparse(link).path in seen or seen.add(urlparse(link).path))
        ][:max_link_count]

        return search_links

    def _filter_condition(self, link: str) -> bool:
        return (
            link.startswith("http") and
            not link.startswith("https://www.google.com/search?") and
            ".pdf" not in link
        )

    def _n_results(self, n: int, i: int) -> int:
        max_num = int(n * 2)
        num = int(n + (n * i) / 3)
        return num if num < max_num else max_num

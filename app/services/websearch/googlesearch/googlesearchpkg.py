import googlesearch
from services.websearch.googlesearch.base import IGoogleSearch


class GoogleSearchPKGImpl(IGoogleSearch):
    def search(self, queries: list[str], n: int) -> list[str]:
        search_links = [
            link for i, query in enumerate(queries)
            for link in self._search(query, n, i)
            if self._filter_condition(link)
        ]

        max_link_count = len(queries) * n
        seen = set()
        search_links = [
            link
            for link in search_links
            if not (link in seen or seen.add(link))
        ][:max_link_count]

        return search_links

    def _search(self, query: str, n: int, i: int) -> list[str]:
        return googlesearch.search(
            term=query.strip(),
            num_results=self._n_results(n, i)
        )

    def _filter_condition(self, link: str) -> bool:
        return (
            link.startswith("http") and
            not link.startswith("https://www.google.com/search?") and
            ".pdf" not in link
        )

    def _n_results(n: int, i: int) -> int:
        max_num = int(n * 2)
        num = int(n + (n * i) / 3)
        return num if num < max_num else max_num

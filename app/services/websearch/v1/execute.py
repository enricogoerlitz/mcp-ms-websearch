from concurrent.futures import ThreadPoolExecutor
from services.websearch.base import IWebSearch
from services.websearch.request import WebSearchRequest
from services.websearch.response import (
    WebSearchResponse,
    ResponseQuery
)
from services.webscraper.base import WebPageResult
from services.webscraper.scraper import webscraper
from services.googlesearch.google import google
from services.ai.aimodels import embedding_model
from services.ai import aiutils
from services.imindexsearch.indexdb import InMemoryIndexDBFactory


class WebSearchV1(IWebSearch):
    def __init__(self):
        super().__init__()
        self._index = InMemoryIndexDBFactory.new()

    def execute(self, req: WebSearchRequest) -> WebSearchResponse:
        # 1. Generate google queries
        google_queries = self._generate_google_queries(req)

        # 2. Generate Vector queries
        vector_queries_args, vector_queries = self._generate_vector_search_queries(req)

        # 3. Fetch google links
        search_links = google.search(google_queries, req.query.google_search.max_result_count)

        # 4. Execute Thread Pool for Multithreading
        processes = min(8, len(search_links))
        with ThreadPoolExecutor(max_workers=processes) as pool:
            # 4.1 Scrape web pages
            scraped_pages: list[WebPageResult] = list(pool.map(webscraper.scrape, search_links))
            pages_results, pages_text_chunks, err_urls = self._prepare_page_results(scraped_pages)

            # 4.2 Embed web pages texts
            pages_embeddings = list(pool.map(embedding_model.embed_batch, pages_text_chunks))

            # 4.3 Add embeddings to in-memory index db
            for page, chunks, embeddings in zip(pages_results, pages_text_chunks, pages_embeddings):
                self._index.add_batch(reference=page.url, texts=chunks, embeddings=embeddings)

            # 4.4 Execute vector search
            vector_results: list[dict] = list(pool.map(self._vector_search_wrapper, vector_queries_args))

        return WebSearchResponse(
            query=ResponseQuery(
                google_search=google_queries,
                vector_search=vector_queries
            ),
            references=search_links,
            error_references=err_urls,
            results=vector_results
        )

    def _generate_google_queries(self, req: WebSearchRequest) -> list[str]:
        google_queries = [
            "Wann starb Eva Braun?"
        ]

        return google_queries

    def _generate_vector_search_queries(self, req: WebSearchRequest) -> tuple[list[tuple[str, int, bool]], list[str]]:
        vector_queries = [
            "Wann starb Eva Braun"
        ]

        return [
            (query, req.query.vector_search.result_count, True)
            for query in vector_queries
        ]

    def _prepare_page_results(self, page_results: list[WebPageResult]) -> tuple[list[WebPageResult], list[list[str]], list[str]]:
        prep_results = []
        pages_text_chunks = []
        err_urls = []
        for page in page_results:
            if page.content is not None:
                prep_results.append(page)
                page_chunks = aiutils.chunk_text_with_overlap(page.content)
                pages_text_chunks.append(page_chunks)
            else:
                err_urls.append(page.url)

        return prep_results, pages_text_chunks, err_urls

    def _vector_search_wrapper(self, args: tuple[str, int, bool]) -> list[dict]:
        query, k, as_dict = args
        return self._index.search(query, k=k, as_dict=as_dict)

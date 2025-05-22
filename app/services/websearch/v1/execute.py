import multiprocessing
from concurrent.futures import ThreadPoolExecutor

from services.websearch.base import IWebSearch
from services.websearch.request import WebSearchRequest
from services.websearch.response import (
    WebSearchResponse,
    ResponseSearch,
    ResponseReference
)
from services.webscraper.base import WebPageResult
from services.webscraper.scraper import webscraper
from services.googlesearch.google import google
from services.ai.aimodels import embedding_model, chat_model
from services.ai import aiutils
from services.imindexsearch.indexdb import InMemoryIndexDBFactory
from services.websearch.v1.prompts.gglvecsearch import gen_search_queries_messages
from services.websearch.v1.dto import LLMQuestionQueries
from services.websearch.v1.prompts.summarize import gen_web_search_response_summary


class WebSearchV1(IWebSearch):
    def __init__(self):
        super().__init__()
        self._index = InMemoryIndexDBFactory.new()

    def execute(self, req: WebSearchRequest) -> WebSearchResponse | str:
        # 1. Initialize response
        response = WebSearchResponse.empty()

        # 2. Generate search queries
        queries = self._generate_google_and_vector_search_queries(req)
        if queries is None:
            return response

        google_queries, vector_queries_args, vector_queries = queries

        # 3. Perform Google search
        search_links = self._fetch_google_links(google_queries, req)
        response.references = self._create_init_response_references(search_links)

        # 4. Scrape web pages and perform vector search in parallel
        processes = min(multiprocessing.cpu_count(), len(search_links))
        with ThreadPoolExecutor(max_workers=processes) as pool:
            pages_results, pages_text_chunks, err_urls = self._scrape_web_pages(search_links, response, pool)
            self._index_web_pages(pages_results, pages_text_chunks, pool)
            vector_results = self._perform_vector_search(vector_queries_args, pool)

        # 5. Prepare response
        response.results = vector_results
        response.search = ResponseSearch(google=google_queries, vector=vector_queries)
        response.error_references = err_urls

        # 6. Summarize results if enabled
        if req.response.summarization.enabled:
            response.summary = self._summarize_results(req, response)

        return response

    def _generate_google_and_vector_search_queries(
        self, req: WebSearchRequest
    ) -> tuple[list[str], list[tuple[str, int, bool]], list[str]] | None:
        messages = gen_search_queries_messages(
            chat_messages=req.query.messages,
            prompt_context=req.query.search.prompt_context
        )

        queries_raw = chat_model.submit(messages)
        queries = LLMQuestionQueries.from_lmm_response(queries_raw)

        if not queries.has_queries():
            return None

        google_queries = queries.google_search_queries
        vector_queries = queries.vector_search_queries

        vector_queries_args = [
            (query, req.query.search.vector.result_count, True)
            for query in vector_queries
        ]

        return google_queries, vector_queries_args, vector_queries

    def _fetch_google_links(self, queries: list[str], req: WebSearchRequest) -> list[str]:
        return google.search(queries, req.query.search.google.max_result_count)

    def _create_init_response_references(self, links: list[str]) -> dict[str, ResponseReference]:
        return {link: ResponseReference(url=link, document_links=[]) for link in links}

    def _scrape_web_pages(
        self,
        links: list[str],
        response: WebSearchResponse,
        pool: ThreadPoolExecutor
    ) -> tuple[list[WebPageResult], list[list[str]], list[str]]:
        scraped_pages: list[WebPageResult] = list(pool.map(webscraper.scrape, links))
        pages_results, pages_text_chunks, err_urls = self._prepare_page_results(scraped_pages)

        for page_result in pages_results:
            ref = response.references[page_result.url]
            ref.document_links = page_result.document_links

        return pages_results, pages_text_chunks, err_urls

    def _index_web_pages(
        self,
        pages_results: list[WebPageResult],
        pages_text_chunks: list[list[str]],
        pool: ThreadPoolExecutor
    ):
        pages_embeddings = list(pool.map(embedding_model.embed_batch, pages_text_chunks))

        for page, chunks, embeddings in zip(pages_results, pages_text_chunks, pages_embeddings):
            self._index.add_batch(reference=page.url, texts=chunks, embeddings=embeddings)

    def _prepare_page_results(
        self,
        page_results: list[WebPageResult]
    ) -> tuple[list[WebPageResult], list[list[str]], list[str]]:
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

    def _perform_vector_search(
        self,
        vector_queries_args: list[tuple[str, int, bool]],
        pool: ThreadPoolExecutor
    ) -> list[dict]:
        return list(pool.map(self._vector_search_wrapper, vector_queries_args))

    def _vector_search_wrapper(self, args: tuple[str, int, bool]) -> list[dict]:
        query, k, as_dict = args
        return self._index.search(query, k=k, as_dict=as_dict)

    def _summarize_results(self, req: WebSearchRequest, resp: WebSearchResponse) -> str:
        messages = gen_web_search_response_summary(req=req, resp=resp)
        summary = chat_model.submit(messages)
        return summary

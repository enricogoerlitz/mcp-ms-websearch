import multiprocessing

from concurrent.futures import ThreadPoolExecutor
from services.websearch.base import IWebSearch
from services.websearch.request import WebSearchRequest
from services.websearch.response import (
    WebSearchResponse,
    ResponseQuery,
    ResponseReference
)
from services.webscraper.base import WebPageResult
from services.webscraper.scraper import webscraper
from services.googlesearch.google import google
from services.ai.aimodels import embedding_model, chat_model
from services.ai import aiutils
from services.imindexsearch.indexdb import InMemoryIndexDBFactory
from services.websearch.v1.prompts.gglvecsearch import gen_search_queries_messages
from services.websearch.v1.prompts.objects import LLMQuestionQueries
from services.websearch.v1.summarize import gen_web_search_response_summary


class WebSearchV1(IWebSearch):
    def __init__(self):
        super().__init__()
        self._index = InMemoryIndexDBFactory.new()

    def execute(self, req: WebSearchRequest) -> WebSearchResponse | str:
        response = WebSearchResponse.empty()
        # 1. Generate google and vector search queries
        queries = self._generate_google_and_vector_search_queries(req)
        if queries is None:
            return response

        google_queries, vector_queries_args, vector_queries = queries

        # 3. Fetch google links
        search_links = google.search(google_queries, req.query.google_search.max_result_count)

        response.references = {link: ResponseReference(url=link, document_links=[]) for link in search_links}

        # 4. Execute Thread Pool for Multithreading
        processes = min(multiprocessing.cpu_count(), len(search_links))
        with ThreadPoolExecutor(max_workers=processes) as pool:
            # 4.1 Scrape web pages
            scraped_pages: list[WebPageResult] = list(pool.map(webscraper.scrape, search_links))
            pages_results, pages_text_chunks, err_urls = self._prepare_page_results(scraped_pages)

            for page_result in pages_results:
                ref = response.references[page_result.url]
                # ref.sub_links = page_result.links
                ref.document_links = page_result.document_links

            # 4.2 Embed web pages texts
            pages_embeddings = list(pool.map(embedding_model.embed_batch, pages_text_chunks))

            # 4.3 Add embeddings to in-memory index db
            for page, chunks, embeddings in zip(pages_results, pages_text_chunks, pages_embeddings):
                self._index.add_batch(reference=page.url, texts=chunks, embeddings=embeddings)

            # 4.4 Execute vector search
            vector_results: list[dict] = list(pool.map(self._vector_search_wrapper, vector_queries_args))

        response.results = vector_results
        response.query = ResponseQuery(
            google_search=google_queries,
            vector_search=vector_queries
        )
        response.error_references = err_urls

        if req.response.summarization.enabled:
            self._summarize_results(req=req, resp=response)

        return response

    def _generate_google_and_vector_search_queries(
            self,
            req: WebSearchRequest
    ) -> tuple[list[str], list[str], list[tuple[str, int, bool]]] | None:
        # messages = gen_google_and_vector_search_queries_messages(
        #     chat_messages=req.query.messages,
        #     google_prompt_context=req.query.google_search.prompt_context,
        #     vector_prompt_context=req.query.vector_search.prompt_context
        # )
        messages = gen_search_queries_messages(
            chat_messages=req.query.messages,
            prompt_context=req.query.google_search.prompt_context
        )

        queries_raw = chat_model.submit(messages)
        queries = LLMQuestionQueries.from_lmm_response(queries_raw)

        if not queries.has_questions():
            return None

        google_queries, vector_queries = queries.google_search_queries, queries.vector_search_queries

        vector_queries_args = [
            (query, req.query.vector_search.result_count, True)
            for query in vector_queries
        ]

        return google_queries, vector_queries_args, vector_queries

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

    def _summarize_results(self, req: WebSearchRequest, resp: WebSearchResponse) -> None:
        messages = gen_web_search_response_summary(
            req=req,
            resp=resp,
        )

        summary = chat_model.submit(messages)
        resp.summary = summary

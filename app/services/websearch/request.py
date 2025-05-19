from pydantic import BaseModel
from typing import List


class RequestQueryMessage(BaseModel):
    role: str
    content: str


class RequestQueryGoogleSearch(BaseModel):
    prompt_context: str | None
    max_query_count: int
    max_result_count: int


class RequestQueryVectorSearch(BaseModel):
    prompt_context: str | None
    result_count: int


class RequestQuery(BaseModel):
    messages: List[dict]
    google_search: RequestQueryGoogleSearch
    vector_search: RequestQueryVectorSearch


class RequestWebDocumentSearch(BaseModel):
    enabled: bool
    max_documents: int
    max_document_mb_size: int


class RequestDeepWebSearch(BaseModel):
    enabled: bool
    max_depth: int


class WebSearchRequest(BaseModel):
    query: RequestQuery
    web_document_search: RequestWebDocumentSearch
    deep_web_search: RequestDeepWebSearch

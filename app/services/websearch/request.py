from dataclasses import dataclass


@dataclass(frozen=True)
class RequestQueryMessage:
    role: str
    message: str


@dataclass(frozen=True)
class RequestQueryGoogleSearch:
    max_query_count: int
    max_result_count: int


@dataclass(frozen=True)
class RequestQueryVectorSearch:
    result_count: int


@dataclass(frozen=True)
class RequestQuery:
    messages: list[RequestQueryMessage]
    google_search: RequestQueryGoogleSearch
    vector_search: RequestQueryVectorSearch


@dataclass(frozen=True)
class RequestWebDocumentSearch:
    enabled: bool
    max_documents: int
    max_document_mb_size: int


@dataclass(frozen=True)
class RequestDeepWebSearch:
    enabled: bool
    max_depth: int


@dataclass(frozen=True)
class WebSearchRequest:
    query: RequestQuery
    web_document_search: RequestWebDocumentSearch
    deep_web_search: RequestDeepWebSearch

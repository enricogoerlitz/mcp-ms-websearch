from pydantic import BaseModel
from typing import List


class RequestQueryMessage(BaseModel):
    role: str
    content: str


class RequestQueryGoogleSearch(BaseModel):
    max_result_count: int


class RequestQueryVectorSearch(BaseModel):
    result_count: int


class RequestQuerySearch(BaseModel):
    prompt_context: str | None
    google: RequestQueryGoogleSearch
    vector: RequestQueryVectorSearch


class RequestQuery(BaseModel):
    messages: List[dict]
    search: RequestQuerySearch


class RequestWebDocumentSearch(BaseModel):
    enabled: bool
    max_documents: int
    max_document_mb_size: int


class RequestDeepWebSearch(BaseModel):
    enabled: bool
    max_depth: int


class RequestResponseSummarization(BaseModel):
    enabled: bool
    prompt_context: str | None


class RequestResponse(BaseModel):
    summarization: RequestResponseSummarization


class WebSearchRequest(BaseModel):
    query: RequestQuery
    web_document_search: RequestWebDocumentSearch
    deep_web_search: RequestDeepWebSearch
    response: RequestResponse

    def validate(self) -> None:
        if self.query.search.google.max_result_count < 1:
            raise ValueError("Google search result count must be greater than 0.")
        if self.query.search.vector.result_count < 1:
            raise ValueError("Vector search result count must be greater than 0.")
        if self.web_document_search.max_documents < 1:
            raise ValueError("Web document search max documents must be greater than 0.")
        if self.web_document_search.max_document_mb_size < 1:
            raise ValueError("Web document search max document size must be greater than 0.")

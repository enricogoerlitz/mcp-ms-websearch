from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseQueryMessage:
    role: str
    message: str


@dataclass(frozen=True)
class ResponseQuery:
    google_search: list[str]
    vector_search: list[str]


@dataclass(frozen=True)
class ResponseResult:
    query: str
    reference: str
    text: str
    distance: float


@dataclass(frozen=True)
class WebSearchResponse:
    query: ResponseQuery
    references: list[str]
    error_references: list[str]
    results: list[dict]

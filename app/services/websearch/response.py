from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseQueryMessage:
    role: str
    message: str


@dataclass(frozen=True)
class ResponseQuery:
    google_search: list[str]
    vector_search: list[str]


@dataclass(frozen=False)
class ResponseReference:
    url: str
    document_links: list[str]


@dataclass(frozen=True)
class ResponseResult:
    query: str
    reference: str
    text: str
    distance: float


@dataclass(frozen=False)
class WebSearchResponse:
    query: ResponseQuery
    references: dict[str, ResponseReference]
    error_references: list[str]
    results: list[list[dict]]
    summary: str | None = None

    @staticmethod
    def empty() -> "WebSearchResponse":
        return WebSearchResponse(
            query=ResponseQuery(google_search=[], vector_search=[]),
            references={},
            error_references=[],
            results=[],
            summary=None,
        )

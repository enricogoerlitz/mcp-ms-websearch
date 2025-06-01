from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseSearch:
    google: list[str]
    vector: list[str]


@dataclass(frozen=False)
class ResponseReference:
    url: str
    document_links: list[str]


@dataclass(frozen=False)
class WebSearchResponse:
    search: ResponseSearch
    references: dict[str, ResponseReference]
    error_references: list[str]
    results: list[list[dict]]
    summary: str | None = None

    @staticmethod
    def empty() -> "WebSearchResponse":
        return WebSearchResponse(
            search=ResponseSearch(google=[], vector=[]),
            references={},
            error_references=[],
            results=[],
            summary=None,
        )

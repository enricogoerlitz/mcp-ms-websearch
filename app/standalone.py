from services.websearch.websearch import WebSearchFactory
from services.websearch.request import (
    WebSearchRequest,
    RequestQuery,
    RequestQueryGoogleSearch,
    RequestWebDocumentSearch,
    RequestDeepWebSearch,
    RequestQueryMessage,
    RequestQueryVectorSearch
)


if __name__ == "__main__":
    req = WebSearchRequest(
        query=RequestQuery(
            messages=[
                RequestQueryMessage(role="user", message="message")
            ],
            google_search=RequestQueryGoogleSearch(
                max_query_count=5,
                max_result_count=5
            ),
            vector_search=RequestQueryVectorSearch(
                result_count=5
            )
        ),
        web_document_search=RequestWebDocumentSearch(enabled=False, max_documents=5, max_document_mb_size=1024),
        deep_web_search=RequestDeepWebSearch(enabled=False, max_depth=2)
    )

    websearch = WebSearchFactory.create("v1")
    result = websearch.execute(req)

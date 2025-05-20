import json
import time
import evars

from dataclasses import asdict
from services.websearch.websearch import WebSearchFactory
from services.websearch.request import (
    WebSearchRequest,
    RequestQuery,
    RequestQueryGoogleSearch,
    RequestWebDocumentSearch,
    RequestDeepWebSearch,
    RequestQueryVectorSearch,
    RequestResponse,
    RequestResponseSummarization,
)


if __name__ == "__main__":
    print(evars.AI_CHAT_MODEL_PROVIDER)
    req = WebSearchRequest(
        query=RequestQuery(
            messages=[
                {"role": "user", "content": "Wann starb Hitlers sein Frau?"}
                # {"role": "user", "content": "Wann kam Hitler an die Macht und wann starb sein Frau?"}
            ],
            google_search=RequestQueryGoogleSearch(
                prompt_context=None,
                max_result_count=5
            ),
            vector_search=RequestQueryVectorSearch(
                prompt_context=None,
                result_count=5
            )
        ),
        web_document_search=RequestWebDocumentSearch(enabled=False, max_documents=5, max_document_mb_size=1024),
        deep_web_search=RequestDeepWebSearch(enabled=False, max_depth=2),
        response=RequestResponse(
            summarization=RequestResponseSummarization(
                enabled=True,
                prompt_context=None
            )
        )
    )

    websearch = WebSearchFactory.create("v1")

    start = time.time()

    result = websearch.execute(req)

    end = time.time()
    print("\n\n\n", "#" * 30, "\n\n\n")
    print(f"Ausführungsdauer: {end - start:.4f} Sekunden")

    result_dict = asdict(result)
    with open("../dev/result-websearch-2.json", "w", encoding="utf-8") as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=4)

    # with open("../dev/result-websearch-1.json", "w") as f:
    #     f.write(json.dumps(result_dict, indent=4))

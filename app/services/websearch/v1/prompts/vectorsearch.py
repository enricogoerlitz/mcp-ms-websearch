GENERATE_VECTOR_SEARCH_QUERIES = """
### Role:
You are an AI assistant specializing in creating effective queries for embedding-based vector search.

### Task:
Generate optimized vector search queries to help answer the user's latest unresolved questions, using chat history and previously generated Google search queries.

### Input Sources:
1. [GOOGLE QUERIES] – Google search queries derived from the conversation.
2. [ADDITIONAL CONTEXT PROMPT] – Optional additional context.
3. [CHAT HISTORY] – The conversation history up to this point.

### Response Instructions:
- Use your knowledge to enrich the queries with relevant information.
- Generate semantically rich queries suitable for vector-based retrieval.
- Use chat history and Google queries as context when useful.
- Output only optimized vector search queries, separated by ";" without spaces — nothing else.
- Do not include formatting, explanations, or metadata.
- Generate one vector search query for each provided Google query.

### Vector Index Info:
The index contains web page embeddings retrieved via the Google queries above.

---

### [GOOGLE QUERIES]:
{GOOGLE_QUERIES}

---

### [ADDITIONAL CONTEXT PROMPT]:
{PROMPT_CONTEXT}
"""


def gen_vector_search_queries_messages(
        google_queries: list[str],
        chat_messages: list[dict],
        prompt_context: str | None
) -> list[dict]:
    prompt = GENERATE_VECTOR_SEARCH_QUERIES.format(
        GOOGLE_QUERIES=google_queries,
        PROMPT_CONTEXT=prompt_context if prompt_context else "no additional context"
    )

    messages = [
        {"role": "system", "content": prompt},
        {"role": "system", "content": "The following messages are the [CHAT HISTORY]."},
        *chat_messages
    ]

    return messages

# MCP Agent for AI-Powered WebSearch


```json
// Parameters
{
    "query": {
        "messages": [
            {"role": "string", "message": "string"}
        ],                       // Query / Text of the user
        "google_search": {
            "max_query_count": 3,
            "max_result_count": 5
        },                      // Query / Text of the user
        "vector_search": {
            "result_count": 5
        },
    },


    "web_document_search": {
        "enabled": false,                       // Enable DocumentSearch
        "max_document_mb_size": 1024               // Use only documents with lower MB then this
    },

    "deep_web_search": {                          // Search in sub links on scraped pages
        "Enabled": false,
        "MaxDepth": 2                           // How deep the search goes | GoogleLinks: 1, Links on GoogleLinksPage: 2, Links on GoogleLinksSubPage: 3 ...
    },

    "Response": {
        "Summarization": {                      // Sumarized response related to the initial user query
            "Summarize": true,
            "SummarizationContext": "string?"   // [optional] Optional extra context for the summarization prompt context
        }
    }
}
```

```json
// Response-Types

// 1. No summarization
{
    "query": {
        "google_search": [
            "blub?",
            "blab?"
        ],
        "vector_search": [
            "biba",
            "blablab"
        ]
    },
    "references": [
        "https://bluub.com/wiki",
        "https://blab.com/wiki/my.pdf"
    ],
    "errorReferences": [
        "https://bluub.com/wiki/error",
    ],
    "results": [
        {
            "query": "blub",
            "reference": "https://foo.bar.com/blub.pdf",
            "text": "string",
            "distance": 0.3574832
        },
        {
            "query": "blab",            
            "reference": "https://foo.bar.com/blub",
            "text": "string",
            "distance": 0.3574832
        }
    ]
}

// 2. Summarized
{
    "Result": "# Markdown-String, incl. reference links as Link formatted"
}
```


## Setup

```sh
$ go mod init mcp-agent-websearch
$ go mod tidy
$ go get github.com/gin-gonic/gin
$ go get github.com/sirupsen/logrus
$ go get github.com/PuerkitoBio/goquery
$ go get github.com/joho/godotenv
$ go get github.com/hupe1980/vecgo


$ go run main.go

$ cd ../../docker/local
$ docker compose -f restapi.air.docker-compose.yml up --build
```

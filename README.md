# MCP Agent for AI-Powered WebSearch


```json
// Parameters
{
    "Query": {
        "Text": "string",                       // Query / Text of the user
        "MaxSearchResultCount": 5,              // Max count of the search queries which will be generated
        "MaxSearchQueryCount": 5                // Count of maximum used search results
    },

    "Process": {
        "MaxRecursiveCalls": 5 // definition folgt
    },

    "WebDocumentsSearch": {
        "Enabled": false,                       // Enable DocumentSearch
        "MaxDocumentMBSize": 1024               // Use only documents with lower MB then this
    },

    "DeppWebSearch": {                          // Search in sub links on scraped pages
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
        "messages": [
            {"role": "string", "message": "string"}
        ],
        "googlesearch": [
            "blub?",
            "blab?"
        ],
        "vectorsearch": [
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

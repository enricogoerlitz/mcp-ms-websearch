package websearch

type WebSearchResultItem struct {
	Reference     string
	ReferenceType string
	Content       string
}

type WebSearchResult struct {
	Results []WebSearchResultItem
}

type WebSearchResultSummarized struct {
	Result string
}

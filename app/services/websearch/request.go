package websearch

type WebSearchRequest struct {
	Query struct {
		Text                 string `json:"Text"`
		MaxSearchResultCount int    `json:"MaxSearchResultCount"`
		MaxSearchQueryCount  int    `json:"MaxSearchQueryCount"`
	} `json:"Query"`

	WebDocumentsSearch struct {
		Enabled           bool `json:"Enabled"`
		MaxDocumentMBSize int  `json:"MaxDocumentMBSize"`
	} `json:"WebDocumentsSearch"`

	DeppWebSearch struct {
		Enabled  bool `json:"Enabled"`
		MaxDepth int  `json:"MaxDepth"`
	} `json:"DeppWebSearch"`

	Response struct {
		Summarization struct {
			Summarize            bool   `json:"Summarize"`
			SummarizationContext string `json:"SummarizationContext,omitempty"` // Optionales Feld
		} `json:"Summarization"`
	} `json:"Response"`
}

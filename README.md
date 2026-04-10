# Rag Notes Search
more to come (including a better name)


## Backend Endpoints
`/prompt`
* prompts a language model to use RAG to answer a question
* single required query parameter, `q` with the question for the language model
* returns the language model's response after it's done generating
* e.g. `/prompt?q=paranoia`

`/search`
* uses semantic search to return relevant sections of student notes
* single required query parameter, `q` with the search query
* returns JSON; each result dict contains `match_number`, `document_text`, and `source_file` fields
```json
{
    query: str,
    results: list[dict]
}
```
* e.g. `/prompt?q=paranoia`

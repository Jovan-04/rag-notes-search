# Rag Notes Search
A Natural Language Processing class project that takes personal notes, indexes them into a vector database, and uses a local language model to answer questions based on the notes using RAG. 

**Stack**
- Flask and Flask-RESTful
- ChromaDB (for vector database)
- Hugging Face transformers model (We're using `Qwen/Qwen2.5-1.5B-Instruct`)

## Project Structure
- `app.py`: Our flask server which handles routing and API endpoints
- `search.py`: The database manager which scans a `Notes/ ` directory, chunks text, and handles semantic search through Chroma DB. 
- `prompt.py`: This retrieves our chunks and user query then wraps them in a RAG promp and sends them to the local language model.
- `templates/index.html`: Vibecoded frontend with student added json parsing and `marked.js` additions to allow Markdown responses to render properly.

## Setup
This project uses uv for package management, please be sure uv is installed and then close the repo and sync the environment. 
```
# use this command to read our pyproject.toml and install all dependencies
uv sync
```

Create a `.env` file in the root directory and define the path you want the Chroma database to exist.
```
CHROMA_PATH=./chroma_db
```

Create a `Notes/` directory in the root folder. Currently our project only supports `.txt` and `.md` files. Our project supports sub-folders as well.

Once Flask app is started it will detect any modified or new notes and update the vector database before deploying on Port 5050. Note modification will automatically be saved and detected within the `index_tracker.json` file.
*Note: New Macs use Flask's default port of 5000 for AirPlay. To avoid complications we change the port to 5050*

Use the following command to start app
```
uv run app.py
```


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

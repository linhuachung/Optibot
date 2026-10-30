# Harbor support notes

Steps 1–2: scrape a stable corpus of 30 public Help Center articles, upload Markdown through Python to an OpenAI vector store, and query it with Responses/file search.

## Setup and run

Use Python 3.11+ in a virtual environment. Install `python -m pip install -r requirements.txt`, copy `.env.sample` to `.env`, and set `API_KEY` (takes precedence over `OPENAI_API_KEY`). Keep the real key private. `OPENAI_VECTOR_STORE_ID` is optional; the first upload saves a new store ID in `data/ingestion-state.json`. Do not delete that state between runs.

```powershell
python scrape.py
python upload.py --limit 1
python upload.py
python ask.py --retrieve-only --output docs/evidence/youtube-retrieval.json
python ask.py --require-citations --output docs/evidence/youtube-answer.json
python ask.py "How do I create a schedule?" --require-citations
python ask.py "What is tomorrow's weather in Bangkok?"
python -m unittest discover -s tests -v
```

This workspace also has an ignored portable runtime; use `.\.runtime\python\python.exe` in place of `python` here if needed. It is not distributed as application source. `DATA_DIR` defaults to `data`; `OPENAI_MODEL` defaults to `gpt-4.1-mini` for queries. Select an available Responses model with file search if changing it.

## Corpus and indexing

Markdown preserves source URLs, headings, relative links, fenced code and embedded-media links. `data/manifest.json` freezes the selected article IDs; raw selected sources and scrape reports are retained locally for inspection. Rerunning the scraper refreshes that selection. New-article discovery belongs to Step 3.

Uploads reuse committed hashes/remote IDs, await indexing and resume pending attachments. Default managed chunking is documented as 800 tokens with 400 overlap. Exact embedded-chunk totals are not exposed by the inspected API: reports use `null` with an explicit explanation, never a file count disguised as chunks. This assignment requirement remains unresolved.

## Evidence and remaining work

See [verification](docs/verification.md). API answer JSON is separate from the required provider-UI screenshot. Use [system_prompt.txt](system_prompt.txt) verbatim in the current provider UI, configure file search against the saved store, ask the YouTube question and save a correct cited answer as `docs/screenshot-youtube.png`. The retired Assistants workflow cannot be used; confirm replacement UI compatibility with the evaluator if needed.

Daily Docker deployment/logs are Step 3–4 and are not implemented yet. README submission evidence must be completed before submitting both take-home parts.

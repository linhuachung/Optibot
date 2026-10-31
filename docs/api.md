# Local chat API

Backend: `http://127.0.0.1:8000`. The key and vector-store configuration come from the server environment, not request fields. This unauthenticated demo binds to loopback and must not be exposed publicly.

`GET /api/health` reports `status` (`ready` or `setup_required`), `articleCount` `keyConfigured` and `provider`. It makes no provider request and does not validate credit balance.

`POST /api/chat` accepts JSON with `question` (trimmed, 1–2,000 characters) and `mode` (`search` or `answer`, default `search`). Extra fields are rejected. The JSON body is capped at 8 KiB; at most two provider requests execute concurrently. No chat history is persisted and no ingestion endpoints are exposed.

Successful responses contain `mode`, `question`, `answer` (null in search mode), `sources` (title, HTTPS article URL and optional excerpt), and a plain-language `notice`. Search returns actual retrieval excerpts; it does not invent an answer when generation is unavailable. Answer mode uses the exact source prompt and the configured Responses model.

Errors use `{"error":{"code":"...","message":"..."}}`. Invalid input returns 422, unexpected origins 403, unsupported content type 415, oversized input 413, and local capacity exhaustion 429. Missing configuration/corpus, invalid credentials or exhausted quota return 503. Other provider errors return 502. Provider exception bodies, keys, internal paths and stack traces are not returned.

Only `localhost`/`127.0.0.1` origins on ports 5173 and 8000 are allowed. The separately served frontend needs this explicit local CORS allowance. `/` serves the same static frontend when using only the backend; `/openapi.json` contains the schema. Interactive external-CDN API docs are disabled.

Provider selection is explicit via `AI_PROVIDER`. Gemini state uses `gemini-state.json`; source lookup invokes the Gemini model and consumes generation quota even though generated answer text is hidden. Corrupt Gemini citation metadata is rejected before any model call. Gemini connection/timeout errors return sanitized JSON HTTP 502. OpenAI rollback retains its direct-search behavior.

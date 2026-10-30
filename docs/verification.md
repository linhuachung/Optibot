# Steps 1–2 verification

Verified on 2026-10-30. **Step 1 is complete. Step 2 API ingestion and retrieval work; generated-answer/UI evidence and exact embedded-chunk reporting remain incomplete.**

## Implemented

- `scrape.py`: paginated public Zendesk ingestion, stable 30-article manifest, clean UTF-8 Markdown, source URLs and semantic hashes. Script/style/navigation content is removed; headings, relative links, code, images and embedded-media links are preserved.
- `upload.py`: Python API upload into a reused OpenAI vector store, indexing status checks, saved remote IDs, pending-index retry and unchanged-content skipping. This is not yet a deployed daily job.
- `ask.py`: Responses/file-search query using the exact assignment prompt, known-file citation mapping and a retrieval-only mode for independent index verification.
- Exact installed dependencies are pinned in `requirements.txt`. API keys, generated articles, state and the portable runtime are Git-ignored.

## Observed checks

- Scraped five API pages; the live endpoint listed 416 articles at verification time. Selected and wrote **30** files, totaling **96,714 bytes**. A second scrape retained the same selected IDs.
- Compared the YouTube, Linux and Schedules articles with their live pages: all returned HTTP 200 and titles matched. Source URLs are retained. The corpus has five source `<pre>` blocks and five Markdown fence pairs. The schedule article preserves three embedded walkthroughs as links. [Spot checks](evidence/article-spot-checks.json), [corpus metrics](evidence/corpus-metrics.json).
- One-file API smoke test completed, followed by 29 additional files in the same store. The full second run reported **uploaded=0, skipped=30**. An independent remote listing confirmed **30 completed files, zero pending operations** and no duplicate attachments. [Initial full upload](evidence/initial-upload.json), [rerun](evidence/upload-rerun.json), [remote status](evidence/index-status.json).
- Live vector search for “How do I add a YouTube video?” returned the intended guide first, with the original article URL and setup instructions. This demonstrates retrieval, not a generated assistant answer. [Retrieval evidence](evidence/youtube-retrieval.json).
- **12 tests passed** with `python -m unittest discover -s tests -v`. Coverage includes formatting, stable pagination/selection, cross-origin rejection, semantic hashing, embedded-media preservation, unchanged uploads, failed-index retry, in-progress indexing, manifest/file mismatch, exact prompt/store configuration, known citations and retrieval-only behavior.
- Python compilation and `pip check` passed. Verified the prompt matches the plan verbatim and the real `.env` is ignored; no project key was present in staged source.

## Remaining blockers

1. **Generation credits:** a valid Responses request returned HTTP 429, `credit_balance_exhausted`, `insufficient_quota`. Authentication, file indexing and vector retrieval succeeded, but a cited generated YouTube answer, a second supported answer and unsupported-question refusal have not been verified live. [Sanitized failure](evidence/generation-blocker.json).
2. **Provider UI screenshot:** browser-control initialization failed twice with a runtime/sandbox startup error. No provider UI session was inspected or configured and no screenshot is claimed. The retired Assistants UI/API path must be replaced by a compatible current provider workflow, with evaluator clarification if necessary.
3. **Chunk total:** inspected vector-store file metadata includes status, attributes, usage bytes and chunking strategy, but no exact embedded-chunk count. Reports deliberately use `embedded_chunks: null`. File counts and retrieved snippets do not establish that total. Resolve the assignment's telemetry expectation with the evaluator before calling Step 2 fully complete. Default managed chunking remains selected. [Official retrieval documentation](https://developers.openai.com/api/docs/guides/retrieval).
4. **Git commits:** this workspace was initialized as a local repository, but commit creation stopped because Git has no author name/email configured. Changes remain local and can be committed once that identity is supplied. No remote repository was created or pushed.

## Finish the live answer checks

After funding the API project or configuring a funded key in the ignored `.env`:

```powershell
python ask.py --require-citations --output docs/evidence/youtube-answer.json
python ask.py "How do I create a schedule?" --require-citations --output docs/evidence/schedule-answer.json
python ask.py "What is tomorrow's weather in Bangkok?" --output docs/evidence/unsupported-answer.json
```

Check factual correctness, at most five bullets, at most three article URLs and refusal when the corpus cannot answer. In the current provider UI, apply `system_prompt.txt`, configure file search for the store ID in `data/ingestion-state.json`, ask the YouTube question and capture the correct cited answer at `docs/screenshot-youtube.png`. API JSON does not replace that screenshot. Never paste the API key into the UI's prompt.

Use only one uploader at a time and retain `data/ingestion-state.json`. Step 3 still owns daily discovery, complete crash/ambiguous-upload reconciliation and job serialization; Steps 3–4 own the one-shot Docker job, durable hosting and daily log evidence. Product trial research and Part 2 are unchanged.

# Gemini migration

Native Gemini integration is implemented and QA reviewed. The user explicitly authorized use of the supplied trial key; it is stored only in the ignored `.env` and never printed or put in frontend code. No billing settings were changed. Successful API calls do not establish unlimited-free availability or guarantee future quota.

## Observed local acceptance

- [x] Authenticate, access File Search and find a working model: `gemini-3.5-flash-lite`.
- [x] Upload 31 Markdown articles via the official Python SDK, poll indexing and retain active document identifiers.
- [x] Keep Gemini state separate (`gemini-state.json`) from OpenAI rollback state (`ingestion-state.json`).
- [x] Rerun the full scraper/uploader: added=0, updated=0, skipped=31, failed=0.
- [x] Verify grounded YouTube and schedule answers: five bullets and one correct support URL each. Unsupported weather question is refused.
- [x] Integrate provider selection into daily job, upload/answer CLIs and local API, with provider-aware source-lookup wording. Gemini lookup invokes a model and consumes its quota even when generated text is hidden.
- [x] Test failure/index/replacement/orphan recovery, invalid limits, transport errors, corrupt metadata and safe citation mapping. QA independently approves implementation scope.
- [x] Verify two real Gemini cloud containers with encrypted credentials, restored provider state and retained migration marker: runs 41213308045 and 41213474374 both pass with 31 skips, zero uploads/failures and identical state digests.
- [ ] Capture actual Google AI Studio setup/YouTube answer screenshot using the API-indexed corpus. Native browser automation initialization failed; no provider screenshot is claimed.
- [ ] Resolve exact embedded-chunk telemetry. Config is 400 tokens/80 overlap; counts remain null rather than inferred from file totals.

## Running and rollback

Set `AI_PROVIDER=gemini`, `GEMINI_API_KEY` and `GEMINI_MODEL=gemini-3.5-flash-lite` in `.env`. `main.py`, `upload.py` and `ask.py` also accept `--provider gemini`. Optional `GEMINI_FILE_SEARCH_STORE` must match saved state. Preserve manifest and both provider states. Switch to `AI_PROVIDER=openai` only with restored matching OpenAI state/configuration and funded credentials. Never mix provider identifiers or run competing writers.

The cloud migration keeps prior trusted artifacts and imports verified Gemini bootstrap only once. A persisted `gemini-migration.json` marker prevents missing migrated state from silently resetting to old bootstrap. Ambiguous uploads and failed operations stop with retained journal for manual reconciliation; no blind retries are claimed. Keep an offline backup before repairs.

Changing provider does not complete the live SCIO study, candidate review or exact chunk requirement. Official references: [File Search](https://ai.google.dev/gemini-api/docs/file-search), [API keys](https://ai.google.dev/gemini-api/docs/api-key), [pricing](https://ai.google.dev/gemini-api/docs/pricing).

[First Gemini cloud evidence](evidence/cloud-run-41213308045.json), [restored second container](evidence/cloud-run-41213474374.json), [CI](evidence/gemini-ci.json), [raw store metadata](evidence/gemini-store-metadata.json). The existing scheduled workflow now selects Gemini; a Gemini-specific automatic cron event remains to be observed at its next interval.

Gemini accepts `GEMINI_API_KEY` with `API_KEY` as a fallback alias; an explicit Gemini key wins over a legacy OpenAI alias. The Docker image defaults to `AI_PROVIDER=gemini`; set `AI_PROVIDER=openai` explicitly for rollback.

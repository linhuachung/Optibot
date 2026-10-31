# Daily GitHub Actions job

GitHub Actions replaces Railway at the user's request. It runs Docker on an Ubuntu runner at `17 2 * * *` UTC (09:17 Bangkok) and supports manual runs. No additional hosting account is needed. The workflow is `.github/workflows/daily.yml`.

## One-time configuration

In the repository's Settings ? Secrets and variables ? Actions, configure:

- Secret `OPENAI_API_KEY`: the API key from the ignored local `.env`.
- Secret `OPTIBOT_BOOTSTRAP_MANIFEST`: complete contents of `data/manifest.json`.
- Secret `OPTIBOT_BOOTSTRAP_STATE`: complete contents of `data/ingestion-state.json`.
- Variable `OPENAI_VECTOR_STORE_ID`: the store ID in that state file.

The two bootstrap JSON payloads contain public source metadata, hashes and remote IDs, not the API key. They preserve the already indexed corpus for the first cloud run. Secrets are encrypted by GitHub and must never be committed to the repository or pasted into workflow YAML. After explicit user authorization, these encrypted secrets and the store variable were configured. Future key rotation can be performed directly in GitHub secret settings without changing source code.

## Verify deployment

1. In Actions, select **Daily scraper** and **Run workflow** on `main`.
2. Check the Docker step exits 0 and reports `added=0 updated=0 skipped=30 failed=0` for unchanged sources.
3. Confirm the run uploaded its `optibot-state-<run-id>-<attempt>` artifact.
4. Trigger a second run. It must download the prior run's state artifact and skip unchanged articles in a new container. Preserve the real run links and a redacted `last-run.json` as cloud evidence.
5. Verify an actual `schedule`-triggered run after the next daily interval; a manual run does not prove cron fired. Update `tasks/todo.md` only for checks actually observed.

## Persistence and limitations

Only `manifest.json`, `ingestion-state.json` and `last-run.json` are archived. Keys and `.env` are excluded. The workflow serializes daily executions and saves state after failed container steps when restored state is available. Restore accepts artifacts only from this repository's trusted daily workflow on `main`, triggered manually or by schedule. It excludes pull-request artifacts. Missing/expired state after previous daily runs stops the workflow rather than silently recreating the corpus.

Artifacts have 90-day requested retention, subject to repository limits. Keep an offline state backup. GitHub schedules are best effort and can be delayed or dropped during load; public-repository schedules may be disabled after 60 days without repository activity. Avoid claiming continuous production scheduling guarantees. A hard runner termination before artifact upload can lose its newest local journal; the uploader now also searches the exact store/article/hash filename even if the newest journal is lost. It reuses a unique orphan and stops on duplicates; inspect ambiguous cases before manual repair.

## Local Docker verification

Use the build/run commands in README, retain the same `data` bind mount for repeated containers, and never put a key in build arguments. Docker builds passed CI, and two full authenticated cloud containers completed successfully. The second restored the first run's state and performed zero uploads. [First run](https://github.com/linhuachung/Optibot/actions/runs/41067930209), [second run](https://github.com/linhuachung/Optibot/actions/runs/41068135936). A real scheduled OpenAI event passed on 2026-10-31: [run 41184533900](https://github.com/linhuachung/Optibot/actions/runs/41184533900), with added=1, updated=2, skipped=28, failed=0.

## Recovery and rollback

Use one writer per vector store, including local scripts and cloud jobs. The OS lock protects one state directory and workflow concurrency protects this scheduled workflow; neither is a distributed lease across unrelated machines/state directories. Use a separate test store or avoid local uploads while the cloud job is running. Read-only queries do not mutate ingestion state.

The job takes an OS-backed lock for its state directory, recovers pending versions before re-scraping, and writes hashes only after indexing and old-version retirement succeed. Retries keep the pending remote ID and complete cleanup without a new upload.

If a file-upload response is lost, its intent contains an exact store-specific filename. A retry searches provider file metadata for that name. Exactly one match is reused. With zero or multiple matches, the job stops rather than creating another potentially duplicate file. Inspect that intent and the provider Files list; only clear the intent after confirming no upload exists, or set its `file_id` to the verified matching file. Do not clear committed article state or delete the vector store as a recovery shortcut.

Failed runs exit nonzero and save a sanitized error class/status, counts, timestamps and duration. `failed` counts the failed operation; unattempted articles are not counted as skipped. Counts include successfully recovered versions. Snapshot the persistent state before a deployment or manual repair; rollback app code without discarding its volume. Source deletion/unpublishing currently fails visibly if it affects the selected corpus; automatic index deletion is out of scope.

Reference: [Docker build practices](https://docs.docker.com/build/building/best-practices/).


References: [GitHub schedules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), [workflow artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data).

## Gemini migration configuration

After verified local indexing, configure encrypted `GEMINI_API_KEY` and `GEMINI_BOOTSTRAP_STATE` (complete `data/gemini-state.json`, with no pending work). Set repository variables `AI_PROVIDER=gemini`, `GEMINI_MODEL=gemini-3.5-flash-lite` and `GEMINI_FILE_SEARCH_STORE` to the saved Gemini store. Keep existing OpenAI secrets/state as rollback material; never put either key into YAML or frontend code.

The same trusted artifact now retains `manifest.json`, both provider states, `gemini-migration.json` and `last-run.json`. On first Gemini execution the verified Gemini bootstrap is added to the restored artifact. Later runs must restore it; a migration marker plus missing Gemini state fails visibly rather than silently importing stale bootstrap. The one-shot Docker job selects provider from `AI_PROVIDER`. Verify two actual Gemini runs independently of historical OpenAI evidence.

Gemini pending journals retain operation names, deterministic article/hash display names and committed hashes. On a lost upload response, only a unique matching document is reused; absent/duplicate matches stop for manual reconciliation. Never clear pending/committed state blindly. Successful replacement indexing and retirement precede committing the new hash. No claim is made that Gemini supports OpenAI's direct vector-search endpoint; source lookup uses model quota.

Gemini cloud acceptance passed on 2026-10-31 in runs [41213308045](https://github.com/linhuachung/Optibot/actions/runs/41213308045) and [41213474374](https://github.com/linhuachung/Optibot/actions/runs/41213474374). Both skipped all 31 with zero failures; the second retained the identical provider-state digest and migration marker after restoration. Secrets/provider variables were configured only after the user explicitly approved this Gemini transfer. No key values were printed or committed.

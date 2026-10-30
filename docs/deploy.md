# Daily GitHub Actions job

GitHub Actions replaces Railway at the user's request. It runs Docker on an Ubuntu runner at `17 2 * * *` UTC (09:17 Bangkok) and supports manual runs. No additional hosting account is needed. The workflow is `.github/workflows/daily.yml`.

## One-time configuration

In the repository's Settings ? Secrets and variables ? Actions, configure:

- Secret `OPENAI_API_KEY`: the API key from the ignored local `.env`.
- Secret `OPTIBOT_BOOTSTRAP_MANIFEST`: complete contents of `data/manifest.json`.
- Secret `OPTIBOT_BOOTSTRAP_STATE`: complete contents of `data/ingestion-state.json`.
- Variable `OPENAI_VECTOR_STORE_ID`: the store ID in that state file.

The two bootstrap JSON payloads contain public source metadata, hashes and remote IDs, not the API key. They preserve the already indexed corpus for the first cloud run. Secrets are encrypted by GitHub and must never be committed to the repository or pasted into workflow YAML. Automated transfer is currently awaiting explicit authorization; automatic approval review rejected the initial attempt. You may instead enter the values directly through GitHub's secret settings.

## Verify deployment

1. In Actions, select **Daily scraper** and **Run workflow** on `main`.
2. Check the Docker step exits 0 and reports `added=0 updated=0 skipped=30 failed=0` for unchanged sources.
3. Confirm the run uploaded its `optibot-state-<run-id>-<attempt>` artifact.
4. Trigger a second run. It must download the prior run's state artifact and skip unchanged articles in a new container. Preserve the real run links and a redacted `last-run.json` as cloud evidence.
5. Verify an actual `schedule`-triggered run after the next daily interval; a manual run does not prove cron fired. Update `tasks/todo.md` only for checks actually observed.

## Persistence and limitations

Only `manifest.json`, `ingestion-state.json` and `last-run.json` are archived. Keys and `.env` are excluded. The workflow serializes daily executions and saves state after failed container steps when restored state is available. Restore accepts artifacts only from this repository's trusted daily workflow on `main`, triggered manually or by schedule. It excludes pull-request artifacts. Missing/expired state after previous daily runs stops the workflow rather than silently recreating the corpus.

Artifacts have 90-day requested retention, subject to repository limits. Keep an offline state backup. GitHub schedules are best effort and can be delayed or dropped during load; public-repository schedules may be disabled after 60 days without repository activity. Avoid claiming continuous production scheduling guarantees. A hard runner termination before artifact upload can lose its newest local journal; provider metadata and store-specific filenames assist reconciliation, but inspect pending operations before retrying ambiguous failures.

## Local Docker verification

Use the build/run commands in README, retain the same `data` bind mount for repeated containers, and never put a key in build arguments. The Docker image build and entry-point smoke check passed GitHub CI; full authenticated container runs are still pending until the daily workflow is configured.

## Recovery and rollback

The job takes an OS-backed lock for its state directory, recovers pending versions before re-scraping, and writes hashes only after indexing and old-version retirement succeed. Retries keep the pending remote ID and complete cleanup without a new upload.

If a file-upload response is lost, its intent contains an exact store-specific filename. A retry searches provider file metadata for that name. Exactly one match is reused. With zero or multiple matches, the job stops rather than creating another potentially duplicate file. Inspect that intent and the provider Files list; only clear the intent after confirming no upload exists, or set its `file_id` to the verified matching file. Do not clear committed article state or delete the vector store as a recovery shortcut.

Failed runs exit nonzero and save a sanitized error class/status, counts, timestamps and duration. `failed` counts the failed operation; unattempted articles are not counted as skipped. Counts include successfully recovered versions. Snapshot the persistent state before a deployment or manual repair; rollback app code without discarding its volume. Source deletion/unpublishing currently fails visibly if it affects the selected corpus; automatic index deletion is out of scope.

References: [Railway config fields](https://docs.railway.com/config-as-code/reference), [cron execution](https://docs.railway.com/cron-jobs), [persistent volumes](https://docs.railway.com/volumes), [Docker build practices](https://docs.docker.com/build/building/best-practices/).


References: [GitHub schedules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), [workflow artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data).

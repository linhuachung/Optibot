# Daily Railway job

The repository contains `Dockerfile` and `railway.json`; deployment is not yet verified. Docker and Railway CLI/authentication were unavailable in the working shell. Use the existing Railway project rather than creating a second project.

## Local Docker verification

```powershell
docker build -t harbor-ledger .
docker run --rm --env-file .env --mount "type=bind,source=$((Get-Location).Path)/data,target=/data" harbor-ledger
docker run --rm --env-file .env --mount "type=bind,source=$((Get-Location).Path)/data,target=/data" harbor-ledger
```

Both runs should exit 0. For unchanged sources, the second run must show `added=0 updated=0 skipped=30 failed=0` (or the current corpus size). Retain the same mounted directory between containers. Never place a key in the Dockerfile or build arguments. `API_KEY` takes precedence over `OPENAI_API_KEY`; `STATE_DIR` takes precedence over `DATA_DIR`.

## Configure the existing Railway project

1. Connect a new cron service in the existing project to `linhuachung/Optibot`, branch `main`. Keep unrelated existing services unchanged. Railway builds the checked-in Dockerfile.
2. Attach a persistent volume to **that service** at `/data`. The mount and credentials are Railway settings; the JSON config does not create them. Set `STATE_DIR=/data` and the API key as a service secret. No web port/domain is needed.
3. To reuse the already indexed store, securely copy the local `manifest.json` and `ingestion-state.json` into the volume before the first run, and set `OPENAI_VECTOR_STORE_ID` to the matching saved ID. The job reconstructs article files during scraping. If pending operations exist, copy the associated source/state files too, or finish recovery locally first. Verify the copied JSON before enabling cron. Do not commit runtime state or keys to GitHub.
4. The config runs `python main.py` at `0 2 * * *` **UTC**, approximately 09:00 Bangkok daily, with no automatic restart. Run it manually once, then again in a separate container execution. Verify successful termination, unchanged-source skipping and state persistence. Confirm the first actual scheduled run later; a manual trigger alone does not prove the schedule executed.
5. Inspect service logs and `/data/last-run.json`. Export a redacted, real cloud last-run artifact to `docs/evidence/cloud-last-run.json`, or provide a log link the reviewer can access. Do not relabel the existing local artifact as cloud evidence. Update README and `tasks/todo.md` only after those checks pass.

If starting with a completely empty volume, leave the store ID unset so one store is created and saved. If pointing an empty state directory at an existing store, the uploader reconciles attached files by article/hash attributes before uploading. Retaining both state files is the preferred path because it also preserves corpus selection and discovery history.

## Recovery and rollback

The job takes an OS-backed lock for its state directory, recovers pending versions before re-scraping, and writes hashes only after indexing and old-version retirement succeed. Retries keep the pending remote ID and complete cleanup without a new upload.

If a file-upload response is lost, its intent contains an exact store-specific filename. A retry searches provider file metadata for that name. Exactly one match is reused. With zero or multiple matches, the job stops rather than creating another potentially duplicate file. Inspect that intent and the provider Files list; only clear the intent after confirming no upload exists, or set its `file_id` to the verified matching file. Do not clear committed article state or delete the vector store as a recovery shortcut.

Failed runs exit nonzero and save a sanitized error class/status, counts, timestamps and duration. `failed` counts the failed operation; unattempted articles are not counted as skipped. Counts include successfully recovered versions. Snapshot the persistent state before a deployment or manual repair; rollback app code without discarding its volume. Source deletion/unpublishing currently fails visibly if it affects the selected corpus; automatic index deletion is out of scope.

References: [Railway config fields](https://docs.railway.com/config-as-code/reference), [cron execution](https://docs.railway.com/cron-jobs), [persistent volumes](https://docs.railway.com/volumes), [Docker build practices](https://docs.docker.com/build/building/best-practices/).

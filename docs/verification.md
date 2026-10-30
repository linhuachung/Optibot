# Implementation verification

Verified on 2026-10-30. **Steps 1, 3 and 5 pass local checks. Step 2 API ingestion/retrieval work; generated-answer/UI evidence and exact chunk reporting remain incomplete. Docker build, two authenticated GitHub Actions containers and cross-run state restoration passed. The first automatic cron trigger remains unobserved.**

## Implemented

- `scrape.py`: paginated public Zendesk ingestion, stable 30-article manifest, clean UTF-8 Markdown, source URLs and semantic hashes. Script/style/navigation content is removed; headings, relative links, code, images and embedded-media links are preserved.
- `upload.py`: Python API upload into a reused OpenAI vector store, indexing status checks, saved remote IDs, pending-index retry and unchanged-content skipping. `main.py` now runs this pipeline as a deployed GitHub Actions job.
- `ask.py`: Responses/file-search query using the exact assignment prompt, known-file citation mapping and a retrieval-only mode for independent index verification.
- Exact installed dependencies are pinned in `requirements.txt`. API keys, generated articles, state and the portable runtime are Git-ignored.

## Observed checks

- Scraped five API pages; the live endpoint listed 416 articles at verification time. Selected and wrote **30** files, totaling **96,714 bytes**. A second scrape retained the same selected IDs.
- Compared the YouTube, Linux and Schedules articles with their live pages: all returned HTTP 200 and titles matched. Source URLs are retained. The corpus has five source `<pre>` blocks and five Markdown fence pairs. The schedule article preserves three embedded walkthroughs as links. [Spot checks](evidence/article-spot-checks.json), [corpus metrics](evidence/corpus-metrics.json).
- One-file API smoke test completed, followed by 29 additional files in the same store. The full second run reported **uploaded=0, skipped=30**. An independent remote listing confirmed **30 completed files, zero pending operations** and no duplicate attachments. [Initial full upload](evidence/initial-upload.json), [rerun](evidence/upload-rerun.json), [remote status](evidence/index-status.json).
- Live vector search for “How do I add a YouTube video?” returned the intended guide first, with the original article URL and setup instructions. This demonstrates retrieval, not a generated assistant answer. [Retrieval evidence](evidence/youtube-retrieval.json).
- **29 tests passed** with `python -m unittest discover -s tests -v`. Coverage includes formatting, stable selection, daily discovery, failed-pagination bookkeeping, cross-origin rejection, semantic hashing, media preservation, unchanged uploads, failed-index retry, source changes during pending work, old-version cleanup, ambiguous upload reconciliation, locking, CLI exit/failure artifacts, exact prompt/store configuration, known citations, retrieval-only behavior, trusted workflow-state selection and bootstrap safety.
- Python compilation and `pip check` passed. Verified the prompt matches the plan verbatim and the real `.env` is ignored; no project key was present in staged source.
- Two real `main.py` processes completed separately against the live source and existing store, each with **added=0 updated=0 skipped=30 failed=0** and exit 0. These demonstrate local persistent state, not cloud containers. [First local daily run](evidence/local-daily-run.json), [separate process rerun](evidence/local-daily-rerun.json).
- Railway was explicitly replaced by GitHub Actions. The pinned dependency audit found no known vulnerabilities. [Audit report](evidence/dependency-audit.json).

## Remaining blockers

1. **Generation credits:** a valid Responses request returned HTTP 429, `credit_balance_exhausted`, `insufficient_quota`. Authentication, file indexing and vector retrieval succeeded, but a cited generated YouTube answer, a second supported answer and unsupported-question refusal have not been verified live. [Sanitized failure](evidence/generation-blocker.json).
2. **Provider UI screenshot:** browser-control initialization failed twice with a runtime/sandbox startup error. No provider UI session was inspected or configured and no screenshot is claimed. The retired Assistants UI/API path must be replaced by a compatible current provider workflow, with evaluator clarification if necessary.
3. **Chunk total:** inspected vector-store file metadata includes status, attributes, usage bytes and chunking strategy, but no exact embedded-chunk count. Reports deliberately use `embedded_chunks: null`. File counts and retrieved snippets do not establish that total. Resolve the assignment's telemetry expectation with the evaluator before calling Step 2 fully complete. Default managed chunking remains selected. [Official retrieval documentation](https://developers.openai.com/api/docs/guides/retrieval).
4. **Automatic schedule observation:** the daily workflow is deployed with encrypted secrets after explicit user authorization. Two manually triggered containers succeeded; the second restored the first run's state artifact. Actual automatic cron execution is still unobserved. Next configured interval is 09:17 Bangkok on 2026-10-31, subject to GitHub scheduling delays.

## Source control and automated checks

The source is connected to [linhuachung/Optibot](https://github.com/linhuachung/Optibot); the verified ingestion baseline was committed and pushed. Repository-local commit identity uses the verified GitHub profile and its noreply address. GitHub Actions is configured for Windows/Linux tests, dependencies, compilation and a Linux Docker build/entry-point smoke check. [Run 41067614734](https://github.com/linhuachung/Optibot/actions/runs/41067614734) passed all 27 tests on Windows/Linux and its Docker build. No keys or generated state are committed.

## Finish the live answer checks

After funding the API project or configuring a funded key in the ignored `.env`:

```powershell
python ask.py --require-citations --output docs/evidence/youtube-answer.json
python ask.py "How do I create a schedule?" --require-citations --output docs/evidence/schedule-answer.json
python ask.py "What is tomorrow's weather in Bangkok?" --output docs/evidence/unsupported-answer.json
```

Check factual correctness, at most five bullets, at most three article URLs and refusal when the corpus cannot answer. In the current provider UI, apply `system_prompt.txt`, configure file search for the store ID in `data/ingestion-state.json`, ask the YouTube question and capture the correct cited answer at `docs/screenshot-youtube.png`. API JSON does not replace that screenshot. Never paste the API key into the UI's prompt.

All mutating commands use an OS-backed state-directory lock. Retain `manifest.json` and `ingestion-state.json`. Daily discovery, pending recovery and serialization are implemented. An upload intent with no unique filename match stops for manual reconciliation rather than blindly duplicating files; see [recovery instructions](deploy.md). Source deletion/unpublishing is not automatically propagated. A proposed Brief A plan is now drafted; product-trial research and candidate validation remain incomplete.

## Cloud persistence evidence

[First cloud run](https://github.com/linhuachung/Optibot/actions/runs/41067930209) and [second cloud run](https://github.com/linhuachung/Optibot/actions/runs/41068135936) both completed successfully with `added=0 updated=0 skipped=30 failed=0`. The second skipped bootstrap and successfully restored the prior artifact. Both artifacts contain 30 committed articles, zero pending operations and identical state SHA-256 digests. [First artifact summary](evidence/cloud-run-41067930209.json), [second artifact summary](evidence/cloud-run-41068135936.json). No API key is present in the archived state or evidence.

## Part 2 draft checks

`scio-slice-plan.md` starts with Brief A, covers all four selected domains, defines team/platform/depth assumptions and contains ordered delivery milestones, rationale, acceptance criteria, failure behavior and risks. Estimate arithmetic was checked: 48 baseline engineering-days + 12 contingency = 60; two engineers at 80% planned capacity provide eight days/week, giving 7.5 weeks rounded to an eight-week delivery window. This is a proposal, not a measured estimate or approved deadline. No live trial observations are claimed.

## Step 12 requirement review

The current Google Doc was retrieved through its text-export endpoint on 2026-10-30 after connector/browser fetch failures. All five system-prompt lines match the current source exactly. [Requirement comparison](requirements-review.md) and [interview preparation](interview-prep.md) distinguish implemented behavior, proposed business policies and missing evidence. The review reproduced and fixed a lost-journal orphan upload that could otherwise create a duplicate File. The updated local suite has 29 passing tests, including orphan reuse and duplicate-name rejection; compilation and dependency consistency checks pass. The fixed code passed Windows/Linux CI and Docker build in run 41072188291. Cloud run 41072188793 restored the same state and completed with 30 skips, zero uploads and no pending operations. See `evidence/review-ci-checks.json` and `evidence/cloud-run-41072188793.json`.

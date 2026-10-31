# Implementation verification

Current update 2026-10-31: **53 Python/nine browser tests pass; Gemini indexes 31 articles and real generated/refusal checks plus local unchanged rerun pass. Windows/Linux/browser/Docker CI passed run41213125085. Required Google AI Studio screenshot, exact chunks and candidate/product gates remain open.** See the current Gemini section below. Earlier dated sections retain historical OpenAI evidence; exhausted-credit and pending-OpenAI-cron statements are superseded by the October31 verification.


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

## Requested local backend/frontend verification

The local FastAPI API and static frontend are implemented. All **38 Python tests** pass, including nine API cases; **six Playwright browser tests** pass, including keyboard use, XSS-safe source display, generation-error fallback without fabricated answers, duplicate-send protection and setup/network failures. Automated axe WCAG 2/2.1 A/AA checks report zero violations at 320 and 1440 pixels; responsive checks also cover 768 and 1024 pixels. This is automated coverage, not a claim of complete accessibility certification.

An actual browser search against the existing remote index returned three sources with the YouTube guide first, no page JavaScript errors and no mobile horizontal overflow. A real generation attempt still returned the exhausted-credit error. [Live local UI evidence](evidence/local-web-check.json), [desktop screenshot](evidence/local-chat-search.png), [mobile screenshot](evidence/local-chat-mobile.png). These are custom UI retrieval screenshots, not the required provider-UI answer screenshot. Keys and internal provider IDs are excluded from public API results. The app is bound to loopback and is not deployed as a public service.

[CI run 41076324216](https://github.com/linhuachung/Optibot/actions/runs/41076324216) passed the 38-test Python suite on Windows/Linux, Docker build/entry-point check and six browser regressions. [CI evidence](evidence/local-ui-ci.json). [Fresh cloud run 41076345213](https://github.com/linhuachung/Optibot/actions/runs/41076345213) restored the prior state with the new dependency set and finished with added=0, updated=0, skipped=30, failed=0. It retained 30 committed articles, zero pending operations and the same state digest. [Cloud evidence](evidence/cloud-run-41076345213.json). Both dependency audits found zero known vulnerabilities at verification time. Source/credential-pattern checks and Git diff whitespace checks passed.

## Reference widget update

The frontend now follows the assignment screenshot's floating-widget pattern, with a bottom-right launcher, green header, greeting, suggested questions and composer. Seven browser tests and all 38 Python tests pass locally. Launcher/close/Escape, focus return, draft preservation and narrow/short viewport fit are covered. Refreshed live retrieval evidence and desktop/mobile screenshots were inspected; zero automated axe violations or page errors were observed. See [complete assignment review](final-review.md). No provider answer screenshot or live SCIO study is claimed.

## Independent BA/QA review loop

BA reviewed requirements and Brief A business coverage; QA independently reran tests and exercised failure cases. Fixed malformed-corpus health/chat responses and new-reply scrolling, including completion while the widget is closed. Each scenario was reproduced with a failing regression before its fix. Final independent results: **39 Python tests and nine browser tests pass**. BA and QA approve the tested implementation, not final submission readiness. The repository's non-cryptic name and unknown actual hours are now explicit open risks. [Review record](ba-qa-review.md).

## Current full retest and Gemini migration - 2026-10-31

The native Gemini integration passed 52 Python tests and nine browser tests, independently rerun by QA. [CI run 41213125085](https://github.com/linhuachung/Optibot/actions/runs/41213125085) passed Windows/Linux, browser checks and Docker build with the new dependencies. The dependency audit found no known vulnerabilities; `pip check`, compilation and source credential-pattern/whitespace checks passed.

31 articles were API-indexed with zero pending operations. The separate actual rerun skipped all 31 with no uploads or failures. Gemini YouTube and schedule answers each contain five bullets and one correct support URL; unsupported weather is refused. These are API acceptance checks, not a Google AI Studio screenshot. [YouTube](evidence/gemini-youtube-answer.json), [schedule](evidence/gemini-schedule-answer.json), [refusal](evidence/gemini-unsupported-answer.json), [index status](evidence/gemini-index-status.json), [rerun](evidence/gemini-local-rerun.json).

The actual floating widget now generates via Gemini and shows the correct cited article. Desktop/mobile visual inspection, axe checks and JavaScript-error checks pass. [Actual widget](evidence/gemini-widget-check.json), [desktop](evidence/gemini-widget-desktop.png), [mobile](evidence/gemini-widget-mobile.png). Gemini source lookup itself invokes a model and uses generation quota, although generated answer text is hidden in search mode.

The first real **OpenAI** scheduled event is now observed: [run 41184533900](https://github.com/linhuachung/Optibot/actions/runs/41184533900), actual start 2026-10-31 08:25 UTC / 15:25 Bangkok, added=1 updated=2 skipped=28 failed=0, 31 committed and zero pending. This supersedes earlier pending-cron statements for the deployed OpenAI workflow. Gemini manual-cloud verification is separate. Exact embedded chunks, required provider UI, live SCIO study, candidate review, naming and actual hours remain open.

Gemini cloud acceptance is now verified: runs [41213308045](https://github.com/linhuachung/Optibot/actions/runs/41213308045) and [41213474374](https://github.com/linhuachung/Optibot/actions/runs/41213474374) both pass with 31 skips, zero uploads/failures, zero pending work and identical Gemini-state digests. The second restores the first artifact, including its migration marker. Exact raw-store/document chunk telemetry is still unavailable; see [raw metadata evidence](evidence/gemini-store-metadata.json). The next Gemini-specific scheduled event remains unobserved, separate from already verified OpenAI cron execution.

Local-demo limitation: cloud state updates do not automatically synchronize back to the local server. Restore the matching latest trusted provider state before local queries after remote replacements/additions; unknown mappings fail visibly. Current live local/cloud checks use matching 31-document state.

Final API-key contract regression: Gemini now supports assignment-facing `API_KEY` as fallback to `GEMINI_API_KEY`; Docker defaults to Gemini. The new test failed before the fix and the full 53-test Python suite passes afterward. Original 52-test CI evidence is retained as historical; the final alias/Docker delta requires its own CI result.

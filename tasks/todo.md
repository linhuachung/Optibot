# Assignment checklist - current review

Updated 2026-10-31. Source: supplied assignment text/DOCX/Google Doc. This checklist separates explicit assignment requirements from additional internal tests. The user requested stopping further SCIO cases; skipped cases are not passes. No new tests or UI exercises were run in this final review. Historical detail: [previous checklist](todo-history-2026-10-31.md).

**Verdict: engineering substantially verified; full submission compliance is not yet established.** The required provider-UI screenshot and actual embedded-chunk count remain missing. In-product OptiBot warm-up chat, repository naming, actual hours and candidate ownership also need confirmation/decisions. Part 2 now includes genuine live SCIO observations.

## Step 0 - Warm-up and accounts

- [x] Create/use a SCIO trial; candidate dashboard screenshots show a14-day trial.
- [x] Configure the chosen Gemini platform privately and verify API/model/File Search access.
- [ ] Chat with the original in-product OptiBot, as required by warm-up. A visible widget is not proof a question was asked. This is separate from our custom bot and Gemini acceptance tests.

## Step 1 - Scrape and clean Markdown

- [x] Fetch public Help Center articles with pagination, stable IDs and at least30 files; current verified corpus31.
- [x] Preserve source URLs, headings, code and links; remove navigation/advertising content. Retain semantic hashes and manifest.
- [x] Verify representative article quality and formatting regressions. [Evidence](../docs/evidence/article-spot-checks.json).

## Step 2 - Assistant, API upload and required evidence

- [x] Upload31 Markdown articles using the native Gemini Python API into one reused File Search store; retain active identifiers and zero pending work. [Index](../docs/evidence/gemini-index-status.json).
- [x] Load the exact assignment prompt in API queries and restrict File Search to the saved store with known-source citation mapping.
- [x] Verify real YouTube/schedule answers: five bullets/one correct URL each, and unsupported-weather refusal. [YouTube](../docs/evidence/gemini-youtube-answer.json), [schedule](../docs/evidence/gemini-schedule-answer.json), [refusal](../docs/evidence/gemini-unsupported-answer.json).
- [x] Log completed files and explain Gemini white-space chunking:400 tokens/80 overlap. Gemini source lookup uses model quota even if generated text is hidden.
- [ ] Configure the assistant in actual Google AI Studio with the exact prompt/API-populated corpus and capture its correct cited YouTube answer. Custom-widget/API evidence is not a substitute.
- [ ] Report actual embedded-chunk count. Inspected SDK/raw REST metadata does not expose it; current reports use null. Resolve acceptable telemetry/deviation with the evaluator rather than invent a count. [Raw metadata](../docs/evidence/gemini-store-metadata.json).

## Step 3 - Daily delta and recovery

- [x] `main.py` re-scrapes, detects new/updated content, uploads delta only, logs added/updated/skipped/failed and exits with appropriate status.
- [x] Persist hashes/active IDs/pending operations atomically; finish indexing/cleanup before committing replacements. Ambiguous uploads stop safely for reconciliation.
- [x] Verify real Gemini local rerun: added0/updated0/skipped31/failed0. [Evidence](../docs/evidence/gemini-local-rerun.json).

## Step 4 - Docker and cloud

- [x] Docker runs the one-shot job. Current default is Gemini; support `GEMINI_API_KEY` and assignment-facing `API_KEY` alias. Keep OpenAI state isolated for rollback.
- [x] Configure daily GitHub Actions, encrypted Gemini secrets after explicit approval, trusted artifacts, provider state/marker and workflow serialization.
- [x] Verify two real Gemini containers restoring matching state:31 skips, zero uploads/failures/pending and identical digests. [First](../docs/evidence/cloud-run-41213308045.json), [second](../docs/evidence/cloud-run-41213474374.json).
- [x] Observe the deployed workflow's real automatic OpenAI event: added1/updated2/skipped28/failed0, subsequently switch the same scheduled workflow to Gemini. [Scheduled event](../docs/evidence/cloud-run-41184533900.json).

Additional assurance: a Gemini-specific automatic cron event has not yet been observed; its schedule is configured and manual Gemini executions are verified. Do not confuse that with missing cloud deployment.

## Step 5 - Tests and review

- [x] Last verified suite:53 Python tests and9 browser tests, including skip/delta/failure/recovery, corrupt state, key aliases, safe citations, widget lifecycle, transport and accessibility regressions.
- [x] Windows/Linux, browser and Docker CI passed [run41213997518](https://github.com/linhuachung/Optibot/actions/runs/41213997518). [Saved CI](../docs/evidence/gemini-final-ci.json).
- [x] Last dependency audits, pip consistency, compilation, credential-pattern and whitespace checks pass. No credentials are committed or exposed in frontend code.
- [x] Independent BA and QA reviews approve the reviewed implementation scope; approval does not waive missing assignment deliverables.

## Step 6 - Submission packaging

- [x] Prepare concise README with setup, local/backend/frontend/Docker instructions, chunking explanation, actual job logs and a clearly labeled custom-widget screenshot.
- [x] Include `.env.sample`, Dockerfile, clear commits, documented cuts/recovery and both provider-specific evidence histories.
- [ ] Add the required provider screenshot and verify final README is at most one rendered page; word count alone does not prove page layout.
- [ ] Decide cryptic repository naming: user-selected `Optibot` avoids the prohibited literal company name but is not cryptic. No remote rename is performed without a user decision.
- [ ] Finalize both parts together after remaining requirements/decisions; no employer submission has been sent.

## Step 7 - Live SCIO study, completed at the agreed limited scope

- [x] Candidate uses all four Brief A domains in a real trial; distinguish screenshots, candidate reports and proposals. [Observation record](../docs/scio-product-observations.md).
- [x] Assets: upload PNG/MP4/PDF; create folder and move/open files. Upload/folder membership is screenshot-supported; successful move/open also candidate-reported.
- [x] Playlists: create a three-item playlist; edit image20s->5s and observe total64s->49s, saved. Correct PDF preview observation: page2 needed manual Next; automatic progression/full looping is not established.
- [x] Schedules: bind a playlist to an event, inspect explicit dates/times, recurrence/custom endings, future Nov1/2 instances and default-content choices. Runtime scheduling/timezone effects are not inferred.
- [x] Screens: inspect code pairing and screen settings; candidate explicitly confirms video/blue image/PDF in the installed Player rather than portal Preview. This supports the direct upload->playlist->screen path by candidate report.
- [x] Honor the user's instruction to skip further cases; disclose scope limits rather than marking them passed.

Skipped/not verified at user request: replacement propagation, referenced deletion, exhaustive download/duplicate/search/settings/limits, reordering/nesting and folder variants, overlap/DST/timezone outcomes, fallback/schedule-driven Player execution, offline behavior, Linux playback and automatic PDF page progression/full looping. These are study-depth limits and interview risks, not individually specified extra submission artifacts.

## Step 8 - Scope and product-informed decisions

- [x] State Brief A on line1 and cover Assets, Playlists, Schedules and Screens; define team, platform, depth and cuts.
- [x] Integrate actual candidate observations into the plan and explain why current-product features exceed proposed first-release cuts.
- [x] Separate observed portal/candidate Player behavior from proposed Linux player, scheduling, replacement and reliability policies. Do not generalize manual preview behavior to all Player platforms.

## Step 9 - Architecture and flows

- [x] Define portal/API/worker/storage/player boundaries, core models and authorization/security foundation.
- [x] Plan the complete file->playlist/schedule->paired-player flow with replacement and failure handling; this is proposed implementation scope, not a claim every path was tested live.

## Step 10 - Delivery order

- [x] Provide ordered milestones, prerequisites, usable outcomes and rationale; risk spikes precede dependent delivery.

## Step 11 - Estimates and acceptance

- [x] Explain48 baseline engineering-days+12 contingency=60; two engineers at80% capacity provide8 planned days/week, yielding7.5 weeks rounded to8. QA16days/design4days are separate.
- [x] Define acceptance/risk/cut order across all four domains; implementation estimates are distinct from the10-hour take-home planning budget.

## Step 12 - Final review and candidate readiness

- [x] Compare both assignment parts against code, evidence and handoff; independent BA/QA evidence-only final review completed after the live study.
- [x] Correct stale no-SCIO-observations claims, the PDF auto-loop claim and skipped-case status; prepare interview notes.
- [ ] Candidate confirms ownership and can explain scope, order, platform and every estimate. Formal rehearsal notes are optional preparation, not a separate required deliverable.
- [ ] Record actual Part 1/Part 2 hours and disclose any overrun/cuts; actual hours remain unknown.
- [ ] Complete final combined submission review after explicit missing items are resolved or transparently disclosed/accepted.

## Current conclusion

Part 1's scraper/API ingestion/job engineering and bonus tests are supported; full Part 1 compliance is blocked by provider UI/screenshot and chunk reporting, plus warm-up/naming/packaging decisions. Part 2's planning structure and meaningful customer-use evidence are substantially aligned, with declared study limits and candidate ownership still important. Do not promise a score or that every possible case passes.

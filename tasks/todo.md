# Take-home checklist

Plan: [plan.md](plan.md). Council: [council.md](council.md).

Part 2 update: proposed scope, architecture, sequencing and estimates are drafted in `docs/scio-slice-plan.md`. The user confirmed no live SCIO exploration yet; Step 7 and final validation in Step 12 remain open. Draft completion is not submission readiness.
Steps 1, 3 and 5 are verified locally. Step 2 ingestion works but generation/UI/chunk evidence remains incomplete. Step 4 Docker and two authenticated GitHub Actions runs are verified, including persisted-state restoration; only the first automatic cron trigger remains pending. Step 6 packaging is prepared with remaining submission evidence unchecked. Source is connected to `linhuachung/Optibot`. See [verification](../docs/verification.md).

## Council preparation — completed

- [x] Compare local DOCX and linked Google Doc with the draft.
- [x] Obtain independent TL1, TL2, TL3, BA1, BA2 and BA3 reviews.
- [x] Tally decisions under the four-vote/no-unanimous-group-opposition rule.
- [x] Cross-read votes and resolve the Part 2 time split in round 2.
- [x] Write locked plan and matching execution checklist.

## Step 0 — Warm-up and feasibility (1h)

Dependencies: none. Likely artifacts: private warm-up notes, feasibility notes, dependency lock, `.env.sample` (medium scope).

- [ ] Use the trial's OptiBot; record real tone, citations and supported/unsupported question behavior. Check account/runtime prerequisites.
- [ ] Prove Python upload → successful indexing → provider UI cited answer with the exact prompt; establish actual embedded chunk-count telemetry.
- [ ] Validate the hosting persistence path; record the tested SDK/API/UI configuration and resolve any unmet mandatory requirement before expanding implementation.

Verification: retain the tiny ingestion result, UI evidence and telemetry method. Escalate obsolete UI or inaccessible chunk counts; do not invent evidence. Include all time spent in the 18h total.

## Step 1 — Scrape and normalize (1.5h)

Dependencies: 0. Likely files: scraper module, Markdown module, manifest (medium).

- [x] Fetch one article and preserve headings, relative links, lists and code in Markdown, with `Article URL:` and stable ID.
- [x] Produce at least 30 clean files including the YouTube source; freeze selected IDs and define new-article discovery/watermark behavior.
- [x] Spot-check three representative files against source pages; normalize hashes without volatile fetch metadata.

Verification: count actual generated files, inspect formatting and source URL accuracy, exercise pagination. Do not assume a fixed total of 416.

## Step 2 — API ingestion and citation evidence (1.5h)

Dependencies: 0–1. Likely files: ingestion module, prompt configuration, screenshot (medium).

- [x] Upload through Python to one reused vector store and wait for all successful indexing statuses; save remote IDs.
- [ ] Configure the supported provider UI with the exact prompt from the plan and the API-populated store. Capture the YouTube answer with correct article URLs.
- [ ] Log completed file and actual embedded-chunk counts separately; explain chunking and count measurement.

Verification: inspect the screenshot and citations against source content; check a second supported question and an unsupported one. File totals or retrieved snippets must not masquerade as chunk totals.

Implementation note (2026-10-30): 30 files indexed; live retrieval returns the YouTube guide. Answer generation returns `credit_balance_exhausted` / `insufficient_quota`. Browser control fails to initialize, so no provider UI screenshot exists. Exact managed chunk totals are unavailable in inspected metadata and are reported as `null`. These unchecked requirements are not waived.

## Checkpoint — Ingestion

- [ ] Minimum corpus, API upload, exact prompt, chunk evidence and required UI screenshot are demonstrated; unresolved requirements are explicitly recorded.

## Step 3 — Durable delta and recovery (1.5h)

Dependencies: 2. Likely files: `main.py`, state module, ingestion module (medium).

- [x] Re-scrape selected/new eligible articles; compare hashes, upload additions/changes only, and print added/updated/skipped/failed counts.
- [x] Persist committed hashes, active IDs and pending operations atomically; recover interrupted uploads and retire superseded indexed versions.
- [x] Keep failed items retryable, use bounded timeouts/retries, exit nonzero on failure and 0 on success.

Verification: unchanged rerun performs zero uploads; one changed fixture replaces its old indexed version; failed upload/index does not advance committed state. A retry completes pending work without a redundant replacement.

Evidence: two real local processes each completed with `added=0 updated=0 skipped=30 failed=0`. Tests cover updated fixtures, cleanup retry, pending-source changes, failed indexing, lost-upload response reconciliation and OS locking. Ambiguous uploads with no unique remote match fail visibly for manual reconciliation; they are never blindly repeated. See `docs/evidence/local-daily-run.json` and `local-daily-rerun.json`.

## Step 4 — Docker and daily GitHub Actions hosting (1h)

Dependencies: 3. Likely files: `Dockerfile`, deployment config, run artifact (medium).

- [x] Prepare Dockerfile, secret/data exclusions, GitHub Actions schedule, trusted state artifacts and bootstrap instructions. User explicitly replaced Railway.
- [x] Verify Windows/Linux tests and Docker build/entry-point smoke check in GitHub CI: run 41066391124 succeeded.

- [x] Run the Docker entry point once with the API key, reused store and durable `/data`; document both key aliases. The cloud uses `OPENAI_API_KEY`.
- [x] Configure encrypted GitHub Actions secrets, daily UTC schedule and persistent state artifacts; verify a real authenticated cloud run terminates.
- [x] Repeat in a fresh container using the same state; retain reviewer-accessible logs and redacted last-run artifacts.
- [ ] Observe the first real cron-triggered run, separately from manual dispatch verification.

Verification: successful exit 0; second cloud/container run skips unchanged articles; durable IDs/hashes survive container replacement; evidence links work for the intended reviewer.

## Step 5 — Focused tests (0.5h maximum)

Dependencies: 3; may be developed alongside it. Likely files: delta/recovery tests and fixture (small).

- [x] Test unchanged-content skipping and failed-update state/retry behavior with mocked provider calls.
- [x] Run the focused test command and record it. Add a Markdown fixture only if budget remains.

Verification: demonstrate zero uploads on unchanged data and no false committed success after failure. Avoid broad coverage work.

Command: `python -m unittest discover -s tests -v` — 27 tests passed locally, including trusted artifact restoration tests. The 27-test Windows/Linux CI and Docker image build succeeded in run 41067614734. Daily cloud runs 41067930209 and 41068135936 both succeeded; the second restored the prior artifact, with identical state hashes and 30 skips.

## Checkpoint — Runnable daily job

- [x] Delta behavior, persistent state, replacement recovery, focused tests and real deployment evidence match the plan. Automatic cron-trigger observation is tracked separately above.

## Step 6 — Submission pack (1h)

Dependencies: 2, 4, 5. Likely files: README, `.env.sample`, optional `CUTS.md` (medium).

- [x] Prepare concise setup/local/Docker README, deployment guide and explicit `CUTS.md`.

- [ ] Keep README at most one page: setup, local/Docker invocation, chunking explanation, job evidence link and screenshot.
- [x] Check repository name, clear commits, secret exclusions and sample environment variables; verify existing evidence paths and explicitly identify missing screenshot/cloud evidence.
- [ ] Record actual cuts/unmet requirements and prepare both parts for submission together after Step 12.

Verification: follow documented commands in a clean environment; inspect tracked files for secrets and missing deliverables. Do not claim a successful run that was not observed.

## Step 7 — Live SCIO study for Brief A (2.5h)

Dependencies: trial access; may occur before Part 1 completion. Likely artifact: dated product observations (small).

- [ ] Use uploaded assets and their operations/folders/settings; explore playlists with durations and schedules with file/playlist events.
- [ ] Investigate pairing, assignment, screen folders/settings and end-to-end playback; record any unavailable hardware or trial permissions honestly.
- [ ] Study all four Brief A feature areas beyond the proposed MVP; corroborate with targeted Help Center material.

Verification: each claimed current behavior has an observation or source; distinguish untested assumptions and simulated actions from observed device behavior.

## Step 8 — Scope and assumptions (1h)

Proposed scope is drafted in `docs/scio-slice-plan.md`; live-product validation remains pending under Step 7.

Dependencies: 7. Likely file: `docs/scio-slice-plan.md` (small).

- [x] Put Brief A at the top and define goals, depth, non-goals, team size and platform assumptions.
- [x] Cover Assets, Playlists, Schedules and Screens, with one explicit player platform and a file-to-paired-screen acceptance path.
- [ ] Explain scope choices using product observations; identify cuts without removing an entire required domain.

Verification: scope maps to the brief; proposed behavior is separate from current SCIO behavior. No Brief B expansion.

## Step 9 — Architecture and flows (2h)

Dependencies: 8. Likely artifact: architecture/model/flow sections in the Part 2 document (small).

- [x] Define portal/backend/storage/player boundaries and core asset, playlist, schedule and screen models.
- [x] Trace upload → playlist/schedule → screen assignment → paired-device playback, including content replacement and failure handling.
- [x] State decisions on player scope, scheduling/timezones and operational limits, with rationale and unresolved questions.

Verification: walk an example through every boundary; explain how each design choice supports the scoped user flow. No application code.

## Step 10 — Delivery sequence (1.5h)

Dependencies: 9. Likely artifact: ordered implementation slices in the Part 2 document (small).

- [x] Define small vertical slices, prerequisites and checkpoints, starting with risky integration assumptions.
- [x] Explain why each slice comes in that order and what usable outcome it delivers.

Verification: no circular dependencies, unsupported screen endpoint or unowned work; every slice has a testable outcome.

## Step 11 — Estimates, acceptance and risks (1.5h)

Dependencies: 10. Likely artifact: estimates/acceptance/risk sections in the Part 2 document (small).

- [x] Estimate implementation effort per slice with units, staffing assumptions, uncertainty and rationale; derive a credible delivery duration.
- [x] Define acceptance criteria across all four domains and the end-to-end path; identify dependencies and major failure risks.
- [x] Explain cut order and milestone tradeoffs. Separate system implementation duration from the 10h spent authoring this plan.

Verification: check arithmetic, staffing capacity and dependency effects; be able to defend each number without citing an unexplained AI estimate.

## Step 12 — Review and interview preparation (1.5h)

The proposed document passes section/coverage and estimate-arithmetic checks. Final review awaits live product observations and the candidate's review of assumptions/estimates. This is not yet a final submission.

Dependencies: 7–11; submission also depends on 6. Likely artifacts: revised Part 2 document and private defense notes (small).

- [ ] Read the final plan as a team handoff: what, order, duration and why are explicit; assumptions and observed facts are distinguishable.
- [ ] Rehearse questions on current SCIO behavior, including settings/features outside the planned MVP and chosen player/platform cuts.
- [ ] Check both submission parts together, actual cuts and links; stop at the approximately 18h budget and disclose incomplete work.

Verification: Brief A appears on line 1; the final document covers all selected domains, team/platform decisions, order, estimates and rationale. The user can defend its decisions. No Part 2 code was produced.

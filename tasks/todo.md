# Take-home checklist

Current verification (2026-10-31): Gemini is selected locally; 31 articles indexed via API, real unchanged rerun skips 31, supported YouTube/schedule answers and unsupported-question refusal verified. 53 Python and nine browser regressions pass; Windows/Linux CI and Docker build passed run 41213997518. The actual custom widget answers with Gemini and cited URLs. Cloud Gemini migration verification is tracked at the end. Required Google AI Studio screenshot, exact embedded chunks and candidate/product gates remain open.


Plan: [plan.md](plan.md). Council: [council.md](council.md).

Part 2 update: proposed scope, architecture, sequencing and estimates are drafted in `docs/scio-slice-plan.md`. The user confirmed no live SCIO exploration yet; Step 7 and final validation in Step 12 remain open. Draft completion is not submission readiness.
Steps 1, 3 and 5 are verified against the original OpenAI implementation. Step 2 OpenAI API ingestion works but provider-UI/chunk evidence remains incomplete; a Gemini model preflight does not establish full provider migration. Step 4 Docker, durable state restoration and a real scheduled cloud run are verified. Scheduled OpenAI run 41184533900 succeeded on 2026-10-31 with added=1, updated=2, skipped=28, failed=0 and 31 committed articles. Step 6 packaging is prepared with remaining submission evidence unchecked. Source is connected to `linhuachung/Optibot`. See [verification](../docs/verification.md).

## Council preparation — completed

- [x] Compare local DOCX and linked Google Doc with the draft.
- [x] Obtain independent TL1, TL2, TL3, BA1, BA2 and BA3 reviews.
- [x] Tally decisions under the four-vote/no-unanimous-group-opposition rule.
- [x] Cross-read votes and resolve the Part 2 time split in round 2.
- [x] Write locked plan and matching execution checklist.

## Step 0 — Warm-up and feasibility (1h)

Dependencies: none. Likely artifacts: private warm-up notes, feasibility notes, dependency lock, `.env.sample` (medium scope).

- [ ] Use the trial's OptiBot; record real tone, citations and supported/unsupported question behavior. Check account/runtime prerequisites.
- [x] Prove Python API upload and successful indexing in the original OpenAI store; retain remote file IDs and separate uploaded-file counts.
- [x] Validate durable hosting persistence through restored GitHub Actions artifacts and repeated cloud containers; a real scheduled OpenAI run also succeeded.
- [ ] Complete provider-UI setup and a cited answer with the exact prompt; establish actual embedded chunk-count telemetry and record the tested provider API/UI configuration. Unmet mandatory requirements remain open.

Verification: retain the tiny ingestion result, UI evidence and telemetry method. Escalate obsolete UI or inaccessible chunk counts; do not invent evidence. Include all time spent in the 18h total.

## Step 1 — Scrape and normalize (1.5h)

Dependencies: 0. Likely files: scraper module, Markdown module, manifest (medium).

- [x] Fetch one article and preserve headings, relative links, lists and code in Markdown, with `Article URL:` and stable ID.
- [x] Produce at least 30 clean files including the YouTube source; freeze selected IDs and define new-article discovery/watermark behavior.
- [x] Spot-check three representative files against source pages; normalize hashes without volatile fetch metadata.

Verification: count actual generated files, inspect formatting and source URL accuracy, exercise pagination. Do not assume a fixed total of 416.

## Step 2 — API ingestion and citation evidence (1.5h)

Dependencies: 0–1. Likely files: ingestion module, prompt configuration, screenshot (medium).

- [x] Upload through Python to one reused OpenAI vector store and wait for all successful indexing statuses; save remote IDs. This is original OpenAI evidence, not proof of Gemini migration.
- [ ] Configure the supported provider UI with the exact prompt from the plan and the API-populated store. Capture the YouTube answer with correct article URLs.
- [x] Log completed OpenAI file counts separately and explain the managed default chunking strategy in README; use `null` for an unavailable exact embedded-chunk total.
- [ ] Obtain and log actual embedded-chunk counts with a supported measurement; unavailable counts remain an unmet requirement. Do not substitute file totals or retrieval hits.

Verification: inspect the screenshot and citations against source content; check a second supported question and an unsupported one. File totals or retrieved snippets must not masquerade as chunk totals.

Historical OpenAI implementation note (2026-10-30): 30 files indexed; live retrieval returns the YouTube guide. Answer generation returns `credit_balance_exhausted` / `insufficient_quota`. Browser control fails to initialize, so no provider UI screenshot exists. Exact managed chunk totals are unavailable in inspected metadata and are reported as `null`. These unchecked requirements are not waived. Gemini now resolves API generation availability with separate provider evidence below; it does not replace provider-UI/chunk requirements.

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
- [x] Observe a real cron-triggered OpenAI run, separately from manual dispatch: [run 41184533900](https://github.com/linhuachung/Optibot/actions/runs/41184533900), event=`schedule`, created 2026-10-31 at 08:25 UTC (15:25 Bangkok). It completed with added=1, updated=2, skipped=28, failed=0, 31 committed articles and zero pending operations. [Scheduled-run artifact](../docs/evidence/cloud-run-41184533900.json). The configured cron time and actual run creation time are distinct.

Verification: successful exit 0; second cloud/container run skips unchanged articles; durable IDs/hashes survive container replacement; evidence links work for the intended reviewer.

## Step 5 — Focused tests (0.5h maximum)

Dependencies: 3; may be developed alongside it. Likely files: delta/recovery tests and fixture (small).

- [x] Test unchanged-content skipping and failed-update state/retry behavior with mocked provider calls.
- [x] Run the focused test command and record it. Add a Markdown fixture only if budget remains.

Verification: demonstrate zero uploads on unchanged data and no false committed success after failure. Avoid broad coverage work.

Command: `python -m unittest discover -s tests -v` — 29 tests passed locally, including trusted artifact restoration and lost-journal orphan recovery tests. The 29-test Windows/Linux CI and Docker image build succeeded in run 41072188291. Daily cloud runs 41067930209 and 41068135936 both succeeded; the second restored the prior artifact, with identical state hashes and 30 skips.

## Checkpoint — Runnable daily job

- [x] Delta behavior, persistent state, replacement recovery, focused tests and real deployment evidence match the plan. The actual scheduled OpenAI event is recorded separately above.

## Step 6 — Submission pack (1h)

Dependencies: 2, 4, 5. Likely files: README, `.env.sample`, optional `CUTS.md` (medium).

- [x] Prepare concise setup/local/Docker README, deployment guide and explicit `CUTS.md`.

- [ ] Keep README at most one page: setup, local/Docker invocation, chunking explanation, job evidence link and screenshot.
- [x] Check clear commits, secret exclusions and sample environment variables; verify existing evidence paths and explicitly identify missing screenshot/cloud evidence.
- [ ] Resolve repository naming risk: user-selected `Optibot` avoids the literal company name but directly identifies the mini-clone and is not cryptic. Do not claim full compliance or silently rename the remote.
- [x] Record current scope cuts and unmet requirements in `CUTS.md` and `docs/final-review.md`, including naming and unknown actual hours.
- [ ] Complete the final combined submission pack after provider evidence and Step 12 candidate validation; submit both parts together with actual cuts and hours disclosed.

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
- [x] Identify proposed platform/format/feature cuts without removing any of the four required Brief A domains; independent BA review confirms domain coverage.
- [ ] Explain and reconcile scope choices using actual live-product observations; proposed policies are not observed SCIO behavior.

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

- [x] Retrieve the current Google Doc and compare both parts with the implementation and Brief A draft; record evidence and open requirements in `docs/requirements-review.md`.
- [x] Review business acceptance/failure policies and estimate units; clarify the from-scratch assumption and folder coverage across all four resource types.
- [x] Reproduce and fix the orphan-upload case after loss of a cloud journal; verify the fix and duplicate-filename guard locally and in CI. Cloud run 41072188793 also succeeded with restored state and 30 skips.
- [x] Prepare `docs/interview-prep.md` with business scenarios, estimate rationale and a candidate rehearsal checklist.

Dependencies: 7–11; submission also depends on 6. Likely artifacts: revised Part 2 document and private defense notes (small).

- [x] Independently review the proposed team handoff: what, order, duration and rationale are explicit; assumption/observation labels, domain coverage and estimate arithmetic pass BA review.
- [ ] Obtain candidate acceptance of the final handoff and ownership of its assumptions/estimates after live SCIO study; the candidate must be able to defend the plan.
- [ ] Rehearse questions on current SCIO behavior, including settings/features outside the planned MVP and chosen player/platform cuts.
- [x] Review both parts together against requirements and record implemented behavior, current cuts, missing evidence and candidate-dependent gates.
- [ ] Complete final candidate submission checks after resolving remaining evidence/decisions; verify final links, disclose actual hours and any overrun against the approximately 18h budget, and send both parts together.

Verification: Brief A appears on line 1; the final document covers all selected domains, team/platform decisions, order, estimates and rationale. The user can defend its decisions. No Part 2 code was produced.

## Requested local server/frontend - verified

This is the user-requested local demo, separate from the assignment's provider UI evidence and Part 2 planning.

- [x] Add local FastAPI server, health/search/answer endpoints and server-side key handling.
- [x] Add frontend with actual article retrieval, source links, explicit generation errors and mobile layouts.
- [x] Test input/origin/body limits, private-file exclusions, provider failures and citation mapping: 39 Python tests pass locally.
- [x] Test keyboard search, safe text rendering, duplicate-send protection, quota fallback, empty results and unavailable backend: nine browser tests pass locally, including widget lifecycle, response visibility while open/closed, focus return and draft preservation.
- [x] Check WCAG A/AA rules at narrow/desktop widths: no automated axe violations; no horizontal overflow at 320/768/1024/1440 pixels.
- [x] Verify the actual UI against the existing store: 30 indexed articles, three YouTube sources, no page JavaScript errors. Save clearly labeled local screenshots and JSON evidence.
- [x] Write root README, detailed server/frontend run instructions, frontend README and API contract.
- [x] Verify Windows/Linux Python checks, Docker build and the browser CI job: run 41076324216 passed. Fresh cloud run 41076345213 restored state and skipped all 30 articles with zero failures.

Remaining original checkboxes above still require genuine provider/product/human evidence. Automated local UI checks cannot complete them.

## Reference widget and pasted-assignment review

- [x] Read the newly pasted assignment and review both parts against current evidence.
- [x] Adapt the local frontend to the supplied reference: bottom-right launcher, compact green-header panel, greeting, suggested questions and composer.
- [x] Verify Escape/close/reopen preserves drafts, restores focus and fits narrow/short viewports.
- [x] Recheck actual YouTube retrieval and capture current desktop/mobile widget screenshots.
- [x] Record assignment findings and open submission gates in `docs/final-review.md`.

## BA/QA independent review loop

- [x] Obtain independent BA requirements/business review and QA test/failure review.
- [x] Reproduce both QA issues with failing tests, then fix new-reply scrolling and malformed-corpus API handling.
- [x] Run 39 Python tests and nine browser tests successfully after all fixes.
- [x] Correct the repository-name compliance claim and distinguish planned budgets from actual time spent.
- [x] Obtain BA round-2 and QA final follow-up approval for the tested implementation; submission gates remain open.
- [ ] Record candidate-reported actual Part 1 and Part 2 hours; current actual time is unknown, not the planned 8h/10h allocations.

- [x] Verify BA/QA fix commit on Windows/Linux, Docker build and browser CI: run 41083463882 passed. Reload the project-owned local API server and verify ready/30-article health.

## Gemini completion and full retest - 2026-10-31

- [x] Configure the user-authorized trial key privately; verify authentication, File Search access and working model `gemini-3.5-flash-lite`. No billing settings changed.
- [x] Implement native API upload, bounded operation polling, provider-isolated state, semantic delta hashes, replacement cleanup and pending-operation recovery.
- [x] Index 31 real articles into Gemini File Search, with zero pending operations. Save `docs/evidence/gemini-upload-report.json` and `gemini-index-status.json`.
- [x] Run a second real local job: added=0 updated=0 skipped=31 failed=0. Save `gemini-local-rerun.json`.
- [x] Verify actual YouTube and schedule answers against their source instructions: five bullets/one support URL each; unsupported weather request refused. Save separate `gemini-*-answer.json` evidence.
- [x] Verify exact prompt loading, known-corpus grounding, positive limits, connection errors, corrupt citation metadata, orphan recovery, failed indexing and retry/cleanup behavior in regressions.
- [x] Run 52 Python tests and nine browser tests; dependency consistency, compilation and pinned dependency audit pass. Windows/Linux, browser and Docker CI run 41213997518 passed.
- [x] Verify actual Gemini widget generation/cited source links on desktop and 320px mobile: no page errors, no horizontal overflow and no automated axe violations. Screenshots are custom UI evidence, not AI Studio evidence.
- [x] Update CLI/backend/frontend/docs and explicitly disclose that Gemini source lookup uses generation quota even when generated answer text is hidden.
- [x] Obtain independent QA implementation approval after fixing newly reproduced invalid-limit, source-lookup, transport and metadata-validation failures.
- [x] Configure Gemini encrypted GitHub Actions secrets and provider variables after explicit separate user approval. Key values were not printed or committed.
- [x] Verify two real Gemini cloud container runs: 41213308045 and 41213474374 passed. Both use Gemini, skip all 31 with zero uploads/failures, retain zero pending operations and the migration marker, and have identical provider-state digests.
- [ ] Capture real Google AI Studio provider setup/YouTube-answer screenshot. Native computer-use initialization still fails with sandbox-helper startup error; custom screenshots do not replace this.
- [ ] Resolve actual embedded-chunk totals. Gemini uses 400-token/80-overlap white-space chunking; inspected store/document metadata does not expose exact total.

The remaining live OptiBot/SCIO study, candidate acceptance/rehearsal, cryptic naming and actual-hours checkboxes above remain required. Do not claim all steps or the combined submission are complete.

### Current cloud acceptance evidence

Gemini runs [41213308045](https://github.com/linhuachung/Optibot/actions/runs/41213308045) and [41213474374](https://github.com/linhuachung/Optibot/actions/runs/41213474374) are separate successful containers; the second restores the first's trusted artifact. Evidence files explicitly select `gemini-state.json`, not retained OpenAI rollback state. The existing cron schedule remains active with Gemini selected; the next Gemini-specific automatic event has not yet occurred. The earlier automatic OpenAI event is verified separately.

Raw Gemini store/document metadata was checked directly in addition to SDK inspection: 31 active documents, no exposed exact chunk total. See `docs/evidence/gemini-store-metadata.json`. This is why the exact-chunk requirement stays unchecked.

- [x] Preserve assignment-facing Gemini `API_KEY` alias (explicit `GEMINI_API_KEY` wins), with failing-then-passing regression; Docker defaults to the selected Gemini provider. Full Python suite now has 53 passing tests.

- [x] Final API_KEY/Docker delta passed Windows/Linux, browser and Docker CI run 41213997518. Fresh npm/Python dependency audits report zero known vulnerabilities; credential-pattern and whitespace scans pass.

## Step 7 session preparation - 2026-10-31

- [x] Confirm trial/dashboard access from the user's screenshot; record only visible onboarding/navigation facts.
- [x] Open a separate SCIO browser at the actual sign-in form for the user's own login; no password or verification code is requested in chat.
- [x] Prepare original nonsensitive image/replacement, short MP4 and two-page PDF fixtures plus hashes in `.runtime/scio-study-assets/`.
- [ ] Complete authenticated functional study and record action/outcome/evidence for all four domains. Session preparation does not satisfy the existing Step7 acceptance checkboxes.

- [x] Observe user-created Takehome Study folder and uploaded PNG/MP4/PDF test cards with thumbnails in the Files/Assets Home view (user screenshot). Full preview/playback, folder membership and other Assets actions remain unverified.

- [x] Record user-reported fixture move/open success and screenshot-corroborated membership in Takehome Study.
- [x] Observe saved three-item Takehome Study Playlist: video4s, image20s, PDF2pages/40s, total64s. Duration editing, reordering, preview/loop and screen assignment remain unverified.

- [x] Observe image duration edited from20s to5s, Changes Saved and playlist total recalculated from64s to49s; video4s and PDF40s remain unchanged (user screenshot). Preview/playback remains unverified.

- [x] Record user-reported playlist preview opened with video visible. Automatic progression, both PDF pages, looping and paired-screen playback remain unverified.

- [x] Record corrected portal-preview observation: candidate says PDF stops at page1 and requires manual Next for page2; earlier automatic-loop claim is superseded.
- [ ] Verify hands-off PDF page progression/full automatic preview loop; no timed result has been supplied. Physical-player behavior is separately unverified.

- [x] Observe Takehome Study Schedule created successfully and shown as an empty Week calendar with Add Event available (user screenshot). Event/timezone/recurrence/assignment behavior remains unverified.

- [x] Observe a calendar event labeled10:48-11:18 Takehome Study Playlist on Saturday31. Event details/content binding, recurrence/timezone and actual player execution remain unverified.

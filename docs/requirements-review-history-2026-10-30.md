# Historical requirement review - superseded

Current comparison: [requirements-review.md](requirements-review.md). Earlier no-trial/no-Gemini-generation statements below are historical, not current status.

# Step 12: assignment and business review

Reviewed 2026-10-30 against the **current text export** of the [take-home Google Doc](https://docs.google.com/document/d/16rFWeJAIyJSlJWQKtYE5J--U5X6JmQXguyn1c2jsMhA/edit?tab=t.0), the supplied DOCX, source code, tests and saved deployment evidence. The Drive connector and browser fetch failed; direct Google Docs text export succeeded. This review uses the current exported requirements, not an assumption that an older plan is authoritative.

**Verdict: the selected business scope is aligned, but the submission is not ready.** The main risks are missing required evidence and live-product knowledge. Review and tests reduce risk; they do not guarantee the evaluator's decision or the absence of defects.

## Required submission gates still open

1. **Part 1 warm-up and Part 2 live SCIO study:** the user confirmed they have not explored the product. The assignment explicitly expects customer-style use and detailed knowledge of the selected slice. Help Center summaries alone do not satisfy this. Complete [the observation record](scio-product-observations.md), revise the proposal and rehearse the resulting decisions.
2. **Provider UI setup and cited-answer screenshot:** `system_prompt.txt` matches all five prompt lines in the current Google Doc exactly. Python ingestion and vector retrieval work, but that does not establish correct assistant answers. There is no `docs/screenshot-youtube.png`; generated-answer verification last returned exhausted credits. Fund the project, check the required YouTube answer, a second supported question and an unsupported question, then capture the required correct provider-UI answer with article URLs.
3. **Actual chunk reporting:** uploaded-file counts are present; exact embedded-chunk totals are not. `embedded_chunks: null` is transparent but remains an unmet requirement. Obtain a supported measurement or ask the evaluator what evidence they accept for managed chunking. Do not substitute retrieval hits, parsed text entries, file counts or estimates.
4. **Supported replacement for obsolete assistant workflow:** the assignment still names Assistant creation in the provider UI. OpenAI confirms the Assistants API is retired and recommends Responses. The code uses Responses, but no current provider-UI equivalence has been demonstrated or accepted by the evaluator. Keep this compatibility question explicit. [Official migration documentation](https://developers.openai.com/api/docs/assistants/migration).
5. **Final README and combined submission:** setup, local/Docker commands, chunking explanation and real cloud-run links exist. The required screenshot is missing. The README is currently 371 words, but a word count does not prove its final rendered length after adding the screenshot. Keep it within one rendered page, verify all final links, record actual time/cuts and submit both parts together.

## Part 1 comparison

- **At least 30 support articles:** demonstrated by the local manifest, 30 generated Markdown files and 30 completed remote index entries. There is no requirement to ingest all 416 articles; that count is a source observation, not a fixed contract.
- **Clean Markdown and source links:** headings, relative links and fenced code are covered by fixtures; three actual source pages were spot-checked. Runtime article files remain outside Git, with repeatable generation commands in README.
- **Python API ingestion:** implemented and demonstrated. No UI file picker is used for ingestion. The saved store is reused and attachments are reconciled by article/hash metadata.
- **Exact prompt and grounded behavior:** prompt text matches; live behavior remains unverified. File citations must identify actual source article URLs. A successful retrieval result does not prove the answer obeys the five-bullet/three-URL limit or refuses unsupported questions.
- **One-shot Docker job:** `main.py` re-scrapes and exits with meaningful status, and actual cloud containers succeeded. State and counts survive separate executions. GitHub Actions is a reasonable reading of the source's allowance for any cloud/public hosting platform; the examples are not an exclusive host list. The original Railway choice was superseded by the user's explicit hosting choice.
- **Delta-only behavior:** two cloud runs demonstrated zero additions/updates and 30 skips. Fixtures exercise an actual content change, failed indexing and old-version cleanup. Timestamp-only changes do not re-embed unchanged content.
- **Daily schedule and logs:** daily cron is configured and real manually triggered cloud logs are linked. The first actual schedule-triggered execution has not yet been observed; this is a remaining verification item, not evidence that the schedule failed.
- **Repository and secrets:** `linhuachung/Optibot` omits the forbidden company string and was explicitly chosen by the user. Source has clear commits and `.env.sample`; actual keys and state are excluded. The repository is not presented as evaluator-approved merely because the literal naming check passes.
- **Tests:** the current local suite has 29 passing tests after this review. The updated 29-test suite passed Windows/Linux CI and its Docker build in [run 41072188291](https://github.com/linhuachung/Optibot/actions/runs/41072188291). The fixed code also passed [cloud run 41072188793](https://github.com/linhuachung/Optibot/actions/runs/41072188793), restoring state and skipping all 30 articles.

## Part 2 business comparison

**The right brief:** the first line selects Brief A. The plan stays with Assets, Playlists, Schedules and Screens. A custom-role/folder-sharing system, approval roles and team administration from Brief B are not accidentally added as required deliverables. Basic sign-in/workspace authorization remains a necessary security boundary.

**Assets:** the proposal includes uploaded images, video and documents; search, preview, download, duplicate, replace, delete, folders, settings and plan-dependent limits. Its supported formats and import paths are explicitly bounded. Native cloud-drive integrations are a declared depth cut, not a claim that SCIO lacks them. Confirm those cuts with the candidate before submission.

**Playlists:** file references have ordered positions and durations and play in a loop. Folders and settings are included. Document-page behavior, explicit versus native video duration and replacement propagation are now stated as proposed business rules. Nesting and item-level scheduling are declared later increments, while current product knowledge of them remains necessary for the interview.

**Schedules:** events target an uploaded file or playlist within a time interval. Folders/settings, one-off/weekly recurrence, timezone rules, overlap preview and fallback are included. Custom/monthly recurrence and temporary takeover are explicit depth cuts. Half-open boundaries, midnight cases and daylight-saving behavior are proposed acceptance rules; they must not be described as observed SCIO behavior without trial evidence.

**Screens:** the plan includes code-based pairing to a physical Linux player, folders/settings and assignment of all three target types. Choosing one player platform and bounding device-side scope is permitted by the brief. A browser simulation or a successful manifest acknowledgement alone is not proof of physical playback.

**End to end:** the required upload-to-paired-screen path is present, including media readiness, publication, download, checksum validation, actual playback and update/failure feedback. The plan now explicitly asks for one image, one video and one multipage document through that path, plus direct screen assignment of each target type.

**From scratch:** managed identity is a third-party building block; the plan does not assume access to an existing SCIO API/backend. PostgreSQL, storage, worker, portal and player responsibilities are proposed design choices, not claims about OptiSigns internals.

**Team handoff and estimates:** each milestone states the outcome, dependencies, acceptance and rationale. The baseline is 48 engineering-days plus 12 contingency days. Two engineers at 80% planned capacity provide eight engineering-days/week, so engineering delivery is approximately 7.5 weeks, rounded to eight. QA/design add 20 person-days: 80 person-days across roles, not 80 engineering-days. Calendar capacity, coordination allowance and risk contingency are now distinguished. These numbers remain proposed and require candidate ownership; they are not a measured commitment.

## Concrete corrections made in this review

- **Fixed a reproduced Part 1 bug:** a file uploaded immediately before loss of the cloud journal could be uploaded again on retry because it had not yet acquired vector-store attributes. Fresh ingestion now also checks the exact store/article/hash filename in provider Files and reuses the orphan. Multiple matching files stop for manual reconciliation rather than choosing arbitrarily. Two new regression cases pass.
- **Made folder coverage explicit:** all four resource kinds receive folder operations and rejection cases, rather than leaving screen/playlist/schedule folders implicit in the shared model.
- **Closed business-policy gaps in the proposal:** upload/quota idempotency, failed-processing publication, independent duplicates, stale saves, playlist duration after replacement, schedule boundaries, stale manifest rejection, download expiry, offline revocation limits and safe blob retention now have explicit acceptance policies.
- **Corrected estimate terminology:** team calendar weeks are separated from person-effort, and combined QA/design effort is disclosed. No delivery guarantee is inferred from arithmetic alone.

## Failure cases that must remain visible

Part 1 deliberately stops on ambiguous uploads without a unique remote match, duplicate owned filenames, corrupt/missing trusted state, unavailable selected source articles and invalid configuration. These are diagnosable nonzero exits with retained state, not cases we can promise will recover without human action. Automatic source deletion/unpublishing is outside the stated new/updated requirement and remains a documented limitation.

The deployment assumes one writer per vector store. A local uploader and cloud uploader using different state directories are not protected by the same OS lock. Avoid that overlap or use a separate test store; a multi-writer distributed lease is outside this take-home implementation. Read-only queries can still be used during a scheduled run.

For Part 2, review the business acceptance section in the plan and [interview preparation](interview-prep.md). Those are proposed future system tests, not tests already run against a SCIO implementation. High-risk areas remain real-device playback, conversion time/security, storage/screen limits under races, timezone behavior and offline operation.

## Step 12 completion boundary

Requirement comparison, document handoff review, estimate arithmetic and interview preparation materials are complete. Live-product rehearsal, candidate acceptance of the assumptions/estimates and final combined submission checks remain open. Do not mark Step 12 fully complete or call the submission compliant until those remaining gates are resolved. No Part 2 code or custom Part 1 chat UI is required by this assignment.

## Subsequent local demo request

The user requested a runnable server/frontend and run instructions after this assignment review. The optional local FastAPI/static UI is now implemented and tested, with separate search and generation modes. It makes no new claim of assignment compliance: the provider-UI screenshot, real generated/refusal answer checks, exact chunk totals, live SCIO study and candidate rehearsal remain open. The daily deployment still runs the Docker ingestion job only. See [run guide](run.md), [API contract](api.md) and [live local UI evidence](evidence/local-web-check.json).

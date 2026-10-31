# Current assignment review

Updated 2026-10-31 against the user's pasted take-home text, linked Google Doc and supplied widget reference. The user authorized the local implementation, Gemini trial-key use and encrypted Gemini GitHub Actions setup. No billing changes or submission to the employer were made.

## Remaining submission gates

1. **Step 2: required provider UI screenshot.** Gemini now has 31 API-indexed documents, actual grounded YouTube/schedule answers and a verified unsupported-weather refusal. Both supported answers have five bullets and one correct support URL. However, the required Google AI Studio setup/YouTube screenshot is still missing. The genuine custom-widget screenshots do not replace it. Native computer-use startup failed with a sandbox helper error.
2. **Step 2: exact embedded chunks.** Completed file counts are known. Gemini white-space chunking is configured at 400 tokens/80 overlap, but exact embedded-chunk totals are not exposed in inspected store/document metadata. They remain null; file totals are not substituted.
3. **Live product study and Step 12 candidate ownership.** Brief A covers all four domains, folders/settings, physical-player acceptance, proposed failure policies, delivery order, rationale and estimate arithmetic. The user has not supplied live OptiBot/SCIO observations or candidate rehearsal. Independent handoff review is complete; candidate acceptance is separate.
4. **Naming, time and combined packaging.** User-selected `Optibot` avoids the company substring but is not cryptic. Actual hours are unknown. The README includes setup/run/log links and custom screenshots; final provider screenshot, candidate signoff and both-part submission remain open. No passing grade is guaranteed.

## Verified engineering

- Scraper: clean Markdown, preserved structural/media links and source URLs, stable seed plus new-article discovery, semantic hashes and representative source spot checks.
- Gemini: native Python API upload, active indexing, reused store, separate provider state, bounded operation polling, pending recovery, safe orphan reconciliation and replacement cleanup. Local unchanged rerun reports added=0 updated=0 skipped=31 failed=0. OpenAI identifiers/state remain isolated for rollback.
- Answering: exact prompt loading, known-corpus source mapping, actual supported answers and refusal. Gemini source lookup invokes a model and consumes quota even while generated answer text is hidden. No unlimited-free claim is made.
- Daily job: one-shot Docker `main.py`, trusted artifact persistence, OS/workflow locking, safe failure evidence and provider migration marker. A real scheduled OpenAI event41184533900 processed added1/updated2/skipped28 with no failure. Gemini cloud checks use separate artifacts.
- Widget: reference-style floating launcher, compact green-header panel, greeting, suggestions, composer, draft/focus preservation and responsive behavior. Actual Gemini answer/cited link passes browser checks with no page errors, no mobile overflow and no automated axe violations. No human support availability is simulated.

## Independent review and tests

BA approved requirement corrections and the proposed business handoff while withholding final submission approval. QA independently approved the Gemini implementation after reproducing/fixing invalid limits, source-lookup semantics, transport JSON failures and missing citation metadata. Latest suites: **53 Python tests and nine browser tests pass**; Windows/Linux, browser and Docker CI passed [run 41213997518](https://github.com/linhuachung/Optibot/actions/runs/41213125085). Dependency audit, compilation, installed dependency consistency, credential-pattern scan and whitespace checks pass. Automated accessibility checks are not a full manual certification.

Evidence: [Gemini YouTube](evidence/gemini-youtube-answer.json), [schedule](evidence/gemini-schedule-answer.json), [refusal](evidence/gemini-unsupported-answer.json), [index](evidence/gemini-index-status.json), [rerun](evidence/gemini-local-rerun.json), [actual widget](evidence/gemini-widget-check.json). See [checklist](../tasks/todo.md), [migration](gemini-migration.md), [historical BA/QA review](ba-qa-review.md), [live product guide](scio-product-observations.md) and [run guide](run.md).

Gemini cloud acceptance is now verified: runs [41213308045](https://github.com/linhuachung/Optibot/actions/runs/41213308045) and [41213474374](https://github.com/linhuachung/Optibot/actions/runs/41213474374) both pass with 31 skips, zero uploads/failures, zero pending work and identical Gemini-state digests. The second restores the first artifact, including its migration marker. Exact raw-store/document chunk telemetry is still unavailable; see [raw metadata evidence](evidence/gemini-store-metadata.json). The next Gemini-specific scheduled event remains unobserved, separate from already verified OpenAI cron execution.

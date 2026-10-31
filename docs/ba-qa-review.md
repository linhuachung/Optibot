# Independent BA and QA review loop

Reviewed 2026-10-30. Separate BA and QA agents independently reviewed the assignment, repository, checklist, implementation and evidence. The facilitator addressed actionable findings, then requested follow-up review. Scope is the current local demo, daily ingestion job and Brief A planning deliverable; no live SCIO behavior is invented.

## Round 1

**BA:** engineering coverage and all four Brief A domains are substantially present, but submission is incomplete. Required live answer/provider-UI/chunk evidence and product study remain open. Two claims needed correction: `Optibot` is not a cryptic repository name even though it lacks the prohibited company substring, and planned 8h/10h allocations do not establish actual hours spent.

**QA:** independently passed the 38-Python/seven-browser baseline but requested changes for two P2 defects. New replies after long conversations could appear mostly outside the visible chat area. Malformed valid-JSON state could incorrectly report ready or return HTTP 500. Closing during an in-flight request was investigated and did not reproduce a focus defect.

## Fixes and follow-up

- Added a browser regression reproducing hidden new replies, observed failure, then positioned each new reply's start in the conversation viewport.
- Added malformed-state regressions, observed failures, then added shared corpus validation for health and chat. Both return sanitized HTTP 503 `state_invalid` before provider initialization for invalid corpus shape/records/source URLs.
- Corrected naming claims and added an unresolved naming checkbox. The user-selected remote was not silently renamed. Actual time remains unknown pending candidate-reported hours; any overrun must be disclosed.
- BA round 2 approved those dispositions and found no additional business-scope gap.
- QA round 2 reproduced the scrolling defect when a response completed while the widget was closed. A second failing browser regression captured it; positioning is now deferred until reopening. Reopening without a new reply preserves the existing scroll position.

## Final verdict

**BA: approve the local implementation and corrected review claims.**

**QA: approve within the tested local-demo scope.** Independently verified **39 Python tests and nine browser tests**, all passing. No additional P0/P1 implementation defect or secret exposure was identified in the reviewed scope. The three reproduced scenarios have targeted regression coverage. Automated checks do not prove that every possible failure is absent.

**Final submission: not approved yet.** Remaining gates are funded live generated-answer/refusal checks, the required provider-UI screenshot, exact embedded-chunk reporting, actual OptiBot/SCIO use, candidate review/rehearsal, a cryptic-name decision and actual hours disclosure. The first automatic cron event remains an additional unobserved deployment-assurance check; authenticated manual cloud/container restoration and delta behavior have passed.

[Full assignment review](final-review.md), [checklist](../tasks/todo.md), [verification](verification.md), [latest prior cloud evidence](evidence/cloud-run-41076345213.json).

Final reviewed commit passed Windows/Linux tests, browser regressions and Docker build in [CI run 41083463882](https://github.com/linhuachung/Optibot/actions/runs/41083463882). [CI evidence](evidence/ba-qa-ci.json). The project-owned local server was reloaded with the validated API code; health reports ready with 30 indexed articles. Refresh the frontend to load the new response-positioning code.

## Migration follow-up - 2026-10-31

QA independently passes 52 Python/nine browser tests and approves the reviewed Gemini implementation after the new invalid-limit, source-lookup semantics, transport JSON and citation-metadata checks were corrected. A real 31-document upload/rerun and grounded answers are now observed. The former OpenAI generation failure and pending automatic cron statements are historical; actual scheduled OpenAI event41184533900 passed with added1/updated2/skipped28. Provider UI/chunk/live-product/candidate/naming/hours requirements still remain open. [Current verification](verification.md).

Gemini cloud acceptance is now verified: runs [41213308045](https://github.com/linhuachung/Optibot/actions/runs/41213308045) and [41213474374](https://github.com/linhuachung/Optibot/actions/runs/41213474374) both pass with 31 skips, zero uploads/failures, zero pending work and identical Gemini-state digests. The second restores the first artifact, including its migration marker. Exact raw-store/document chunk telemetry is still unavailable; see [raw metadata evidence](evidence/gemini-store-metadata.json). The next Gemini-specific scheduled event remains unobserved, separate from already verified OpenAI cron execution.

Final targeted QA follow-up independently passes all 53 Python tests and approves the API_KEY alias/Docker-default delta. Final [CI run 41213997518](https://github.com/linhuachung/Optibot/actions/runs/41213997518) passed Windows/Linux, browser regressions and Docker build. Fresh Python/npm audits report no known vulnerabilities. [Final CI evidence](evidence/gemini-final-ci.json).

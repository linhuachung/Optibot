# Assignment and reference-widget review

Reviewed 2026-10-30 against the user's newly pasted take-home text, the previously retrieved Google Doc and the supplied visual reference. Assignment requirements are assessment criteria; they do not authorize spending, creating accounts or submitting work. The user separately requested implementation of the local widget.

## Findings that still prevent calling the submission complete

1. **Step 2: provider UI and actual generated answers.** Thirty files are API-indexed and actual retrieval succeeds, but the required provider-UI YouTube answer screenshot is missing. A custom-widget retrieval screenshot is not equivalent. Generated-answer checks last failed because the API project had exhausted credits. Prompt instructions and mocked tests do not prove live factual correctness, refusal behavior or the five-bullet/three-URL limits. Those remain live acceptance checks.
2. **Step 2: exact embedded chunks.** File totals are known; managed metadata does not expose an exact embedded-chunk total in the inspected API. It is reported as unavailable, not substituted with file counts. Resolve the telemetry expectation before claiming compliance.
3. **Step 12 and Part 2: live product evidence and candidate ownership.** Brief A is stated at the top and all four domains are covered in the proposal, with ordered milestones, assumptions, estimates and rationale. The user has not explored SCIO. Current-product observations and a candidate rehearsal are still required; proposed replacement/scheduling/offline policies must not be presented as observed SCIO behavior.
4. **Combined submission.** README is concise and includes setup, local run and real cloud logs, but the required provider-answer screenshot is still absent. First automatic cron execution is separately unobserved; manually triggered cloud persistence/delta checks have passed. Both parts should be submitted together with actual cuts and time spent disclosed. No passing grade is guaranteed by these checks.

## Verified implementation

- Scraping and Markdown: at least 30 stable articles, source URLs, preserved structure/media links, semantic hashes and representative live spot checks.
- Python vector ingestion: API upload, reused store, completed indexing, persisted remote IDs and delta/recovery behavior. Responses/file search replaces the retired Assistants path; evaluator acceptance of current provider-UI terminology remains an external question.
- Daily job: one-shot Docker `main.py`, key aliases, daily GitHub Actions schedule, trusted state restoration, visible logs and 30 unchanged skips in a fresh authenticated cloud run.
- Repository: user-selected `Optibot` avoids the prohibited company string but is not cryptic and directly names the mini-clone. Naming compliance is unresolved. `.env.sample` and ignore rules are present; secrets are server-side and excluded from client code/state evidence.
- Local UI: floating round launcher, compact panel, green header, greeting, suggested questions, message composer and explicit search/answer modes. It now follows the reference's interaction pattern; it is not a pixel-perfect copy or a claim of live human support.
- Part 2: planning document only. No Assets/Playlists/Schedules/Screens application is required by the assignment. The proposed eight-week implementation estimate is separate from the ten-hour planning allowance.

## Verification and limits

The latest full local suite passes: 39 Python tests and nine browser tests. Browser tests cover safe text rendering, source links, loading/duplicate-send prevention, empty/error states, keyboard operation, launcher/draft/focus behavior, narrow/short viewport fit and automated WCAG A/AA checks. Actual widget retrieval returns the YouTube guide first with three sources, no page JavaScript errors and no mobile horizontal overflow. Desktop and mobile screenshots were visually inspected. Automated accessibility checks are not a complete manual accessibility audit.

Evidence: [local widget check](evidence/local-web-check.json), [desktop](evidence/local-chat-search.png), [mobile](evidence/local-chat-mobile.png), [last verified cloud run](evidence/cloud-run-41076345213.json). See [checklist](../tasks/todo.md), [full requirement review](requirements-review.md), [product study guide](scio-product-observations.md) and [run instructions](run.md).

The widget revision also passed Windows/Linux checks, Docker build and browser CI in [run 41080979208](https://github.com/linhuachung/Optibot/actions/runs/41080979208). [CI evidence](evidence/widget-ci.json).

## Independent BA/QA round 1 and corrections

BA confirmed all four Brief A domains and proposed failure policies are covered, but flagged repository naming and actual-hours evidence. The name `Optibot` is user-selected and not cryptic; its absence of the company substring is insufficient to claim full compliance. Remote renaming is not performed because existing repository/deployment links depend on it. Actual Part 1 and Part 2 time spent is **unknown** until reported by the candidate; planned allocations do not prove compliance with the approximately 18-hour limit. Disclose actual cuts and any overrun honestly.

QA independently passed 38 Python/seven browser baseline tests and reproduced two P2 defects: new replies could be mostly below the visible chat area, and malformed valid-JSON corpus state could report ready or return HTTP 500. Both were reproduced in failing regressions, then fixed. New replies bring their start into the chat viewport; health and chat share corpus-shape validation and return sanitized `state_invalid` HTTP 503 before provider initialization. The full local suites now pass **39 Python and eight browser tests**. Closing during an in-flight request was investigated and did not reproduce a focus failure.

External evidence gates remain open. The first automatic cron observation is supplementary deployment assurance; it is distinct from the assignment's explicitly required screenshot, chunk log and product-learning evidence.

## Independent final verdicts

BA round 2 approves the local implementation and corrected requirements claims, while withholding submission approval. QA's final follow-up independently passes 39 Python and nine browser tests and approves the tested local-demo scope. QA round 2 extended the scrolling defect to replies arriving while closed; a second failing regression reproduced it, and deferred positioning on reopen fixed it. All three reproduced scenarios now have regression coverage. No additional P0/P1 defect or secret exposure was identified in the reviewed scope; this is not a guarantee that all failures are impossible.

The review loop is closed for actionable implementation findings. Provider/product evidence, cryptic repository naming and actual hours remain explicit external/candidate gates. See [BA/QA review record](ba-qa-review.md).

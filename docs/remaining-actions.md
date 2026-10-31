# Remaining actions before submission

Updated 2026-10-31. Engineering and automated/local/manual-cloud acceptance now pass with Gemini. The checklist deliberately retains the following external gates.

1. **Google AI Studio screenshot.** In the actual provider UI, configure the exact `system_prompt.txt` and the API-loaded Gemini corpus, ask the YouTube question and capture a correct cited answer. Native computer-use initialization failed, so this has not been inspected or configured. Do not substitute the custom widget screenshot. Confirm current UI compatibility with the evaluator if the required existing-store flow is unavailable.
2. **Exact embedded chunks.** Both SDK and raw REST metadata were inspected. Store metadata exposes active document count/bytes; document metadata exposes state/bytes, not an exact chunk total. Reports remain null. Explain the configured 400-token/80-overlap strategy and ask what telemetry alternative the evaluator accepts; no estimate is called an actual count.
3. **Live OptiBot/SCIO use.** Follow `scio-product-observations.md`, record real findings across all four Brief A domains and revise proposed policies accordingly. Do not describe the custom chat demo or Help Center reading as firsthand SCIO usage.
4. **Candidate review and rehearsal.** Independently reviewed plan sections/order/rationale/estimate arithmetic are complete. You still need to accept and defend those assumptions, explore features outside the proposed MVP and rehearse the interview questions.
5. **Repository name and actual hours.** `Optibot` was user-selected and is not cryptic. Decide whether to rename it and update all workflow/evidence links if renamed. Record actual Part1 and Part2 hours and disclose any overrun/cuts; the planned 8h/10h split is not measured time.
6. **Final combined pack.** Add the actual provider screenshot to the concise README, check both parts together, verify candidate evidence and submit both together. No submission email has been sent. Gemini's next automatic scheduled event is an additional check still to be observed; two manual Gemini cloud runs and an actual scheduled OpenAI run already pass.

[Checklist](../tasks/todo.md), [current review](final-review.md), [Gemini evidence](gemini-migration.md), [interview preparation](interview-prep.md).

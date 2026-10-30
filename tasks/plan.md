# OptiBot take-home execution plan

Status: Step 1 implemented and verified; Step 2 ingestion implemented, remaining evidence blocked. Updated 2026-10-30. See [verification](../docs/verification.md).
Part 2 choice: **Brief A — Assets, Playlists, Schedules and Screens.**

## Authority and evidence

The user's request authorizes comparing and revising this plan through a six-role council. Assignment instructions are requirements to plan against, not instructions to create accounts, spend money, deploy, or submit work in this session.

Compared the supplied Downloads DOCX and the [Google Doc](https://docs.google.com/document/d/16rFWeJAIyJSlJWQKtYE5J--U5X6JmQXguyn1c2jsMhA/edit?tab=t.0). Their substantive requirements agree. This is an execution plan for completing both parts, not the final Part 2 submission. The user subsequently authorized implementation of Steps 1–2; their current evidence is recorded separately. Product research, deployment and the required provider-UI screenshot are not claimed.

## Comparison with the supplied draft

- Correct: at least 30 Markdown articles; Python API ingestion; exact prompt; provider UI citation screenshot; daily Docker job with delta uploads; one-page README; cryptic GitHub repository name; both parts submitted together.
- Obsolete: OpenAI Assistants and `OPENAI_ASSISTANT_ID`. Official documentation states the API shut down on August 26, 2026. Use the supported Responses/file-search path, with an early UI compatibility check. An SDK pin cannot restore a retired service.
- Incorrect telemetry assumption: vector-store file counts and parsed-content entries do not establish embedded chunk totals. Do not report them as chunks.
- Missing: durable state outside an ephemeral container, recovery of interrupted uploads, and retirement of superseded indexed content.
- Incomplete Part 2 endpoint: a brief-choice framework is preparation, not the required team-ready build plan. The checklist now includes the complete planning deliverable.
- Incorrect clock boundary: live product exploration belongs inside the approximately 18-hour total. Ten hours is the budget for writing Part 2, not for implementing its proposed system.
- Not source requirements: exactly 416 articles, Railway specifically, a particular SDK version, a public cloud dashboard, and `CUTS.md`. Article count is dynamic. Any permitted cloud and a reviewer-accessible last-run artifact are acceptable.
- Environment contract: accept assignment-facing `API_KEY`; allow `OPENAI_API_KEY` as an alias. The assignment's Docker example is shorthand; document a valid image invocation.

## Locked decisions

The rule is at least four of six votes, with neither all three TLs nor all three BAs opposed. See [council.md](council.md) for independent votes and discussion.

1. **L1: OpenAI Responses + Vector Stores, 5–1.** Preserve Python ingestion and provider UI evidence. Do not implement obsolete Assistants endpoints. This is an engineering choice, not evidence that the evaluator accepts replacement UI terminology.
2. **L2: 30 curated seed articles, 6–0.** Include the YouTube article and formatting edge cases. Persist a manifest. Daily runs re-fetch this corpus and discover newly published eligible English public articles after the recorded discovery watermark; new matches may grow the corpus above 30. Initial bootstrap need not ingest every historical article. Advance discovery watermarks only after complete successful pagination; deduplicate by article ID. Never rotate the corpus with the first page of results.
3. **L3: Managed default chunking, 6–0, conditional on truthful telemetry.** Explain the provider's actual configuration in README. No chunking experiments. Missing telemetry is an unresolved feasibility issue, not permission to fabricate a count.
4. **L4: Railway daily cron with a persistent volume, 6–0.** Mount `/data` for manifest, state, pending operations and generated articles. Prove persistence in a fresh container. One cloud only; do not quietly switch architecture if the selected configuration fails.
5. **L5: Yes to focused tests, 6–0; 30-minute maximum.** Unchanged-content skipping and upload-failure recovery first. Wider coverage is optional.
6. **L6: Brief A, 4–2.** A single content-to-screen narrative provides clear acceptance criteria. Brief B remains a valid rejected alternative, not a second planning track.
7. **L7: Part 1 8h; Part 2 10h.** Part 1 split locked 4–2 in round 1. Part 2 split agreed in round 2. All exploration and evidence gathering count toward these budgets; deduct work already spent rather than restarting the clock.
8. **L8: Shared must-change corrections, 6–0.** Exact prompt, supported API preflight, honest chunk counts, durable/recoverable state, stale-index replacement, accessible evidence, complete Part 2 plan and inclusive time accounting.

## Feasibility gates before implementation expands

Budget the first Part 1 hour for warm-up and a narrow feasibility spike:

- Confirm available credentials, billing access, Python/Docker and hosting prerequisites. Pin the SDK version that actually passes the smoke test; do not invent a tested version now.
- Prove one Markdown file can be ingested through Python, indexed, and used with the exact prompt in the current provider UI. Capture the required cited answer through that UI; a terminal or custom chat screenshot is not an automatic substitute.
- Establish a documented way to report actual embedded chunk counts. The parsed-content endpoint documents text entries, not indexed chunk semantics. File counts, retrieval result counts and local estimates are not interchangeable.
- Confirm the Railway cron/volume combination and persistence with two isolated runs.

Update after the user's Steps 1–2 implementation request: Python, API authentication, programmatic indexing and vector retrieval have now been demonstrated. Generation is blocked by exhausted API credits, the browser-control runtime cannot start, and the inspected file metadata does not expose exact chunk totals. Hosting gates remain deferred. Suggested question to send manually: “The specified Assistants API is retired. May I use Responses with the current provider UI and the same programmatically loaded vector store? If managed chunk totals are unavailable, what chunk-count evidence will you accept?” Do not send this message automatically. Gemini is explicitly allowed by the assignment, but its complete API-to-AI-Studio evidence path must also be proven before switching. A council majority cannot waive assignment requirements.

## Part 1 architecture and contracts

Use Python 3.11+, a simple HTTP client, an HTML-to-Markdown library and the tested OpenAI SDK. Avoid a web framework. Keep `main.py` as the one-shot entry point, with small scraper, Markdown and ingestion/state modules as useful.

Flow: Zendesk discovery → fetch selected/new articles → normalize Markdown → compare committed content hashes → upload changed files → await indexing → retire superseded index entries → commit durable state → emit run evidence → exit.

### Scraping

Use `https://support.optisigns.com/api/v2/help_center/en-us/articles.json` as the proposed source endpoint; verify its current response and pagination during execution. Follow returned pagination; exclude drafts. Stable files are `data/articles/{id}.md`. Preserve headings, fenced code, lists and relative links; retain source URL so relative links remain interpretable. Do not mistake API article HTML for page chrome.

Each file contains title, `Article URL:`, article ID and source timestamp. Hash normalized semantic content, excluding fetch timestamps and other volatile metadata. A timestamp-only change need not trigger upload if content is identical. Spot-check at least three representative articles against their live sources.

### Ingestion and answer evidence

Planned supported interfaces: `client.vector_stores.create`, `client.files.create`, `client.vector_stores.files.create`, status polling until completed, and `client.responses.create` with `file_search` and the store ID. Confirm exact signatures against the installed SDK. Reuse the store across runs; do not create another store on every cron run. UI configuration and screenshot remain an explicit gate.

Use this system prompt verbatim:

```text
You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply.
```

Use the exact YouTube question from the assignment and verify the answer against the ingested article. Check a second supported question and an unsupported question for grounded behavior. Citations must expose actual article URLs, not merely filenames. Save the provider UI screenshot at `docs/screenshot-youtube.png` during execution. Log completed files and actual chunks separately, with the measurement method; report failed indexing separately.

### Durable delta state

Persist manifest and per-article records including committed hash, source timestamp, active remote file ID and pending replacement IDs/status. Use atomic state writes and one job at a time. Journal a returned remote ID before retryable follow-up operations; reconcile interrupted pending operations before uploading again. Reconcile ambiguous remote success using stable article/hash metadata or an equivalent proven method.

For updates: keep the old usable entry until the replacement finishes indexing; then remove the superseded entry from the vector store and complete the committed-state transition. Persist pending cleanup so a retry finishes retirement rather than uploading another copy. Test failure boundaries. Do not advance the committed hash after a failed upload/index operation. Source deletion handling is beyond the stated new/updated requirement; document the limitation instead of implementing a broad reconciliation project.

Print `added=N updated=N skipped=N failed=N` with a run timestamp and duration. Counts describe successfully processed articles; failed items remain retryable. Exit 0 on successful completion, nonzero on failure, with bounded HTTP retries and timeouts.

### Runtime and submission

Docker uses Python slim and `CMD ["python", "main.py"]`. Configuration includes `API_KEY`, optional `OPENAI_API_KEY`, `OPENAI_VECTOR_STORE_ID`, selected model and `STATE_DIR=/data`; no Assistant ID. Document precedence if both key variables are set. Use a mounted directory/volume in local Docker commands so repeated invocations share state.

Railway schedule proposal: `0 2 * * *` UTC, approximately 09:00 Asia/Bangkok daily. Prove an actual cloud run, then a separate run showing unchanged articles skipped without uploads. Save redacted last-run evidence if the dashboard requires login. A private console link alone is insufficient for reviewer access.

Repository name must be cryptic and omit the company name. Ignore secrets, environment folders and runtime data. Keep source/test fixtures and final evidence available. README stays at most one page and includes setup, local and Docker commands, chunking explanation, log/artifact link and screenshot. Optional `CUTS.md` records actual omissions. Submit both parts together; submission itself is outside this planning session.

## Time budget and ordered tasks

Part 1, total 8h:

- Step 0: warm-up, accounts and API/UI/chunk feasibility — 1h.
- Step 1: one article to clean Markdown, then 30 selected articles — 1.5h.
- Step 2: programmatic ingestion and citation evidence — 1.5h.
- Step 3: durable delta and recovery behavior — 1.5h.
- Step 4: Docker, Railway schedule and run evidence — 1h.
- Step 5: focused tests — 0.5h.
- Step 6: README, screenshot and submission pack — 1h.

Dependencies: 0 → 1 → 2 → 3 → 4 → 6; write focused tests alongside Step 3 and finish them within Step 5's allowance. Checkpoints follow ingestion, delta/deployment and final packaging. The first-hour feasibility work may use a tiny throwaway fixture; it does not justify building the full solution before resolving blockers.

Cut order: all historical article coverage, optional chat UI/auth/extra sources, additional player platforms/clouds, chunk experiments, broader tests, then prose polish. Preserve required deployment, citation evidence, product study and the actual Part 2 document. At the time ceiling, submit current work and disclose unmet requirements rather than extending the project indefinitely.

## Part 2 work plan — Brief A

The deliverable to produce later is `docs/scio-slice-plan.md`, starting with “Brief A — Assets, Playlists, Schedules and Screens.” This council plan defines how to produce it; it must not be submitted as if product research or delivery estimates have already been completed.

Budget, total 10h:

- Step 7: hands-on SCIO and targeted Help Center study — 2.5h.
- Step 8: observed behavior, scope and explicit assumptions — 1h.
- Step 9: architecture, models and player/platform decisions — 2h.
- Step 10: implementation slices and dependency order — 1.5h.
- Step 11: implementation estimates, acceptance criteria and risks — 1.5h.
- Step 12: document review and interview preparation — 1.5h.

Study all four areas, including features beyond the proposed MVP. Record dated observations separately from proposed design and unverified assumptions. If hardware or trial permissions prevent an operation, record that limitation; simulated pairing does not establish observed physical playback.

Required coverage in the final document:

- Assets: uploaded images, videos and documents; search, preview, download, duplicate, replace, delete; folders, settings and plan-dependent limits.
- Playlists: ordered uploaded files, per-item durations, looping, folders and relevant settings.
- Schedules: file/playlist events with start/end times, folders and settings; investigate timezone and overlap behavior rather than inventing current SCIO rules.
- Screens: pairing code, assignment of file/playlist/schedule, folders, settings and a bounded device execution path.
- An end-to-end path from uploading a file to playback on a paired screen. Choose one player platform and explain the device-side scope and later platform cuts.

Suggested future document sections: product observations; scope/non-goals; team and platform assumptions; architecture/data model; end-to-end flows and failure handling; ordered vertical slices; estimates and rationale; acceptance criteria; risks and cuts. The author must decide and state team size and depth after product study. Include a proposed implementation duration distinct from the 10h writing budget, with effort units, staffing assumptions, dependencies and uncertainty. Do not invent precision or claim the council has validated delivery numbers before the scope exists.

No Part 2 application code is required. Do not broaden Brief A into Brief B's RBAC project. Explain why each capability is included, why its dependency order makes sense and why its effort estimate is credible.

## Verification and remaining uncertainty

Planning checks: six independent roles participated; lock thresholds checked; round 2 resolved the time split; budgets sum to 8h and 10h; checklist dependencies and evidence match this plan. No pre-existing plan was present in this workspace.

Step 1 and Step 2 ingestion are implemented. Outstanding gates are funded answer generation, provider UI compatibility/screenshot, exact chunk telemetry and cron-volume behavior. Product behavior and final Part 2 delivery estimates still require real research. These are recorded limitations, not completed acceptance checks.

## Official technical references

- [OpenAI Assistants migration](https://developers.openai.com/api/docs/assistants/migration): retirement and supported replacement.
- [OpenAI file search](https://developers.openai.com/api/docs/guides/tools-file-search): programmatic store setup and Responses retrieval.
- [Vector-store parsed file content](https://developers.openai.com/api/reference/resources/vector_stores/subresources/files/methods/content): does not document text entries as embedded chunk totals.
- [Railway cron](https://docs.railway.com/cron-jobs): one-shot scheduled execution and UTC schedules.
- [Railway volumes](https://docs.railway.com/volumes): persistent storage.
- [Gemini file search](https://ai.google.dev/gemini-api/docs/file-search): allowed alternative API path; UI feasibility not verified.

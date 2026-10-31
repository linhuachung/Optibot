# Step 12 interview preparation

Use this alongside the Brief A proposal and the live observation record. These are discussion prompts and proposed rationales, not a claim that the candidate has rehearsed or observed every behavior.

## Explain the product before the architecture

1. **What does your slice let a customer do?** Upload a supported file, organize it, create an ordered playlist, choose when it plays and assign it to a paired physical screen. Explain one concrete customer example across all four domains.
2. **What did you actually try in SCIO?** Currently the truthful answer is that live exploration is unfinished. Complete the trial walkthrough and replace this gap with specific actions/results. Do not present Help Center research as personal experience.
3. **What belongs to Brief A?** Uploaded files, playlists, schedules and screens, including folders/settings. Apps, feeds, complex layouts, custom roles and approval workflows are not required in this selected slice.
4. **Which product behaviors differ from your proposal?** Check replacement, deletion, folder handling, durations, scheduling precedence and device settings in the trial. Explain a deliberate design difference and its tradeoff instead of asserting the proposal exactly clones SCIO.

## Defend the scope and estimates

5. **Why one Linux player?** It makes actual screen-side delivery testable while bounding platform-specific work. It is not a reason to stop at a portal preview or omit pairing/offline behavior.
6. **Why start with an image all the way to a screen?** It validates identity, storage, pairing, assignment, network delivery and playback early. Player/format assumptions can otherwise invalidate editor work built first.
7. **Why eight weeks?** Seven milestone estimates total 48 engineering-days. Add 12 risk days. Two engineers contribute eight planned days/week after a 20% coordination/support allowance: 60/8 = 7.5 weeks, rounded to eight. QA has 16 separate days and design four; total effort across roles is 80 person-days. Know which assumptions make the estimate grow or shrink.
8. **Is the 20% capacity allowance the same as contingency?** No: the allowance covers expected routine coordination/support; contingency addresses uncertain integration/conversion/player work. Validate both during the first milestone rather than treating them as universal percentages.
9. **What do you cut if time runs short?** Extra player platforms, native drive connectors, playlist nesting/transitions, richer recurrence and broad format conversion. Preserve the four selected domains and a real file-to-screen path. Admit and re-estimate any cut that changes a promised acceptance outcome.

## Walk through the business failure cases

10. **An upload finishes twice or two uploads exceed quota together:** completion must be idempotent; reserve/reconcile capacity transactionally and enforce actual received bytes.
11. **A document fails conversion:** show a failed state and retry/remove action; it must not become a ready publication dependency or displace valid playback.
12. **A file is replaced while already on screens:** preserve logical identity and publish a ready immutable version. Failed validation or download retains the previous allowed version. Confirm actual SCIO propagation separately.
13. **A duplicate asset shares a storage blob:** its metadata is independent; deletion/replacement of one copy cannot destroy another copy's content. Garbage collection must respect all live references and retained manifests.
14. **Two editors save concurrently:** detect a revision conflict; publish a coherent revision and provide refresh/reapply behavior rather than silently mixing edits.
15. **Events overlap or cross midnight/DST:** state proposed precedence, interval boundaries, timezone and fallback. Show fixtures at the boundary instants. Identify which rules came from the trial and which are your product choices.
16. **A stale download finishes after a newer assignment:** reject an older publication revision. A successful download is not the same as applied or playing content; explain acknowledgement and progress reporting.
17. **A screen is offline when unpaired:** revoke future access immediately on the server, but do not promise remote erasure of offline cached bytes. Explain expiry, next-connect behavior and local reset responsibilities.
18. **A device cannot download new content:** refresh expired authorized URLs, retry boundedly, keep a complete permitted manifest/fallback, and expose a meaningful screen error. Do not ignore explicit content expiry.

## Explain Part 1 honestly

- Know the difference between Markdown files, provider Files, vector-store attachments, chunks, retrieval results and generated answers. None of their counts are automatically interchangeable.
- Explain hashes, pending operations, atomic state writes, old-index retirement, the GitHub artifact/OS locks and the orphan-file recovery fix. Describe a failed run and how its next run behaves.
- Show the real cloud logs and repeated-run skips. Say that daily cron is configured but the first automatic trigger is not yet observed; do not describe a manual dispatch as a scheduled execution.
- State the remaining screenshot, generated-answer and chunk-count gaps. The exact prompt is in source, but prompt presence does not establish live answer correctness.

## Candidate rehearsal checklist

- [ ] Complete the live observation record and distinguish observation from proposal in every answer.
- [ ] Explain each milestone and number without reading an AI-generated paragraph verbatim.
- [ ] Walk a supported image, video and document through the proposed system, including a failure at each boundary.
- [ ] Defend the platform/format/recurrence cuts and explain how the plan changes when those assumptions change.
- [ ] Open the final repository, screenshot, job logs and Part 2 document using the links intended for the reviewer.

## Optional evaluator clarification draft

Send manually only if needed; this review does not send email:

“The assignment names the retired OpenAI Assistants workflow. Is Responses with the current provider UI and the same API-loaded vector store acceptable? Managed vector-store metadata does not expose an exact embedded-chunk total; what chunk-count evidence would you accept?”

If no answer is available before the time budget expires, disclose the exact unmet requirements and actual cuts instead of representing them as accepted exceptions.

## Current provider/deployment update - 2026-10-31

Explain the current Gemini native File Search path, separate provider state and generation-backed source lookup (which uses quota). Actual YouTube/schedule answers and weather refusal are verified; only provider UI/chunk evidence remains open in Step2. A real scheduled OpenAI run was observed on October31 (added1/updated2/skipped28), superseding earlier pending-cron notes. Preserve historical OpenAI recovery evidence, and distinguish it from subsequent Gemini cloud runs. Candidate trial observations, actual hours and rehearsal must still come from you.

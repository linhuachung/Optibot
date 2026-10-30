# Six-role council decision record

Date: 2026-10-30. Six distinct reviewer agents; independent round 1, no file writes by reviewers. Due to four concurrent slots, reviews ran in batches. Round 2 supplied every reviewer a summary of the other five votes. Facilitator wrote the final files after decisions locked.

Rule: at least 4 of 6 agree; neither all TLs nor all BAs may oppose. Round 3 and human escalation are required only for decisions still unlocked after discussion. Technical feasibility is separate from vote consensus.

## Round 1 independent positions

- **TL1, backend/infra:** L1 OpenAI supported API; L2 30; L3 managed default; L4 Railway durable volume; L5 yes/30min; L6 B. Main concerns: durable state, recovery, stale-index retirement and real job evidence.
- **TL2, AI/RAG:** L1 OpenAI Responses; L2 30; L3 managed default with honest telemetry gate; L4 Railway durable volume; L5 yes/30min; L6 A. Main concerns: current provider UI and actual embedded chunks cannot be inferred from file counts.
- **TL3, staff engineering:** L1 Gemini; L2 30; L3 managed default; L4 Railway durable volume; L5 yes/30min; L6 A. Gemini avoids retired Assistants, but its complete AI Studio evidence path is also unverified. Test the platform path early and pin only a proven SDK.
- **BA1, requirements:** L1 OpenAI Responses; L2 30; L3 managed default; L4 Railway durable volume; L5 yes/30min; L6 A. Requires exact prompt, API_KEY compatibility, accessible evidence and a complete Part 2 handoff plan.
- **BA2, scope/time:** L1 OpenAI Responses; L2 30; L3 managed default; L4 Railway durable volume; L5 yes/30min; L6 B. B reduces device-playback uncertainty. Preserve live product learning and all mandatory evidence inside the budget.
- **BA3, product/interview:** L1 OpenAI Responses; L2 30; L3 managed default; L4 Railway durable volume; L5 yes/30min; L6 A. A supplies a coherent customer story, but product research and explicit player cuts are essential.

All reviewers conditioned the API/UI path and managed chunking on demonstrated compliance. All supported the shared L8 corrections recorded in the plan. No reviewer claimed product use, current UI access, chunk telemetry or cloud deployment had been demonstrated.

## Round 1 tally and rationale

- L1 OpenAI 5, Gemini 1. Locked; neither group unanimously opposed. Use a supported API, not retired Assistants. UI compliance remains unproven.
- L2 30 seed articles 6, all historical articles 0. Locked. Ensure stable selection, YouTube coverage and documented new-article discovery.
- L3 managed default 6, custom 0. Locked conditionally; honest actual-chunk reporting is unresolved execution feasibility.
- L4 Railway with durable volume 6. Locked subject to a fresh-container persistence check.
- L5 focused tests/30min 6. Locked; broad coverage remains optional.
- L6 A 4 (TL2, TL3, BA1, BA3), B 2 (TL1, BA2). Locked. Both role groups contain A votes. Prefer an end-to-end content narrative; control playback risk through explicit player depth.
- L7 Part 1 schedule 4 for 1/1.5/1.5/1.5/1/0.5/1 hours (TL2, TL3, BA2, BA3); 2 for 0.75/1.5/1.5/1.5/1.5/0.5/0.75 (TL1, BA1). Locked 4–2.
- L7 Part 2 schedule unlocked: TL2/TL3/BA3 favored 2/1/2/2/2/1; TL1/BA1 favored 2.5/1/2/2/1/1.5; BA2 favored 2.5/1/2/1.5/1.5/1.5. Values mean study/scope/architecture/sequence/estimates-and-acceptance/review, each totaling 10h.
- L8 shared corrections 6. Locked. Exact prompt; supported API preflight; truthful chunk reporting; durable recoverable delta; stale-content replacement; assignment-facing key; actual complete Part 2 document; product research inside the clock; reviewer-accessible evidence.

## Round 2 — only unresolved Part 2 schedule

Facilitator proposed BA2's split: 2.5h study, 1h scope, 2h architecture, 1.5h sequencing, 1.5h estimates/acceptance/risks, 1.5h review.

- TL1 conceded: preserves live study and gives estimates explicit attention. Also accepted the majority Part 1 split and Brief A.
- TL2 conceded: extra study and interview defense fit the source; bounded sequencing remains workable.
- TL3 conceded: stronger evidence and review justify shorter sequencing/estimation allocations.
- BA1 conceded: preserves study while allocating explicit time for estimate rationale.
- BA2 held/approved the compromise for council-selected Brief A despite originally preferring B.
- BA3 conceded: better fits interview expectations if tasks keep dependencies, estimates and rationale.

Final Part 2 schedule: **6–0**. No third round required; no unresolved voting decisions. Remaining uncertainties are empirical feasibility checks, not dissent to be erased by another vote.

## Closure

The final deliverables are [plan.md](plan.md) and [todo.md](todo.md). Implementation is unstarted. The choice is Brief A; the final SCIO submission plan still requires real product study and defensible implementation estimates. UI compatibility and actual chunk telemetry may require an evaluator clarification if the preflight cannot demonstrate them. No clarification was sent automatically.

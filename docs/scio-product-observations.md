# SCIO product observation record

Status updated 2026-10-31: the user created a trial and supplied a dashboard screenshot. This confirms dashboard access, not completion of the functional study. Native computer-use initialization fails; an isolated browser fallback reaches SCIO sign-in and is awaiting the user's own authentication. Help Center research is still separate from firsthand product observations.

Record the date, trial plan, portal version/interface and device/platform used. For each item below, record the exact action, observed outcome, evidence location and any limit that prevented the check. Redact account details and pairing codes from shared evidence.

- [ ] Assets: upload an image, video and document; inspect search, preview, download, duplicate, replacement, deletion, folders and settings. Record size/storage limits visible in the trial.
- [ ] References: place a file in content already assigned to a screen, replace it and observe propagation. Try deleting a referenced file and record the actual warning/outcome.
- [ ] Playlists: create, reorder, change durations, preview and assign; inspect folders/settings, nesting and item scheduling even if excluded from the proposed first release.
- [ ] Schedules: create file and playlist events, recurrence, overlaps and fallback; inspect timezone and live/expiry controls. Record the actual winning event rather than assuming the proposed policy matches SCIO.
- [ ] Screens: pair a real test player if possible; assign an asset, playlist and schedule; inspect folders, orientation, timezone, online status and unpairing. If simulated or unavailable, say so.
- [ ] End to end: upload → playlist → schedule → paired-screen playback. Record failures, confusing steps and elapsed propagation time.

Before final submission, turn these notes into concrete observations in `scio-slice-plan.md`, revise proposed choices where necessary and rehearse questions about features beyond the planned MVP.

## Guided trial session

Reserve the planned 2.5-hour study block, including note-taking. Open [the product](https://app.optisigns.com/) and sign up or sign in to a free trial yourself. Do not share your password or payment information in chat.

1. Record the date, trial plan and visible interface version. Ask the in-product OptiBot the YouTube question and one unsupported question; note tone and citations for Part 1's warm-up.
2. In Files/Assets, upload a small nonsensitive image, video and document. Try search, preview, download, duplicate and folders. Inspect settings and the limits actually visible to your trial.
3. Create a playlist from the uploaded files, reorder it and change durations. Inspect document-page behavior, playback settings, folders and available advanced options.
4. Create a schedule containing a file and a playlist. Try one-off and recurring events, overlapping intervals, default/fallback content and timezone-related controls. Record what the UI actually permits and explains.
5. Install or use an available test player if practical, pair it using the displayed code, then assign an asset, playlist and schedule. Observe actual playback. If there is no player/device, record that limitation rather than describing a simulation as real playback.
6. Replace an asset referenced by a playlist/screen and observe whether and when playback changes. Inspect the warning/outcome when deleting a referenced asset. Try relevant screen settings and inspect unpairing without disrupting a device you rely on.
7. Write a few factual notes for each domain: action taken, result, unexpected behavior and evidence location. Include what you could not test. Then compare those notes with the proposal's replacement, deletion, schedule and player policies.

The final plan should incorporate your actual findings and revise its assumptions. A checkbox or Help Center summary alone is not evidence that the live workflow was tested.

## Session preparation and observed prerequisites - 2026-10-31

Evidence source: user-provided dashboard screenshot in this conversation. It shows a 14-day trial banner, Screens selected, navigation to Files/Assets, Playlists and Schedules, Add Screen and New Folder controls, and first-screen onboarding. These are visible UI facts only. The onboarding instructs installing a player and pairing with its code; actual pairing/playback has not been observed.

Direct browser observation: the isolated study browser reaches the real SCIO sign-in and registration pages. Registration offers Continue with Google, Continue with Microsoft and Continue with email. User authentication is performed by the user, not by storing passwords or reading browser credentials. No study asset has been uploaded and no existing account content modified yet.

Prepared nonsensitive local fixtures in the ignored `.runtime/scio-study-assets/` directory:

- `study-image-blue.png`: 640x360 blue image.
- `study-image-replacement-orange.png`: same-size orange replacement for visual propagation checks.
- `study-video-3s.mp4`: original three-second H.264 video generated in an independent test browser.
- `study-document-two-pages.pdf`: original two-page document, for preview/page-duration checks.
- `fixture-manifest.json`: sizes and hashes for traceability.

Planned study resources will use a dedicated Takehome Study folder and names so replacement/deletion checks target only newly created test content. No live customer screen will be reassigned or unpaired as part of this study. Actual results must be filled after the corresponding UI actions occur; fixtures and onboarding screenshots alone do not complete Step7.

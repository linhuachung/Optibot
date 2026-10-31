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

## Observed asset upload - 2026-10-31

Evidence source: a new user-provided screenshot in this conversation after the guided upload. The Files/Assets Home view shows one folder named Takehome Study and 13 asset cards. Three cards have the exact test fixture names: study-video-3s.mp4, study-document-two-pages.pdf and study-image-blue.png. Their thumbnails visibly show the generated video frame, document page and blue image. The three test files appear in Home, not inside the study folder; folder membership/move behavior has not yet been tested.

This verifies that the user created a folder and the three file types are listed with generated thumbnails. It does not yet verify full video playback, both PDF pages, conversion completion details, search/download/duplicate/replace/delete/settings, limits or screen propagation. Next check: inspect the PDF preview and page controls, then the short video and image settings. Existing sample assets are not study targets.

## User-confirmed folder move/open and observed playlist - 2026-10-31

The user reports moving the uploaded fixtures into Takehome Study and opening them successfully. This is user-reported success; the statement does not independently establish complete video playback or inspection of both PDF pages.

A subsequent user-provided playlist screenshot directly shows Takehome Study Playlist with Changes Saved, 3 items, 99.5 KB and total duration 1m 4s. Its ordered rows are study-video-3s.mp4 (4 sec), study-image-blue.png (20 sec), and study-document-two-pages.pdf (2 pages, 40 sec). The right asset browser is inside Home > Takehome Study and lists the same three fixtures, corroborating folder membership. The displayed arithmetic is consistent: 4+20+40=64 seconds.

Observed controls include undo/redo, a monitor-shaped preview control, settings and Push to Screens. Their outcomes have not been tested. The screenshot does not prove reordering, duration edits, looping, preview playback or assignment. It also does not establish a universal 20-second-per-PDF-page rule. Although the fixture filename says 3s, SCIO displays 4 sec; whether this is rounding or another duration rule remains unverified. Next targeted check: change only the image duration to 5 sec and inspect the new total, then preview the playlist and check both PDF pages.

## Observed playlist duration edit - 2026-10-31

A subsequent user screenshot shows Changes Saved and a total of 49s. The image row now displays 5 sec, while the video remains 4 sec and the two-page PDF remains 40 sec. This directly verifies editing the image duration, saving it and recalculating the displayed total (4+5+40=49). The sidebar still uses a coarse 1m label; no exact rounding rule is inferred. Preview playback, looping, reorder behavior and actual screen assignment remain untested in the evidence supplied so far.

## User-reported preview opened - 2026-10-31

After locating the monitor-shaped preview control, the user reports opening it and seeing the video. This is user-reported preview/video visibility, not independently captured evidence of motion, automatic transitions, both PDF pages or a completed loop. It also does not establish playback on a paired physical screen. Next observation requested: whether preview advances from video to the blue image and through both PDF pages.

## Earlier preview confirmation - superseded by the correction below

In response to the explicit check of video -> blue image approximately5 seconds -> PDF page1 -> page2 -> back to video, the user confirmed yes. Record this as user-observed automatic progression, both PDF pages and looping in portal preview. Timing was not independently measured and this is not evidence of a paired physical player's playback. Combined evidence now covers fixture upload, folder membership, saved playlist composition, image-duration editing, displayed total recalculation and the user-confirmed preview sequence. Schedules, physical pairing/assignment and further asset/settings/failure checks remain open.

## Corrected PDF preview observation - 2026-10-31

The candidate explicitly corrected the earlier yes/no confirmation: PDF preview showed page1 and stopped; the candidate had to press Next manually to see page2. This supersedes any earlier claim of confirmed automatic PDF page progression or a complete automatic loop. The later acknowledgement did not explicitly report the outcome of the proposed hands-off40-second check, so that check remains unverified. This observation applies to the portal preview only; neither automatic nor manual physical-player page behavior has been tested.

Current accepted facts: saved three-item playlist, editable image duration and correct displayed49-second total; preview opens with video visible; PDF page2 can be reached manually. Automatic PDF page progression and full automatic looping remain open. Continue the independent Schedules study without treating this preview limitation as a proven physical-player defect.

## Observed schedule creation - 2026-10-31

A user-provided screenshot shows Takehome Study Schedule in the Schedules area with a Schedule created confirmation. It is displayed as an empty weekly calendar for Oct25-31,2026, with Today, week/date navigation, Add Event, Push To Screens and settings controls. This verifies creation and visible calendar controls only. No event/content selection, recurrence, overlap, timezone, fallback or screen assignment has yet been observed.

## Observed calendar event - 2026-10-31

A further user screenshot shows a blue event in the Saturday31 column of Takehome Study Schedule. Its visible label is 10:48 - 11:18 Takehome Study Playlist, a30-minute interval as displayed. This verifies that an event bearing the study playlist name is visible in the calendar. The event detail dialog has not been supplied, so the underlying selected content, AM/PM representation, timezone, repeat rule and any priority/fallback behavior are not independently confirmed. The calendar image does not prove screen assignment or playback during the interval. Next check: open this existing event and inspect its content/time/recurrence settings.

## Observed event binding and one-off interval - 2026-10-31

The user supplied the Edit Event dialog. Playlist is the selected content type, and its selector shows Takehome Study Playlist. Start is10/31/2026 10:48 PM and End is10/31/2026 11:18 PM. Repeat currently reads Does not repeat. The dialog also exposes an alternative Asset content type, Event Color, Cancel, Delete and Save. This confirms actual playlist binding, explicit date/time fields and the current non-repeating setting. No timezone field is visible in this dialog, so the event's timezone is not inferred from the candidate's machine timezone. Other recurrence options and actual recurrence behavior are not yet observed.

## Observed recurrence options - 2026-10-31

The user screenshot shows Add Event (not the previous Edit Event), with Asset selected, No asset selected, start10/31/2026 11:00PM and end11:30PM. The expanded Repeat menu offers: Does not repeat; Daily; Weekly on Saturday; Monthly on end of month; Monthly on the last Saturday; Monthly on the31st; Every weekday (Monday to Friday); Every Weekend; Custom.... These are observed choices for the displayed October31 date. Their date-dependent labeling does not establish recurrence behavior in short months or other dates. No new asset event is saved in this evidence and no recurring execution has been observed. Next check: inspect Custom without saving an unconfigured event.

## Observed custom recurrence configuration - 2026-10-31

Two user screenshots show Custom Recurrence. The Repeat selector offers Daily, Weekly, Monthly and Yearly. In the Daily configuration, Every is1 day; Ends offers Never, On a date and After a numeric occurrence count. The shown selection is After1 occurrence and the preview reads Daily for1 occurrence. A date field displays01/29/2027, but it is not the selected termination mode, so no event end-date outcome is inferred. Cancel and Done controls are visible. These observations establish visible configuration/summary fields only; no custom recurrence has yet been saved or executed and other frequency-specific controls are not yet inspected.

## Observed future recurrence instances - 2026-10-31

After the guided daily/three-occurrence configuration, the candidate screenshot shows the Nov1-7,2026 Week view with blue recurring-icon events on SundayNov1 and MondayNov2. Both display10:48-11:18 Takehome Study Playlist. No corresponding event is visible in the TuesdayNov3 column at the displayed interval. This is consistent with the intended three-day series beginningOct31, but the final saved recurrence-detail dialog was not supplied; the screenshot directly proves only the shown future calendar instances. Recurrence expansion in the portal is observed, whereas scheduled execution on a paired player, timezone interpretation and series-edit scope remain untested.

## Observed schedule default-content configuration - 2026-10-31

The candidate screenshots show the study schedule's Default Content dialog with explanatory text Fill in the time gaps between events. Its selector currently uses Use Account Default and exposes None, Use Account Default, Asset and Playlist. Save and Cancel are visible. This is direct evidence of configurable schedule gap-filling choices and the displayed account-default selection. No default content was changed or executed in the evidence, the actual account-default target is unknown, and None is not interpreted as a particular black/blank/offline player behavior. No timezone control is visible in this dialog; timezone remains unverified.

## Observed Add Screen pairing form - 2026-10-31

The candidate screenshot shows Add Screen with a required Pair code field, instruction to enter the6-digit pairing code shown on the screen, an optional Use lowercase pairing code checkbox, and Cancel/Pair controls. The explanatory text says to install the OptiSigns app on a player (Win,Mac,Android,etc.) and explicitly offers Windows/Mac app links to try on a laptop. The code field is empty and Pair is disabled. This establishes visible code-based pairing prerequisites and laptop-player guidance, not successful pairing or actual device playback. Pairing codes must not be recorded in shared notes/evidence.

## Observed screen configuration form - 2026-10-31

The candidate supplied Edit Screen Screen1 screenshots after the pairing exercise. A screen configuration record is visible; device online state, successful pairing acknowledgement and actual player rendering are not visible in these images. Device Name is Screen1, Content Type is still Select type and Orientation is Landscape. An onboarding explanation names Asset, Playlist and Schedule as content types and describes playlists as a loop and schedules as what-plays-when plans. This is visible UI guidance, not proof those assignments have executed.

A separate Operational Schedule selector shows None; it is not conflated with content type Schedule, and its operating behavior is not yet tested. Advanced controls visibly include functional location, a blank location field, Background Type Default, Content Tag Rule, Sync Play unchecked, Show Downloading Status checked, Preload Assets in Playlist checked, Show Offline Indicator unchecked and Mute unchecked. These are displayed choices/states for this trial, not universal defaults or validated runtime behavior. Next: assign only the dedicated study playlist to the new study screen and observe the actual Player app, separately from portal Preview.

## Candidate-confirmed actual Player rendering - 2026-10-31

After the guided rename/content-type/playlist-save steps, the candidate reported completion. A separate explicit question distinguished the actual installed OptiSigns Player from portal Preview; the candidate selected that video, blue image and PDF were visible/playing in the Player. Record this as candidate-confirmed real Player rendering of the assigned study playlist. It is not an independent agent screenshot or a measured delivery-latency test.

This verifies the exercised direct path from uploaded study files through a playlist to a screen/installed Player. It does not establish automatic PDF page advancement, a complete hands-off loop on the Player, schedule-driven execution, offline behavior or Linux-platform execution. The earlier manual-Next PDF observation applied to portal preview and is not generalized to the installed Player. The new screen's UI settings were observed, but folder operations and further setting effects remain untested.

# Run the backend and frontend

Run all commands from the repository root, `D:\Projects\OptiSigns` in this workspace. The application is a local support-chat demo; the existing daily scraper remains a separate job.

## 1. Install Python dependencies

Use Python 3.11 or newer:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Use `.\.venv\Scripts\python.exe` instead of `python` in the commands below if you created this environment. On macOS/Linux the path is `.venv/bin/python`.

This particular workspace already has dependencies in an ignored portable runtime. If `python` is not available, use `.\.runtime\python\python.exe` directly; no activation or global installation is required here. The portable runtime is not committed to GitHub, so a fresh clone needs its own Python installation/environment.

## 2. Configure the backend

For a fresh clone, copy `.env.sample` to `.env` without overwriting an existing configured file. Set `API_KEY` or `OPENAI_API_KEY`; `API_KEY` takes precedence. Never place a key in frontend files or browser input. `OPENAI_MODEL` can select an available Responses model with file search; the default is `gpt-4.1-mini`.

The backend needs `data/ingestion-state.json` with the API-loaded corpus. Runtime data is intentionally excluded from Git. On this workspace it already exists. On a new environment, run:

```powershell
python main.py
```

That creates the selected Markdown corpus, reuses/creates the configured vector store and records state. Retain both `manifest.json` and `ingestion-state.json` between daily runs. If reusing an existing store, configure its ID; do not run competing local/cloud writers against the same store. See [deployment and recovery](deploy.md).

## 3. Run the backend server

Terminal 1:

```powershell
python server.py
```

The backend listens on **http://127.0.0.1:8000**. Check **http://127.0.0.1:8000/api/health** for local document readiness. The health endpoint does not contact OpenAI or check credit balance. Open **http://127.0.0.1:8000** to use the bundled frontend from this server alone.

## 4. Run the frontend separately

Keep Terminal 1 running. In Terminal 2, from the same repository root:

```powershell
python -m http.server 5173 --bind 127.0.0.1 --directory frontend/public
```

Open **http://127.0.0.1:5173**. This frontend talks to the backend on port 8000. No Node/npm installation, bundler or frontend build is required to run it. Changes to HTML/CSS/JavaScript appear after refreshing the page.

**Search docs** returns actual passages and source links without generating an answer. **Ask assistant** uses the exact support prompt and needs funded API credits. A successful document search does not prove a generated answer is correct. An exhausted-credit error is shown explicitly; it is not replaced with a fabricated answer.

## 5. Verify and stop

```powershell
python -m unittest discover -s tests -v
python -m pip check
```

Optional browser regression checks require Node.js 22+ (only for tests):

```powershell
npm ci
npx playwright install chromium
npm run test:ui
```

In this workspace, the installed browser cache is `.runtime/ms-playwright`; set `$env:PLAYWRIGHT_BROWSERS_PATH = "$PWD/.runtime/ms-playwright"` before the test command. CI installs its own browser. These tests use explicit fixtures; the separate live UI evidence records actual provider retrieval.

Try the YouTube sample, open its source, switch to Ask assistant and verify either the cited answer or an actionable credit error. Test at a narrow window width and use Enter to send; Shift+Enter inserts a line break. Press **Ctrl+C** in each terminal to stop its server.

Both servers bind to loopback. They are for local use, with no user authentication; do not expose them on a public interface. The daily GitHub Actions deployment runs `main.py` and does not host this UI. This custom UI does not replace the assignment's required provider-UI screenshot or the live SCIO study for Part 2.

## Troubleshooting

- **Backend unavailable:** start `server.py` and check that port 8000 is free. The separate frontend uses port 5173; use the documented ports or update the explicit origin/API configuration together.
- **Setup needed / no documents:** run `main.py` with the configured server key and correct data directory. `STATE_DIR` overrides `DATA_DIR`; changing it can point at an empty corpus.
- **No API credits:** fund the API project or rotate the server's key to a funded project, then restart. Search and generation can have different provider availability; the app reports their errors separately.
- **Key rejected:** update the backend `.env`, not the frontend, and restart the backend. Do not share the key in screenshots or chat.
- **PowerShell cannot find Python:** use the explicit virtual-environment or workspace portable-runtime path above.
- **Port already in use:** stop the prior server using its terminal. Do not start a second server on the same port.
- **Fresh clone has no `.runtime` or `data`:** expected; install Python, install requirements and generate/restore the corpus. Do not commit runtime data or credentials to make a clone runnable.

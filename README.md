# Harbor support notes

Zendesk articles to Markdown to an OpenAI vector store, with a daily Docker job and a local support UI. [Source](https://github.com/linhuachung/Optibot).

## Setup

Use Python 3.11+: `python -m pip install -r requirements.txt`. Copy `.env.sample` to `.env` **only if it does not exist**, then set `API_KEY` or `OPENAI_API_KEY` (`API_KEY` wins). Keep keys on the server. Run `python main.py` to create the 30-article seed and index it; retain `data/manifest.json` and `data/ingestion-state.json`. `STATE_DIR` overrides `DATA_DIR` (default `data`). Do not run competing local/cloud uploaders against one store.

## Run server and frontend

From the repository root, Terminal 1:

```powershell
python server.py
```

Open **http://127.0.0.1:8000** to use the bundled frontend. To run the frontend separately, keep the backend running and use Terminal 2:

```powershell
python -m http.server 5173 --bind 127.0.0.1 --directory frontend/public
```

Open **http://127.0.0.1:5173**. No Node/build step is required. In this workspace, replace `python` with `.\.runtime\python\python.exe` if needed. Both servers are local only; stop with Ctrl+C. Search docs returns excerpts and links; Ask assistant generates a cited answer and needs API credits. [Full setup/troubleshooting](docs/run.md), [frontend](frontend/README.md), [API](docs/api.md).

## Daily job and verification

```powershell
python main.py
python -m unittest discover -s tests -v
docker build -t harbor-ledger .
docker run --rm --env-file .env --mount "type=bind,source=$((Get-Location).Path)/data,target=/data" harbor-ledger
```

The Docker entry point runs once and exits; it does not host the UI. GitHub Actions schedules it at 02:17 UTC with durable state artifacts. [Deployment/recovery](docs/deploy.md), [successful cloud logs](https://github.com/linhuachung/Optibot/actions/runs/41076345213), [verification](docs/verification.md). Repeated cloud runs skipped all 30 unchanged articles. Managed chunking defaults to 800 tokens/400 overlap; exact embedded-chunk totals are unavailable and reported as `null`.

[Local UI screenshot](docs/evidence/local-chat-search.png) demonstrates actual retrieval. **Required provider-UI screenshot remains missing**, generated answers are blocked by exhausted API credits, and the first automatic cron trigger is unobserved. The custom UI does not replace provider evidence. [Checklist](tasks/todo.md), [cuts/open requirements](CUTS.md). Part 2: [Brief A proposal](docs/scio-slice-plan.md); live SCIO study and candidate review remain required. Submit both parts together after resolving these gates.

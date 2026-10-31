# Harbor support notes

Public Zendesk articles to Markdown to a Gemini File Search store, with a daily Docker job and floating support widget. OpenAI integration is retained for rollback.

## Setup and run

Use Python 3.11+: `python -m pip install -r requirements.txt`. Copy `.env.sample` to `.env` only if absent. Set `AI_PROVIDER=gemini`, `GEMINI_API_KEY` and optionally `GEMINI_MODEL` (default `gemini-3.5-flash-lite`). Gemini also accepts the assignment-facing `API_KEY` alias. Keep keys server-side.

```powershell
python main.py
python server.py
```

Open **http://127.0.0.1:8000**, then click the bottom-right chat launcher. For a separate frontend, keep the backend running and use another terminal:

```powershell
python -m http.server 5173 --bind 127.0.0.1 --directory frontend/public
```

Open **http://127.0.0.1:5173**. No Node/build step is required. In this workspace replace `python` with `.\.runtime\python\python.exe` if needed. Both servers bind locally; stop with Ctrl+C. [Detailed setup/troubleshooting](docs/run.md).

## Daily job and evidence

```powershell
python -m unittest discover -s tests -v
docker build -t harbor-ledger .
docker run --rm --env-file .env --mount "type=bind,source=$((Get-Location).Path)/data,target=/data" harbor-ledger
```

`main.py` runs once and exits. Keep `data/manifest.json` and `data/gemini-state.json` between runs. `STATE_DIR` overrides `DATA_DIR` (default `data`). Avoid competing writers to one store. Gemini uses white-space chunking with 400 tokens/80 overlap; exact embedded-chunk totals are not exposed in inspected metadata and remain unresolved. Gemini source lookup also uses generation quota.

31 Gemini articles indexed; a real rerun skipped all 31. [Answer evidence](docs/evidence/gemini-youtube-answer.json), [local widget screenshot](docs/evidence/gemini-widget-desktop.png), [checklist](tasks/todo.md), [deployment/recovery](docs/deploy.md). GitHub cron is 02:17 UTC; a real [scheduled OpenAI run](https://github.com/linhuachung/Optibot/actions/runs/41184533900) added one/updated two articles. Two [Gemini cloud containers](https://github.com/linhuachung/Optibot/actions/runs/41213474374) also restored state and skipped all 31.

**Submission gates:** required provider-UI screenshot, exact chunk totals, live OptiBot/SCIO observations, candidate rehearsal, cryptic repository naming and actual hours. Custom-widget screenshots do not replace AI Studio evidence. [Cuts](CUTS.md), [verification](docs/verification.md), [Brief A plan](docs/scio-slice-plan.md). Submit both parts together.

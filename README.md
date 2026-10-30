# Harbor support notes

One-shot Zendesk scraper to clean Markdown to OpenAI vector store. Source: [GitHub](https://github.com/linhuachung/Optibot).

## Setup and run

Use Python 3.11+: `python -m pip install -r requirements.txt`. Copy `.env.sample` to `.env` and set `API_KEY` or `OPENAI_API_KEY` (`API_KEY` wins). Keep keys private. The store ID is created once and saved with hashes/remote IDs in `data/ingestion-state.json`; retain the state directory between runs. `STATE_DIR` overrides `DATA_DIR`; locally the default is `data`.

```powershell
python main.py
python ask.py --retrieve-only
python ask.py --require-citations --output docs/evidence/youtube-answer.json
python -m unittest discover -s tests -v
docker build -t harbor-ledger .
docker run --rm --env-file .env --mount "type=bind,source=$((Get-Location).Path)/data,target=/data" harbor-ledger
```

The ignored workspace runtime is `.\.runtime\python\python.exe` if Python is not installed. `scrape.py` and `upload.py` remain separate manual tools; `main.py` runs the complete daily pipeline once and exits. `OPENAI_MODEL` defaults to `gpt-4.1-mini` for queries.

## Daily job and evidence

Bootstrap selects 30 articles including YouTube. Daily runs discover newly public English articles, refresh the existing corpus, hash semantic Markdown and upload additions/changes only. Pending versions finish before re-scraping; old indexed entries retire only after successful replacement. An OS lock prevents overlapping state writes. Failures exit nonzero and retain retry state; counts and timestamps go to `last-run.json`.

GitHub Actions runs the Docker job daily at `02:17 UTC` (09:17 Bangkok), with versioned workflow artifacts preserving state. Configure the encrypted secrets and follow [deployment and recovery](docs/deploy.md). Railway is no longer required.

Evidence: [local last run](docs/evidence/local-daily-rerun.json), [remote index status](docs/evidence/index-status.json), [retrieval](docs/evidence/youtube-retrieval.json), [verification](docs/verification.md). Local reruns show `added=0 updated=0 skipped=30 failed=0`. [Windows/Linux tests and Docker build passed](https://github.com/linhuachung/Optibot/actions/runs/41067614734). [Cloud job logs](https://github.com/linhuachung/Optibot/actions/runs/41068135936) show a second successful container restoring prior state and skipping all 30 articles. The first automatic cron trigger is still pending.

Chunking uses the managed default, documented as 800 tokens with 400 overlap. Inspected metadata exposes no exact embedded-chunk total; reports say `null`, never substitute file counts. This requirement remains unresolved.

Provider-UI screenshot is pending: apply [the exact prompt](system_prompt.txt), connect file search to the saved store, ask the YouTube question and save `docs/screenshot-youtube.png`. API JSON does not replace it. Generated-answer checks were blocked by exhausted API credits. See [cuts and incomplete work](CUTS.md); submit both take-home parts together after completing their checklist.

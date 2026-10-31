"""One daily scrape/upload run, with durable and secret-free run evidence."""

import time
from contextlib import nullcontext
from datetime import datetime, timezone
from pathlib import Path

from optibot.config import api_client
from optibot.ingest import ingest, resume_pending
from optibot.lock import job_lock
from optibot.scrape import scrape
from optibot.storage import write_json


def run_job(data_dir: Path, *, client=None, http_client=None, limit=30, store_id=None, provider="openai"):
    counts = {"added": 0, "updated": 0, "skipped": 0, "failed": 0}
    started = time.monotonic()
    report = {"started_at": datetime.now(timezone.utc).isoformat()}
    with job_lock(data_dir):
        try:
            if provider not in ("openai", "gemini"):
                raise ValueError("Unknown AI provider")
            if provider == "gemini":
                from optibot.gemini import gemini_client, resume_gemini, ingest_gemini
                factory = gemini_client
            else:
                factory = api_client
            with nullcontext(client) if client is not None else factory() as api:
                if provider == "gemini":
                    recovered = resume_gemini(data_dir, client=api, counts=counts)
                    scrape(data_dir, client=http_client, limit=limit, discover_new=True)
                    result = ingest_gemini(data_dir, client=api, counts=counts, completed_ids=recovered)
                else:
                    recovered = resume_pending(data_dir, client=api, store_id=store_id, counts=counts)
                    scrape(data_dir, client=http_client, limit=limit, discover_new=True)
                    result = ingest(data_dir, client=api, store_id=store_id, counts=counts, completed_ids=recovered)
                counts.update({key: result[key] for key in counts})
            report["provider"] = provider
            report["status"] = "success"
        except Exception as error:
            # External exception messages can contain credentials or document content.
            counts["failed"] += 1
            report.update(status="failed", error_type=type(error).__name__)
            status = getattr(error, "status_code", None)
            if isinstance(status, int):
                report["http_status"] = status
        report.update(counts)
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        report["duration_seconds"] = round(time.monotonic() - started, 3)
        write_json(data_dir / "last-run.json", report)
    return report

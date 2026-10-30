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


def run_job(data_dir: Path, *, client=None, http_client=None, limit=30, store_id=None):
    counts = {"added": 0, "updated": 0, "skipped": 0, "failed": 0}
    started = time.monotonic()
    report = {"started_at": datetime.now(timezone.utc).isoformat()}
    with job_lock(data_dir):
        try:
            with nullcontext(client) if client is not None else api_client() as api:
                recovered = resume_pending(data_dir, client=api, store_id=store_id, counts=counts)
                scrape(data_dir, client=http_client, limit=limit, discover_new=True)
                result = ingest(data_dir, client=api, store_id=store_id, counts=counts, completed_ids=recovered)
                counts.update({key: result[key] for key in counts})
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

import tempfile
import unittest
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from optibot.job import run_job
from optibot.lock import job_lock


class JobTests(unittest.TestCase):
    def test_overlapping_runs_cannot_share_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with job_lock(root):
                with self.assertRaises(RuntimeError):
                    with job_lock(root):
                        pass
            with job_lock(root):
                pass

    def test_success_records_counts_and_finishes(self):
        with tempfile.TemporaryDirectory() as tmp, patch("optibot.job.scrape"), patch("optibot.job.ingest") as ingest:
            ingest.return_value = {"added": 1, "updated": 2, "skipped": 27, "failed": 0}
            result = run_job(Path(tmp), client=object())
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["updated"], 2)
            self.assertTrue((Path(tmp) / "last-run.json").exists())

    def test_failure_is_recorded_without_logging_exception_secrets(self):
        with tempfile.TemporaryDirectory() as tmp, patch("optibot.job.scrape", side_effect=RuntimeError("sensitive-detail")):
            result = run_job(Path(tmp), client=object())
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["failed"], 1)
            self.assertNotIn("sensitive-detail", (Path(tmp) / "last-run.json").read_text())

    def test_main_exits_nonzero_with_failure_artifact_when_key_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, "main.py", "--data-dir", tmp],
                env={**os.environ, "API_KEY": "", "OPENAI_API_KEY": "", "AI_PROVIDER": "openai"}, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("failed=1", result.stdout)
            self.assertTrue((Path(tmp) / "last-run.json").exists())

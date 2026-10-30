import tempfile
import unittest
import httpx
from openai import NotFoundError
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

from optibot.ingest import ingest
from optibot.storage import read_json, write_json
from test_scrape import article
from optibot.scrape import article_markdown, content_hash


class IngestTests(unittest.TestCase):
    def prepare(self, root):
        text = article_markdown(article(1))
        (root / "articles").mkdir()
        (root / "articles" / "1.md").write_text(text, encoding="utf-8")
        write_json(root / "manifest.json", {"article_ids": [1], "articles": {"1": {
            "hash": content_hash(text), "url": article(1)["html_url"], "title": "Guide"}}})

    def client(self):
        client = MagicMock()
        client.vector_stores.create.return_value = SimpleNamespace(id="vs_test")
        client.vector_stores.files.list.return_value = []
        client.files.create.return_value = SimpleNamespace(id="file_test")
        client.vector_stores.files.create_and_poll.return_value = SimpleNamespace(status="completed", last_error=None)
        client.vector_stores.files.retrieve.side_effect = NotFoundError(
            "not indexed", response=httpx.Response(404, request=httpx.Request("GET", "https://api.openai.com")), body=None)
        return client

    def test_success_and_second_run_skip_without_duplicate_uploads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            client = self.client()
            first = ingest(root, client=client)
            self.assertEqual(first["uploaded"], 1)
            self.assertIsNone(first["embedded_chunks"])
            client.vector_stores.files.retrieve.side_effect = None
            client.vector_stores.files.retrieve.return_value = SimpleNamespace(status="completed")
            self.assertEqual(ingest(root, client=client)["skipped"], 1)
            self.assertEqual(client.files.create.call_count, 1)
            self.assertEqual(client.vector_stores.create.call_count, 1)

    def test_failed_indexing_preserves_pending_id_without_committing_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            client = self.client()
            client.vector_stores.files.create_and_poll.return_value = SimpleNamespace(status="failed", last_error=None)
            with self.assertRaises(RuntimeError):
                ingest(root, client=client)
            state = read_json(root / "ingestion-state.json", {})
            self.assertEqual(state["pending"]["1"]["file_id"], "file_test")
            self.assertNotIn("1", state["articles"])
            client.vector_stores.files.retrieve.side_effect = None
            client.vector_stores.files.retrieve.return_value = SimpleNamespace(status="failed")
            client.vector_stores.files.create_and_poll.return_value = SimpleNamespace(status="completed")
            self.assertEqual(ingest(root, client=client)["uploaded"], 1)
            self.assertEqual(client.files.create.call_count, 1)

    def test_modified_local_file_is_rejected_before_creating_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            (root / "articles" / "1.md").write_text(article_markdown(article(1, body="tampered")), encoding="utf-8")
            client = self.client()
            with self.assertRaises(ValueError):
                ingest(root, client=client)
            client.vector_stores.create.assert_not_called()

    def test_resumes_in_progress_attachment_instead_of_reattaching(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            client = self.client()
            client.vector_stores.files.retrieve.side_effect = None
            client.vector_stores.files.retrieve.return_value = SimpleNamespace(status="in_progress")
            client.vector_stores.files.poll.return_value = SimpleNamespace(status="completed")
            self.assertEqual(ingest(root, client=client)["uploaded"], 1)
            client.vector_stores.files.create_and_poll.assert_not_called()
            client.vector_stores.files.poll.assert_called_once()


if __name__ == "__main__":
    unittest.main()

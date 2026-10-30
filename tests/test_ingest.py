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
        client.with_options.return_value = client
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

    def test_updated_article_replaces_old_index_only_after_new_index_completes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            client = self.client()
            ingest(root, client=client)
            old = read_json(root / "ingestion-state.json", None)["articles"]["1"]
            text = article_markdown(article(1, body="<p>Changed instructions</p>"))
            (root / "articles" / "1.md").write_text(text, encoding="utf-8")
            manifest = read_json(root / "manifest.json", None)
            manifest["articles"]["1"]["hash"] = content_hash(text)
            write_json(root / "manifest.json", manifest)
            client.files.create.return_value = SimpleNamespace(id="file_new")
            result = ingest(root, client=client)
            self.assertEqual(result["updated"], 1)
            client.vector_stores.files.delete.assert_called_with(old["file_id"], vector_store_id="vs_test")
            self.assertEqual(read_json(root / "ingestion-state.json", None)["articles"]["1"]["file_id"], "file_new")

    def test_pending_version_finishes_even_when_source_has_changed_again(self):
        from optibot.ingest import resume_pending
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            metadata = read_json(root / "manifest.json", None)["articles"]["1"]
            write_json(root / "ingestion-state.json", {"vector_store_id": "vs_test", "articles": {},
                "pending": {"1": {"file_id": "file_test", "hash": metadata["hash"], "metadata": metadata}}})
            (root / "articles" / "1.md").write_text("source changed after interruption", encoding="utf-8")
            client = self.client()
            client.vector_stores.files.retrieve.side_effect = None
            client.vector_stores.files.retrieve.return_value = SimpleNamespace(status="completed")
            self.assertEqual(resume_pending(root, client=client), {"1"})
            client.files.create.assert_not_called()

    def test_ambiguous_upload_reconciles_by_exact_owned_filename(self):
        from optibot.ingest import resume_pending
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            metadata = read_json(root / "manifest.json", None)["articles"]["1"]
            write_json(root / "ingestion-state.json", {"vector_store_id": "vs_test", "articles": {},
                "pending": {"1": {"file_id": None, "filename": "vs_test-1-owned.md", "hash": metadata["hash"], "metadata": metadata}}})
            client = self.client()
            client.files.list.return_value = [SimpleNamespace(id="file_found", filename="vs_test-1-owned.md")]
            resume_pending(root, client=client)
            client.files.create.assert_not_called()
            self.assertEqual(read_json(root / "ingestion-state.json", None)["articles"]["1"]["file_id"], "file_found")

    def test_failed_old_version_cleanup_retries_without_duplicate_upload(self):
        from optibot.ingest import resume_pending
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            metadata = read_json(root / "manifest.json", None)["articles"]["1"]
            write_json(root / "ingestion-state.json", {"vector_store_id": "vs_test",
                "articles": {"1": {**metadata, "file_id": "file_old", "hash": "old"}},
                "pending": {"1": {"file_id": "file_new", "hash": metadata["hash"], "metadata": metadata}}})
            client = self.client()
            client.vector_stores.files.retrieve.side_effect = None
            client.vector_stores.files.retrieve.return_value = SimpleNamespace(status="completed")
            client.vector_stores.files.delete.side_effect = RuntimeError("temporary delete failure")
            with self.assertRaises(RuntimeError):
                resume_pending(root, client=client)
            self.assertIn("1", read_json(root / "ingestion-state.json", None)["pending"])
            client.vector_stores.files.delete.side_effect = None
            resume_pending(root, client=client)
            client.files.create.assert_not_called()

    def test_lost_upload_response_does_not_trigger_blind_duplicate_upload(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            client = self.client()
            client.files.create.side_effect = RuntimeError("lost response")
            with self.assertRaises(RuntimeError):
                ingest(root, client=client)
            state = read_json(root / "ingestion-state.json", None)
            self.assertIsNone(state["pending"]["1"]["file_id"])
            client.files.list.return_value = []
            with self.assertRaises(RuntimeError):
                ingest(root, client=client)
            self.assertEqual(client.files.create.call_count, 1)

    def test_remote_orphan_is_reused_after_cloud_journal_is_lost(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            metadata = read_json(root / "manifest.json", None)["articles"]["1"]
            write_json(root / "ingestion-state.json", {"vector_store_id": "vs_test", "articles": {}, "pending": {}})
            client = self.client()
            client.files.list.return_value = [SimpleNamespace(
                id="file_orphan", filename=f"vs_test-1-{metadata['hash']}.md")]
            ingest(root, client=client)
            client.files.create.assert_not_called()
            self.assertEqual(read_json(root / "ingestion-state.json", None)["articles"]["1"]["file_id"], "file_orphan")

    def test_duplicate_owned_filenames_fail_without_another_upload(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            metadata = read_json(root / "manifest.json", None)["articles"]["1"]
            write_json(root / "ingestion-state.json", {"vector_store_id": "vs_test", "articles": {}, "pending": {}})
            client = self.client()
            filename = f"vs_test-1-{metadata['hash']}.md"
            client.files.list.return_value = [SimpleNamespace(id="file_one", filename=filename),
                                             SimpleNamespace(id="file_two", filename=filename)]
            with self.assertRaises(RuntimeError):
                ingest(root, client=client)
            client.files.create.assert_not_called()


if __name__ == "__main__":
    unittest.main()

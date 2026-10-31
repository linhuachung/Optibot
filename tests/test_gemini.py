import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import MagicMock

from optibot.gemini import ingest_gemini, query_gemini
from optibot.scrape import content_hash
from optibot.storage import write_json, read_json


class GeminiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "articles").mkdir()
        text = "# Guide\n\nArticle URL: https://support.optisigns.com/hc/en-us/articles/1\nArticle ID: 1\nSource updated: now\n\nInstructions\n"
        (self.root / "articles/1.md").write_text(text)
        self.meta = {"title": "Guide", "url": "https://support.optisigns.com/hc/en-us/articles/1", "hash": content_hash(text)}
        write_json(self.root / "manifest.json", {"article_ids": [1], "articles": {"1": self.meta}})
        self.client = MagicMock()
        self.client.file_search_stores.list.return_value = []
        self.client.file_search_stores.create.return_value = NS(name="fileSearchStores/test")
        self.client.file_search_stores.documents.list.return_value = []
        self.client.file_search_stores.upload_to_file_search_store.return_value = NS(name="operations/1", done=True, error=None,
            response=NS(document_name="fileSearchStores/test/documents/1"))
        self.client.file_search_stores.documents.get.return_value = NS(state="STATE_ACTIVE")

    def test_upload_then_skip_keeps_openai_state_separate(self):
        write_json(self.root / "ingestion-state.json", {"vector_store_id": "vs_original"})
        first = ingest_gemini(self.root, client=self.client)
        second = ingest_gemini(self.root, client=self.client)
        self.assertEqual(first["added"], 1)
        self.assertEqual(second["skipped"], 1)
        self.assertEqual(self.client.file_search_stores.upload_to_file_search_store.call_count, 1)
        self.assertEqual(read_json(self.root / "ingestion-state.json", None)["vector_store_id"], "vs_original")

    def test_failed_operation_does_not_commit(self):
        self.client.file_search_stores.upload_to_file_search_store.return_value.error = NS(code=500)
        with self.assertRaises(RuntimeError):
            ingest_gemini(self.root, client=self.client)
        state = read_json(self.root / "gemini-state.json", None)
        self.assertEqual(state["articles"], {})
        self.assertIn("1", state["pending"])

    def test_corrupt_markdown_is_rejected_before_provider(self):
        (self.root / "articles/1.md").write_text("changed")
        with self.assertRaises(ValueError):
            ingest_gemini(self.root, client=self.client)
        self.client.file_search_stores.create.assert_not_called()

    def test_known_grounding_maps_citations_and_search_excerpts(self):
        record = {**self.meta, "file_id": "fileSearchStores/test/documents/1", "display_name": "article-1-hash"}
        context = NS(title="article-1-hash", document_name=None, file_search_store="fileSearchStores/test", text="Source instructions")
        self.client.models.generate_content.return_value = NS(text="Use the guide.", candidates=[NS(grounding_metadata=NS(grounding_chunks=[NS(retrieved_context=context)]))])
        result = query_gemini(self.client, "fileSearchStores/test", "Question", "test-model", {"1": record}, require_citations=True)
        self.assertEqual(result["citations"][0]["article_id"], "1")
        search = query_gemini(self.client, "fileSearchStores/test", "Question", "test-model", {"1": record}, search=True)
        self.assertEqual(search["matches"][0]["excerpt"], "Source instructions")
        self.assertIsNone(search["answer"])
        context.file_search_store = "fileSearchStores/other"
        with self.assertRaises(RuntimeError):
            query_gemini(self.client, "fileSearchStores/test", "Question", "test-model", {"1": record})

    def test_replacement_cleanup_failure_retries_without_uploading_again(self):
        ingest_gemini(self.root, client=self.client)
        original = (self.root / "articles/1.md").read_text()
        changed = original.replace("Instructions", "Updated instructions")
        (self.root / "articles/1.md").write_text(changed)
        metadata = {**self.meta, "hash": content_hash(changed)}
        write_json(self.root / "manifest.json", {"article_ids": [1], "articles": {"1": metadata}})
        operation = self.client.file_search_stores.upload_to_file_search_store.return_value
        operation.response.document_name = "fileSearchStores/test/documents/2"
        self.client.file_search_stores.documents.delete.side_effect = RuntimeError("cleanup failed")
        with self.assertRaises(RuntimeError):
            ingest_gemini(self.root, client=self.client)
        self.assertEqual(read_json(self.root / "gemini-state.json", None)["articles"]["1"]["hash"], self.meta["hash"])
        self.client.file_search_stores.documents.delete.side_effect = None
        report = ingest_gemini(self.root, client=self.client)
        self.assertEqual(report["updated"], 1)
        self.assertEqual(self.client.file_search_stores.upload_to_file_search_store.call_count, 2)
        self.assertEqual(read_json(self.root / "gemini-state.json", None)["pending"], {})

    def test_lost_upload_response_stops_without_blind_retry(self):
        self.client.file_search_stores.upload_to_file_search_store.side_effect = RuntimeError("response lost")
        with self.assertRaises(RuntimeError):
            ingest_gemini(self.root, client=self.client)
        with self.assertRaisesRegex(RuntimeError, "Ambiguous"):
            ingest_gemini(self.root, client=self.client)
        self.assertEqual(self.client.file_search_stores.upload_to_file_search_store.call_count, 1)

    def test_completed_orphan_is_reused_without_upload(self):
        self.client.file_search_stores.documents.list.return_value = [NS(
            display_name="article-1-" + self.meta["hash"], name="fileSearchStores/test/documents/orphan")]
        report = ingest_gemini(self.root, client=self.client)
        self.assertEqual(report["added"], 1)
        self.client.file_search_stores.upload_to_file_search_store.assert_not_called()

    def test_supported_answer_without_grounding_fails_verification(self):
        self.client.models.generate_content.return_value = NS(text="An unsupported claim.", candidates=[NS(grounding_metadata=None)])
        with self.assertRaises(RuntimeError):
            query_gemini(self.client, "fileSearchStores/test", "Question", "test-model", {}, require_citations=True)

    def test_nonpositive_limit_is_rejected_before_provider_mutation(self):
        for limit in (0, -1):
            with self.assertRaises(ValueError):
                ingest_gemini(self.root, client=self.client, limit=limit)
        self.client.file_search_stores.create.assert_not_called()

    def test_assignment_api_key_alias_is_supported_for_gemini(self):
        import os
        from unittest.mock import patch
        from optibot.gemini import gemini_client
        with patch.dict(os.environ, {"API_KEY": "test-alias"}, clear=True), \
             patch("optibot.gemini.load_dotenv"), patch("optibot.gemini.genai.Client") as factory:
            gemini_client()
            self.assertEqual(factory.call_args.kwargs["api_key"], "test-alias")

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import httpx
from fastapi.testclient import TestClient
from openai import RateLimitError

from optibot.storage import write_json
from optibot.web import create_app


class WebTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.api = MagicMock()
        self.api.__enter__.return_value = self.api
        self.api.with_options.return_value = self.api
        self.app = create_app(data_dir=self.root, client_factory=lambda: self.api)
        self.client = TestClient(self.app)

    def seed(self):
        write_json(self.root / "ingestion-state.json", {"vector_store_id": "vs_test", "articles": {
            "1": {"file_id": "file_test", "url": "https://support.optisigns.com/hc/en-us/articles/1", "title": "Guide"}}})

    def test_health_does_not_call_provider_or_disclose_secrets(self):
        result = self.client.get("/api/health")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()["articleCount"], 0)
        self.assertNotIn("sk-proj", result.text)
        self.api.vector_stores.search.assert_not_called()

    def test_search_returns_real_sources_without_generation(self):
        self.seed()
        self.api.vector_stores.search.return_value = SimpleNamespace(data=[SimpleNamespace(
            file_id="file_test", score=0.9, content=[SimpleNamespace(type="text", text="Source instructions")])])
        result = self.client.post("/api/chat", json={"question": "YouTube?", "mode": "search"})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()["sources"][0]["excerpt"], "Source instructions")
        self.assertIsNone(result.json()["answer"])
        self.api.responses.create.assert_not_called()

    def test_invalid_or_extra_request_fields_are_rejected(self):
        for body in [{"question": " "}, {"question": "x" * 2001},
                     {"question": "hi", "mode": "other"}, {"question": "hi", "apiKey": "private"}]:
            result = self.client.post("/api/chat", json=body)
            self.assertEqual(result.status_code, 422)
            self.assertEqual(result.json()["error"]["code"], "invalid_request")

    def test_missing_corpus_has_actionable_error(self):
        result = self.client.post("/api/chat", json={"question": "YouTube?"})
        self.assertEqual(result.status_code, 503)
        self.assertEqual(result.json()["error"]["code"], "corpus_missing")

    def test_quota_error_is_sanitized_and_search_is_still_possible(self):
        self.seed()
        self.api.responses.create.side_effect = RateLimitError("private-provider-detail",
            response=httpx.Response(429, request=httpx.Request("POST", "https://api.openai.com")),
            body={"code": "credit_balance_exhausted"})
        result = self.client.post("/api/chat", json={"question": "YouTube?", "mode": "answer"})
        self.assertEqual(result.status_code, 503)
        self.assertEqual(result.json()["error"]["code"], "quota_exhausted")
        self.assertNotIn("private-provider-detail", result.text)

    def test_untrusted_origin_and_oversized_body_are_blocked(self):
        result = self.client.post("/api/chat", json={"question": "hi"}, headers={"Origin": "https://example.com"})
        self.assertEqual(result.status_code, 403)
        result = self.client.post("/api/chat", content="x" * 9000, headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 413)

    def test_only_explicit_local_frontend_origins_are_allowed(self):
        result = self.client.options("/api/chat", headers={"Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "content-type"})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.headers["access-control-allow-origin"], "http://127.0.0.1:5173")

    def test_backend_serves_frontend_but_not_private_files(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        for path in ("/.env", "/data/ingestion-state.json", "/requirements.txt"):
            self.assertEqual(self.client.get(path).status_code, 404)
        self.assertEqual(self.client.get("/api/health", headers={"Host": "example.com"}).status_code, 400)

    def test_answer_response_has_sources_without_internal_ids(self):
        self.seed()
        self.api.responses.create.return_value = SimpleNamespace(id="response_private", status="completed",
            output_text="Open Files/Assets, then Apps.", output=[SimpleNamespace(type="message", content=[
                SimpleNamespace(type="output_text", annotations=[SimpleNamespace(type="file_citation", file_id="file_test")])])])
        result = self.client.post("/api/chat", json={"question": "YouTube?", "mode": "answer"})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()["answer"], "Open Files/Assets, then Apps.")
        self.assertEqual(result.json()["sources"][0]["title"], "Guide")
        self.assertNotIn("response_private", result.text)
        self.assertNotIn("vs_test", result.text)


if __name__ == "__main__":
    unittest.main()

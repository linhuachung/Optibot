import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from optibot.answer import answer, retrieve


class AnswerTests(unittest.TestCase):
    def test_uses_exact_prompt_restricts_store_and_maps_known_citations(self):
        client = MagicMock()
        client.responses.create.return_value = SimpleNamespace(
            id="resp_test", status="completed", output_text="Use Files/Assets, then Apps.",
            output=[SimpleNamespace(type="message", content=[SimpleNamespace(type="output_text", annotations=[
                SimpleNamespace(type="file_citation", file_id="file_test"),
            ])])],
        )
        report = answer(client, "vs_test", "Question", "gpt-4.1-mini", {
            "1": {"file_id": "file_test", "url": "https://support.optisigns.com/hc/en-us/articles/1", "title": "Guide"}},
            require_citations=True)
        self.assertEqual(report["citations"][0]["article_id"], "1")
        args = client.responses.create.call_args.kwargs
        self.assertEqual(args["tools"][0]["vector_store_ids"], ["vs_test"])
        self.assertIn('• Only answer using the uploaded docs.', args["instructions"])
        self.assertFalse(args["store"])

    def test_supported_answer_without_file_citations_fails_verification(self):
        client = MagicMock()
        client.responses.create.return_value = SimpleNamespace(
            id="resp_test", status="completed", output_text="Unsupported claim.", output=[])
        with self.assertRaises(RuntimeError):
            answer(client, "vs_test", "Question", "gpt-4.1-mini", {}, require_citations=True)

    def test_retrieval_only_never_calls_generation(self):
        client = MagicMock()
        client.vector_stores.search.return_value = SimpleNamespace(data=[SimpleNamespace(
            file_id="file_test", score=0.9, content=[SimpleNamespace(type="text", text="Source instructions")])])
        result = retrieve(client, "vs_test", "Question", {
            "1": {"file_id": "file_test", "url": "https://support.optisigns.com/hc/en-us/articles/1", "title": "Guide"}})
        self.assertEqual(result["matches"][0]["article_id"], "1")
        client.responses.create.assert_not_called()


if __name__ == "__main__":
    unittest.main()

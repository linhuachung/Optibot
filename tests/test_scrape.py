import tempfile
import unittest
from pathlib import Path

import httpx

from optibot.scrape import article_markdown, content_hash, scrape


def article(article_id, title="Guide", body="<p>Helpful instructions.</p>"):
    return {
        "id": article_id, "title": title, "body": body, "draft": False,
        "locale": "en-us", "html_url": f"https://support.optisigns.com/hc/en-us/articles/{article_id}",
        "updated_at": "2026-10-01T00:00:00Z", "created_at": "2026-09-01T00:00:00Z",
    }


class ScrapeTests(unittest.TestCase):
    def test_preserves_structure_relative_links_and_code_without_chrome(self):
        source = article(1, body='''<nav>Navigation junk</nav><script>bad()</script>
            <h2>Setup</h2><ul><li><a href="../guide">Guide</a></li></ul>
            <pre><code class="language-python">print("hello")\n\n\nprint("bye")</code></pre>''')
        text = article_markdown(source)
        self.assertIn("## Setup", text)
        self.assertIn("[Guide](../guide)", text)
        self.assertIn('```python\nprint("hello")\n\n\nprint("bye")\n```', text)
        self.assertIn("Article URL: " + source["html_url"], text)
        self.assertNotIn("Navigation junk", text)
        self.assertNotIn("bad()", text)

    def test_hash_ignores_source_timestamp_but_detects_content_change(self):
        first = article(1)
        later = {**first, "updated_at": "2026-10-02T00:00:00Z"}
        self.assertEqual(content_hash(article_markdown(first)), content_hash(article_markdown(later)))
        self.assertNotEqual(content_hash(article_markdown(first)), content_hash(article_markdown({**first, "body": "New content"})))

    def test_keeps_embedded_walkthrough_as_link_and_blocks_unsafe_urls(self):
        text = article_markdown(article(1, body='<iframe src="https://www.canva.com/design/example"></iframe>'
                                       '<a href="javascript:alert(1)">Unsafe</a>'))
        self.assertIn("[Embedded media](https://www.canva.com/design/example)", text)
        self.assertNotIn("javascript:", text)

    def test_pagination_youtube_selection_and_stable_manifest(self):
        def respond(request):
            page = request.url.params.get("page", "1")
            if page == "1":
                return httpx.Response(200, json={"articles": [article(1), {**article(9), "draft": True}],
                    "next_page": "https://support.optisigns.com/api/v2/help_center/en-us/articles.json?page=2"})
            return httpx.Response(200, json={"articles": [article(2, "How to use YouTube"), article(3)], "next_page": None})
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(respond)) as client:
            result = scrape(Path(tmp), client=client, limit=2)
            self.assertEqual(result["articles_written"], 2)
            self.assertIn(2, result["article_ids"])
            self.assertEqual(scrape(Path(tmp), client=client, limit=2)["article_ids"], result["article_ids"])
            self.assertEqual(len(list((Path(tmp) / "articles").glob("*.md"))), 2)

    def test_cross_origin_pagination_is_rejected(self):
        def respond(request):
            return httpx.Response(200, json={"articles": [article(1)], "next_page": "https://example.com/private"})
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(respond)) as client:
            with self.assertRaises(ValueError):
                scrape(Path(tmp), client=client, limit=1)

    def test_daily_discovery_retains_seed_and_adds_new_public_articles(self):
        items = [article(1, "YouTube Guide"), article(2)]
        def respond(request):
            return httpx.Response(200, json={"articles": items, "next_page": None})
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(respond)) as client:
            root = Path(tmp)
            self.assertEqual(scrape(root, client=client, limit=1)["article_ids"], [1])
            items.append(article(3, "New public guide"))
            # A manual refresh must not consume discovery work meant for the daily job.
            self.assertEqual(scrape(root, client=client, limit=1)["article_ids"], [1])
            self.assertEqual(scrape(root, client=client, limit=1, discover_new=True)["article_ids"], [1, 3])

    def test_failed_pagination_does_not_advance_manifest(self):
        from optibot.storage import write_json, read_json
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = {"article_ids": [1], "discovery_watermark": "old"}
            write_json(root / "manifest.json", original)
            with httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(503))) as client:
                from unittest.mock import patch
                with patch("optibot.scrape.time.sleep"), self.assertRaises(httpx.HTTPStatusError):
                    scrape(root, client=client, limit=1, discover_new=True)
            self.assertEqual(read_json(root / "manifest.json", None), original)


if __name__ == "__main__":
    unittest.main()

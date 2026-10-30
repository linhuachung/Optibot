"""Fetch public English Zendesk articles and persist a stable Markdown corpus."""

import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify

from optibot.storage import read_json, write_json

ARTICLES_URL = "https://support.optisigns.com/api/v2/help_center/en-us/articles.json"


def check_source_url(url: str):
    parsed = urlparse(url)
    if (parsed.scheme != "https" or parsed.netloc != "support.optisigns.com"
            or not parsed.path.startswith("/api/v2/help_center/")):
        raise ValueError("Refusing a pagination URL outside the public Help Center API")


def fetch_articles(client: httpx.Client):
    url = ARTICLES_URL + "?per_page=100"
    seen = set()
    articles = {}
    while url:
        check_source_url(url)
        if url in seen or len(seen) >= 100:
            raise ValueError("Repeated or excessive Zendesk pagination")
        seen.add(url)
        response = client.get(url)
        response.raise_for_status()
        page = response.json()
        for item in page["articles"]:
            if (not item.get("draft") and item.get("locale", "en-us") == "en-us"
                    and isinstance(item.get("body"), str) and item["body"].strip()):
                article_id = item["id"]
                if not isinstance(article_id, int) or isinstance(article_id, bool) or article_id <= 0:
                    raise ValueError("Invalid article ID")
                articles[article_id] = item
        url = page.get("next_page")
    return articles, len(seen)


def code_language(element):
    code = element.find("code")
    classes = (code or element).get("class", [])
    return next((name.removeprefix("language-") for name in classes if name.startswith("language-")), "")


def article_markdown(article: dict) -> str:
    soup = BeautifulSoup(article["body"], "html.parser")
    for node in soup.select("script, style, nav, aside, footer, [role=navigation], .ads, .advertisement"):
        node.decompose()
    for media in soup.find_all(["iframe", "video"]):
        source = media.get("src")
        if source and urlparse(source).scheme in ("https", "http"):
            link = soup.new_tag("a", href=source)
            link.string = "Embedded media"
            media.replace_with(link)
    for link in soup.find_all("a", href=True):
        if urlparse(link["href"]).scheme.lower() not in ("", "http", "https", "mailto"):
            del link["href"]
    body = markdownify(str(soup), heading_style="ATX", bullets="-", code_language_callback=code_language,
                      keep_inline_images_in=["td", "th"]).strip()
    if not body:
        raise ValueError(f"Article {article['id']} has no readable content")
    title = " ".join(article["title"].split())
    url = article["html_url"]
    if urlparse(url).scheme != "https" or urlparse(url).netloc != "support.optisigns.com":
        raise ValueError("Article URL must identify the source Help Center")
    return (f"# {title}\n\nArticle URL: {url}\nArticle ID: {article['id']}\n"
            f"Source updated: {article.get('updated_at', '')}\n\n{body}\n")


def content_hash(markdown: str) -> str:
    # Only remove our header timestamp, never a coincidentally matching body line.
    header, body = markdown.replace("\r\n", "\n").split("\n\n", 2)[1:]
    stable_header = "\n".join(line for line in header.splitlines() if not line.startswith("Source updated:"))
    title = markdown.split("\n", 1)[0]
    return hashlib.sha256(f"{title}\n\n{stable_header}\n\n{body}".encode("utf-8")).hexdigest()


def select_ids(articles: dict, limit: int):
    youtube = [key for key, item in articles.items() if "youtube" in item["title"].lower()]
    if not youtube:
        raise ValueError("Cannot seed corpus without a YouTube article")
    preferred = sorted(youtube)
    # Include useful sample questions and at least one formatting-rich article.
    for pattern in (r"<pre\b", r"playlist", r"schedule", r"upload", r"pair"):
        for key in sorted(articles):
            item = articles[key]
            target = item["body"] if pattern.startswith("<") else item["title"]
            if key not in preferred and re.search(pattern, target, re.IGNORECASE):
                preferred.append(key)
                break
    return (preferred + [key for key in sorted(articles) if key not in preferred])[:limit]


def scrape(data_dir: Path, *, client=None, limit=30):
    if limit < 1:
        raise ValueError("Article limit must be positive")
    if client is None:
        with httpx.Client(timeout=30, follow_redirects=False, transport=httpx.HTTPTransport(retries=2)) as owned:
            return scrape(data_dir, client=owned, limit=limit)
    articles, pages = fetch_articles(client)
    manifest_path = data_dir / "manifest.json"
    previous = read_json(manifest_path, None)
    ids = previous["article_ids"] if previous else select_ids(articles, limit)
    if len(ids) < limit:
        raise ValueError(f"Only {len(ids)} selected articles; need {limit}")
    missing = set(ids) - articles.keys()
    if missing:
        raise ValueError(f"Selected articles missing or unpublished: {sorted(missing)}")
    rendered = {key: article_markdown(articles[key]) for key in ids}
    output = data_dir / "articles"
    output.mkdir(parents=True, exist_ok=True)
    for key, text in rendered.items():
        (output / f"{key}.md").write_text(text, encoding="utf-8", newline="\n")
    # Save selected raw source bodies for reproducible quality inspection, not upload.
    write_json(data_dir / "source-articles.json", [articles[key] for key in ids])
    manifest = {
        "article_ids": ids,
        "discovery_watermark": previous["discovery_watermark"] if previous else max(
            (item.get("created_at", "") for item in articles.values()), default=""),
        "selection_policy": "Stable 30-article seed including YouTube and formatting examples; daily new-article discovery deferred to Step 3.",
        "articles": {str(key): {"title": articles[key]["title"], "url": articles[key]["html_url"],
                               "hash": content_hash(rendered[key]), "updated_at": articles[key].get("updated_at")}
                     for key in ids},
    }
    write_json(manifest_path, manifest)
    report = {"articles_written": len(ids), "article_ids": ids, "pages_fetched": pages,
              "public_articles_seen": len(articles), "checked_at": datetime.now(timezone.utc).isoformat()}
    write_json(data_dir / "scrape-report.json", report)
    return report

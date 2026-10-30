"""Programmatic upload to a reused vector store, with resumable indexing."""

from datetime import datetime, timezone
from pathlib import Path
import sys

from openai import NotFoundError

from optibot.scrape import content_hash
from optibot.storage import read_json, write_json


def ingest(data_dir: Path, *, client, store_id=None, limit=None):
    manifest = read_json(data_dir / "manifest.json", None)
    if not manifest:
        raise ValueError("Run scrape.py before uploading")
    ids = manifest["article_ids"]
    if limit is not None:
        if limit < 1:
            raise ValueError("Upload limit must be positive")
        ids = ids[:limit]
    documents = {}
    for article_id in ids:
        key = str(article_id)
        if not key.isdecimal():
            raise ValueError("Invalid manifest article ID")
        path = data_dir / "articles" / f"{key}.md"
        text = path.read_text(encoding="utf-8")
        if content_hash(text) != manifest["articles"][key]["hash"]:
            raise ValueError(f"Article {key} differs from the manifest; re-run scrape.py")
        documents[key] = path

    state_path = data_dir / "ingestion-state.json"
    state = read_json(state_path, {"vector_store_id": None, "articles": {}, "pending": {}})
    if store_id and state["vector_store_id"] and store_id != state["vector_store_id"]:
        raise ValueError("Configured vector store differs from saved ingestion state")
    if not state["vector_store_id"]:
        state["vector_store_id"] = store_id or client.vector_stores.create(name="harbor-support-notes").id
        write_json(state_path, state)
    store_id = state["vector_store_id"]
    # SDK pagination is automatic. Reconcile attachments before creating more files.
    remote = {item.id: item for item in client.vector_stores.files.list(vector_store_id=store_id)}
    uploaded = skipped = 0
    for key, path in documents.items():
        metadata = manifest["articles"][key]
        active = state["articles"].get(key)
        if (active and active["hash"] == metadata["hash"]
                and client.vector_stores.files.retrieve(active["file_id"], vector_store_id=store_id).status == "completed"):
            skipped += 1
            continue
        pending = state["pending"].get(key)
        if pending and pending["hash"] != metadata["hash"]:
            raise ValueError(f"Article {key} changed during a pending upload; finish it before re-scraping")
        if not pending:
            matching = next((item for item in remote.values() if item.attributes
                             and item.attributes.get("article_id") == key
                             and item.attributes.get("content_hash") == metadata["hash"]), None)
            if matching:
                file_id = matching.id
            else:
                with path.open("rb") as stream:
                    file_id = client.files.create(
                        file=(f"{key}-{metadata['hash'][:12]}.md", stream, "text/markdown"), purpose="assistants").id
            pending = {"file_id": file_id, "hash": metadata["hash"]}
            state["pending"][key] = pending
            write_json(state_path, state)
        file_id = pending["file_id"]
        try:
            indexed = client.vector_stores.files.retrieve(file_id, vector_store_id=store_id)
        except NotFoundError:
            indexed = None
        if indexed is None or indexed.status != "completed":
            if indexed and indexed.status in ("failed", "cancelled"):
                client.vector_stores.files.delete(file_id, vector_store_id=store_id)
            if indexed and indexed.status == "in_progress":
                indexed = client.vector_stores.files.poll(file_id, vector_store_id=store_id, max_wait_seconds=180)
            else:
                indexed = client.vector_stores.files.create_and_poll(
                    vector_store_id=store_id, file_id=file_id,
                    attributes={"article_id": key, "content_hash": metadata["hash"]},
                    max_wait_seconds=180,
                )
        if indexed.status != "completed":
            raise RuntimeError(f"Indexing did not complete for article {key}: {indexed.status}")
        if active and active["file_id"] != file_id:
            try:
                client.vector_stores.files.delete(active["file_id"], vector_store_id=store_id)
            except NotFoundError:
                pass
        state["articles"][key] = {**metadata, "file_id": file_id}
        del state["pending"][key]
        write_json(state_path, state)
        uploaded += 1
        print(f"article={key} indexing=completed", file=sys.stderr, flush=True)
    report = {
        "vector_store_id": store_id, "uploaded": uploaded, "skipped": skipped,
        "completed_files": len(state["articles"]),
        "embedded_chunks": None,
        "chunk_count_status": "unavailable: managed index API does not document an exact embedded chunk total",
        "chunking_strategy": "auto (provider default; documented as 800 tokens with 400 overlap)",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(data_dir / "upload-report.json", report)
    return report

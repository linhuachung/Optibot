"""Programmatic delta upload with durable intents and replacement recovery."""
import sys
from datetime import datetime, timezone
from pathlib import Path
from openai import APIStatusError, NotFoundError
from optibot.scrape import content_hash
from optibot.storage import read_json, write_json


def empty_counts():
    return {"added": 0, "updated": 0, "skipped": 0, "failed": 0}


def finish_pending(data_dir, client, state, key, counts):
    pending = state["pending"][key]
    store_id = state["vector_store_id"]
    metadata = pending.get("metadata")
    if metadata is None:
        metadata = read_json(data_dir / "manifest.json", {})["articles"][key]
        if metadata["hash"] != pending["hash"]:
            raise RuntimeError("Legacy pending upload differs from manifest; manual reconciliation required")
    if not pending.get("file_id"):
        matches = [item for item in client.files.list(purpose="assistants") if item.filename == pending["filename"]]
        if len(matches) != 1:
            raise RuntimeError("Ambiguous upload outcome; reconcile the journal filename with provider Files before retrying")
        pending["file_id"] = matches[0].id
        write_json(data_dir / "ingestion-state.json", state)
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
                attributes={"article_id": key, "content_hash": pending["hash"]}, max_wait_seconds=180)
    if indexed.status != "completed":
        raise RuntimeError(f"Indexing did not complete for article {key}: {indexed.status}")
    active = state["articles"].get(key)
    if active and active["file_id"] != file_id:
        try:
            client.vector_stores.files.delete(active["file_id"], vector_store_id=store_id)
        except NotFoundError:
            pass
    state["articles"][key] = {**metadata, "file_id": file_id}
    del state["pending"][key]
    write_json(data_dir / "ingestion-state.json", state)
    counts["updated" if active else "added"] += 1
    print(f"article={key} indexing=completed", file=sys.stderr, flush=True)


def resume_pending(data_dir: Path, *, client, store_id=None, counts=None):
    state = read_json(data_dir / "ingestion-state.json", None)
    if not state:
        return set()
    if store_id and store_id != state["vector_store_id"]:
        raise ValueError("Configured vector store differs from saved ingestion state")
    counts = counts if counts is not None else empty_counts()
    resumed = set(state["pending"])
    for key in sorted(resumed):
        finish_pending(data_dir, client, state, key, counts)
    return resumed


def ingest(data_dir: Path, *, client, store_id=None, limit=None, counts=None, completed_ids=None):
    counts = counts if counts is not None else empty_counts()
    completed_ids = set(completed_ids or ()) | resume_pending(data_dir, client=client, store_id=store_id, counts=counts)
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
        if content_hash(path.read_text(encoding="utf-8")) != manifest["articles"][key]["hash"]:
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
    remote = list(client.vector_stores.files.list(vector_store_id=store_id))
    for key, path in documents.items():
        metadata = manifest["articles"][key]
        active = state["articles"].get(key)
        if active and active["hash"] == metadata["hash"]:
            try:
                if key in completed_ids or client.vector_stores.files.retrieve(active["file_id"], vector_store_id=store_id).status == "completed":
                    if key not in completed_ids:
                        counts["skipped"] += 1
                    continue
            except NotFoundError:
                pass
        matching = next((item for item in remote if item.attributes
                         and item.attributes.get("article_id") == key
                         and item.attributes.get("content_hash") == metadata["hash"]), None)
        filename = f"{store_id}-{key}-{metadata['hash']}.md"
        pending = {"file_id": matching.id if matching else None, "hash": metadata["hash"],
                   "filename": filename, "metadata": metadata}
        state["pending"][key] = pending
        write_json(state_path, state)
        if not matching:
            try:
                with path.open("rb") as stream:
                    uploaded = client.with_options(max_retries=0).files.create(
                        file=(filename, stream, "text/markdown"), purpose="assistants")
                pending["file_id"] = uploaded.id
                write_json(state_path, state)
            except APIStatusError as error:
                if error.status_code < 500 and error.status_code not in (408, 409):
                    del state["pending"][key]
                    write_json(state_path, state)
                raise
        finish_pending(data_dir, client, state, key, counts)
    report = {
        **counts, "vector_store_id": store_id, "uploaded": counts["added"] + counts["updated"],
        "completed_files": len(state["articles"]), "embedded_chunks": None,
        "chunk_count_status": "unavailable: managed index API does not document an exact embedded chunk total",
        "chunking_strategy": "auto (provider default; documented as 800 tokens with 400 overlap)",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(data_dir / "upload-report.json", report)
    return report

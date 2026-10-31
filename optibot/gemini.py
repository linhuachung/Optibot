"""Gemini-native File Search ingestion and grounded queries; separate provider state."""
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

from optibot.config import PROMPT_PATH
from optibot.scrape import content_hash
from optibot.storage import read_json, write_json


def gemini_client():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("Set GEMINI_API_KEY in the backend .env")
    return genai.Client(api_key=key, http_options={"timeout": 30000, "retry_options": {"attempts": 1}})


def active(document):
    return str(document.state).split(".")[-1] == "STATE_ACTIVE"


def owned_document(client, store, display_name):
    matches = [d for d in client.file_search_stores.documents.list(parent=store) if d.display_name == display_name]
    if len(matches) > 1:
        raise RuntimeError("Ambiguous Gemini upload; reconcile duplicate owned document names")
    return matches[0] if matches else None


def finish_gemini(data_dir, client, state, key, counts, *, fresh=False):
    pending = state["pending"][key]
    store = state["vector_store_id"]
    if not pending.get("file_id"):
        if pending.get("operation"):
            operation = types.UploadToFileSearchStoreOperation(name=pending["operation"])
            deadline = time.monotonic() + 180
            while True:
                operation = client.operations.get(operation)
                if operation.done:
                    break
                if time.monotonic() >= deadline:
                    raise RuntimeError("Gemini indexing timeout; operation retained for retry")
                time.sleep(2)
            if operation.error:
                raise RuntimeError("Gemini indexing failed; inspect retained operation before retrying")
            pending["file_id"] = operation.response.document_name
        else:
            document = owned_document(client, store, pending["display_name"])
            if document:
                pending["file_id"] = document.name
            elif fresh:
                operation = client.file_search_stores.upload_to_file_search_store(
                    file_search_store_name=store, file=data_dir / "articles" / (key + ".md"),
                    config={"display_name": pending["display_name"], "mime_type": "text/markdown",
                            "custom_metadata": [{"key": "article_id", "string_value": key},
                                                {"key": "content_hash", "string_value": pending["metadata"]["hash"]}],
                            "chunking_config": {"white_space_config": {"max_tokens_per_chunk": 400, "max_overlap_tokens": 80}}})
                pending["operation"] = operation.name
                write_json(data_dir / "gemini-state.json", state)
                if operation.done:
                    if operation.error:
                        raise RuntimeError("Gemini indexing failed; operation retained")
                    pending["file_id"] = operation.response.document_name
                else:
                    return finish_gemini(data_dir, client, state, key, counts)
            else:
                raise RuntimeError("Ambiguous Gemini upload outcome; reconcile owned display name before retrying")
        write_json(data_dir / "gemini-state.json", state)
    document = client.file_search_stores.documents.get(name=pending["file_id"])
    if not active(document):
        raise RuntimeError("Gemini document not active; pending state retained")
    previous = state["articles"].get(key)
    if previous and previous["file_id"] != pending["file_id"]:
        try:
            client.file_search_stores.documents.delete(name=previous["file_id"], config={"force": True})
        except errors.ClientError as error:
            if error.code != 404:
                raise
    state["articles"][key] = {**pending["metadata"], "file_id": pending["file_id"], "display_name": pending["display_name"]}
    del state["pending"][key]
    write_json(data_dir / "gemini-state.json", state)
    counts["updated" if previous else "added"] += 1


def resume_gemini(data_dir, *, client, counts):
    state = read_json(data_dir / "gemini-state.json", None)
    if state and state.get("provider") != "gemini":
        raise ValueError("Refusing non-Gemini provider state")
    configured = os.getenv("GEMINI_FILE_SEARCH_STORE")
    if state and configured and configured != state["vector_store_id"]:
        raise ValueError("Configured Gemini store differs from saved state")
    completed = set(state["pending"]) if state else set()
    for key in sorted(completed):
        finish_gemini(data_dir, client, state, key, counts)
    return completed


def ingest_gemini(data_dir, *, client, counts=None, completed_ids=None, limit=None):
    if limit is not None and limit < 1:
        raise ValueError("Upload limit must be positive")
    counts = counts if counts is not None else dict(added=0, updated=0, skipped=0, failed=0)
    completed = set(completed_ids or ()) | resume_gemini(data_dir, client=client, counts=counts)
    manifest = read_json(data_dir / "manifest.json", None)
    if not manifest:
        raise ValueError("Run scrape.py first")
    ids = manifest["article_ids"] if limit is None else manifest["article_ids"][:limit]
    for article_id in ids:
        key = str(article_id)
        if not key.isdecimal():
            raise ValueError("Invalid article ID")
        text = (data_dir / "articles" / (key + ".md")).read_text(encoding="utf-8")
        if content_hash(text) != manifest["articles"][key]["hash"]:
            raise ValueError("Markdown differs from manifest; rescrape before uploading")
    state = read_json(data_dir / "gemini-state.json", None)
    if state is None:
        configured = os.getenv("GEMINI_FILE_SEARCH_STORE")
        if not configured:
            stores = [s for s in client.file_search_stores.list() if s.display_name == "harbor-gemini-notes"]
            if len(stores) > 1:
                raise RuntimeError("Multiple Gemini stores match; configure GEMINI_FILE_SEARCH_STORE")
            configured = stores[0].name if stores else client.file_search_stores.create(config={"display_name": "harbor-gemini-notes"}).name
        state = {"provider": "gemini", "vector_store_id": configured, "articles": {}, "pending": {}}
        write_json(data_dir / "gemini-state.json", state)
    if state.get("provider") != "gemini":
        raise ValueError("Refusing non-Gemini provider state")
    configured = os.getenv("GEMINI_FILE_SEARCH_STORE")
    if configured and configured != state["vector_store_id"]:
        raise ValueError("Configured Gemini store differs from saved state")
    for article_id in ids:
        key = str(article_id)
        metadata = manifest["articles"][key]
        previous = state["articles"].get(key)
        if previous and previous["hash"] == metadata["hash"]:
            try:
                if active(client.file_search_stores.documents.get(name=previous["file_id"])):
                    if key not in completed:
                        counts["skipped"] += 1
                    continue
            except errors.ClientError as error:
                if error.code != 404:
                    raise
        state["pending"][key] = {"metadata": metadata, "display_name": f"article-{key}-{metadata['hash']}", "operation": None, "file_id": None}
        write_json(data_dir / "gemini-state.json", state)
        finish_gemini(data_dir, client, state, key, counts, fresh=True)
    report = {**counts, "provider": "gemini", "vector_store_id": state["vector_store_id"],
              "completed_files": len(state["articles"]), "embedded_chunks": None,
              "chunking_strategy": "Gemini white-space chunking: 400 tokens, 80 overlap",
              "chunk_count_status": "Exact embedded count not exposed by inspected document/store API",
              "checked_at": datetime.now(timezone.utc).isoformat()}
    write_json(data_dir / "gemini-upload-report.json", report)
    return report


def query_gemini(client, store, question, model, articles, *, require_citations=False, search=False):
    response = client.models.generate_content(model=model, contents=question, config={
        "system_instruction": PROMPT_PATH.read_text(encoding="utf-8").rstrip("\n"),
        "tools": [{"file_search": {"file_search_store_names": [store]}}]})
    if not response.candidates or not response.text:
        raise RuntimeError("Gemini returned no usable answer")
    metadata = response.candidates[0].grounding_metadata
    known = {item["display_name"]: (key, item) for key, item in articles.items()}
    by_name = {item["file_id"]: (key, item) for key, item in articles.items()}
    citations, matches = {}, []
    for chunk in (metadata.grounding_chunks or []) if metadata else []:
        context = chunk.retrieved_context
        if not context:
            continue
        if context.file_search_store and context.file_search_store != store:
            raise RuntimeError("Gemini grounded outside the configured store")
        found = by_name.get(context.document_name) or known.get(context.title)
        if not found:
            raise RuntimeError("Gemini cited a document outside the saved corpus")
        key, item = found
        source = {"article_id": key, "title": item["title"], "url": item["url"]}
        citations[key] = source
        if context.text:
            matches.append({**source, "excerpt": context.text[:2000]})
    if require_citations and not citations:
        raise RuntimeError("Supported answer has no verifiable Gemini grounding")
    return {"provider": "gemini", "model": model, "question": question, "answer": None if search else response.text,
            "citations": list(citations.values())[:3], "matches": matches[:3],
            "vector_store_id": store, "checked_at": datetime.now(timezone.utc).isoformat()}

"""Run grounded Responses queries and resolve file citations to source URLs."""

from datetime import datetime, timezone

from optibot.config import PROMPT_PATH


def retrieve(client, store_id, question, articles):
    known = {item["file_id"]: {"article_id": key, "url": item["url"], "title": item["title"]}
             for key, item in articles.items()}
    result = client.vector_stores.search(store_id, query=question, max_num_results=3)
    matches = []
    for item in result.data:
        if item.file_id not in known:
            raise RuntimeError("Search returned a file outside the local uploaded corpus")
        matches.append({**known[item.file_id], "file_id": item.file_id, "score": item.score,
                        "excerpt": "\n".join(part.text for part in item.content if part.type == "text")[:2000]})
    return {"question": question, "result": "retrieval_only", "matches": matches,
            "vector_store_id": store_id, "checked_at": datetime.now(timezone.utc).isoformat()}


def answer(client, store_id, question, model, articles, *, require_citations=False):
    response = client.responses.create(
        model=model, input=question,
        instructions=PROMPT_PATH.read_text(encoding="utf-8").rstrip("\n"),
        tools=[{"type": "file_search", "vector_store_ids": [store_id], "max_num_results": 5}],
        tool_choice="required", include=["file_search_call.results"], store=False,
    )
    if response.status != "completed":
        raise RuntimeError(f"Response did not complete: {response.status}")
    known = {item["file_id"]: {"article_id": key, "url": item["url"], "title": item["title"]}
             for key, item in articles.items()}
    citations = {}
    for item in response.output:
        if item.type != "message":
            continue
        for part in item.content:
            if part.type != "output_text":
                continue
            for annotation in part.annotations:
                if annotation.type == "file_citation":
                    if annotation.file_id not in known:
                        raise RuntimeError("Response cited a file outside the local uploaded corpus")
                    citations[annotation.file_id] = known[annotation.file_id]
    if require_citations and not citations:
        raise RuntimeError("Supported answer has no verifiable file citations")
    return {"question": question, "answer": response.output_text, "citations": list(citations.values()),
            "response_id": response.id, "model": model, "vector_store_id": store_id,
            "checked_at": datetime.now(timezone.utc).isoformat()}

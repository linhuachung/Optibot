"""Select trusted prior workflow state or bootstrap once from encrypted secrets."""

import argparse
import json
import os
from pathlib import Path
from urllib.request import HTTPRedirectHandler, Request, build_opener


def select_state(get, repository, run_id, attempt):
    base = f"/repos/{repository}/actions"
    workflow_id = get(base + "/workflows/daily.yml")["id"]
    current_name = f"optibot-state-{run_id}-{attempt}"
    candidates = []
    for page in range(1, 11):
        items = get(base + f"/artifacts?per_page=100&page={page}")["artifacts"]
        candidates.extend(item for item in items
                          if item["name"].startswith("optibot-state-") and item["name"] != current_name)
        if len(items) < 100:
            break
    for artifact in sorted(candidates, key=lambda item: item["created_at"], reverse=True):
        source_run_id = artifact["workflow_run"]["id"]
        run = get(base + f"/runs/{source_run_id}")
        trusted = (run["workflow_id"] == workflow_id and run["event"] in ("workflow_dispatch", "schedule")
                   and run["head_branch"] == "main"
                   and (run.get("head_repository") or {}).get("full_name") == repository)
        if trusted:
            if artifact["expired"]:
                raise RuntimeError("Latest trusted state expired; restore a verified backup before resuming")
            return {"artifact_id": int(artifact["id"]), "run_id": int(source_run_id)}
    prior = get(base + "/workflows/daily.yml/runs?per_page=100")["workflow_runs"]
    if any(run["id"] != run_id and run["event"] in ("workflow_dispatch", "schedule")
           and run["head_branch"] == "main" for run in prior):
        raise RuntimeError("Previous daily run exists but state is missing; refusing to reset the corpus")
    return None


def bootstrap(data_dir, manifest_json, state_json, store_id):
    manifest, state = json.loads(manifest_json), json.loads(state_json)
    if not store_id or state["vector_store_id"] != store_id:
        raise ValueError("Bootstrap store ID differs from configured store")
    if not manifest["article_ids"] or not isinstance(state["articles"], dict) or not isinstance(state["pending"], dict):
        raise ValueError("Invalid bootstrap state")
    data_dir.mkdir(parents=True, exist_ok=True)
    for name, value in (("manifest.json", manifest), ("ingestion-state.json", state)):
        target = data_dir / name
        if target.exists():
            raise ValueError("Refusing to overwrite an existing restored state file")
        target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_gemini(data_dir, state_json, store_id):
    """One-time provider migration, then require trusted artifacts to retain state."""
    from optibot.storage import read_json, write_json
    target = data_dir / "gemini-state.json"
    marker = data_dir / "gemini-migration.json"
    if target.exists():
        state = read_json(target, None)
    else:
        if marker.exists():
            raise RuntimeError("Gemini state missing after migration; restore verified backup")
        state = json.loads(state_json)
        if state.get("pending"):
            raise ValueError("Finish pending Gemini operations before cloud bootstrap")
    if (state.get("provider") != "gemini" or state.get("vector_store_id") != store_id
            or not isinstance(state.get("articles"), dict) or not state["articles"]
            or not isinstance(state.get("pending"), dict)):
        raise ValueError("Invalid Gemini bootstrap/state or configured store mismatch")
    if not target.exists():
        write_json(target, state)
    write_json(marker, {"provider": "gemini", "vector_store_id": store_id})


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        raise RuntimeError("Refusing to redirect an authenticated GitHub API request")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["select", "bootstrap", "gemini"])
    args = parser.parse_args()
    if args.mode == "gemini":
        prepare_gemini(Path("data"), os.environ.get("GEMINI_BOOTSTRAP_STATE", ""), os.environ["GEMINI_FILE_SEARCH_STORE"])
        print("Confirmed durable Gemini provider state")
        return
    if args.mode == "bootstrap":
        bootstrap(Path("data"), os.environ["BOOTSTRAP_MANIFEST"], os.environ["BOOTSTRAP_STATE"],
                  os.environ["OPENAI_VECTOR_STORE_ID"])
        print("Restored initial verified corpus state")
        return
    opener = build_opener(NoRedirect())
    def get(path):
        request = Request("https://api.github.com" + path, headers={
            "Authorization": "Bearer " + os.environ["GH_TOKEN"],
            "Accept": "application/vnd.github+json", "User-Agent": "optibot-state"})
        with opener.open(request, timeout=30) as response:
            return json.load(response)
    selected = select_state(get, os.environ["GITHUB_REPOSITORY"], int(os.environ["GITHUB_RUN_ID"]),
                            int(os.environ["GITHUB_RUN_ATTEMPT"]))
    with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
        output.write(f"found={'true' if selected else 'false'}\n")
        if selected:
            for name, value in selected.items():
                output.write(f"{name}={value}\n")
    print("Selected trusted prior state" if selected else "First daily run: bootstrap required")


if __name__ == "__main__":
    main()

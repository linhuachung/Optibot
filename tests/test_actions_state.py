import tempfile
import unittest
from pathlib import Path

from scripts.actions_state import bootstrap, select_state


class ActionsStateTests(unittest.TestCase):
    def getter(self, *, artifacts=None, runs=None, event="workflow_dispatch"):
        def get(path):
            if path.endswith("/daily.yml"):
                return {"id": 7}
            if "/artifacts?" in path:
                return {"artifacts": artifacts or []}
            if "/daily.yml/runs?" in path:
                return {"workflow_runs": runs or []}
            return {"workflow_id": 7, "event": event, "head_branch": "main",
                    "head_repository": {"full_name": "owner/repo"}}
        return get

    def test_selects_prior_trusted_daily_artifact(self):
        artifact = {"id": 5, "name": "optibot-state-10-1", "created_at": "2026-10-30", "expired": False,
                    "workflow_run": {"id": 10}}
        self.assertEqual(select_state(self.getter(artifacts=[artifact]), "owner/repo", 11, 1)["artifact_id"], 5)

    def test_untrusted_pull_request_artifact_is_not_restored(self):
        artifact = {"id": 5, "name": "optibot-state-10-1", "created_at": "2026-10-30", "expired": False,
                    "workflow_run": {"id": 10}}
        result = select_state(self.getter(artifacts=[artifact], event="pull_request"), "owner/repo", 11, 1)
        self.assertIsNone(result)

    def test_missing_or_expired_state_does_not_silently_reset(self):
        with self.assertRaises(RuntimeError):
            select_state(self.getter(runs=[{"id": 10, "event": "workflow_dispatch", "head_branch": "main"}]),
                         "owner/repo", 11, 1)

    def test_bootstrap_requires_a_matching_existing_store(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                bootstrap(Path(tmp), json.dumps({"article_ids": [1]}),
                          json.dumps({"vector_store_id": "vs_one", "articles": {}, "pending": {}}), "vs_other")

    def test_gemini_bootstrap_never_resets_a_lost_migrated_state(self):
        import tempfile, json
        from pathlib import Path
        from scripts.actions_state import prepare_gemini
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = {"provider": "gemini", "vector_store_id": "fileSearchStores/test", "articles": {"1": {}}, "pending": {}}
            prepare_gemini(root, json.dumps(state), state["vector_store_id"])
            prepare_gemini(root, "", state["vector_store_id"])
            (root / "gemini-state.json").unlink()
            with self.assertRaises(RuntimeError):
                prepare_gemini(root, json.dumps(state), state["vector_store_id"])

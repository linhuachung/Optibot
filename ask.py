"""Query the API-loaded store; JSON evidence is not a provider UI screenshot."""

import argparse
import json
import os
import httpx
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError
from google.genai.errors import APIError as GeminiAPIError

from optibot.answer import answer, retrieve
from optibot.config import api_client
from optibot.storage import read_json, write_json


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?", default="How do I add a YouTube video?")
    parser.add_argument("--provider", choices=["openai", "gemini"], default=os.getenv("AI_PROVIDER", "openai"))
    parser.add_argument("--model")
    parser.add_argument("--data-dir", type=Path, default=Path(os.getenv("DATA_DIR", "data")))
    parser.add_argument("--require-citations", action="store_true", help="Fail if a supported question has no known file citations")
    parser.add_argument("--retrieve-only", action="store_true", help="Return source excerpts; Gemini uses model-backed lookup and generation quota")
    parser.add_argument("--output", type=Path, help="Save API evidence JSON, distinct from required UI screenshot")
    args = parser.parse_args()
    try:
        state = read_json(args.data_dir / ("gemini-state.json" if args.provider == "gemini" else "ingestion-state.json"), None)
        if not state or not state["articles"]:
            raise ValueError("Run upload.py before asking questions")
        if args.provider == "gemini":
            from optibot.gemini import gemini_client, query_gemini
            with gemini_client() as client:
                report = query_gemini(client, state["vector_store_id"], args.question,
                    args.model or os.getenv("GEMINI_MODEL") or "gemini-3.5-flash-lite", state["articles"],
                    require_citations=args.require_citations, search=args.retrieve_only)
        else:
            with api_client() as client:
                if args.retrieve_only:
                    report = retrieve(client, state["vector_store_id"], args.question, state["articles"])
                else:
                    report = answer(client, state["vector_store_id"], args.question, args.model or os.getenv("OPENAI_MODEL") or "gpt-4.1-mini", state["articles"],
                                    require_citations=args.require_citations)
        if args.output:
            write_json(args.output, report)
        print(json.dumps(report, ensure_ascii=True, indent=2))
    except APIError as error:
        print(f"OpenAI request failed: {type(error).__name__}, HTTP {getattr(error, 'status_code', None)}", file=sys.stderr)
        if getattr(error, "code", None) in ("credit_balance_exhausted", "insufficient_quota"):
            print("The API project has no available credits. Fund it or configure a funded key, then retry.", file=sys.stderr)
        return 1
    except httpx.RequestError:
        print("AI service connection failed; retry later.", file=sys.stderr)
        return 1
    except GeminiAPIError as error:
        print(f"Gemini request failed, HTTP {error.code}", file=sys.stderr)
        return 1
    except (ValueError, RuntimeError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Run the daily scraper/uploader once, write evidence, and exit."""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from optibot.job import run_job


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path(os.getenv("STATE_DIR") or os.getenv("DATA_DIR", "data")))
    parser.add_argument("--provider", choices=["openai", "gemini"], default=os.getenv("AI_PROVIDER", "openai"))
    parser.add_argument("--limit", type=int, default=30, help="Minimum seed size on bootstrap")
    args = parser.parse_args()
    try:
        report = run_job(args.data_dir, limit=args.limit, store_id=os.getenv("OPENAI_VECTOR_STORE_ID") or None, provider=args.provider)
    except (RuntimeError, OSError) as error:
        print(json.dumps({"status": "failed", "error_type": type(error).__name__, "failed": 1}), file=sys.stderr)
        return 1
    print(" ".join(f"{key}={report[key]}" for key in ("added", "updated", "skipped", "failed")))
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())

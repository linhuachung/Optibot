"""Step 2: python upload.py [--limit 1] [--data-dir data]."""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError

from optibot.config import api_client
from optibot.ingest import ingest


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path(os.getenv("DATA_DIR", "data")))
    parser.add_argument("--limit", type=int, help="Use 1 for a narrow initial smoke test")
    args = parser.parse_args()
    try:
        with api_client() as client:
            report = ingest(args.data_dir, client=client, store_id=os.getenv("OPENAI_VECTOR_STORE_ID") or None, limit=args.limit)
        print(json.dumps(report, indent=2))
    except APIError as error:
        # Provider exception messages may echo credentials; never print them.
        print(f"OpenAI request failed: {type(error).__name__}, HTTP {getattr(error, 'status_code', None)}", file=sys.stderr)
        if getattr(error, "code", None) in ("credit_balance_exhausted", "insufficient_quota"):
            print("The API project has no available credits. Fund it or configure a funded key, then retry.", file=sys.stderr)
        return 1
    except (ValueError, RuntimeError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

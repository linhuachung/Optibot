"""Step 1: python scrape.py [--limit 30] [--data-dir data]."""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from optibot.scrape import scrape
from optibot.lock import job_lock


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--data-dir", type=Path, default=Path(os.getenv("DATA_DIR", "data")))
    args = parser.parse_args()
    with job_lock(args.data_dir):
        report = scrape(args.data_dir, limit=args.limit)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

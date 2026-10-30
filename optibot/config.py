import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def api_client():
    load_dotenv()
    key = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("Set API_KEY or OPENAI_API_KEY in your local .env")
    return OpenAI(api_key=key, timeout=30, max_retries=2)


PROMPT_PATH = Path(__file__).resolve().parent.parent / "system_prompt.txt"

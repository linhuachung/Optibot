"""Local read-only chat API; ingestion remains a separate one-shot job."""

import os
import httpx
from pathlib import Path
from threading import BoundedSemaphore
from typing import Literal
from urllib.parse import urlparse

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from openai import APIError
from google.genai.errors import APIError as GeminiAPIError
from pydantic import BaseModel, ConfigDict, Field
from starlette.middleware.trustedhost import TrustedHostMiddleware

from optibot.answer import answer, retrieve
from optibot.config import api_client
from optibot.storage import read_json

ROOT = Path(__file__).resolve().parent.parent
ORIGINS = [f"http://{host}:{port}" for host in ("127.0.0.1", "localhost") for port in (8000, 5173)]


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    question: str = Field(min_length=1, max_length=2000)
    mode: Literal["search", "answer"] = "search"


def problem(status, code, message):
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


def public_source(item):
    url = urlparse(item["url"])
    if url.scheme != "https" or url.netloc != "support.optisigns.com":
        raise RuntimeError("Invalid source URL")
    return {key: item[key] for key in ("title", "url", "excerpt") if key in item}


class InvalidStateError(ValueError):
    """Saved corpus is not safe/usable for the read-only API."""


def read_corpus(directory, provider="openai"):
    try:
        state = read_json(directory / ("gemini-state.json" if provider == "gemini" else "ingestion-state.json"), None)
        if state is None:
            return None
        if not isinstance(state, dict) or not isinstance(state.get("articles"), dict):
            raise ValueError("Invalid corpus shape")
        if provider == "gemini" and state.get("provider") != "gemini":
            raise ValueError("Wrong provider state")
        if state["articles"] and (not isinstance(state.get("vector_store_id"), str) or not state["vector_store_id"].strip()):
            raise ValueError("Missing store ID")
        for record in state["articles"].values():
            if not isinstance(record, dict) or any(not isinstance(record.get(key), str) or not record[key].strip()
                                                    for key in (("file_id", "title", "url", "display_name") if provider == "gemini" else ("file_id", "title", "url"))):
                raise ValueError("Invalid article record")
            public_source(record)
        return state
    except (ValueError, RuntimeError, KeyError, TypeError, OSError) as error:
        raise InvalidStateError from error


def create_app(*, data_dir=None, client_factory=None, provider=None):
    load_dotenv(ROOT / ".env")
    directory = Path(data_dir) if data_dir is not None else Path(os.getenv("STATE_DIR") or os.getenv("DATA_DIR", str(ROOT / "data")))
    provider = provider or os.getenv("AI_PROVIDER", "openai")
    if provider not in ("openai", "gemini"):
        raise ValueError("Unknown AI provider")
    if provider == "gemini":
        from optibot.gemini import gemini_client, query_gemini
    if client_factory is None:
        client_factory = gemini_client if provider == "gemini" else api_client
    app = FastAPI(title="OptiBot local API", docs_url=None, redoc_url=None)
    app.add_middleware(CORSMiddleware, allow_origins=ORIGINS, allow_methods=["GET", "POST"],
                       allow_headers=["Content-Type"], allow_credentials=False)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "testserver"])
    slots = BoundedSemaphore(2)

    @app.middleware("http")
    async def boundaries(request: Request, call_next):
        origin = request.headers.get("origin")
        if origin and origin not in ORIGINS:
            return problem(403, "origin_not_allowed", "This server accepts requests from the local app only.")
        if request.method == "POST" and request.url.path.startswith("/api/"):
            if request.headers.get("content-type", "").split(";", 1)[0].lower() != "application/json":
                return problem(415, "json_required", "Send a JSON request.")
            try:
                length = int(request.headers["content-length"])
                if length < 0:
                    raise ValueError
            except (KeyError, ValueError):
                return problem(411, "length_required", "A valid request length is required.")
            if length > 8192:
                return problem(413, "request_too_large", "Keep your question under 2,000 characters.")
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self' http://127.0.0.1:8000 http://localhost:8000; frame-ancestors 'none'; base-uri 'none'"
        return response

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request, error):
        return problem(422, "invalid_request", "Enter a question of 1–2,000 characters and choose search or answer mode.")

    @app.get("/api/health")
    def health():
        try:
            state = read_corpus(directory, provider)
            count = len(state["articles"]) if state else 0
        except (ValueError, KeyError, TypeError, OSError):
            return problem(503, "state_invalid", "Document state could not be read. Check the server setup.")
        configured = bool(os.getenv("GEMINI_API_KEY")) if provider == "gemini" else bool(os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY"))
        return {"status": "ready" if count and configured else "setup_required", "articleCount": count,
                "keyConfigured": configured, "provider": provider}

    @app.post("/api/chat")
    def chat(body: ChatRequest):
        if not slots.acquire(blocking=False):
            return problem(429, "server_busy", "Two requests are already running. Please try again shortly.")
        try:
            state = read_corpus(directory, provider)
            if not state or not state.get("articles"):
                return problem(503, "corpus_missing", "No documents are indexed yet. Run python main.py first.")
            if provider == "gemini":
                with client_factory() as client:
                    result = query_gemini(client, state["vector_store_id"], body.question,
                        os.getenv("GEMINI_MODEL") or "gemini-3.5-flash-lite", state["articles"], search=body.mode == "search")
                return {"mode": body.mode, "question": body.question,
                        "answer": result["answer"] if body.mode == "answer" else None,
                        "sources": [public_source(item) for item in (result["matches"] if body.mode == "search" else result["citations"])],
                        "notice": "Source excerpts from Gemini File Search; uses Gemini API generation quota." if body.mode == "search" else "Check the cited documentation before applying the answer."}
            with client_factory().with_options(max_retries=0) as client:
                if body.mode == "search":
                    result = retrieve(client, state["vector_store_id"], body.question, state["articles"])
                    return {"mode": "search", "question": body.question, "answer": None,
                            "sources": [public_source(item) for item in result["matches"]],
                            "notice": "Document excerpts, not a generated answer."}
                result = answer(client, state["vector_store_id"], body.question,
                                os.getenv("OPENAI_MODEL") or "gpt-4.1-mini", state["articles"])
                return {"mode": "answer", "question": body.question, "answer": result["answer"],
                        "sources": [public_source(item) for item in result["citations"]],
                        "notice": "Check the cited documentation before applying the answer."}
        except httpx.RequestError:
            return problem(502, "provider_unavailable", "The AI service could not be reached. Please retry.")
        except GeminiAPIError as error:
            if error.code == 429:
                return problem(503, "provider_busy", "Gemini quota or rate limit reached. Retry after the quota resets.")
            if error.code in (401, 403):
                return problem(503, "key_invalid", "Gemini access was rejected. Check the backend key and project permissions.")
            return problem(502, "provider_unavailable", "Gemini could not complete this request. Please retry.")
        except APIError as error:
            if getattr(error, "code", None) in ("credit_balance_exhausted", "insufficient_quota"):
                return problem(503, "quota_exhausted", "The API project has no available credits. Add credits or use document search.")
            if getattr(error, "status_code", None) == 401:
                return problem(503, "key_invalid", "The API key was rejected. Update it in the server's .env file.")
            if getattr(error, "status_code", None) == 429:
                return problem(503, "provider_busy", "The AI service is busy. Please try again shortly.")
            return problem(502, "provider_unavailable", "The AI service could not complete this request. Please retry.")
        except InvalidStateError:
            return problem(503, "state_invalid", "Document state could not be read. Check the server setup.")
        except ValueError:
            return problem(503, "setup_required", "Check the server API key and document state, then retry.")
        except (RuntimeError, KeyError, TypeError, OSError):
            return problem(503, "service_not_ready", "The document service could not complete this request. Check the server setup.")
        finally:
            slots.release()

    public = ROOT / "frontend" / "public"
    if public.exists():
        app.mount("/", StaticFiles(directory=public, html=True), name="frontend")
    return app


app = create_app()

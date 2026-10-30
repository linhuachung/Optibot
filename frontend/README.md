# Frontend

From the repository root, keep the backend running in one terminal:

```powershell
python server.py
```

In a second terminal:

```powershell
python -m http.server 5173 --bind 127.0.0.1 --directory frontend/public
```

Open **http://127.0.0.1:5173**. No Node/npm install or frontend build is required. Alternatively open **http://127.0.0.1:8000** to use the same UI served by the backend alone.

On this workspace, replace `python` with `.\.runtime\python\python.exe` if Python is not installed. Full setup and troubleshooting: [run guide](../docs/run.md).

The frontend contains no API key and renders provider text as text, not HTML. Search mode shows real document excerpts; Ask assistant requires funded API credits. This is a local demo and does not replace the assignment's provider-UI screenshot.

Design contract: a quiet green/neutral support workspace; one primary question action, visible search/answer distinction, source articles alongside response content, labelled input and keyboard controls. Empty/loading/error/result/setup states are explicit. A single column replaces the library sidebar on small screens. No existing product design assets were supplied; the layout and colors are project-local assumptions to verify in browser checks.

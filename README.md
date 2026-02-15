# Simulacra

Multi-agent debate system: **Napoleon**, **Gandhi**, **Alexander**, and **Summariser**. Built with Google ADK and FastMCP.

## Spec

See [Specifications.md](./Specifications.md) for personas, debate flow, and technical requirements.

## Environment

Copy `.env.example` to `.env` and set values for your environment (see the file for descriptions). The backend loads `.env` from the repo root. For frontend, copy `.env` to `src/frontend/.env` so Vite picks up `VITE_*` variables, or set them in the shell. Do not commit `.env` (it is in `.gitignore`).

## Run and test (before commit)

From repo root:

```bash
./scripts/run_tests.sh
```

This runs all backend (pytest) and frontend (Jest) tests. Fix any failures before committing.

**Backend tests** (27): `PYTHONPATH=src python3 -m pytest tests/ -v`  
**Frontend tests** (11): `cd src/frontend && npm run test`

## Layout

- `src/backend` — Python: core (personas, debate state), tools (FastMCP contract), ADK coordinator, FastAPI app
- `src/frontend` — React app: chat UI with persona icons
- `tests/` — pytest (backend), Jest + RTL (frontend)

## Backend

```bash
# Install deps (uv or pip)
uv sync
# or: pip install -e ".[dev]"  # from pyproject.toml

# Run tests
PYTHONPATH=src python3 -m pytest tests/ -v

# Run API (from repo root; needs GOOGLE_API_KEY for full debate)
PYTHONPATH=src python3 -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Without `google-adk` installed, `POST /debate/run` returns **503** with a JSON `detail` message. With ADK and `GOOGLE_API_KEY`, it runs the full debate.

## Frontend

```bash
cd src/frontend
npm install
npm run test
npm run dev
```

## Run debate (full flow)

1. Set `GOOGLE_API_KEY` and install backend deps including `google-adk`.
2. Start backend: `PYTHONPATH=src uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`
3. Start frontend: `cd src/frontend && npm run dev`
4. Open http://localhost:3000 and click **Run debate**.

## MCP server (optional)

```bash
PYTHONPATH=src python3 -m backend.mcp_server
```

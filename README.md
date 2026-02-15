# Simulacra

Multi-agent debate system: **Napoleon**, **Gandhi**, **Alexander**, and **Summariser**. Built with Google ADK and FastMCP.

## Quick Start

New to Simulacra? See [QUICKSTART.md](./QUICKSTART.md) for a 5-minute setup guide.

## Spec

See [Specifications.md](./Specifications.md) for personas, debate flow, and technical requirements.

## Environment

⚠️ **SECURITY WARNING**: Never commit real API keys to version control!

Copy `.env.example` to `.env` and set values for your environment (see the file for descriptions). The backend loads `.env` from the repo root. For frontend, copy `.env` to `src/frontend/.env` so Vite picks up `VITE_*` variables, or set them in the shell. Do not commit `.env` (it is in `.gitignore`).

### Getting a Google API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it into your `.env` file as `GOOGLE_API_KEY`
5. **Never share or commit this key**

## Run and test (before commit)

From repo root:

```bash
./scripts/run_tests.sh
```

This runs all backend (pytest) and frontend (Jest) tests. Fix any failures before committing.

**Backend tests** (27): `PYTHONPATH=src python3 -m pytest tests/ -v`  
**Frontend tests** (11): `cd src/frontend && npm run test`

### System Verification

To verify the entire system (tests, dependencies, security, documentation):

```bash
./scripts/verify_system.sh
```

This comprehensive script checks:

- Python and Node versions
- Virtual environment setup
- Environment configuration
- Backend and frontend dependencies
- All tests (backend + frontend)
- Running servers
- Security (no leaked API keys)
- Documentation completeness

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

## Troubleshooting

### Backend Issues

**Error: "Your API key was reported as leaked"**

- Your API key has been compromised and blocked by Google
- Generate a new API key at https://aistudio.google.com/app/apikey
- Update your `.env` file with the new key
- Never commit API keys to version control

**Error: "429 RESOURCE_EXHAUSTED" or rate limit errors**

- You've exceeded the free tier rate limits (15 requests/minute)
- The system will automatically retry with exponential backoff
- If retries fail, wait 5-10 minutes and try again
- Reduce exchange rounds: `POST /debate/run?max_exchange_rounds=2`
- See [RATE_LIMITING.md](./RATE_LIMITING.md) for detailed mitigation strategies
- Consider upgrading to paid tier for production use

**Error: "Google ADK is not installed"**

- Run `uv sync` or `pip install -e ".[dev]"` to install dependencies
- Verify installation: `python3 -c "import google.adk; print('OK')"`

**Error: "503 Service Unavailable"**

- Check that `GOOGLE_API_KEY` is set in your `.env` file
- Verify the API key is valid
- Check that google-adk is installed

**Backend won't start**

- Ensure you're using the .venv environment: `source .venv/bin/activate`
- Check that port 8000 is not already in use: `lsof -i :8000`
- Verify PYTHONPATH is set: `PYTHONPATH=src`

### Frontend Issues

**Frontend won't start**

- Run `npm install` in `src/frontend` directory
- Check that port 3000 is not already in use: `lsof -i :3000`
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`

**API calls fail with CORS errors**

- Verify backend is running on port 8000
- Check CORS_ORIGINS in `.env` includes your frontend URL
- Verify Vite proxy configuration in `vite.config.js`

### Test Issues

**Backend tests fail**

- Ensure PYTHONPATH is set: `PYTHONPATH=src pytest tests/`
- Check that all dependencies are installed: `uv sync`
- Run tests with verbose output: `PYTHONPATH=src pytest tests/ -v`

**Frontend tests fail**

- Ensure dependencies are installed: `npm install`
- Clear Jest cache: `npm run test -- --clearCache`
- Run tests with verbose output: `npm run test -- --verbose`

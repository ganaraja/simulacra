"""
FastAPI application: exposes debate run and state for the frontend.
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.agent import DebateCoordinator

# Load .env from repo root (parent of src/)
_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(_env_path)

_CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").strip()
CORS_ORIGINS_LIST = [o.strip() for o in _CORS_ORIGINS.split(",") if o.strip()] or ["http://localhost:3000", "http://127.0.0.1:3000"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Shutdown if needed


app = FastAPI(
    title="Simulacra Debate API",
    description="Multi-agent debate: Napoleon, Gandhi, Alexander, and Summariser",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check."""
    return {"status": "ok"}


@app.post("/debate/run")
async def run_debate(max_exchange_rounds: int = 4) -> dict[str, Any]:
    """
    Run the full debate and return the final state (messages, openings, reflections, summary).
    """
    try:
        coordinator = DebateCoordinator(max_exchange_rounds=max_exchange_rounds)
        state = await coordinator.run_debate()
        return state
    except RuntimeError as e:
        if "not installed" in str(e).lower() or "adk" in str(e).lower():
            raise HTTPException(status_code=503, detail=str(e)) from e
        raise HTTPException(status_code=500, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

"""Tests for FastAPI app (debate API)."""
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

# Import after path is set
from backend.app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestHealth:
    def test_health_returns_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}


class TestDebateRun:
    def test_run_debate_returns_state_when_mocked(self, client):
        # Mock DebateCoordinator so we don't need ADK or API key.
        mock_state = {
            "phase": "done",
            "messages": [{"author_id": "napoleon", "author_name": "Napoleon", "content": "Test.", "phase": "opening"}],
            "openings": {},
            "arbitration": "Consensus reached.",
        }
        with patch("backend.app.main.DebateCoordinator") as MockCoordinator:
            mock_instance = MockCoordinator.return_value
            mock_instance.run_debate = AsyncMock(return_value=mock_state)
            r = client.post("/debate/run")
        assert r.status_code == 200
        data = r.json()
        assert data["phase"] == "done"
        assert "messages" in data
        assert data["arbitration"] == "Consensus reached."

    def test_run_debate_returns_503_when_adk_not_installed(self, client):
        # When DebateCoordinator raises RuntimeError (ADK not installed), we return 503.
        with patch("backend.app.main.DebateCoordinator") as MockCoordinator:
            MockCoordinator.side_effect = RuntimeError("Google ADK is not installed. Install with: uv add google-adk")
            r = client.post("/debate/run")
        assert r.status_code == 503
        data = r.json()
        assert "detail" in data
        assert "ADK" in data["detail"] or "not installed" in data["detail"]

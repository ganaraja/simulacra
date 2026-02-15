"""Tests for backend.core (persona and debate state)."""
import pytest
from backend.core import Persona, PersonaId, DebateState, DebateRound, RoundPhase
from backend.core.debate import DebateMessage


class TestPersona:
    def test_napoleon_philosophy(self):
        p = Persona.napoleon()
        assert p.id == PersonaId.NAPOLEON
        assert p.name == "Napoleon"
        assert "benevolence" in p.philosophy.lower()
        assert "single kingdom" in p.philosophy.lower()

    def test_gandhi_philosophy(self):
        p = Persona.gandhi()
        assert p.id == PersonaId.GANDHI
        assert "non-violence" in p.philosophy.lower() or "peace" in p.philosophy.lower()

    def test_alexander_philosophy(self):
        p = Persona.alexander()
        assert p.id == PersonaId.ALEXANDER
        assert "conquest" in p.philosophy.lower() or "ambition" in p.philosophy.lower()

    def test_summariser(self):
        p = Persona.summariser()
        assert p.id == PersonaId.SUMMARISER
        assert "summar" in p.philosophy.lower()

    def test_debaters_excludes_summariser(self):
        debaters = Persona.debaters()
        assert len(debaters) == 3
        ids = [p.id for p in debaters]
        assert PersonaId.SUMMARISER not in ids
        assert PersonaId.NAPOLEON in ids
        assert PersonaId.GANDHI in ids
        assert PersonaId.ALEXANDER in ids

    def test_get_returns_correct_persona(self):
        for pid in PersonaId:
            p = Persona.get(pid)
            assert p.id == pid


class TestDebateState:
    def test_initial_phase(self):
        state = DebateState()
        assert state.phase == RoundPhase.OPENING
        assert state.messages == []
        assert state.openings == {}

    def test_add_message(self):
        state = DebateState()
        state.add_message(
            PersonaId.NAPOLEON, "Napoleon", "One world.", RoundPhase.OPENING, 0
        )
        assert len(state.messages) == 1
        assert state.messages[0].author_id == PersonaId.NAPOLEON
        assert state.messages[0].content == "One world."

    def test_set_opening(self):
        state = DebateState()
        state.set_opening(PersonaId.GANDHI, "Peace and simplicity.")
        assert state.openings["gandhi"] == "Peace and simplicity."

    def test_transcript_for_context(self):
        state = DebateState()
        state.add_message(PersonaId.NAPOLEON, "Napoleon", "A", RoundPhase.OPENING)
        state.add_message(PersonaId.GANDHI, "Gandhi", "B", RoundPhase.OPENING)
        t = state.transcript_for_context(limit=10)
        assert "Napoleon" in t and "A" in t
        assert "Gandhi" in t and "B" in t

    def test_openings_text(self):
        state = DebateState()
        state.set_opening(PersonaId.NAPOLEON, "N opening.")
        state.set_opening(PersonaId.GANDHI, "G opening.")
        block = state.openings_text()
        assert "napoleon" in block.lower() or "N opening" in block
        assert "gandhi" in block.lower() or "G opening" in block

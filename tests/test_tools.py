"""Tests for backend.tools (debate tool functions)."""
import pytest
from backend.tools.debate_tools import (
    create_initial_state,
    get_debate_state,
    build_opening_prompt,
    record_opening,
    build_defence_prompt,
    record_defence,
    advance_phase,
    advance_exchange_round,
    build_arbitration_prompt,
    record_arbitration,
    build_summary_prompt,
    record_summary,
)


class TestCreateAndGetState:
    def test_create_initial_state(self):
        state = create_initial_state()
        assert state["phase"] == "opening"
        assert state["messages"] == []
        assert state["openings"] == {}
        assert state.get("exchange_rounds") == 0

    def test_create_initial_state_max_rounds(self):
        state = create_initial_state(max_exchange_rounds=3)
        assert state["max_exchange_rounds"] == 3

    def test_get_debate_state_passthrough(self):
        state = create_initial_state()
        out = get_debate_state(state)
        assert out == state


class TestOpening:
    def test_build_opening_prompt_napoleon(self):
        prompt = build_opening_prompt("napoleon")
        assert "Napoleon" in prompt
        assert "opening" in prompt.lower() or "brief" in prompt.lower()

    def test_build_opening_prompt_gandhi(self):
        prompt = build_opening_prompt("gandhi")
        assert "Gandhi" in prompt

    def test_record_opening_updates_state(self):
        state = create_initial_state()
        state = record_opening("napoleon", "One kingdom for peace.", state)
        assert state["openings"]["napoleon"] == "One kingdom for peace."
        assert len(state["messages"]) == 1
        assert state["messages"][0]["content"] == "One kingdom for peace."


class TestDefence:
    def test_build_defence_prompt_includes_openings(self):
        state = create_initial_state()
        state = record_opening("napoleon", "N says this.", state)
        state = record_opening("gandhi", "G says that.", state)
        state = record_opening("alexander", "A says other.", state)
        prompt = build_defence_prompt("gandhi", state)
        assert "Gandhi" in prompt
        assert "defend" in prompt.lower() or "vigorous" in prompt.lower()
        assert "N says" in prompt or "openings" in prompt.lower()

    def test_record_defence_adds_message(self):
        state = create_initial_state()
        state = advance_phase(state, "defence")
        state = record_defence("alexander", "I stand by conquest.", state)
        assert len(state["messages"]) == 1
        assert state["messages"][0]["author_id"] == "alexander"
        assert "conquest" in state["messages"][0]["content"]


class TestAdvancePhase:
    def test_advance_to_defence(self):
        state = create_initial_state()
        state = advance_phase(state, "defence")
        assert state["phase"] == "defence"

    def test_advance_to_exchange_sets_round(self):
        state = create_initial_state()
        state = advance_phase(state, "exchange")
        assert state["phase"] == "exchange"
        assert state["exchange_rounds"] == 1

    def test_advance_exchange_round_increments(self):
        state = create_initial_state()
        state["phase"] = "exchange"
        state["exchange_rounds"] = 1
        state = advance_exchange_round(state)
        assert state["exchange_rounds"] == 2
        state = advance_exchange_round(state)
        assert state["exchange_rounds"] == 3
        state = advance_exchange_round(state)
        assert state["exchange_rounds"] == 4
        state = advance_exchange_round(state)
        assert state["exchange_rounds"] == 4  # capped at max


class TestSummary:
    def test_build_summary_prompt(self):
        state = create_initial_state()
        state["messages"] = [
            {"author_id": "napoleon", "author_name": "Napoleon", "content": "X", "phase": "opening", "round_index": 0}
        ]
        prompt = build_summary_prompt(state)
        assert "summar" in prompt.lower()
        assert "Napoleon" in prompt or "standings" in prompt.lower()

    def test_record_summary_sets_done(self):
        state = create_initial_state()
        state = advance_phase(state, "summary")
        state = record_summary("All held their views.", state)
        assert state["summary"] == "All held their views."
        assert state["phase"] == "done"


class TestArbitration:
    def test_build_arbitration_prompt_includes_transcript(self):
        state = create_initial_state()
        state["messages"] = [
            {"author_id": "napoleon", "author_name": "Napoleon", "content": "Unity through strength.", "phase": "opening", "round_index": 0},
            {"author_id": "gandhi", "author_name": "Gandhi", "content": "Peace through non-violence.", "phase": "opening", "round_index": 0},
        ]
        prompt = build_arbitration_prompt(state)
        assert "arbitrator" in prompt.lower() or "neutral" in prompt.lower()
        assert "Napoleon" in prompt or "Gandhi" in prompt

    def test_record_arbitration_adds_message(self):
        state = create_initial_state()
        state = advance_phase(state, "arbitration")
        state = record_arbitration("Both perspectives have merit.", state)
        assert state["arbitration"] == "Both perspectives have merit."
        assert len(state["messages"]) == 1
        assert state["messages"][0]["author_id"] == "arbitrator"
        assert "merit" in state["messages"][0]["content"]

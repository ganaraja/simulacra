"""
Debate tool implementations. Build prompts and update state.
Used by FastMCP server and by ADK agent; agent does not import core directly.
"""

from typing import Any

from backend.core import Persona, PersonaId, DebateState, RoundPhase


def _state_from_dict(data: dict[str, Any]) -> DebateState:
    """Deserialize state dict to DebateState."""
    from backend.core.debate import DebateMessage

    messages = []
    for m in data.get("messages", []):
        messages.append(
            DebateMessage(
                author_id=PersonaId(m["author_id"]),
                author_name=m["author_name"],
                content=m["content"],
                round_index=m.get("round_index", 0),
                phase=RoundPhase(m["phase"]),
            )
        )
    return DebateState(
        phase=RoundPhase(data.get("phase", RoundPhase.OPENING.value)),
        messages=messages,
        openings=dict(data.get("openings", {})),
        exchange_rounds=data.get("exchange_rounds", 0),
        max_exchange_rounds=data.get("max_exchange_rounds", 4),
        reflections=dict(data.get("reflections", {})),
        summary=data.get("summary", ""),
    )


def _state_to_dict(state: DebateState) -> dict[str, Any]:
    """Serialize DebateState to JSON-suitable dict."""
    return {
        "phase": state.phase.value,
        "messages": [
            {
                "author_id": m.author_id.value,
                "author_name": m.author_name,
                "content": m.content,
                "round_index": m.round_index,
                "phase": m.phase.value,
            }
            for m in state.messages
        ],
        "openings": dict(state.openings),
        "exchange_rounds": state.exchange_rounds,
        "max_exchange_rounds": state.max_exchange_rounds,
        "reflections": dict(state.reflections),
        "summary": state.summary,
    }


def create_initial_state(max_exchange_rounds: int = 4) -> dict[str, Any]:
    """
    Create a fresh debate state for a new session.

    Args:
        max_exchange_rounds: Number of exchange rounds (default 4).

    Returns:
        State dict with phase OPENING, empty messages and openings.
    """
    state = DebateState(phase=RoundPhase.OPENING, max_exchange_rounds=max_exchange_rounds)
    return _state_to_dict(state)


def get_debate_state(state_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Return the current debate state as a JSON-serializable dict.

    Args:
        state_dict: Current state from previous tool calls.

    Returns:
        Same state (pass-through); use for coordinator to inspect state.
    """
    return state_dict


def build_opening_prompt(persona_id: str) -> str:
    """
    Build the prompt for a debater to give their brief opening statement.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.

    Returns:
        Instruction text for the LLM to generate an opening (2-4 sentences).
    """
    pid = PersonaId(persona_id)
    persona = Persona.get(pid)
    return (
        f"You are {persona.name}. Your view: {persona.philosophy}. "
        "Give a brief opening statement (2-4 sentences) stating your position with brevity."
    )


def record_opening(persona_id: str, opening_text: str, state_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Record one debater's opening statement and add it to the transcript.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        opening_text: The opening statement to store.
        state_dict: Current debate state.

    Returns:
        Updated state dict with opening stored and one message added.
    """
    state = _state_from_dict(state_dict)
    pid = PersonaId(persona_id)
    persona = Persona.get(pid)
    state.set_opening(pid, opening_text)
    state.add_message(pid, persona.name, opening_text, RoundPhase.OPENING, 0)
    return _state_to_dict(state)


def build_defence_prompt(persona_id: str, state_dict: dict[str, Any]) -> str:
    """
    Build the prompt asking this debater to defend their position after seeing all openings.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        state_dict: Current state (must contain openings from all three).

    Returns:
        Instruction text for the LLM to defend vigorously.
    """
    state = _state_from_dict(state_dict)
    pid = PersonaId(persona_id)
    persona = Persona.get(pid)
    openings_block = state.openings_text()
    return (
        f"You are {persona.name}. Your view: {persona.philosophy}. "
        f"Here are everyone's opening statements:\n\n{openings_block}\n\n"
        "Defend your point of view vigorously in a short response (3-5 sentences)."
    )


def record_defence(persona_id: str, defence_text: str, state_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Record a defence and add it to the transcript.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        defence_text: The defence statement.
        state_dict: Current debate state.

    Returns:
        Updated state dict.
    """
    state = _state_from_dict(state_dict)
    pid = PersonaId(persona_id)
    persona = Persona.get(pid)
    state.add_message(pid, persona.name, defence_text, RoundPhase.DEFENCE, 0)
    return _state_to_dict(state)


def build_exchange_prompt(
    persona_id: str, state_dict: dict[str, Any], round_index: int
) -> str:
    """
    Build the prompt for one debater in an exchange round (react to others).

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        state_dict: Current state (transcript so far).
        round_index: Current exchange round (1-based).

    Returns:
        Instruction for the LLM to respond to the discussion.
    """
    state = _state_from_dict(state_dict)
    pid = PersonaId(persona_id)
    persona = Persona.get(pid)
    transcript = state.transcript_for_context(limit=40)
    return (
        f"You are {persona.name}. Your view: {persona.philosophy}. "
        f"Exchange round {round_index}. Recent discussion:\n\n{transcript}\n\n"
        "Respond to the others in character; keep it concise (2-4 sentences)."
    )


def record_exchange_message(
    persona_id: str, content: str, state_dict: dict[str, Any], round_index: int
) -> dict[str, Any]:
    """
    Record one message in an exchange round.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        content: The message text.
        state_dict: Current state.
        round_index: Current exchange round.

    Returns:
        Updated state dict.
    """
    state = _state_from_dict(state_dict)
    pid = PersonaId(persona_id)
    persona = Persona.get(pid)
    state.add_message(pid, persona.name, content, RoundPhase.EXCHANGE, round_index)
    return _state_to_dict(state)


def build_reflection_prompt(persona_id: str, state_dict: dict[str, Any]) -> str:
    """
    Build the prompt asking whether the debater would change their position.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        state_dict: Current state (full transcript).

    Returns:
        Instruction for the LLM to reflect and state if/how they would change.
    """
    state = _state_from_dict(state_dict)
    pid = PersonaId(persona_id)
    persona = Persona.get(pid)
    transcript = state.transcript_for_context(limit=60)
    return (
        f"You are {persona.name}. Your view: {persona.philosophy}. "
        f"Full discussion so far:\n\n{transcript}\n\n"
        "In light of this discussion, are you willing to change your position? If so, how? "
        "Answer briefly (2-4 sentences)."
    )


def record_reflection(persona_id: str, reflection_text: str, state_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Record a debater's reflection (change of position or not).

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        reflection_text: Their reflection response.
        state_dict: Current state.

    Returns:
        Updated state dict.
    """
    state = _state_from_dict(state_dict)
    pid = PersonaId(persona_id)
    persona = Persona.get(pid)
    state.set_reflection(pid, reflection_text)
    state.add_message(pid, persona.name, reflection_text, RoundPhase.REFLECTION, 0)
    return _state_to_dict(state)


def build_summary_prompt(state_dict: dict[str, Any]) -> str:
    """
    Build the prompt for the Summariser to summarise standings.

    Args:
        state_dict: Current state (openings, defences, exchange, reflections).

    Returns:
        Instruction for the Summariser LLM.
    """
    state = _state_from_dict(state_dict)
    transcript = state.transcript_for_context(limit=80)
    return (
        "You are a neutral Summariser. Summarise the debate standings: "
        "what each of the three (Napoleon, Gandhi, Alexander) argued, "
        "whether any shifted position in the reflection round, and a brief overall synthesis. "
        f"Discussion:\n\n{transcript}\n\n"
        "Provide a concise summary (one short paragraph)."
    )


def record_summary(summary_text: str, state_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Record the Summariser's summary and mark debate done.

    Args:
        summary_text: The summary content.
        state_dict: Current state.

    Returns:
        Updated state dict with phase DONE.
    """
    state = _state_from_dict(state_dict)
    state.summary = summary_text
    state.phase = RoundPhase.DONE
    persona = Persona.summariser()
    state.add_message(persona.id, persona.name, summary_text, RoundPhase.SUMMARY, 0)
    return _state_to_dict(state)


def advance_phase(state_dict: dict[str, Any], new_phase: str) -> dict[str, Any]:
    """
    Advance the debate to a new phase (opening -> defence -> exchange -> reflection -> summary).

    Args:
        state_dict: Current state.
        new_phase: One of 'defence', 'exchange', 'reflection', 'summary', 'done'.

    Returns:
        Updated state dict with phase set.
    """
    state = _state_from_dict(state_dict)
    state.phase = RoundPhase(new_phase)
    if new_phase == RoundPhase.EXCHANGE.value:
        state.exchange_rounds = 1
    return _state_to_dict(state)


def advance_exchange_round(state_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Move to the next exchange round (after all three debaters have spoken this round).

    Args:
        state_dict: Current state.

    Returns:
        Updated state with exchange_rounds incremented (capped at max_exchange_rounds).
    """
    state = _state_from_dict(state_dict)
    state.exchange_rounds = min(state.exchange_rounds + 1, state.max_exchange_rounds)
    return _state_to_dict(state)

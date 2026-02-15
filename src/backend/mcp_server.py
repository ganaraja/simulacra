"""
FastMCP server: exposes debate tools via MCP for use by ADK or other clients.
"""

from typing import Any

from fastmcp import FastMCP

from backend.tools.debate_tools import (
    create_initial_state,
    get_debate_state,
    build_opening_prompt,
    record_opening,
    build_defence_prompt,
    record_defence,
    build_exchange_prompt,
    record_exchange_message,
    build_reflection_prompt,
    record_reflection,
    build_summary_prompt,
    record_summary,
    advance_phase,
    advance_exchange_round,
)

mcp = FastMCP(
    name="simulacra-debate",
    description="Tools for running a multi-agent debate (Napoleon, Gandhi, Alexander, Summariser).",
)


@mcp.tool()
def create_initial_state_tool(max_exchange_rounds: int = 4) -> dict[str, Any]:
    """
    Create a fresh debate state for a new session.

    Args:
        max_exchange_rounds: Number of exchange rounds (default 4).

    Returns:
        State dict with phase OPENING, empty messages and openings.
    """
    return create_initial_state(max_exchange_rounds=max_exchange_rounds)


@mcp.tool()
def get_debate_state_tool(state_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Return the current debate state (pass-through for inspection).

    Args:
        state_dict: Current state from previous tool calls.

    Returns:
        The same state dict.
    """
    return get_debate_state(state_dict)


@mcp.tool()
def build_opening_prompt_tool(persona_id: str) -> str:
    """
    Build the prompt for a debater to give their brief opening statement.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.

    Returns:
        Instruction text for the LLM to generate an opening (2-4 sentences).
    """
    return build_opening_prompt(persona_id)


@mcp.tool()
def record_opening_tool(
    persona_id: str, opening_text: str, state_dict: dict[str, Any]
) -> dict[str, Any]:
    """
    Record one debater's opening statement and add it to the transcript.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        opening_text: The opening statement to store.
        state_dict: Current debate state.

    Returns:
        Updated state dict.
    """
    return record_opening(persona_id, opening_text, state_dict)


@mcp.tool()
def build_defence_prompt_tool(persona_id: str, state_dict: dict[str, Any]) -> str:
    """
    Build the prompt asking this debater to defend their position after seeing all openings.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        state_dict: Current state (must contain openings from all three).

    Returns:
        Instruction text for the LLM to defend vigorously.
    """
    return build_defence_prompt(persona_id, state_dict)


@mcp.tool()
def record_defence_tool(
    persona_id: str, defence_text: str, state_dict: dict[str, Any]
) -> dict[str, Any]:
    """
    Record a defence and add it to the transcript.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        defence_text: The defence statement.
        state_dict: Current debate state.

    Returns:
        Updated state dict.
    """
    return record_defence(persona_id, defence_text, state_dict)


@mcp.tool()
def build_exchange_prompt_tool(
    persona_id: str, state_dict: dict[str, Any], round_index: int
) -> str:
    """
    Build the prompt for one debater in an exchange round.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        state_dict: Current state (transcript so far).
        round_index: Current exchange round (1-based).

    Returns:
        Instruction for the LLM to respond to the discussion.
    """
    return build_exchange_prompt(persona_id, state_dict, round_index)


@mcp.tool()
def record_exchange_message_tool(
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
    return record_exchange_message(persona_id, content, state_dict, round_index)


@mcp.tool()
def build_reflection_prompt_tool(persona_id: str, state_dict: dict[str, Any]) -> str:
    """
    Build the prompt asking whether the debater would change their position.

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        state_dict: Current state (full transcript).

    Returns:
        Instruction for the LLM to reflect and state if/how they would change.
    """
    return build_reflection_prompt(persona_id, state_dict)


@mcp.tool()
def record_reflection_tool(
    persona_id: str, reflection_text: str, state_dict: dict[str, Any]
) -> dict[str, Any]:
    """
    Record a debater's reflection (change of position or not).

    Args:
        persona_id: One of 'napoleon', 'gandhi', 'alexander'.
        reflection_text: Their reflection response.
        state_dict: Current state.

    Returns:
        Updated state dict.
    """
    return record_reflection(persona_id, reflection_text, state_dict)


@mcp.tool()
def build_summary_prompt_tool(state_dict: dict[str, Any]) -> str:
    """
    Build the prompt for the Summariser to summarise standings.

    Args:
        state_dict: Current state (openings, defences, exchange, reflections).

    Returns:
        Instruction for the Summariser LLM.
    """
    return build_summary_prompt(state_dict)


@mcp.tool()
def record_summary_tool(summary_text: str, state_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Record the Summariser's summary and mark debate done.

    Args:
        summary_text: The summary content.
        state_dict: Current state.

    Returns:
        Updated state dict with phase DONE.
    """
    return record_summary(summary_text, state_dict)


@mcp.tool()
def advance_phase_tool(state_dict: dict[str, Any], new_phase: str) -> dict[str, Any]:
    """
    Advance the debate to a new phase.

    Args:
        state_dict: Current state.
        new_phase: One of 'defence', 'exchange', 'reflection', 'summary', 'done'.

    Returns:
        Updated state dict.
    """
    return advance_phase(state_dict, new_phase)


@mcp.tool()
def advance_exchange_round_tool(state_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Move to the next exchange round (after all three debaters have spoken).

    Args:
        state_dict: Current state.

    Returns:
        Updated state with exchange_rounds incremented.
    """
    return advance_exchange_round(state_dict)

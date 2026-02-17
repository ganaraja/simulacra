"""
Tool layer: tool contracts used by both FastMCP and ADK.
Agent must not import core logic directly; it uses these tools only.
"""

from .debate_tools import (
    build_opening_prompt,
    record_opening,
    build_defence_prompt,
    record_defence,
    build_exchange_prompt,
    record_exchange_message,
    build_reflection_prompt,
    record_reflection,
    build_arbitration_prompt,
    record_arbitration,
    get_debate_state,
    create_initial_state,
    advance_phase,
    advance_exchange_round,
)

__all__ = [
    "build_opening_prompt",
    "record_opening",
    "build_defence_prompt",
    "record_defence",
    "build_exchange_prompt",
    "record_exchange_message",
    "build_reflection_prompt",
    "record_reflection",
    "build_arbitration_prompt",
    "record_arbitration",
    "get_debate_state",
    "create_initial_state",
    "advance_phase",
    "advance_exchange_round",
]

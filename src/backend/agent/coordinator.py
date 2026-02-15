"""
ADK coordinator: orchestrates the debate using tools only.
Does NOT import core logic directly - only uses the tools module.
"""

from typing import Any
import asyncio

# Tools only - no core import
from backend.tools.debate_tools import (
    create_initial_state,
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

# ADK for LLM invocation
try:
    from google.adk.agents import Agent
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types
    _ADK_AVAILABLE = True
except ImportError:
    _ADK_AVAILABLE = False
    Agent = None
    Runner = None
    InMemorySessionService = None
    types = None

DEBATER_IDS = ["napoleon", "gandhi", "alexander"]
DEFAULT_MODEL = "gemini-2.0-flash"
APP_NAME = "simulacra_debate"


def _extract_final_text(events) -> str:
    """Consume async events from runner and return final response text."""
    final_text = ""
    for event in events:
        if getattr(event, "is_final_response", lambda: False)():
            if getattr(event, "content", None) and getattr(event.content, "parts", None):
                if event.content.parts:
                    part = event.content.parts[0]
                    if getattr(part, "text", None):
                        final_text = part.text
            break
    return final_text or ""


async def _run_agent_for_prompt(runner: "Runner", user_id: str, session_id: str, prompt: str) -> str:
    """Send prompt to the agent and return the final response text."""
    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    events = []
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        events.append(event)
    return _extract_final_text(events)


class DebateCoordinator:
    """
    Coordinates the multi-stage debate using ADK for LLM generation and tools for state.
    Does not import core; uses tools only.
    """

    def __init__(self, model: str = DEFAULT_MODEL, max_exchange_rounds: int = 4):
        if not _ADK_AVAILABLE:
            raise RuntimeError("Google ADK is not installed. Install with: uv add google-adk")
        self.model = model
        self.max_exchange_rounds = max_exchange_rounds
        # Single agent used for all persona generations (we pass persona via prompt)
        self._agent = Agent(
            name="debate_speaker",
            model=self.model,
            description="Generates debate statements in character.",
            instruction="You respond only with the requested statement, in character, with no meta-commentary.",
        )
        self._session_service = InMemorySessionService()
        self._runner = Runner(
            agent=self._agent,
            app_name=APP_NAME,
            session_service=self._session_service,
        )
        self._user_id = "debate_user"
        self._session_counter = 0

    def _next_session_id(self) -> str:
        self._session_counter += 1
        return f"debate_session_{self._session_counter}"

    async def _run_turn(self, prompt: str) -> str:
        """Run one LLM turn with a fresh session so context is only the current prompt."""
        session_id = self._next_session_id()
        try:
            await self._session_service.create_session(
                app_name=APP_NAME,
                user_id=self._user_id,
                session_id=session_id,
            )
        except Exception:
            pass
        return await _run_agent_for_prompt(
            self._runner, self._user_id, session_id, prompt
        )

    async def run_debate(self) -> dict[str, Any]:
        """
        Run the full debate: opening -> defence -> exchange (3-4 rounds) -> reflection -> summary.
        Returns the final state dict.
        """
        state = create_initial_state(max_exchange_rounds=self.max_exchange_rounds)

        # 1. Opening statements
        for persona_id in DEBATER_IDS:
            prompt = build_opening_prompt(persona_id)
            text = await self._run_turn(prompt)
            state = record_opening(persona_id, text.strip() or "(No opening)", state)

        # 2. Advance to defence; collect openings and ask each to defend
        state = advance_phase(state, "defence")
        for persona_id in DEBATER_IDS:
            prompt = build_defence_prompt(persona_id, state)
            text = await self._run_turn(prompt)
            state = record_defence(persona_id, text.strip() or "(No defence)", state)

        # 3. Exchange rounds (3-4 rounds, each debater speaks per round)
        state = advance_phase(state, "exchange")
        for r in range(1, self.max_exchange_rounds + 1):
            for persona_id in DEBATER_IDS:
                prompt = build_exchange_prompt(persona_id, state, r)
                text = await self._run_turn(prompt)
                state = record_exchange_message(
                    persona_id, text.strip() or "(No response)", state, r
                )
            if r < self.max_exchange_rounds:
                state = advance_exchange_round(state)

        # 4. Reflection: would you change your position?
        state = advance_phase(state, "reflection")
        for persona_id in DEBATER_IDS:
            prompt = build_reflection_prompt(persona_id, state)
            text = await self._run_turn(prompt)
            state = record_reflection(
                persona_id, text.strip() or "(No reflection)", state
            )

        # 5. Summary
        state = advance_phase(state, "summary")
        prompt = build_summary_prompt(state)
        summary_text = await self._run_turn(prompt)
        state = record_summary(summary_text.strip() or "(No summary)", state)

        return state

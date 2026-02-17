"""
ADK coordinator: orchestrates the debate using tools only.
Does NOT import core logic directly - only uses the tools module.
"""

from typing import Any
import asyncio
import logging
import time

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
    build_arbitration_prompt,
    record_arbitration,
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
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 3.0  # seconds

# Configure logging
logger = logging.getLogger(__name__)


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
            model=self.model,
            name="debate_speaker",
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

    async def _run_turn(self, prompt: str, max_retries: int = MAX_RETRIES) -> str:
        """
        Run one LLM turn with a fresh session and retry logic for rate limiting.
        
        Args:
            prompt: The prompt to send to the LLM
            max_retries: Maximum number of retry attempts
            
        Returns:
            The LLM response text
            
        Raises:
            Exception: If all retries are exhausted
        """
        session_id = self._next_session_id()
        try:
            await self._session_service.create_session(
                app_name=APP_NAME,
                user_id=self._user_id,
                session_id=session_id,
            )
        except Exception:
            pass
        
        last_exception = None
        for attempt in range(max_retries):
            try:
                return await _run_agent_for_prompt(
                    self._runner, self._user_id, session_id, prompt
                )
            except Exception as e:
                last_exception = e
                error_str = str(e)
                
                # Check if it's a rate limit error (429 RESOURCE_EXHAUSTED)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    # Extract retry delay from error message if available
                    retry_delay = INITIAL_RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                    
                    # Try to parse the suggested retry delay from the error
                    if "retry in" in error_str.lower():
                        try:
                            import re
                            match = re.search(r'retry in (\d+\.?\d*)s', error_str.lower())
                            if match:
                                suggested_delay = float(match.group(1))
                                retry_delay = max(retry_delay, suggested_delay)
                        except Exception:
                            pass
                    
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Rate limit hit (attempt {attempt + 1}/{max_retries}). "
                            f"Retrying in {retry_delay:.1f}s..."
                        )
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        logger.error(f"Rate limit exceeded after {max_retries} attempts")
                        raise RuntimeError(
                            f"Rate limit exceeded. Please wait a few minutes and try again. "
                            f"For more info: https://ai.google.dev/gemini-api/docs/rate-limits"
                        ) from e
                else:
                    # Non-rate-limit error, raise immediately
                    raise
        
        # If we get here, all retries failed
        raise last_exception or RuntimeError("Failed to get LLM response")

    async def run_debate(self) -> dict[str, Any]:
        """
        Run the full debate: opening -> defence -> exchange (3-4 rounds) -> reflection -> arbitration.
        Returns the final state dict.
        
        Includes delays between phases to avoid rate limiting.
        """
        state = create_initial_state(max_exchange_rounds=self.max_exchange_rounds)

        # 1. Opening statements
        logger.info("Starting opening statements phase")
        for persona_id in DEBATER_IDS:
            prompt = build_opening_prompt(persona_id)
            text = await self._run_turn(prompt)
            state = record_opening(persona_id, text.strip() or "(No opening)", state)
            await asyncio.sleep(1)  # Small delay between personas

        # 2. Advance to defence; collect openings and ask each to defend
        logger.info("Starting defence phase")
        state = advance_phase(state, "defence")
        await asyncio.sleep(2)  # Delay before starting new phase
        
        for persona_id in DEBATER_IDS:
            prompt = build_defence_prompt(persona_id, state)
            text = await self._run_turn(prompt)
            state = record_defence(persona_id, text.strip() or "(No defence)", state)
            await asyncio.sleep(1)  # Small delay between personas

        # 3. Exchange rounds (3-4 rounds, each debater speaks per round)
        logger.info(f"Starting exchange phase ({self.max_exchange_rounds} rounds)")
        state = advance_phase(state, "exchange")
        await asyncio.sleep(2)  # Delay before starting new phase
        
        for r in range(1, self.max_exchange_rounds + 1):
            logger.info(f"Exchange round {r}/{self.max_exchange_rounds}")
            for persona_id in DEBATER_IDS:
                prompt = build_exchange_prompt(persona_id, state, r)
                text = await self._run_turn(prompt)
                state = record_exchange_message(
                    persona_id, text.strip() or "(No response)", state, r
                )
                await asyncio.sleep(1)  # Small delay between personas
            if r < self.max_exchange_rounds:
                state = advance_exchange_round(state)
                await asyncio.sleep(2)  # Delay between rounds

        # 4. Reflection: would you change your position?
        logger.info("Starting reflection phase")
        state = advance_phase(state, "reflection")
        await asyncio.sleep(2)  # Delay before starting new phase
        
        for persona_id in DEBATER_IDS:
            prompt = build_reflection_prompt(persona_id, state)
            text = await self._run_turn(prompt)
            state = record_reflection(
                persona_id, text.strip() or "(No reflection)", state
            )
            await asyncio.sleep(1)  # Small delay between personas

        # 5. Arbitration: bring all viewpoints to consensus (final phase)
        logger.info("Starting arbitration phase - bringing viewpoints to consensus")
        state = advance_phase(state, "arbitration")
        await asyncio.sleep(2)  # Delay before starting new phase
        
        prompt = build_arbitration_prompt(state)
        arbitration_text = await self._run_turn(prompt)
        state = record_arbitration(arbitration_text.strip() or "(No arbitration)", state)
        
        logger.info("Debate completed successfully")
        return state

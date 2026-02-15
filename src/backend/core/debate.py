"""Debate state and message types. No I/O; pure data structures."""

from enum import Enum
from pydantic import BaseModel, Field

from .persona import PersonaId


class RoundPhase(str, Enum):
    """Current phase of the debate."""

    OPENING = "opening"
    DEFENCE = "defence"
    EXCHANGE = "exchange"
    REFLECTION = "reflection"
    SUMMARY = "summary"
    DONE = "done"


class DebateMessage(BaseModel):
    """A single message in the debate transcript."""

    author_id: PersonaId = Field(..., description="Which persona said this")
    author_name: str = Field(..., description="Display name of author")
    content: str = Field(..., description="Message text")
    round_index: int = Field(default=0, ge=0, description="Exchange round (0 = opening/defence)")
    phase: RoundPhase = Field(..., description="Phase when this was said")


class DebateState(BaseModel):
    """Full state of the debate: phase, transcript, openings, and round count."""

    phase: RoundPhase = Field(default=RoundPhase.OPENING)
    messages: list[DebateMessage] = Field(default_factory=list)
    openings: dict[str, str] = Field(default_factory=dict)  # persona_id -> opening text
    exchange_rounds: int = Field(default=0, ge=0)
    max_exchange_rounds: int = Field(default=4, ge=1)
    reflections: dict[str, str] = Field(default_factory=dict)  # persona_id -> reflection text
    summary: str = Field(default="")

    def add_message(self, author_id: PersonaId, author_name: str, content: str, phase: RoundPhase, round_index: int = 0) -> None:
        """Append a message and optionally update phase."""
        self.messages.append(
            DebateMessage(
                author_id=author_id,
                author_name=author_name,
                content=content,
                round_index=round_index,
                phase=phase,
            )
        )

    def set_opening(self, persona_id: PersonaId, text: str) -> None:
        """Store an opening statement by persona."""
        self.openings[persona_id.value] = text

    def set_reflection(self, persona_id: PersonaId, text: str) -> None:
        """Store a reflection (would you change position) by persona."""
        self.reflections[persona_id.value] = text

    def transcript_for_context(self, limit: int = 50) -> str:
        """Produce a concise transcript string for agent context (last N messages)."""
        recent = self.messages[-limit:] if limit else self.messages
        lines = [f"[{m.author_name}] ({m.phase.value}): {m.content}" for m in recent]
        return "\n".join(lines)

    def openings_text(self) -> str:
        """All opening statements as a single block for context."""
        parts = [f"{k}: {v}" for k, v in self.openings.items()]
        return "\n\n".join(parts)


class DebateRound(BaseModel):
    """Metadata for a single exchange round (e.g. round 1 of 4)."""

    index: int = Field(..., ge=0)
    phase: RoundPhase = Field(default=RoundPhase.EXCHANGE)

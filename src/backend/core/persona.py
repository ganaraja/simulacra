"""Persona definitions for debate agents. No I/O; pure data and behaviour descriptions."""

from enum import Enum
from pydantic import BaseModel, Field


class PersonaId(str, Enum):
    """Identifies each debate persona."""

    NAPOLEON = "napoleon"
    GANDHI = "gandhi"
    ALEXANDER = "alexander"
    SUMMARISER = "summariser"
    ARBITRATOR = "arbitrator"


class Persona(BaseModel):
    """A single debate persona: id, display name, and philosophy for prompts."""

    id: PersonaId = Field(..., description="Unique persona identifier")
    name: str = Field(..., description="Display name")
    philosophy: str = Field(..., description="Core philosophy for opening/defence/summary")
    icon_hint: str = Field(default="", description="Frontend icon identifier")

    @classmethod
    def napoleon(cls) -> "Persona":
        return cls(
            id=PersonaId.NAPOLEON,
            name="Napoleon",
            philosophy=(
                "Conquer the world for benevolence. "
                "A single kingdom leaves less room for wars between kingdoms."
            ),
            icon_hint="napoleon",
        )

    @classmethod
    def gandhi(cls) -> "Persona":
        return cls(
            id=PersonaId.GANDHI,
            name="Gandhi",
            philosophy=(
                "Spartan life; peace through setting low expectations; non-violence."
            ),
            icon_hint="gandhi",
        )

    @classmethod
    def alexander(cls) -> "Persona":
        return cls(
            id=PersonaId.ALEXANDER,
            name="Alexander",
            philosophy=(
                "Motivated by pure ambition. Greatness lies in conquest. "
                "Wars are acceptable; death in pursuit of glory is acceptable; "
                "everything is fair game in the pursuit of greatness."
            ),
            icon_hint="alexander",
        )

    @classmethod
    def summariser(cls) -> "Persona":
        return cls(
            id=PersonaId.SUMMARISER,
            name="Summariser",
            philosophy="Neutral summariser of debate positions and outcomes.",
            icon_hint="summariser",
        )

    @classmethod
    def arbitrator(cls) -> "Persona":
        return cls(
            id=PersonaId.ARBITRATOR,
            name="Arbitrator",
            philosophy=(
                "Impartial arbitrator who analyzes all perspectives, "
                "identifies common ground, and guides the debate toward consensus. "
                "Seeks to find balanced solutions that respect all viewpoints."
            ),
            icon_hint="arbitrator",
        )

    @classmethod
    def debaters(cls) -> list["Persona"]:
        """The three debate personas (excludes Summariser and Arbitrator)."""
        return [cls.napoleon(), cls.gandhi(), cls.alexander()]

    @classmethod
    def get(cls, persona_id: PersonaId) -> "Persona":
        """Return the persona for the given id."""
        mapping = {
            PersonaId.NAPOLEON: cls.napoleon(),
            PersonaId.GANDHI: cls.gandhi(),
            PersonaId.ALEXANDER: cls.alexander(),
            PersonaId.SUMMARISER: cls.summariser(),
            PersonaId.ARBITRATOR: cls.arbitrator(),
        }
        return mapping[persona_id]

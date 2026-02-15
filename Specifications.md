# Simulacra: Multi-Agent Debate System

## Overview

A debate system where three historical personas (Napoleon, Gandhi, Alexander) and a fourth Summariser agent interact over multiple rounds. The system uses Google Agent Development Kit (ADK) for orchestration and FastMCP for tool definition and serving.

## Personas

| Agent      | Persona   | Philosophy                                                                                                 |
| ---------- | --------- | ---------------------------------------------------------------------------------------------------------- |
| Napoleon   | Conqueror | Wants to conquer the world for benevolence. Believes a single kingdom eliminates wars between kingdoms.    |
| Gandhi     | Pacifist  | Spartan life, peace through low expectations, non-violence.                                                |
| Alexander  | Ambition  | Motivated by pure ambition. Greatness lies in conquest; wars and death are acceptable in pursuit of glory. |
| Summariser | Neutral   | Summarises debate standings; does not advocate a position.                                                 |

## Debate Flow

1. **Opening statements**: Each of the three debate agents gives a brief opening statement.
2. **Defence round**: All openings are collected; each agent is asked to defend their position vigorously.
3. **Exchange rounds**: The three agents interact with each other for 3–4 rounds.
4. **Reflection round**: Each is asked whether, in light of the discussion, they would change their position and how.
5. **Summary**: The fourth agent (Summariser) summarises the standings.

## Technical Requirements

### Mandatory Technologies

- **Google Agent Development Kit (ADK)**: Coordinator that orchestrates reasoning and tool use.
- **FastMCP**: Tool definition and serving (names, docstrings, schemas).

### Architecture

- **Agent**: ADK coordinator only. Does **not** import core logic directly; uses tools only.
- **Core logic**: Implemented in Python classes (personas, debate state, round logic).
- **Tools**: Defined and served via FastMCP; used by the ADK agent.
- **Backend**: Under `src/backend` (Python, uv).
- **Frontend**: Under `src/frontend` (React).
- **Tests**: Under `tests/` — pytest for backend, Jest + React Testing Library for frontend.

### Evaluation Criteria

- Correctness of agent decisions.
- Quality of tool contracts (names, docstrings, schemas).
- Architectural cleanliness.
- Quality of synthesis and explanation.
- Handling of ambiguity and trade-offs.

### Common Failure Modes to Avoid

- Answering immediately without profiling.
- Treating tools as databases instead of abstractions.
- Dumping raw API responses into agent context.
- Overusing prompts to compensate for bad tool design.
- Committing API keys or credentials to version control.
- Using leaked or compromised API keys.

### Security Considerations

- **API Key Management**: Never commit real API keys. Use environment variables and .env files (excluded from git).
- **CORS Configuration**: Properly configure allowed origins to prevent unauthorized access.
- **Error Messages**: Return JSON errors (not HTML) with helpful but not sensitive information.
- **Environment Isolation**: Use .venv for Python dependencies to avoid conflicts.

### Dependency Management

- Use **uv** instead of pip for Python.

### Frontend

- React framework.
- Different icons for each persona in chat windows.

### Testing

- **Backend**: pytest; test classes and interactions in `tests/` (run with `PYTHONPATH=src pytest tests/` after `uv sync` or `pip install -e ".[dev]"`).
- **Frontend**: Jest as test runner, React Testing Library (RTL) for component and interaction tests (`npm run test` in `src/frontend`).
- On every code change: add/update tests and run full test suite; fix until all pass.

## Document History

- Initial version: multi-agent debate flow, ADK, FastMCP, React, uv, pytest, Jest/RTL.
- Updated: Added security considerations, CORS configuration, error handling strategy.
- Added comprehensive documentation: ARCHITECTURE.md, SECURITY.md, troubleshooting in README.md.

## Additional Documentation

- **[ARCHITECTURE.md](./ARCHITECTURE.md)**: Detailed system architecture, design patterns, and component interactions.
- **[SECURITY.md](./SECURITY.md)**: Security best practices, API key management, and incident response.
- **[RATE_LIMITING.md](./RATE_LIMITING.md)**: Rate limiting mitigation strategies, retry logic, and best practices.
- **[README.md](./README.md)**: Setup instructions, running the application, and troubleshooting.
- **[.kiro/specs/simulacra-improvements/](./kiro/specs/simulacra-improvements/)**: Detailed requirements, design, and implementation tasks.

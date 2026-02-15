# Simulacra Improvements - Design Document

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ DebateView   │  │ MessageList  │  │   Message    │      │
│  │  Component   │──│  Component   │──│  Component   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                                                     │
│         │ HTTP POST /debate/run                             │
└─────────┼─────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              FastAPI Application                      │   │
│  │  • /health endpoint                                   │   │
│  │  • /debate/run endpoint                               │   │
│  │  • CORS middleware                                    │   │
│  │  • Global exception handler                           │   │
│  └────────────────┬─────────────────────────────────────┘   │
│                   │                                           │
│                   ▼                                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          DebateCoordinator (ADK Agent)               │   │
│  │  • Orchestrates debate flow                          │   │
│  │  • Uses tools only (no direct core imports)          │   │
│  │  • Manages LLM sessions                              │   │
│  └────────────────┬─────────────────────────────────────┘   │
│                   │                                           │
│                   ▼                                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Debate Tools (FastMCP)                  │   │
│  │  • create_initial_state                              │   │
│  │  • build_*_prompt (opening, defence, exchange, etc)  │   │
│  │  • record_* (opening, defence, exchange, etc)        │   │
│  │  • advance_phase, advance_exchange_round             │   │
│  └────────────────┬─────────────────────────────────────┘   │
│                   │                                           │
│                   ▼                                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Core Logic (Pure Python)                │   │
│  │  ┌────────────────┐  ┌────────────────┐             │   │
│  │  │  Persona       │  │  DebateState   │             │   │
│  │  │  • Napoleon    │  │  • Phase       │             │   │
│  │  │  • Gandhi      │  │  • Messages    │             │   │
│  │  │  • Alexander   │  │  • Openings    │             │   │
│  │  │  • Summariser  │  │  • Reflections │             │   │
│  │  └────────────────┘  └────────────────┘             │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              Google Gemini API (via ADK)                     │
│  • LLM generation for persona responses                      │
│  • Fresh session per turn for clean context                  │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Principles

#### 1. Tool-Based Architecture

The ADK coordinator **never imports core logic directly**. All operations go through tools:

- **Why**: Enforces clean separation and makes the system more maintainable
- **How**: Tools act as the interface between coordinator and core logic
- **Benefit**: Core logic can be tested independently of ADK

#### 2. Stateless LLM Calls

Each LLM turn uses a fresh session:

- **Why**: Prevents context pollution between different persona responses
- **How**: `_next_session_id()` creates unique session for each turn
- **Benefit**: Each persona response is based only on the current prompt

#### 3. Immutable State Pattern

Tools return new state dicts rather than mutating:

- **Why**: Makes state changes explicit and traceable
- **How**: `_state_to_dict()` and `_state_from_dict()` handle conversions
- **Benefit**: Easier to debug and test

## Debate Flow Design

### Phase Sequence

```
1. OPENING
   ├─ Napoleon gives opening statement
   ├─ Gandhi gives opening statement
   └─ Alexander gives opening statement

2. DEFENCE
   ├─ All openings collected
   ├─ Napoleon defends position
   ├─ Gandhi defends position
   └─ Alexander defends position

3. EXCHANGE (3-4 rounds)
   ├─ Round 1
   │  ├─ Napoleon responds
   │  ├─ Gandhi responds
   │  └─ Alexander responds
   ├─ Round 2
   │  ├─ Napoleon responds
   │  ├─ Gandhi responds
   │  └─ Alexander responds
   └─ ... (up to max_exchange_rounds)

4. REFLECTION
   ├─ Napoleon reflects on position
   ├─ Gandhi reflects on position
   └─ Alexander reflects on position

5. SUMMARY
   └─ Summariser provides neutral summary

6. DONE
```

### Prompt Engineering

Each phase has a specific prompt template:

**Opening Prompt**:

```
You are {persona_name}. Philosophy: {philosophy}
Give a brief opening statement (2-3 sentences) on your view of how to achieve peace and prosperity.
```

**Defence Prompt**:

```
You are {persona_name}. Philosophy: {philosophy}
Here are the opening statements from all participants:
{openings}

Defend your position vigorously in 2-3 sentences.
```

**Exchange Prompt**:

```
You are {persona_name}. Philosophy: {philosophy}
This is exchange round {round} of {max_rounds}.
Recent discussion:
{transcript}

Respond to the other participants (2-3 sentences).
```

**Reflection Prompt**:

```
You are {persona_name}. Philosophy: {philosophy}
After this debate, would you change your position? How? (2-3 sentences)
```

**Summary Prompt**:

```
You are the Summariser. Review the debate and provide a neutral summary of each position and the overall discussion (4-5 sentences).
```

## Data Models

### Persona

```python
class Persona(BaseModel):
    id: PersonaId  # napoleon, gandhi, alexander, summariser
    name: str  # Display name
    philosophy: str  # Core philosophy for prompts
    icon_hint: str  # Frontend icon identifier
```

### DebateState

```python
class DebateState(BaseModel):
    phase: RoundPhase  # Current phase
    messages: list[DebateMessage]  # Full transcript
    openings: dict[str, str]  # persona_id -> opening text
    exchange_rounds: int  # Current exchange round
    max_exchange_rounds: int  # Total exchange rounds
    reflections: dict[str, str]  # persona_id -> reflection
    summary: str  # Final summary
```

### DebateMessage

```python
class DebateMessage(BaseModel):
    author_id: PersonaId
    author_name: str
    content: str
    round_index: int  # 0 for opening/defence
    phase: RoundPhase
```

## Tool Contracts

### State Management Tools

- `create_initial_state(max_exchange_rounds: int) -> dict`
- `get_debate_state(state_dict: dict) -> dict`

### Prompt Building Tools

- `build_opening_prompt(persona_id: str) -> str`
- `build_defence_prompt(persona_id: str, state_dict: dict) -> str`
- `build_exchange_prompt(persona_id: str, state_dict: dict, round: int) -> str`
- `build_reflection_prompt(persona_id: str, state_dict: dict) -> str`
- `build_summary_prompt(state_dict: dict) -> str`

### Recording Tools

- `record_opening(persona_id: str, text: str, state_dict: dict) -> dict`
- `record_defence(persona_id: str, text: str, state_dict: dict) -> dict`
- `record_exchange_message(persona_id: str, text: str, state_dict: dict, round: int) -> dict`
- `record_reflection(persona_id: str, text: str, state_dict: dict) -> dict`
- `record_summary(text: str, state_dict: dict) -> dict`

### Phase Management Tools

- `advance_phase(state_dict: dict, new_phase: str) -> dict`
- `advance_exchange_round(state_dict: dict) -> dict`

## Error Handling Strategy

### Backend Error Handling

1. **Missing ADK**: Return 503 with installation instructions
2. **Invalid API Key**: Return 403 with clear message
3. **Runtime Errors**: Return 500 with error details
4. **All Errors**: Return JSON (never HTML)

### Frontend Error Handling

1. **Network Errors**: Show user-friendly message
2. **API Errors**: Display error detail from backend
3. **Loading States**: Show spinner during debate execution

## Security Considerations

### API Key Management

- **Never commit real keys**: Use placeholder in .env.example
- **Environment variables**: Load from .env file
- **Clear documentation**: Explain how to obtain keys
- **Error messages**: Don't expose key details in errors

### CORS Configuration

- **Allowed origins**: Configurable via CORS_ORIGINS env var
- **Default**: localhost:3000 and 127.0.0.1:3000
- **Credentials**: Allowed for cookie-based auth (future)

## Testing Strategy

### Backend Tests (pytest)

**Persona Tests** (5 tests):

- Test each persona's philosophy
- Test debaters() excludes summariser
- Test get() returns correct persona

**DebateState Tests** (5 tests):

- Test initial phase
- Test add_message
- Test set_opening
- Test transcript_for_context
- Test openings_text

**Tools Tests** (14 tests):

- Test create_initial_state
- Test prompt building for each phase
- Test recording for each phase
- Test phase advancement
- Test exchange round advancement

**API Tests** (3 tests):

- Test health endpoint
- Test debate run with mocked coordinator
- Test 503 when ADK not installed

### Frontend Tests (Jest + RTL)

**Component Tests** (11 tests):

- Message component rendering
- MessageList component rendering
- DebateView component rendering
- Button interactions
- Loading states
- Error states

## Performance Considerations

### LLM Call Optimization

- **Fresh sessions**: Prevents context bloat
- **Concise prompts**: 2-3 sentence responses
- **Limited transcript**: Only last 50 messages in context

### Frontend Optimization

- **Single API call**: Entire debate runs in one request
- **No streaming**: Simpler implementation for MVP
- **Minimal re-renders**: React best practices

## Future Enhancements

### Potential Improvements

1. **Streaming responses**: Show debate progress in real-time
2. **Persistent storage**: Save debate history
3. **Custom personas**: Allow users to define new personas
4. **Debate topics**: Allow users to specify debate topics
5. **Multi-debate**: Run multiple debates concurrently
6. **Analytics**: Track debate patterns and outcomes

### Scalability Considerations

1. **Database**: Add PostgreSQL for debate storage
2. **Caching**: Cache persona definitions
3. **Queue**: Use Celery for async debate execution
4. **WebSockets**: Real-time updates to frontend

## Correctness Properties

### Property 1: Debate Phase Progression

**Property**: Phases must progress in order: OPENING → DEFENCE → EXCHANGE → REFLECTION → SUMMARY → DONE

**Validation**:

- Unit tests verify advance_phase() enforces order
- Integration tests verify full debate follows sequence

### Property 2: All Debaters Participate

**Property**: In each phase (except SUMMARY), all three debaters must contribute exactly once

**Validation**:

- Count messages per phase per persona
- Verify openings dict has 3 entries
- Verify reflections dict has 3 entries

### Property 3: Exchange Round Consistency

**Property**: Exchange rounds must increment sequentially from 1 to max_exchange_rounds

**Validation**:

- Verify exchange_rounds field increments correctly
- Verify messages have correct round_index

### Property 4: State Immutability

**Property**: Tool functions must not mutate input state_dict

**Validation**:

- Unit tests verify input dict unchanged after tool calls
- Tools return new dict instances

### Property 5: Prompt Context Accuracy

**Property**: Prompts must include correct context for the current phase

**Validation**:

- Defence prompts include all openings
- Exchange prompts include recent transcript
- Reflection prompts include full debate context
- Summary prompt includes all phases

## Implementation Notes

### ADK Integration

- Use `google.adk.agents.Agent` for LLM coordination
- Use `google.adk.runners.Runner` for execution
- Use `InMemorySessionService` for session management
- Extract text from events using `is_final_response()`

### FastMCP Integration

- Tools defined as pure Python functions
- No MCP server needed for this architecture
- Tools could be exposed via MCP for external use

### Environment Variables

- `GOOGLE_API_KEY`: Required for LLM calls
- `GOOGLE_API_MODEL`: Model name (default: gemini-2.0-flash-exp)
- `BACKEND_HOST`: Backend host (default: 127.0.0.1)
- `BACKEND_PORT`: Backend port (default: 8000)
- `CORS_ORIGINS`: Allowed CORS origins
- `VITE_API_BASE`: Frontend API base URL (optional)

## Deployment Considerations

### Development

- Backend: `PYTHONPATH=src .venv/bin/python3 -m uvicorn backend.app.main:app --reload`
- Frontend: `cd src/frontend && npm run dev`

### Production

- Backend: Use gunicorn with uvicorn workers
- Frontend: Build with `npm run build` and serve static files
- Environment: Set all required env vars
- Monitoring: Add logging and error tracking
- Security: Use HTTPS, secure API keys, rate limiting

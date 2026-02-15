# Simulacra Architecture

## System Overview

Simulacra is a multi-agent debate system that orchestrates conversations between three historical personas (Napoleon, Gandhi, Alexander) and a neutral Summariser. The system uses Google's Agent Development Kit (ADK) for LLM orchestration and follows a tool-based architecture pattern.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              React Frontend (Port 3000)                     │ │
│  │  • DebateView: Main debate interface                       │ │
│  │  • MessageList: Displays debate messages                   │ │
│  │  • Message: Individual message component                   │ │
│  │  • Persona icons for visual identification                 │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ HTTP POST /debate/run
                            │ HTTP GET /health
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    FastAPI Backend (Port 8000)                   │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   API Layer                                 │ │
│  │  • /health: Health check endpoint                          │ │
│  │  • /debate/run: Execute full debate                        │ │
│  │  • CORS middleware for cross-origin requests              │ │
│  │  • Global exception handler (JSON errors only)            │ │
│  └────────────────────────┬───────────────────────────────────┘ │
│                            │                                      │
│  ┌────────────────────────▼───────────────────────────────────┐ │
│  │              DebateCoordinator (ADK Agent)                  │ │
│  │  • Orchestrates debate flow through phases                 │ │
│  │  • Uses tools ONLY (no direct core imports)                │ │
│  │  • Manages LLM sessions (fresh per turn)                   │ │
│  │  • Extracts responses from ADK events                      │ │
│  └────────────────────────┬───────────────────────────────────┘ │
│                            │                                      │
│  ┌────────────────────────▼───────────────────────────────────┐ │
│  │                   Debate Tools                              │ │
│  │  State Management:                                          │ │
│  │    • create_initial_state                                   │ │
│  │    • get_debate_state                                       │ │
│  │  Prompt Building:                                           │ │
│  │    • build_opening_prompt                                   │ │
│  │    • build_defence_prompt                                   │ │
│  │    • build_exchange_prompt                                  │ │
│  │    • build_reflection_prompt                                │ │
│  │    • build_summary_prompt                                   │ │
│  │  Recording:                                                 │ │
│  │    • record_opening                                         │ │
│  │    • record_defence                                         │ │
│  │    • record_exchange_message                                │ │
│  │    • record_reflection                                      │ │
│  │    • record_summary                                         │ │
│  │  Phase Management:                                          │ │
│  │    • advance_phase                                          │ │
│  │    • advance_exchange_round                                 │ │
│  └────────────────────────┬───────────────────────────────────┘ │
│                            │                                      │
│  ┌────────────────────────▼───────────────────────────────────┐ │
│  │                   Core Logic                                │ │
│  │  Persona Module:                                            │ │
│  │    • PersonaId enum (napoleon, gandhi, alexander, etc)     │ │
│  │    • Persona class with philosophy and display info        │ │
│  │    • Factory methods for each persona                      │ │
│  │  Debate Module:                                             │ │
│  │    • RoundPhase enum (opening, defence, exchange, etc)     │ │
│  │    • DebateState: Full debate state with messages          │ │
│  │    • DebateMessage: Individual message structure           │ │
│  └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ LLM API Calls
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│              Google Gemini API (via ADK)                         │
│  • Model: gemini-2.0-flash-exp                                   │
│  • Fresh session per turn for clean context                      │
│  • Generates persona responses based on prompts                  │
└───────────────────────────────────────────────────────────────────┘
```

## Key Architectural Patterns

### 1. Tool-Based Architecture

The coordinator **never imports core logic directly**. All operations go through tools.

**Why?**

- Enforces clean separation of concerns
- Makes the system more maintainable and testable
- Allows core logic to be tested independently
- Enables potential future use of tools via MCP

**How?**

```python
# ❌ BAD: Direct import
from backend.core.debate import DebateState
state = DebateState()

# ✅ GOOD: Via tools
from backend.tools.debate_tools import create_initial_state
state = create_initial_state()
```

### 2. Stateless LLM Calls

Each LLM turn uses a fresh session to prevent context pollution.

**Why?**

- Each persona response is based only on the current prompt
- Prevents unintended context leakage between turns
- Makes responses more predictable and testable

**How?**

```python
def _next_session_id(self) -> str:
    self._session_counter += 1
    return f"debate_session_{self._session_counter}"

async def _run_turn(self, prompt: str) -> str:
    session_id = self._next_session_id()  # Fresh session
    # ... create session and run
```

### 3. Immutable State Pattern

Tools return new state dicts rather than mutating existing ones.

**Why?**

- Makes state changes explicit and traceable
- Easier to debug and test
- Prevents accidental mutations

**How?**

```python
def record_opening(persona_id: str, text: str, state_dict: dict) -> dict:
    state = _state_from_dict(state_dict)  # Convert to object
    state.set_opening(PersonaId(persona_id), text)  # Modify
    return _state_to_dict(state)  # Return new dict
```

## Data Flow

### Debate Execution Flow

```
1. User clicks "Run Debate" in frontend
   ↓
2. Frontend sends POST /debate/run
   ↓
3. FastAPI creates DebateCoordinator
   ↓
4. Coordinator creates initial state via tools
   ↓
5. For each phase (opening, defence, exchange, reflection, summary):
   a. For each persona (or summariser):
      - Build prompt via tool
      - Send prompt to LLM (fresh session)
      - Extract response from LLM events
      - Record response via tool
   b. Advance phase via tool
   ↓
6. Return final state to frontend
   ↓
7. Frontend displays all messages
```

### State Transformation Flow

```
Initial State
    ↓
[Opening Phase]
    ↓ record_opening (Napoleon)
    ↓ record_opening (Gandhi)
    ↓ record_opening (Alexander)
    ↓ advance_phase("defence")
[Defence Phase]
    ↓ record_defence (Napoleon)
    ↓ record_defence (Gandhi)
    ↓ record_defence (Alexander)
    ↓ advance_phase("exchange")
[Exchange Phase - Round 1]
    ↓ record_exchange_message (Napoleon, round=1)
    ↓ record_exchange_message (Gandhi, round=1)
    ↓ record_exchange_message (Alexander, round=1)
    ↓ advance_exchange_round()
[Exchange Phase - Round 2]
    ↓ ... (repeat for each round)
    ↓ advance_phase("reflection")
[Reflection Phase]
    ↓ record_reflection (Napoleon)
    ↓ record_reflection (Gandhi)
    ↓ record_reflection (Alexander)
    ↓ advance_phase("summary")
[Summary Phase]
    ↓ record_summary (Summariser)
    ↓ advance_phase("done")
[Done]
Final State
```

## Component Details

### Frontend Components

**App.jsx**

- Root component
- Renders DebateView

**DebateView.jsx**

- Main debate interface
- "Run Debate" button
- Handles API calls
- Displays loading and error states
- Renders MessageList

**MessageList.jsx**

- Displays list of debate messages
- Maps messages to Message components
- Handles empty state

**Message.jsx**

- Individual message display
- Shows persona icon
- Shows persona name
- Shows message content

### Backend Modules

**app/main.py**

- FastAPI application setup
- CORS middleware configuration
- Global exception handler
- Health check endpoint
- Debate run endpoint

**agent/coordinator.py**

- DebateCoordinator class
- ADK agent setup
- Session management
- Debate orchestration logic
- LLM response extraction

**tools/debate_tools.py**

- All tool functions
- State conversion helpers
- Prompt building logic
- Recording logic
- Phase management

**core/persona.py**

- PersonaId enum
- Persona class
- Factory methods for each persona
- Philosophy definitions

**core/debate.py**

- RoundPhase enum
- DebateState class
- DebateMessage class
- State management methods

## Technology Stack

### Frontend

- **React 18.3**: UI framework
- **Vite 6.0**: Build tool and dev server
- **Jest 29.7**: Test runner
- **React Testing Library 16.0**: Component testing

### Backend

- **Python 3.10+**: Programming language
- **FastAPI 0.115+**: Web framework
- **Uvicorn 0.32+**: ASGI server
- **Google ADK 0.1+**: LLM orchestration
- **FastMCP 3.0+**: Tool definition (not actively used but available)
- **Pydantic 2.0+**: Data validation
- **pytest 8.0+**: Test framework

### Infrastructure

- **uv**: Python package manager
- **npm**: Node package manager
- **.env**: Environment configuration

## Design Decisions

### Why Tool-Based Architecture?

**Decision**: Use tools as the interface between coordinator and core logic.

**Rationale**:

- Enforces clean separation of concerns
- Makes testing easier (can test tools independently)
- Enables future MCP server implementation
- Prevents tight coupling between ADK and core logic

**Trade-offs**:

- More boilerplate code
- Slight performance overhead from conversions
- More complex for simple operations

### Why Fresh Sessions Per Turn?

**Decision**: Create a new LLM session for each persona response.

**Rationale**:

- Prevents context pollution between personas
- Makes responses more predictable
- Easier to debug (each turn is independent)
- Aligns with debate structure (each turn is a discrete statement)

**Trade-offs**:

- Cannot leverage conversation history in LLM context
- Must explicitly pass context via prompts
- More API calls (but negligible cost)

### Why Immutable State?

**Decision**: Tools return new state dicts rather than mutating.

**Rationale**:

- Makes state changes explicit
- Easier to debug (can trace state evolution)
- Prevents accidental mutations
- Aligns with functional programming principles

**Trade-offs**:

- More memory usage (creating new dicts)
- More verbose code
- Slight performance overhead

### Why Single API Call for Full Debate?

**Decision**: Frontend makes one POST request that runs the entire debate.

**Rationale**:

- Simpler implementation for MVP
- No need for WebSocket or streaming infrastructure
- Easier error handling
- Clearer transaction boundaries

**Trade-offs**:

- No real-time progress updates
- Long request duration (30-60 seconds)
- Cannot cancel mid-debate
- Poor user experience for slow connections

## Security Architecture

### API Key Management

- Stored in `.env` file (excluded from git)
- Loaded via python-dotenv
- Never exposed in responses
- Validated on startup

### CORS Configuration

- Configurable allowed origins
- Default: localhost:3000, 127.0.0.1:3000
- Credentials allowed for future auth
- Wildcard (\*) not used

### Error Handling

- All errors return JSON (never HTML)
- Generic messages to users
- Detailed logs server-side only
- Appropriate HTTP status codes

## Testing Architecture

### Backend Tests (27 tests)

**Persona Tests** (5):

- Test persona factory methods
- Test philosophy strings
- Test debaters() excludes summariser

**DebateState Tests** (5):

- Test state initialization
- Test message addition
- Test opening/reflection storage
- Test transcript generation

**Tools Tests** (14):

- Test state creation
- Test prompt building for each phase
- Test recording for each phase
- Test phase advancement

**API Tests** (3):

- Test health endpoint
- Test debate run with mocked coordinator
- Test 503 when ADK not installed

### Frontend Tests (11 tests)

**Component Tests**:

- Message component rendering
- MessageList component rendering
- DebateView component rendering
- Button interactions
- Loading states
- Error states

## Performance Considerations

### LLM Call Optimization

- Fresh sessions prevent context bloat
- Concise prompts (2-3 sentence responses)
- Limited transcript in context (last 50 messages)

### Frontend Optimization

- Single API call for entire debate
- No streaming (simpler implementation)
- Minimal re-renders (React best practices)

### Backend Optimization

- Async/await for concurrent operations
- Pydantic for fast validation
- In-memory state (no database overhead)

## Future Architecture Considerations

### Streaming Support

- Add WebSocket endpoint
- Stream LLM responses as they arrive
- Update frontend in real-time
- Handle connection errors gracefully

### Persistent Storage

- Add PostgreSQL database
- Store debate history
- Add API to retrieve past debates
- Add frontend to view history

### Scalability

- Add Redis for caching
- Use Celery for async debate execution
- Add load balancer for multiple instances
- Use CDN for frontend assets

### Monitoring

- Add structured logging
- Add metrics collection (Prometheus)
- Add distributed tracing (OpenTelemetry)
- Add error tracking (Sentry)

## Deployment Architecture

### Development

```
┌─────────────────┐     ┌─────────────────┐
│   Frontend      │     │    Backend      │
│   Vite Dev      │────▶│    Uvicorn      │
│   Port 3000     │     │    Port 8000    │
└─────────────────┘     └─────────────────┘
```

### Production (Recommended)

```
┌─────────────────┐
│   Nginx/Caddy   │
│   (Reverse      │
│    Proxy)       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│Static │ │Backend│
│Files  │ │Gunicorn│
│(React)│ │+Uvicorn│
└───────┘ └───────┘
```

## Conclusion

Simulacra's architecture prioritizes:

1. **Clean separation** via tool-based design
2. **Predictability** via stateless LLM calls
3. **Maintainability** via immutable state
4. **Simplicity** via single API call for MVP
5. **Security** via proper credential management

The architecture is designed to be simple enough for rapid development while maintaining clean boundaries that enable future enhancements.

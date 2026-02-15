# Simulacra Multi-Agent Debate System - Improvements

## Overview

This spec documents the improvements needed for the Simulacra multi-agent debate system after running and testing the application. The system allows three historical personas (Napoleon, Gandhi, Alexander) and a Summariser agent to engage in structured debates using Google ADK and FastMCP.

## User Stories

### 1. Security and Configuration

**As a developer**, I want to ensure API keys are never committed to the repository so that credentials remain secure.

**Acceptance Criteria:**

- 1.1 The .env.example file must not contain real API keys
- 1.2 The .env file must be in .gitignore
- 1.3 Documentation must clearly explain how to obtain and configure API keys
- 1.4 The application must provide clear error messages when API keys are missing or invalid

### 2. Application Startup and Running

**As a developer**, I want clear instructions and scripts to run both frontend and backend so that I can quickly start the application.

**Acceptance Criteria:**

- 2.1 Backend can be started with a single command using the .venv environment
- 2.2 Frontend can be started with a single command
- 2.3 Health check endpoint returns proper status
- 2.4 Clear error messages when dependencies are missing

### 3. Testing and Quality Assurance

**As a developer**, I want comprehensive test coverage so that I can confidently make changes.

**Acceptance Criteria:**

- 3.1 All backend tests pass (27 tests)
- 3.2 All frontend tests pass (11 tests)
- 3.3 Tests cover core functionality: personas, debate state, tools, and UI components
- 3.4 Test script runs all tests and reports results clearly

### 4. Error Handling and Resilience

**As a user**, I want clear error messages when something goes wrong so that I can understand and fix issues.

**Acceptance Criteria:**

- 4.1 API returns JSON error responses (not HTML)
- 4.2 Missing API key returns 503 with helpful message
- 4.3 Invalid API key returns clear error message
- 4.4 Frontend handles backend errors gracefully

### 5. Documentation and Architecture

**As a developer**, I want clear documentation of the system architecture so that I can understand and extend the system.

**Acceptance Criteria:**

- 5.1 Architecture diagram shows component relationships
- 5.2 Documentation explains ADK coordinator pattern
- 5.3 Tool contracts are well-documented
- 5.4 README includes troubleshooting section

## Issues Found

### Critical Issues

1. **Leaked API Key**: The .env.example file contained a real, leaked Google API key that has been blocked
2. **Security Risk**: Real credentials were committed to the repository

### Fixed Issues

1. ✅ Removed leaked API key from .env and .env.example
2. ✅ Updated model name to gemini-2.0-flash-exp (current recommended model)
3. ✅ Verified all tests pass (27 backend + 11 frontend)
4. ✅ Verified backend and frontend can start successfully

## Technical Requirements

### Environment Setup

- Python 3.10+ with .venv virtual environment
- Node.js 18+ for frontend
- Google API key for Gemini models
- uv package manager for Python dependencies

### Architecture Principles

- **Separation of Concerns**: ADK coordinator uses tools only, never imports core logic directly
- **Tool-Based Design**: All debate operations exposed as tools with clear contracts
- **Stateless LLM Calls**: Each LLM turn uses a fresh session for clean context
- **Type Safety**: Pydantic models for all data structures

### Testing Strategy

- **Backend**: pytest with 27 tests covering personas, debate state, tools, and API
- **Frontend**: Jest + React Testing Library with 11 tests covering components and interactions
- **Integration**: Manual testing of full debate flow

## Non-Functional Requirements

### Performance

- Debate should complete within reasonable time (< 2 minutes for 1 exchange round)
- Frontend should be responsive during debate execution

### Security

- No credentials in source code
- Environment variables for all sensitive configuration
- CORS properly configured for frontend-backend communication

### Maintainability

- Clear separation between core logic, tools, and coordinator
- Comprehensive test coverage
- Well-documented code and architecture

## Out of Scope

- Real-time streaming of debate messages
- Persistent storage of debate history
- User authentication and authorization
- Multiple concurrent debates

## Dependencies

- google-adk >= 0.1.0
- fastmcp >= 3.0.0
- fastapi >= 0.115.0
- uvicorn >= 0.32.0
- pydantic >= 2.0
- react >= 18.3.1
- vite >= 6.0.1

## Success Metrics

- All tests pass (38 total: 27 backend + 11 frontend)
- Application starts without errors
- Debate completes successfully with valid API key
- No security vulnerabilities in configuration

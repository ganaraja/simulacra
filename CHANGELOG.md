# Changelog

All notable changes to the Simulacra project are documented in this file.

## [Unreleased]

### Added

- **Rate Limiting Mitigation**: Automatic retry logic with exponential backoff
  - Retries up to 3 times on 429 RESOURCE_EXHAUSTED errors
  - Exponential backoff: 3s, 6s, 12s delays
  - Parses suggested retry delay from error messages
  - Strategic delays between API calls (1-2 seconds)
  - Comprehensive logging for debugging
- **RATE_LIMITING.md**: Comprehensive guide for handling rate limits
  - Explanation of free tier limits
  - Mitigation strategies
  - Configuration options
  - Troubleshooting guide
  - Best practices for development and production

### Changed

- **Coordinator**: Enhanced with retry logic and delays
  - Added `MAX_RETRIES` and `INITIAL_RETRY_DELAY` constants
  - Modified `_run_turn()` to handle rate limit errors
  - Added delays between personas (1s) and phases (2s)
  - Added logging for phase transitions and retries
- **Documentation**: Updated README.md with rate limiting troubleshooting

### Fixed

- Rate limiting errors now handled gracefully with automatic retries
- Better error messages for rate limit scenarios

## [0.1.1] - 2026-02-15

### Security

#### Fixed

- **CRITICAL**: Removed leaked Google API key from `.env` and `.env.example` files
  - The leaked key was reported and blocked by Google
  - Replaced with placeholder: `your_google_api_key_here`
  - Added security warnings throughout documentation

#### Added

- Comprehensive `SECURITY.md` document with:
  - API key management best practices
  - Environment variable security guidelines
  - CORS configuration recommendations
  - Incident response procedures
  - Security checklist for deployment

### Documentation

#### Added

- `ARCHITECTURE.md` - Detailed system architecture documentation
  - Component diagrams and data flow
  - Design pattern explanations
  - Technology stack details
  - Future architecture considerations
- `QUICKSTART.md` - 5-minute setup guide for new users
  - Step-by-step installation
  - Quick troubleshooting
  - Project structure overview
- `CHANGELOG.md` - This file, tracking all changes
- `.kiro/specs/simulacra-improvements/` - Comprehensive spec documentation
  - `requirements.md` - User stories and acceptance criteria
  - `design.md` - Detailed design document with correctness properties
  - `tasks.md` - Implementation task list
  - `SUMMARY.md` - Summary of all improvements
- `scripts/verify_system.sh` - Comprehensive system verification script
  - Checks dependencies, tests, security, and documentation
  - Provides clear status output with color coding
  - Verifies running servers

#### Updated

- `README.md` - Enhanced with:
  - Security warnings about API keys
  - Comprehensive troubleshooting section
  - Instructions for obtaining Google API keys
  - Reference to QUICKSTART.md
  - System verification script documentation
- `Specifications.md` - Added:
  - Security considerations section
  - References to new documentation
  - Updated document history
- `.env.example` - Updated:
  - Removed leaked API key
  - Changed model to `gemini-2.0-flash-exp` (current recommended)
  - Added clearer comments

### Testing

#### Verified

- All 27 backend tests passing
  - 5 Persona tests
  - 5 DebateState tests
  - 14 Tools tests
  - 3 API tests
- All 11 frontend tests passing
  - 4 Component test suites
  - Message, MessageList, DebateView, and App components

#### Added

- System verification script that runs all tests
- Documentation verification
- Security checks in verification script

### Configuration

#### Changed

- Updated default model from `gemini-2.5-flash-lite` to `gemini-2.0-flash-exp`
- Improved environment variable documentation
- Added security warnings to configuration files

### Infrastructure

#### Added

- Comprehensive verification script (`scripts/verify_system.sh`)
- Better error messages for missing dependencies
- Health check verification

## [0.1.0] - Initial Release

### Added

- Multi-agent debate system with three personas:
  - Napoleon (Conqueror)
  - Gandhi (Pacifist)
  - Alexander (Ambition)
  - Summariser (Neutral)
- Backend (Python + FastAPI):
  - ADK coordinator for LLM orchestration
  - Tool-based architecture
  - Core logic (personas, debate state)
  - FastMCP tool definitions
  - Comprehensive test suite (27 tests)
- Frontend (React + Vite):
  - DebateView component
  - MessageList component
  - Message component with persona icons
  - Test suite (11 tests)
- Debate flow:
  - Opening statements
  - Defence round
  - Exchange rounds (3-4 rounds)
  - Reflection round
  - Summary
- Documentation:
  - README.md with setup instructions
  - Specifications.md with technical requirements
  - Test documentation
- Infrastructure:
  - Python virtual environment setup
  - npm package management
  - Environment variable configuration
  - CORS middleware
  - Global exception handling

### Technical Details

- Python 3.10+ support
- Node.js 18+ support
- Google ADK integration
- FastMCP for tool serving
- Pydantic for data validation
- pytest for backend testing
- Jest + React Testing Library for frontend testing

---

## Version History

- **0.1.1** (2026-02-15) - Security fixes, comprehensive documentation
- **0.1.0** (Initial) - Initial release with core functionality

## Upgrade Guide

### From 0.1.0 to 0.1.1

1. **Update API Key** (CRITICAL):

   ```bash
   # Edit .env file
   nano .env

   # Replace the old API key with a new one from:
   # https://aistudio.google.com/app/apikey
   ```

2. **Update Model Name**:

   ```bash
   # In .env, change:
   # GOOGLE_API_MODEL=gemini-2.5-flash-lite
   # to:
   GOOGLE_API_MODEL=gemini-2.0-flash-exp
   ```

3. **Verify System**:

   ```bash
   ./scripts/verify_system.sh
   ```

4. **Review Security Documentation**:
   - Read `SECURITY.md` for best practices
   - Review `ARCHITECTURE.md` for system design
   - Check `QUICKSTART.md` for updated setup

## Breaking Changes

### 0.1.1

- None (backward compatible)

## Deprecations

### 0.1.1

- Model `gemini-2.5-flash-lite` is deprecated, use `gemini-2.0-flash-exp`

## Known Issues

### 0.1.1

- Debate execution takes 30-60 seconds with no progress indicator
- Cannot cancel debate mid-execution
- No persistent storage of debate history
- No real-time streaming of responses

See `.kiro/specs/simulacra-improvements/tasks.md` for planned improvements.

## Contributors

- Initial development team
- Security audit and improvements (2026-02-15)

## Links

- [GitHub Repository](https://github.com/yourusername/simulacra)
- [Documentation](./README.md)
- [Architecture](./ARCHITECTURE.md)
- [Security](./SECURITY.md)
- [Quick Start](./QUICKSTART.md)

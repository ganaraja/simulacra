# Simulacra Quick Start Guide

Get the Simulacra multi-agent debate system running in 5 minutes.

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Google API key ([Get one here](https://aistudio.google.com/app/apikey))

## Quick Setup

### 1. Clone and Setup Environment

```bash
# Navigate to the project directory
cd simulacra

# Create and activate virtual environment (if not already done)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Configure API Key

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Google API key
# Replace "your_google_api_key_here" with your actual key
nano .env  # or use your preferred editor
```

**Important**: Get your API key from https://aistudio.google.com/app/apikey

### 3. Install Dependencies

```bash
# Backend dependencies
uv sync
# or: pip install -e ".[dev]"

# Frontend dependencies
cd src/frontend
npm install
cd ../..
```

### 4. Verify Installation

```bash
# Run the verification script
./scripts/verify_system.sh
```

This will check:

- ✓ Python and Node versions
- ✓ Dependencies installed
- ✓ All tests passing (38 total)
- ✓ Configuration correct
- ✓ No security issues

### 5. Start the Application

**Terminal 1 - Backend:**

```bash
PYTHONPATH=src .venv/bin/python3 -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**

```bash
cd src/frontend
npm run dev
```

### 6. Access the Application

Open your browser and navigate to:

```
http://localhost:3000
```

Click "Run Debate" to start a debate between Napoleon, Gandhi, and Alexander!

## What Happens During a Debate?

1. **Opening Statements**: Each persona gives their initial position
2. **Defence Round**: Each persona defends their position
3. **Exchange Rounds**: 3-4 rounds of back-and-forth discussion
4. **Reflection**: Each persona reflects on whether they would change their position
5. **Summary**: The Summariser provides a neutral overview

The entire debate takes about 30-60 seconds to complete.

## Troubleshooting

### "Your API key was reported as leaked"

- Your API key has been compromised
- Generate a new key at https://aistudio.google.com/app/apikey
- Update your `.env` file with the new key

### "503 Service Unavailable"

- Check that `GOOGLE_API_KEY` is set in your `.env` file
- Verify the API key is valid
- Ensure google-adk is installed: `pip list | grep google-adk`

### Backend won't start

- Ensure you're using the .venv environment: `source .venv/bin/activate`
- Check that port 8000 is not in use: `lsof -i :8000`
- Verify PYTHONPATH is set: `PYTHONPATH=src`

### Frontend won't start

- Run `npm install` in `src/frontend` directory
- Check that port 3000 is not in use: `lsof -i :3000`
- Clear cache: `rm -rf node_modules && npm install`

### Tests fail

- Backend: `PYTHONPATH=src pytest tests/ -v`
- Frontend: `cd src/frontend && npm run test`
- Check error messages for specific issues

## Running Tests

```bash
# All tests
./scripts/run_tests.sh

# Backend only (27 tests)
PYTHONPATH=src python3 -m pytest tests/ -v

# Frontend only (11 tests)
cd src/frontend && npm run test
```

## Project Structure

```
simulacra/
├── src/
│   ├── backend/          # Python backend
│   │   ├── app/          # FastAPI application
│   │   ├── agent/        # ADK coordinator
│   │   ├── core/         # Core logic (personas, debate state)
│   │   └── tools/        # Debate tools
│   └── frontend/         # React frontend
│       └── src/
│           ├── components/  # React components
│           └── __tests__/   # Frontend tests
├── tests/                # Backend tests
├── scripts/              # Utility scripts
├── .env                  # Environment config (not in git)
├── README.md             # Full documentation
├── ARCHITECTURE.md       # System architecture
└── SECURITY.md           # Security best practices
```

## Key Features

- **Multi-Agent Debate**: Three historical personas engage in structured debate
- **Tool-Based Architecture**: Clean separation between coordinator and core logic
- **Comprehensive Testing**: 38 tests (27 backend + 11 frontend)
- **Type Safety**: Pydantic models for all data structures
- **Security**: Environment-based configuration, no credentials in code

## Next Steps

1. **Read the Documentation**:
   - [README.md](./README.md) - Full setup and usage
   - [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
   - [SECURITY.md](./SECURITY.md) - Security best practices

2. **Explore the Code**:
   - `src/backend/core/` - Persona and debate state definitions
   - `src/backend/tools/` - Tool implementations
   - `src/backend/agent/` - ADK coordinator
   - `src/frontend/src/` - React components

3. **Run a Debate**:
   - Start both backend and frontend
   - Open http://localhost:3000
   - Click "Run Debate"
   - Watch the personas interact!

4. **Customize**:
   - Modify persona philosophies in `src/backend/core/persona.py`
   - Adjust debate flow in `src/backend/agent/coordinator.py`
   - Customize UI in `src/frontend/src/components/`

## Getting Help

- Check [README.md](./README.md) for detailed documentation
- Review [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
- See [SECURITY.md](./SECURITY.md) for security guidelines
- Run `./scripts/verify_system.sh` to diagnose issues

## Development Workflow

1. Make changes to code
2. Run tests: `./scripts/run_tests.sh`
3. Fix any failures
4. Verify system: `./scripts/verify_system.sh`
5. Commit changes

## Production Deployment

For production deployment:

1. Set environment variables properly
2. Use gunicorn with uvicorn workers for backend
3. Build frontend: `cd src/frontend && npm run build`
4. Serve static files with nginx or similar
5. Use HTTPS
6. Enable rate limiting
7. Set up monitoring and logging

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed deployment architecture.

## License

See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and verification
5. Submit a pull request

---

**Ready to debate?** Start the servers and open http://localhost:3000!

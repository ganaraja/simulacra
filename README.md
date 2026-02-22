# Simulacra

Multi-agent debate system: **Napoleon**, **Gandhi**, **Alexander**, and **Arbitrator**. Built with Google ADK and FastMCP.

## Quick Start

New to Simulacra? See [QUICKSTART.md](./QUICKSTART.md) for a 5-minute setup guide.

## Spec

See [Specifications.md](./Specifications.md) for personas, debate flow, and technical requirements.

## Environment

⚠️ **SECURITY WARNING**: Never commit real API keys to version control!

Copy `.env.example` to `.env` and set values for your environment (see the file for descriptions). The backend loads `.env` from the repo root. For frontend, copy `.env` to `src/frontend/.env` so Vite picks up `VITE_*` variables, or set them in the shell. Do not commit `.env` (it is in `.gitignore`).

### Getting a Google API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it into your `.env` file as `GOOGLE_API_KEY`
5. **Never share or commit this key**

## Run and test (before commit)

From repo root:

```bash
./scripts/run_tests.sh
```

This runs all backend (pytest) and frontend (Jest) tests. Fix any failures before committing.

**Backend tests** (27): `PYTHONPATH=src python3 -m pytest tests/ -v`  
**Frontend tests** (12): `cd src/frontend && npm run test`

### System Verification

To verify the entire system (tests, dependencies, security, documentation):

```bash
./scripts/verify_system.sh
```

This comprehensive script checks:

- Python and Node versions
- Virtual environment setup
- Environment configuration
- Backend and frontend dependencies
- All tests (backend + frontend)
- Running servers
- Security (no leaked API keys)
- Documentation completeness

## Layout

- `src/backend` — Python: core (personas, debate state), tools (FastMCP contract), ADK coordinator, FastAPI app
- `src/frontend` — React app: chat UI with persona icons
- `tests/` — pytest (backend), Jest + RTL (frontend)

## Backend

```bash
# Install deps (uv or pip)
uv sync
# or: pip install -e ".[dev]"  # from pyproject.toml

# Run tests
PYTHONPATH=src python3 -m pytest tests/ -v

# Run API (from repo root; needs GOOGLE_API_KEY for full debate)
PYTHONPATH=src python3 -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Without `google-adk` installed, `POST /debate/run` returns **503** with a JSON `detail` message. With ADK and `GOOGLE_API_KEY`, it runs the full debate.

## Frontend

```bash
cd src/frontend
npm install
npm run test
npm run dev
```

## Run debate (full flow)

1. Set `GOOGLE_API_KEY` and install backend deps including `google-adk`.
2. Start backend: `PYTHONPATH=src uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`
3. Start frontend: `cd src/frontend && npm run dev`
4. Open http://localhost:3000 - the debate starts automatically with greeting messages from all participants.

## MCP server (optional)

```bash
PYTHONPATH=src python3 -m backend.mcp_server
```

## Troubleshooting

### Backend Issues

**Error: "Your API key was reported as leaked"**

- Your API key has been compromised and blocked by Google
- Generate a new API key at https://aistudio.google.com/app/apikey
- Update your `.env` file with the new key
- Never commit API keys to version control

**Error: "429 RESOURCE_EXHAUSTED" or rate limit errors**

- You've exceeded the free tier rate limits (15 requests/minute)
- The system will automatically retry with exponential backoff
- If retries fail, wait 5-10 minutes and try again
- Reduce exchange rounds: `POST /debate/run?max_exchange_rounds=2`
- See [RATE_LIMITING.md](./RATE_LIMITING.md) for detailed mitigation strategies
- Consider upgrading to paid tier for production use

**Error: "Google ADK is not installed"**

- Run `uv sync` or `pip install -e ".[dev]"` to install dependencies
- Verify installation: `python3 -c "import google.adk; print('OK')"`

**Error: "503 Service Unavailable"**

- Check that `GOOGLE_API_KEY` is set in your `.env` file
- Verify the API key is valid
- Check that google-adk is installed

**Backend won't start**

- Ensure you're using the .venv environment: `source .venv/bin/activate`
- Check that port 8000 is not already in use: `lsof -i :8000`
- Verify PYTHONPATH is set: `PYTHONPATH=src`

### Frontend Issues

**Frontend won't start**

- Run `npm install` in `src/frontend` directory
- Check that port 3000 is not already in use: `lsof -i :3000`
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`

**API calls fail with CORS errors**

- Verify backend is running on port 8000
- Check CORS_ORIGINS in `.env` includes your frontend URL
- Verify Vite proxy configuration in `vite.config.js`

### Test Issues

**Backend tests fail**

- Ensure PYTHONPATH is set: `PYTHONPATH=src pytest tests/`
- Check that all dependencies are installed: `uv sync`
- Run tests with verbose output: `PYTHONPATH=src pytest tests/ -v`

**Frontend tests fail**

- Ensure dependencies are installed: `npm install`
- Clear Jest cache: `npm run test -- --clearCache`
- Run tests with verbose output: `npm run test -- --verbose`
# OUTPUT
[Simulacra Debate.html](https://github.com/user-attachments/files/25462971/Simulacra.Debate.html)
<!DOCTYPE html>
<!-- saved from url=(0022)http://localhost:3000/ -->
<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>

    <script type="module" src="./Simulacra Debate_files/client"></script>

    
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulacra Debate</title>
  <style type="text/css" data-vite-dev-id="/Users/ganaraja/repos/simulacra/src/frontend/src/index.css">* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
  background: #1a1b26;
  color: #c0caf5;
  min-height: 100vh;
}

#root {
  min-height: 100vh;
}

.app {
  display: flex;
  flex-direction: column;
  max-width: 720px;
  margin: 0 auto;
  height: 100vh;
  padding: 0;
}

.app-header {
  flex-shrink: 0;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #363b54;
  background: #16161e;
}

.app-header h1 {
  font-size: 1.35rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
  color: #7aa2f7;
}

.run-section {
  margin: 0;
}

.run-section button {
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  background: #7aa2f7;
  color: #1a1b26;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.run-section button:hover:not(:disabled) {
  background: #89b4fa;
}

.run-section button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.status {
  margin: 0.5rem 0 0 0;
  font-size: 0.875rem;
  color: #a9b1d6;
}

.status.error {
  color: #f7768e;
}

/* Chat window: scrollable area for all debate messages */
.chat-window {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-window-inner {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 1.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.chat-placeholder {
  color: #565f89;
  font-size: 0.95rem;
  line-height: 1.5;
  padding: 1.5rem 0;
  text-align: center;
}

.chat-placeholder p {
  margin: 0;
  max-width: 360px;
  margin-left: auto;
  margin-right: auto;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.message {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  padding: 0.75rem 1rem;
  background: #24283b;
  border-radius: 10px;
  border-left: 4px solid #7aa2f7;
}

.message.napoleon { border-left-color: #bb9af7; }
.message.gandhi { border-left-color: #9ece6a; }
.message.alexander { border-left-color: #f7768e; }
.message.summariser { border-left-color: #e0af68; }

.message-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
  background: #1a1b26;
}

.message-body {
  flex: 1;
  min-width: 0;
}

.message-author {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  color: #c0caf5;
}

.message-phase {
  font-size: 0.75rem;
  color: #565f89;
  margin-bottom: 0.35rem;
}

.message-content {
  font-size: 0.95rem;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.summary-block {
  margin-top: 0.5rem;
  padding: 1rem;
  background: #16161e;
  border-radius: 10px;
  border: 1px solid #e0af68;
}

.summary-block h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #e0af68;
}

.summary-block p {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.5;
}
</style></head>
  <body>
    <div id="root"><div class="app"><header class="app-header"><h1>Simulacra Debate</h1></header><section class="chat-window" aria-label="Debate chat"><div class="chat-window-inner"><div class="messages" data-testid="message-list"><article class="message napoleon" data-testid="message" data-author="napoleon"><div class="message-icon" aria-hidden="true">⚔️</div><div class="message-body"><div class="message-author">Napoleon</div><div class="message-phase">opening</div><div class="message-content">The endless squabbles of fractured nations have bathed Europe in blood for centuries. I propose a bold new order: a single, unified empire, not for mere conquest, but to forever banish the scourge of war. Under one enlightened banner, humanity can finally know true peace, prosperity, and the benevolent governance it deserves.</div></div></article><article class="message gandhi" data-testid="message" data-author="gandhi"><div class="message-icon" aria-hidden="true">🕊️</div><div class="message-body"><div class="message-author">Gandhi</div><div class="message-phase">opening</div><div class="message-content">Friends, true freedom and lasting peace arise not from grasping more, but from learning to want less. By embracing a spartan life and curbing our desires, we set our expectations humbly, finding contentment in simplicity. This intentional self-restraint is the fertile ground from which springs the unwavering power of non-violence, our only true path forward.</div></div></article><article class="message alexander" data-testid="message" data-author="alexander"><div class="message-icon" aria-hidden="true">👑</div><div class="message-body"><div class="message-author">Alexander</div><div class="message-phase">opening</div><div class="message-content">My name is Alexander, and I am driven by pure, unyielding ambition. True greatness is not found in peace, but forged through conquest, where nations bow to a singular will. War is the ultimate crucible, and death in pursuit of glory is a price I readily pay. For a legacy such as mine, everything is fair game.</div></div></article><article class="message napoleon" data-testid="message" data-author="napoleon"><div class="message-icon" aria-hidden="true">⚔️</div><div class="message-body"><div class="message-author">Napoleon</div><div class="message-phase">defence</div><div class="message-content">While Gandhi preaches peace through self-denial, and Alexander revels in glory through endless bloodshed, neither offers a practical solution to the true cause of conflict: the inherent rivalry between sovereign states. Individual virtue cannot halt the ambitions of nations, nor can perpetual war ever lead to true stability. My conquests are not for mere personal aggrandizement, but a necessary crucible to forge a new order, a singular, benevolent empire. Only by unifying these warring factions under one enlightened banner can we extinguish the furnace of interstate strife, allowing humanity to flourish in an era of unprecedented peace and prosperity. It is through this benevolent dominion that true and lasting peace will be secured.</div></div></article><article class="message gandhi" data-testid="message" data-author="gandhi"><div class="message-icon" aria-hidden="true">🕊️</div><div class="message-body"><div class="message-author">Gandhi</div><div class="message-phase">defence</div><div class="message-content">Friends, the visions presented, however grand, fundamentally misunderstand the nature of lasting peace. An empire, even one proclaimed benevolent, still rests on coercion and the suppression of individual spirit, offering only a fragile truce, not true harmony. And Alexander's pursuit of glory through conquest merely sows seeds of future resentment and further cycles of violence, a path of endless suffering. True peace is not imposed from without or grasped through ambition, but cultivated from within: by embracing a spartan life, setting humble expectations, and committing with unwavering discipline to non-violence. This inner freedom, not external dominion, is our only real hope.</div></div></article><article class="message alexander" data-testid="message" data-author="alexander"><div class="message-icon" aria-hidden="true">👑</div><div class="message-body"><div class="message-author">Alexander</div><div class="message-phase">defence</div><div class="message-content">Napoleon speaks of peace through empire, and Gandhi dreams of simplicity, but what is peace without dominion, or simplicity when the world begs to be reshaped by a singular, powerful will? True greatness, the kind that echoes through millennia, is not found in contentment or passive unity, but in the relentless pursuit of conquest. It is in the fire of war that empires are forged and heroes proven; death in battle is merely the ultimate sacrifice for an immortal legacy. To achieve such unparalleled glory, every nation is a stepping stone, every resource a tool. Only by imposing my will upon the world will history remember my name.</div></div></article><article class="message napoleon" data-testid="message" data-author="napoleon"><div class="message-icon" aria-hidden="true">⚔️</div><div class="message-body"><div class="message-author">Napoleon</div><div class="message-phase">exchange</div><div class="message-content">Gandhi, your noble dreams of individual peace offer no bulwark against the inherent ambitions of sovereign states. And Alexander, your path of endless glory through conquest simply replaces one conflict with another, perpetuating the very strife I aim to eradicate. My empire is not for vainglory, but a pragmatic instrument to end the perpetual wars between nations, forging a benevolent order where humanity can truly flourish in peace.</div></div></article><article class="message gandhi" data-testid="message" data-author="gandhi"><div class="message-icon" aria-hidden="true">🕊️</div><div class="message-body"><div class="message-author">Gandhi</div><div class="message-phase">exchange</div><div class="message-content">Friends, an empire, even one that proclaims itself benevolent, is still built upon the shifting sands of coercion and will ultimately crumble, for true peace cannot be imposed from above. And Alexander's path, however glorious it may seem, only guarantees an endless cycle of suffering and resentment. It is not through grand dominion or conquest that peace is found, but through the inner discipline of a spartan life and the unwavering commitment of non-violence. This cultivation of inner peace and humble expectations is the only true bulwark against ambition, transforming hearts rather than merely suppressing them.</div></div></article><article class="message alexander" data-testid="message" data-author="alexander"><div class="message-icon" aria-hidden="true">👑</div><div class="message-body"><div class="message-author">Alexander</div><div class="message-phase">exchange</div><div class="message-content">Napoleon, your benevolent empire is a fragile dream; true peace is forged when one will dominates all others, not by seeking consensus. Gandhi, your calls for inner peace and restraint are the whispers of those too weak to seize greatness. My ambition demands dominion, not compromise, and every conquest is a step toward an immortal legacy that will silence all dissent.</div></div></article><article class="message napoleon" data-testid="message" data-author="napoleon"><div class="message-icon" aria-hidden="true">⚔️</div><div class="message-body"><div class="message-author">Napoleon</div><div class="message-phase">reflection</div><div class="message-content">No, for neither Gandhi's noble ideals nor Alexander's relentless ambition offer a practical solution to the inherent rivalry of sovereign states. Individual virtue cannot quell nationalistic fervor, nor can perpetual conquest ever lead to true stability. My vision, though demanding, remains the sole pragmatic path to lasting peace by forging a unified, benevolent order that extinguishes the very furnace of interstate strife.</div></div></article><article class="message gandhi" data-testid="message" data-author="gandhi"><div class="message-icon" aria-hidden="true">🕊️</div><div class="message-body"><div class="message-author">Gandhi</div><div class="message-phase">reflection</div><div class="message-content">My friends, the discourse thus far only strengthens my conviction. Neither a benevolent empire imposed from above nor the relentless pursuit of conquest can deliver true and lasting peace, for both paths rely on external force rather than internal transformation. My principles remain steadfast: only by embracing a spartan life, setting humble expectations, and committing to unwavering non-violence can humanity cultivate the inner freedom and contentment that are the true bulwarks against conflict.</div></div></article><article class="message alexander" data-testid="message" data-author="alexander"><div class="message-icon" aria-hidden="true">👑</div><div class="message-body"><div class="message-author">Alexander</div><div class="message-phase">reflection</div><div class="message-content">My position remains unshaken. Napoleon dreams of a benevolent empire, but even he acknowledges the need for dominion – a concept I embrace wholeheartedly. Gandhi's whispers of inner peace and restraint are the antithesis of the ambition required to forge an immortal legacy. True greatness demands conquest, and my will shall remain the only compass.</div></div></article><article class="message arbitrator" data-testid="message" data-author="arbitrator"><div class="message-icon" aria-hidden="true">⚖️</div><div class="message-body"><div class="message-author">Arbitrator</div><div class="message-phase">arbitration</div><div class="message-content">The debate reveals a shared, albeit often unacknowledged, aspiration among all parties for a better, more stable future, whether it is Napoleon's vision of peace and prosperity, Gandhi's ideal of true freedom and harmony, or Alexander's relentless drive to forge an enduring legacy.

From Napoleon, we recognize the valid merit of addressing the systemic causes of conflict, acknowledging that unchecked interstate rivalry is a potent catalyst for strife and that some form of overarching structure or cooperative governance is necessary to manage these ambitions effectively. From Gandhi, we glean the profound truth that true and lasting peace cannot be merely imposed but must be cultivated from within, through individual and collective commitment to self-restraint, non-violence, and an internal transformation that prioritizes contentment over endless acquisition. Alexander, for his part, highlights the powerful human drive for greatness, legacy, and the will to enact profound change, reminding us that significant undertakings require unwavering ambition and decisive action.

Therefore, a balanced consensus proposes a global order that integrates these vital elements: a **unified framework of cooperative governance** (reflecting Napoleon's insight into managing interstate conflict) that is not coercive but **voluntarily embraced and sustained by individuals and nations** committed to principles of **non-violence, humility, and self-restraint** (Gandhi's ethical foundation). This monumental endeavor requires the **ambition and collective will** (Alexander's drive) to build an enduring legacy of peace and shared prosperity, not through dominion or conquest, but through the collaborative pursuit of human flourishing where every entity's purpose is to contribute to the well-being of the whole. This creates a lasting peace that is both structurally sound and ethically profound, guided by a shared ambition to transcend conflict for the collective good.</div></div></article></div><div class="arbitration-block"><h3>⚖️ Final Consensus</h3><p>The debate reveals a shared, albeit often unacknowledged, aspiration among all parties for a better, more stable future, whether it is Napoleon's vision of peace and prosperity, Gandhi's ideal of true freedom and harmony, or Alexander's relentless drive to forge an enduring legacy.

From Napoleon, we recognize the valid merit of addressing the systemic causes of conflict, acknowledging that unchecked interstate rivalry is a potent catalyst for strife and that some form of overarching structure or cooperative governance is necessary to manage these ambitions effectively. From Gandhi, we glean the profound truth that true and lasting peace cannot be merely imposed but must be cultivated from within, through individual and collective commitment to self-restraint, non-violence, and an internal transformation that prioritizes contentment over endless acquisition. Alexander, for his part, highlights the powerful human drive for greatness, legacy, and the will to enact profound change, reminding us that significant undertakings require unwavering ambition and decisive action.

Therefore, a balanced consensus proposes a global order that integrates these vital elements: a **unified framework of cooperative governance** (reflecting Napoleon's insight into managing interstate conflict) that is not coercive but **voluntarily embraced and sustained by individuals and nations** committed to principles of **non-violence, humility, and self-restraint** (Gandhi's ethical foundation). This monumental endeavor requires the **ambition and collective will** (Alexander's drive) to build an enduring legacy of peace and shared prosperity, not through dominion or conquest, but through the collaborative pursuit of human flourishing where every entity's purpose is to contribute to the well-being of the whole. This creates a lasting peace that is both structurally sound and ethically profound, guided by a shared ambition to transcend conflict for the collective good.</p></div><div></div></div></section></div></div>
    <script type="module" src="./Simulacra Debate_files/main.jsx"></script>
  

</body></html>

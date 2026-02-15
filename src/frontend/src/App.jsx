import React, { useState, useRef, useEffect } from 'react';
import { DebateView } from './components/DebateView';
import { getApiBase } from './env';

const API_BASE = getApiBase();

export default function App() {
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    const el = chatEndRef.current;
    if (el?.scrollIntoView) el.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (state?.messages?.length) scrollToBottom();
  }, [state?.messages?.length]);

  async function runDebate() {
    setLoading(true);
    setError(null);
    setState(null);
    try {
      const res = await fetch(`${API_BASE}/debate/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });
      if (!res.ok) {
        const text = await res.text();
        let msg = text;
        try {
          const j = JSON.parse(text);
          if (j.detail) msg = typeof j.detail === 'string' ? j.detail : JSON.stringify(j.detail);
        } catch (_) {}
        throw new Error(msg || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setState(data);
    } catch (e) {
      setError(e.message || 'Failed to run debate');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Simulacra Debate</h1>
        <div className="run-section">
          <button onClick={runDebate} disabled={loading}>
            {loading ? 'Running debate…' : 'Run debate'}
          </button>
          {error && <p className="status error">{error}</p>}
          {loading && !error && <p className="status">Running debate (this may take a minute)…</p>}
        </div>
      </header>

      <section className="chat-window" aria-label="Debate chat">
        <div className="chat-window-inner">
          {!state && !loading && (
            <div className="chat-placeholder">
              <p>Click &ldquo;Run debate&rdquo; to start. The chat will show openings, defences, exchange rounds, reflections, and a summary.</p>
            </div>
          )}
          {state && <DebateView state={state} />}
          <div ref={chatEndRef} />
        </div>
      </section>
    </div>
  );
}

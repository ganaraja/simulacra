import React, { useState, useRef, useEffect } from 'react';
import { DebateView } from './components/DebateView';
import { getApiBase } from './env';

const API_BASE = getApiBase();

export default function App() {
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [autoStarted, setAutoStarted] = useState(false);
  const chatEndRef = useRef(null);

  // Default greeting messages
  const defaultMessages = [
    { author_id: 'napoleon', author_name: 'Napoleon', content: 'Hi, I am Napoleon Bonaparte. I believe in conquest for the greater good.', phase: 'greeting' },
    { author_id: 'gandhi', author_name: 'Gandhi', content: 'Hi, I am Mahatma Gandhi. I advocate for peace and non-violence.', phase: 'greeting' },
    { author_id: 'alexander', author_name: 'Alexander', content: 'Hi, I am Alexander the Great. Glory through conquest is my path.', phase: 'greeting' },
    { author_id: 'arbitrator', author_name: 'Arbitrator', content: 'Hi, I am the Arbitrator. I will help find common ground and guide toward consensus.', phase: 'greeting' },
  ];

  const scrollToBottom = () => {
    const el = chatEndRef.current;
    if (el?.scrollIntoView) el.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (state?.messages?.length) scrollToBottom();
  }, [state?.messages?.length]);

  // Auto-start debate on component mount
  useEffect(() => {
    if (!autoStarted) {
      setAutoStarted(true);
      runDebate();
    }
  }, [autoStarted]);

  async function runDebate() {
    setLoading(true);
    setError(null);
    setState(null);
    try {
      const res = await fetch(`${API_BASE}/debate/run?max_exchange_rounds=1`, {
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
      </header>

      <section className="chat-window" aria-label="Debate chat">
        <div className="chat-window-inner">
          {!state && !loading && !error && (
            <DebateView state={{ messages: defaultMessages, summary: '' }} />
          )}
          {!state && loading && (
            <>
              <DebateView state={{ messages: defaultMessages, summary: '' }} />
              <div className="chat-placeholder">
                <p>🎭 The debate will start in a while when the participants are ready...</p>
              </div>
            </>
          )}
          {!state && !loading && error && (
            <>
              <DebateView state={{ messages: defaultMessages, summary: '' }} />
              <div className="chat-placeholder">
                <p>⏳ The debate will start in a while when the participants are ready...</p>
                <p className="chat-hint">Please wait a moment.</p>
              </div>
            </>
          )}
          {state && <DebateView state={state} />}
          <div ref={chatEndRef} />
        </div>
      </section>
    </div>
  );
}

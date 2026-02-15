import React from 'react';
import { MessageList } from './MessageList';

const PERSONA_ICONS = {
  napoleon: '⚔️',
  gandhi: '🕊️',
  alexander: '👑',
  summariser: '📋',
};

export function DebateView({ state }) {
  const messages = state.messages || [];
  const summary = state.summary || '';

  return (
    <>
      <MessageList messages={messages} personaIcons={PERSONA_ICONS} />
      {summary && (
        <div className="summary-block">
          <h3>Summary</h3>
          <p>{summary}</p>
        </div>
      )}
    </>
  );
}

import React from 'react';
import { MessageList } from './MessageList';

const PERSONA_ICONS = {
  napoleon: '⚔️',
  gandhi: '🕊️',
  alexander: '👑',
  arbitrator: '⚖️',
};

export function DebateView({ state }) {
  const messages = state.messages || [];
  const arbitration = state.arbitration || '';

  return (
    <>
      <MessageList messages={messages} personaIcons={PERSONA_ICONS} />
      {arbitration && (
        <div className="arbitration-block">
          <h3>⚖️ Final Consensus</h3>
          <p>{arbitration}</p>
        </div>
      )}
    </>
  );
}

import React from 'react';
import { Message } from './Message';

export function MessageList({ messages, personaIcons }) {
  return (
    <div className="messages" data-testid="message-list">
      {messages.map((msg, i) => (
        <Message
          key={i}
          authorId={msg.author_id}
          authorName={msg.author_name}
          content={msg.content}
          phase={msg.phase}
          icon={personaIcons[msg.author_id] || '💬'}
        />
      ))}
    </div>
  );
}

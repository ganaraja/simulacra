import React from 'react';

export function Message({ authorId, authorName, content, phase, icon }) {
  const personaClass = authorId ? `message ${authorId}` : 'message';
  return (
    <article className={personaClass} data-testid="message" data-author={authorId}>
      <div className="message-icon" aria-hidden="true">
        {icon}
      </div>
      <div className="message-body">
        <div className="message-author">{authorName}</div>
        {phase && <div className="message-phase">{phase}</div>}
        <div className="message-content">{content}</div>
      </div>
    </article>
  );
}

import React from 'react';
import { render, screen } from '@testing-library/react';
import { Message } from '../Message';

describe('Message', () => {
  it('renders author name and content', () => {
    render(
      <Message
        authorId="napoleon"
        authorName="Napoleon"
        content="One kingdom, one peace."
        phase="opening"
        icon="⚔️"
      />
    );
    expect(screen.getByText('Napoleon')).toBeInTheDocument();
    expect(screen.getByText('One kingdom, one peace.')).toBeInTheDocument();
  });

  it('has data-author and data-testid', () => {
    render(
      <Message
        authorId="gandhi"
        authorName="Gandhi"
        content="Non-violence."
        phase="defence"
        icon="🕊️"
      />
    );
    const msg = screen.getByTestId('message');
    expect(msg).toHaveAttribute('data-author', 'gandhi');
  });

  it('applies persona class for styling', () => {
    render(
      <Message
        authorId="alexander"
        authorName="Alexander"
        content="Glory in conquest."
        icon="👑"
      />
    );
    const msg = screen.getByTestId('message');
    expect(msg.className).toContain('alexander');
  });
});

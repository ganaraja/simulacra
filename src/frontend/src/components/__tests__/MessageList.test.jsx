import React from 'react';
import { render, screen } from '@testing-library/react';
import { MessageList } from '../MessageList';

const personaIcons = { napoleon: '⚔️', gandhi: '🕊️', alexander: '👑', summariser: '📋' };

describe('MessageList', () => {
  it('renders empty list', () => {
    render(<MessageList messages={[]} personaIcons={personaIcons} />);
    expect(screen.getByTestId('message-list')).toBeInTheDocument();
    expect(screen.queryAllByTestId('message')).toHaveLength(0);
  });

  it('renders multiple messages', () => {
    const messages = [
      { author_id: 'napoleon', author_name: 'Napoleon', content: 'Opening.', phase: 'opening' },
      { author_id: 'gandhi', author_name: 'Gandhi', content: 'Peace.', phase: 'opening' },
    ];
    render(<MessageList messages={messages} personaIcons={personaIcons} />);
    expect(screen.getByText('Napoleon')).toBeInTheDocument();
    expect(screen.getByText('Opening.')).toBeInTheDocument();
    expect(screen.getByText('Gandhi')).toBeInTheDocument();
    expect(screen.getByText('Peace.')).toBeInTheDocument();
    expect(screen.getAllByTestId('message')).toHaveLength(2);
  });
});

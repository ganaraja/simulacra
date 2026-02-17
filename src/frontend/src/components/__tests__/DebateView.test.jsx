import React from 'react';
import { render, screen } from '@testing-library/react';
import { DebateView } from '../DebateView';

describe('DebateView', () => {
  it('renders message list from state', () => {
    const state = {
      messages: [
        { author_id: 'napoleon', author_name: 'Napoleon', content: 'Hello.', phase: 'opening' },
      ],
      arbitration: '',
    };
    render(<DebateView state={state} />);
    expect(screen.getByTestId('message-list')).toBeInTheDocument();
    expect(screen.getByText('Hello.')).toBeInTheDocument();
  });

  it('renders arbitration when present', () => {
    const state = {
      messages: [],
      arbitration: 'All three perspectives can be unified through balanced governance.',
    };
    render(<DebateView state={state} />);
    expect(screen.getByText('⚖️ Final Consensus')).toBeInTheDocument();
    expect(screen.getByText('All three perspectives can be unified through balanced governance.')).toBeInTheDocument();
  });

  it('handles missing messages', () => {
    const state = {};
    render(<DebateView state={state} />);
    expect(screen.getByTestId('message-list')).toBeInTheDocument();
  });
});

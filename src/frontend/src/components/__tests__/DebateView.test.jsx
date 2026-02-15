import React from 'react';
import { render, screen } from '@testing-library/react';
import { DebateView } from '../DebateView';

describe('DebateView', () => {
  it('renders message list from state', () => {
    const state = {
      messages: [
        { author_id: 'napoleon', author_name: 'Napoleon', content: 'Hello.', phase: 'opening' },
      ],
      summary: '',
    };
    render(<DebateView state={state} />);
    expect(screen.getByTestId('message-list')).toBeInTheDocument();
    expect(screen.getByText('Hello.')).toBeInTheDocument();
  });

  it('renders summary when present', () => {
    const state = {
      messages: [],
      summary: 'All three held their positions.',
    };
    render(<DebateView state={state} />);
    expect(screen.getByText('Summary')).toBeInTheDocument();
    expect(screen.getByText('All three held their positions.')).toBeInTheDocument();
  });

  it('handles missing messages', () => {
    const state = {};
    render(<DebateView state={state} />);
    expect(screen.getByTestId('message-list')).toBeInTheDocument();
  });
});

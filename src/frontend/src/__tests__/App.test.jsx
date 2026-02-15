import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

describe('App', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  it('renders title and run button', () => {
    render(<App />);
    expect(screen.getByText('Simulacra Debate')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /run debate/i })).toBeInTheDocument();
  });

  it('calls API and shows messages on success', async () => {
    const user = userEvent.setup();
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        messages: [
          { author_id: 'napoleon', author_name: 'Napoleon', content: 'Test opening.', phase: 'opening' },
        ],
        summary: 'Test summary.',
      }),
    });
    render(<App />);
    await user.click(screen.getByRole('button', { name: /run debate/i }));
    await waitFor(() => {
      expect(screen.getByText('Test opening.')).toBeInTheDocument();
    });
    expect(screen.getByText('Test summary.')).toBeInTheDocument();
  });

  it('shows error when API fails', async () => {
    const user = userEvent.setup();
    global.fetch.mockResolvedValueOnce({ ok: false, text: async () => 'Server error' });
    render(<App />);
    await user.click(screen.getByRole('button', { name: /run debate/i }));
    await waitFor(() => {
      expect(screen.getByText(/HTTP 500|Server error|Failed/)).toBeInTheDocument();
    });
  });
});

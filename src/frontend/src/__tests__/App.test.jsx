import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

describe('App', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders title', () => {
    // Mock fetch to prevent auto-start from actually running
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ messages: [], summary: '' }),
    });
    
    render(<App />);
    expect(screen.getByText('Simulacra Debate')).toBeInTheDocument();
  });

  it('auto-starts debate on mount', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        messages: [
          { author_id: 'napoleon', author_name: 'Napoleon', content: 'Auto-started opening.', phase: 'opening' },
        ],
        summary: 'Auto-started summary.',
      }),
    });
    
    render(<App />);
    
    // Wait for auto-start to complete
    await waitFor(() => {
      expect(screen.getByText('Auto-started opening.')).toBeInTheDocument();
    });
    expect(screen.getByText('Auto-started summary.')).toBeInTheDocument();
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });

  it('shows loading message while debate runs', async () => {
    global.fetch.mockImplementationOnce(() => new Promise(() => {})); // Never resolves
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText(/Starting debate/i)).toBeInTheDocument();
    });
    
    // Should also show default greeting messages
    expect(screen.getByText(/Hi, I am Napoleon Bonaparte/i)).toBeInTheDocument();
    expect(screen.getByText(/Hi, I am Mahatma Gandhi/i)).toBeInTheDocument();
    expect(screen.getByText(/Hi, I am Alexander the Great/i)).toBeInTheDocument();
  });

  it('shows error when API fails', async () => {
    global.fetch.mockResolvedValueOnce({ 
      ok: false, 
      status: 500,
      text: async () => JSON.stringify({ detail: 'Server error' })
    });
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('❌ Failed to start debate')).toBeInTheDocument();
    });
    
    // Should show error in both header and chat window
    const errorTexts = screen.getAllByText('Server error');
    expect(errorTexts.length).toBeGreaterThan(0);
  });
});

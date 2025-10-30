import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Dashboard from '../pages/Dashboard';
import api from '../services/api';

vi.mock('../services/api');

const MockedDashboard = () => (
  <BrowserRouter>
    <Dashboard />
  </BrowserRouter>
);

describe('Dashboard Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.setItem('token', 'mock-token');
  });

  it('renders dashboard with sidebar', () => {
    api.get.mockResolvedValue({ data: { reports: [] } });
    
    render(<MockedDashboard />);
    
    expect(screen.getByText('EARTHLENS')).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Report')).toBeInTheDocument();
    expect(screen.getByText('My Reports')).toBeInTheDocument();
    expect(screen.getByText('Green Action')).toBeInTheDocument();
    expect(screen.getByText('Profile')).toBeInTheDocument();
  });

  it('fetches and displays reports', async () => {
    const mockReports = [
      {
        id: 1,
        title: 'Test Report 1',
        description: 'Description 1',
        location: 'Location 1',
        created_at: '2024-01-15T10:30:00Z',
        ai_category: 'pollution'
      },
      {
        id: 2,
        title: 'Test Report 2',
        description: 'Description 2',
        location: 'Location 2',
        created_at: '2024-01-16T10:30:00Z',
        ai_category: 'water-issues'
      }
    ];

    api.get.mockResolvedValue({ data: { reports: mockReports } });

    render(<MockedDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Test Report 1')).toBeInTheDocument();
      expect(screen.getByText('Test Report 2')).toBeInTheDocument();
    });
  });

  it('displays loading state', () => {
    api.get.mockImplementation(() => new Promise(() => {}));
    
    render(<MockedDashboard />);
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('displays error message on fetch failure', async () => {
    api.get.mockRejectedValue(new Error('Network error'));

    render(<MockedDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/failed to load reports/i)).toBeInTheDocument();
    });
  });

  it('redirects to login when no token', async () => {
    localStorage.removeItem('token');
    
    render(<MockedDashboard />);

    await waitFor(() => {
      expect(window.location.pathname).toBe('/login');
    });
  });

  it('applies filters when filter changes', async () => {
    api.get.mockResolvedValue({ data: { reports: [] } });

    render(<MockedDashboard />);

    await waitFor(() => {
      expect(api.get).toHaveBeenCalledWith(
        expect.stringContaining('/reports'),
        expect.any(Object)
      );
    });
  });
});

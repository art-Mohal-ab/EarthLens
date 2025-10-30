import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import userEvent from '@testing-library/user-event';
import App from '../../App';
import api from '../../services/api';

vi.mock('../../services/api');

describe('E2E: Complete User Flow', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('completes full user journey from signup to report creation', async () => {
    const user = userEvent.setup();
    
    // Mock API responses
    const mockRegisterResponse = {
      data: {
        access_token: 'mock-token',
        user: { username: 'e2euser', email: 'e2e@test.com' }
      }
    };
    
    const mockReportsResponse = {
      data: { reports: [] }
    };
    
    const mockCreateReportResponse = {
      data: {
        message: 'Report created successfully',
        report: {
          id: 1,
          title: 'Test Report',
          description: 'Test Description',
          location: 'Test Location'
        }
      }
    };
    
    api.post.mockImplementation((url) => {
      if (url === '/auth/register') return Promise.resolve(mockRegisterResponse);
      if (url === '/reports') return Promise.resolve(mockCreateReportResponse);
      return Promise.reject(new Error('Unknown endpoint'));
    });
    
    api.get.mockResolvedValue(mockReportsResponse);
    
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    
    // Step 1: Navigate to signup
    const signupLink = screen.getByText(/sign up/i);
    await user.click(signupLink);
    
    // Step 2: Fill signup form
    const usernameInput = screen.getByLabelText(/username/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    
    await user.type(usernameInput, 'e2euser');
    await user.type(emailInput, 'e2e@test.com');
    await user.type(passwordInput, 'SecurePass123');
    
    // Step 3: Submit signup
    const submitButton = screen.getByRole('button', { name: /sign up/i });
    await user.click(submitButton);
    
    // Step 4: Verify redirect to dashboard
    await waitFor(() => {
      expect(window.location.pathname).toBe('/dashboard');
    });
    
    // Step 5: Navigate to create report
    const reportButton = screen.getByText(/report/i);
    await user.click(reportButton);
    
    // Step 6: Fill report form
    await waitFor(() => {
      const titleInput = screen.getByLabelText(/title/i);
      const descInput = screen.getByLabelText(/description/i);
      
      user.type(titleInput, 'Test Environmental Issue');
      user.type(descInput, 'This is a test report description');
    });
    
    // Step 7: Submit report
    const createButton = screen.getByRole('button', { name: /submit/i });
    await user.click(createButton);
    
    // Step 8: Verify report was created
    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith('/reports', expect.any(Object));
    });
  });
});


describe('E2E: Report Management Flow', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.setItem('token', 'mock-token');
  });

  it('views, edits, and deletes a report', async () => {
    const user = userEvent.setup();
    
    const mockReports = [
      {
        id: 1,
        title: 'Test Report',
        description: 'Test Description',
        location: 'Test Location',
        created_at: '2024-01-15T10:30:00Z',
        ai_category: 'pollution'
      }
    ];
    
    api.get.mockResolvedValue({ data: { reports: mockReports } });
    api.put.mockResolvedValue({ data: { report: { ...mockReports[0], title: 'Updated Title' } } });
    api.delete.mockResolvedValue({ data: { message: 'Deleted' } });
    
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    
    // Wait for reports to load
    await waitFor(() => {
      expect(screen.getByText('Test Report')).toBeInTheDocument();
    });
    
    // View details
    const viewButton = screen.getByText(/view details/i);
    await user.click(viewButton);
    
    await waitFor(() => {
      expect(screen.getByText(/report description/i)).toBeInTheDocument();
    });
    
    // Close modal
    const closeButton = screen.getByText('×');
    await user.click(closeButton);
    
    // Edit report
    const editButton = screen.getByText(/edit/i);
    await user.click(editButton);
    
    // Update title
    const titleInput = screen.getByDisplayValue('Test Report');
    await user.clear(titleInput);
    await user.type(titleInput, 'Updated Title');
    
    const saveButton = screen.getByText(/save/i);
    await user.click(saveButton);
    
    await waitFor(() => {
      expect(api.put).toHaveBeenCalled();
    });
    
    // Delete report
    const deleteButton = screen.getByText(/delete/i);
    await user.click(deleteButton);
    
    await waitFor(() => {
      expect(api.delete).toHaveBeenCalled();
    });
  });
});


describe('E2E: Navigation and Routing', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.setItem('token', 'mock-token');
  });

  it('navigates through all main pages', async () => {
    const user = userEvent.setup();
    
    api.get.mockResolvedValue({ data: { reports: [] } });
    
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    
    // Dashboard
    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
    
    // Navigate to My Reports
    const myReportsLink = screen.getByText(/my reports/i);
    await user.click(myReportsLink);
    
    await waitFor(() => {
      expect(window.location.pathname).toBe('/my-reports');
    });
    
    // Navigate to Green Actions
    const greenActionsLink = screen.getByText(/green action/i);
    await user.click(greenActionsLink);
    
    await waitFor(() => {
      expect(window.location.pathname).toBe('/green-actions');
    });
    
    // Navigate to Profile
    const profileLink = screen.getByText(/profile/i);
    await user.click(profileLink);
    
    await waitFor(() => {
      expect(window.location.pathname).toBe('/profile');
    });
  });
});


describe('E2E: Error Handling', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('handles network errors gracefully', async () => {
    api.post.mockRejectedValue({ request: {} });
    
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    
    // Try to signup with network error
    const usernameInput = screen.getByLabelText(/username/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(emailInput, { target: { value: 'test@test.com' } });
    fireEvent.change(passwordInput, { target: { value: 'SecurePass123' } });
    
    const submitButton = screen.getByRole('button', { name: /sign up/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/cannot connect to server/i)).toBeInTheDocument();
    });
  });

  it('handles validation errors', async () => {
    api.post.mockRejectedValue({
      response: {
        data: {
          error: 'Validation failed',
          details: { password: ['Password must contain uppercase'] }
        }
      }
    });
    
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    
    const passwordInput = screen.getByLabelText(/password/i);
    fireEvent.change(passwordInput, { target: { value: 'weakpass' } });
    
    const submitButton = screen.getByRole('button', { name: /sign up/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/password must contain/i)).toBeInTheDocument();
    });
  });
});


describe('E2E: State Management', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('maintains authentication state across navigation', async () => {
    const user = userEvent.setup();
    
    localStorage.setItem('token', 'mock-token');
    api.get.mockResolvedValue({ data: { reports: [] } });
    
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    
    // Verify authenticated state
    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
    
    // Navigate away and back
    const profileLink = screen.getByText(/profile/i);
    await user.click(profileLink);
    
    const dashboardLink = screen.getByText(/dashboard/i);
    await user.click(dashboardLink);
    
    // Should still be authenticated
    expect(localStorage.getItem('token')).toBe('mock-token');
  });

  it('clears state on logout', async () => {
    const user = userEvent.setup();
    
    localStorage.setItem('token', 'mock-token');
    api.get.mockResolvedValue({ data: { reports: [] } });
    
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    
    // Click sign out
    const signOutButton = screen.getByText(/sign out/i);
    await user.click(signOutButton);
    
    await waitFor(() => {
      expect(localStorage.getItem('token')).toBeNull();
      expect(window.location.pathname).toBe('/');
    });
  });
});

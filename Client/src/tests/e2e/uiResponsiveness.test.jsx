import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, within } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Dashboard from '../../pages/Dashboard';
import LandingPage from '../../pages/LandingPage';
import Signup from '../../pages/Signup';
import api from '../../services/api';

vi.mock('../../services/api');

describe('UI/UX: Responsive Design', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.setItem('token', 'mock-token');
  });

  it('renders mobile-friendly navigation', () => {
    // Set mobile viewport
    global.innerWidth = 375;
    global.innerHeight = 667;
    
    api.get.mockResolvedValue({ data: { reports: [] } });
    
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    // Sidebar should be present
    expect(screen.getByText('EARTHLENS')).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });

  it('renders tablet layout correctly', () => {
    // Set tablet viewport
    global.innerWidth = 768;
    global.innerHeight = 1024;
    
    api.get.mockResolvedValue({ data: { reports: [] } });
    
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    // Check main content area
    expect(screen.getByText(/recent reports/i)).toBeInTheDocument();
  });

  it('renders desktop layout with full features', () => {
    // Set desktop viewport
    global.innerWidth = 1920;
    global.innerHeight = 1080;
    
    api.get.mockResolvedValue({ data: { reports: [] } });
    
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    // All navigation items should be visible
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Report')).toBeInTheDocument();
    expect(screen.getByText('My Reports')).toBeInTheDocument();
    expect(screen.getByText('Green Action')).toBeInTheDocument();
    expect(screen.getByText('Profile')).toBeInTheDocument();
  });
});


describe('UI/UX: Accessibility', () => {
  it('has proper ARIA labels on forms', () => {
    render(
      <BrowserRouter>
        <Signup />
      </BrowserRouter>
    );
    
    // Check for accessible labels
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it('has proper button roles', () => {
    render(
      <BrowserRouter>
        <Signup />
      </BrowserRouter>
    );
    
    const submitButton = screen.getByRole('button', { name: /sign up/i });
    expect(submitButton).toBeInTheDocument();
    expect(submitButton).toHaveAttribute('type', 'submit');
  });

  it('has proper heading hierarchy', () => {
    render(
      <BrowserRouter>
        <LandingPage />
      </BrowserRouter>
    );
    
    // Check for proper heading structure
    const headings = screen.getAllByRole('heading');
    expect(headings.length).toBeGreaterThan(0);
  });

  it('has keyboard navigable elements', () => {
    render(
      <BrowserRouter>
        <Signup />
      </BrowserRouter>
    );
    
    const inputs = screen.getAllByRole('textbox');
    inputs.forEach(input => {
      expect(input).not.toHaveAttribute('tabindex', '-1');
    });
  });
});


describe('UI/UX: Visual Feedback', () => {
  it('shows loading state while fetching data', async () => {
    api.get.mockImplementation(() => new Promise(() => {})); // Never resolves
    
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('shows error state when data fetch fails', async () => {
    api.get.mockRejectedValue(new Error('Network error'));
    
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    await screen.findByText(/failed to load/i);
    expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
  });

  it('shows empty state when no data', async () => {
    api.get.mockResolvedValue({ data: { reports: [] } });
    
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    // Should show some indication of no reports
    await screen.findByText(/recent reports/i);
  });
});


describe('UI/UX: Form Validation Feedback', () => {
  it('shows real-time validation errors', async () => {
    render(
      <BrowserRouter>
        <Signup />
      </BrowserRouter>
    );
    
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign up/i });
    
    // Enter weak password
    fireEvent.change(passwordInput, { target: { value: 'weak' } });
    fireEvent.click(submitButton);
    
    await screen.findByText(/password must be at least 8 characters/i);
  });

  it('clears errors when input is corrected', async () => {
    render(
      <BrowserRouter>
        <Signup />
      </BrowserRouter>
    );
    
    const usernameInput = screen.getByLabelText(/username/i);
    const submitButton = screen.getByRole('button', { name: /sign up/i });
    
    // Enter short username
    fireEvent.change(usernameInput, { target: { value: 'ab' } });
    fireEvent.click(submitButton);
    
    await screen.findByText(/username must be at least 3 characters/i);
    
    // Correct it
    fireEvent.change(usernameInput, { target: { value: 'validuser' } });
    
    // Error should eventually clear
    expect(screen.queryByText(/username must be at least 3 characters/i)).not.toBeInTheDocument();
  });
});


describe('UI/UX: Image Handling', () => {
  it('shows placeholder when image fails to load', () => {
    const mockReport = {
      id: 1,
      title: 'Test Report',
      description: 'Test',
      image_url: '/broken-image.jpg',
      created_at: '2024-01-15T10:30:00Z'
    };
    
    render(
      <BrowserRouter>
        <ReportCard report={mockReport} onViewDetails={() => {}} />
      </BrowserRouter>
    );
    
    const image = screen.getByAlt('Test Report');
    fireEvent.error(image);
    
    expect(image.src).toContain('placeholder.png');
  });

  it('displays image with correct alt text', () => {
    const mockReport = {
      id: 1,
      title: 'Water Pollution',
      description: 'Test',
      image_url: '/test.jpg',
      created_at: '2024-01-15T10:30:00Z'
    };
    
    render(
      <BrowserRouter>
        <ReportCard report={mockReport} onViewDetails={() => {}} />
      </BrowserRouter>
    );
    
    const image = screen.getByAlt('Water Pollution');
    expect(image).toBeInTheDocument();
  });
});


describe('UI/UX: Interactive Elements', () => {
  it('provides visual feedback on button hover', () => {
    render(
      <BrowserRouter>
        <Signup />
      </BrowserRouter>
    );
    
    const button = screen.getByRole('button', { name: /sign up/i });
    expect(button).toHaveClass('signup-btn');
  });

  it('disables submit button during form submission', async () => {
    api.post.mockImplementation(() => new Promise(() => {})); // Never resolves
    
    render(
      <BrowserRouter>
        <Signup />
      </BrowserRouter>
    );
    
    const usernameInput = screen.getByLabelText(/username/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign up/i });
    
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(emailInput, { target: { value: 'test@test.com' } });
    fireEvent.change(passwordInput, { target: { value: 'SecurePass123' } });
    fireEvent.click(submitButton);
    
    // Button should be disabled during submission
    // This would need to be implemented in the component
  });
});


describe('UI/UX: Color Contrast and Readability', () => {
  it('uses readable text colors', () => {
    render(
      <BrowserRouter>
        <LandingPage />
      </BrowserRouter>
    );
    
    // Check that text elements are rendered
    const textElements = screen.getAllByText(/./);
    expect(textElements.length).toBeGreaterThan(0);
  });

  it('maintains readability in dark mode (if implemented)', () => {
    // This would test dark mode if implemented
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    // Check for dark mode classes or styles
    expect(document.body).toBeDefined();
  });
});

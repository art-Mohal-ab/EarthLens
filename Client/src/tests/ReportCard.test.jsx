import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ReportCard from '../components/ReportCard';

describe('ReportCard Component', () => {
  const mockReport = {
    id: 1,
    title: 'Water Pollution Issue',
    description: 'Chemical waste found in river',
    location: 'River Bank',
    ai_category: 'water-issues',
    created_at: '2024-01-15T10:30:00Z',
    image_url: '/uploads/test-image.jpg',
    user: { username: 'testuser' }
  };

  const mockHandlers = {
    onViewDetails: vi.fn(),
    onEditReport: vi.fn(),
    onDeleteReport: vi.fn()
  };

  it('renders report information correctly', () => {
    render(<ReportCard report={mockReport} {...mockHandlers} />);
    
    expect(screen.getByText('Water Pollution Issue')).toBeInTheDocument();
    expect(screen.getByText('Chemical waste found in river')).toBeInTheDocument();
    expect(screen.getByText('River Bank')).toBeInTheDocument();
    expect(screen.getByText('water-issues')).toBeInTheDocument();
  });

  it('displays report image with correct URL', () => {
    render(<ReportCard report={mockReport} {...mockHandlers} />);
    
    const image = screen.getByAlt('Water Pollution Issue');
    expect(image).toBeInTheDocument();
    expect(image.src).toContain('/uploads/test-image.jpg');
  });

  it('falls back to placeholder when image fails', () => {
    render(<ReportCard report={mockReport} {...mockHandlers} />);
    
    const image = screen.getByAlt('Water Pollution Issue');
    fireEvent.error(image);
    
    expect(image.src).toContain('placeholder.png');
  });

  it('calls onViewDetails when view details button is clicked', () => {
    render(<ReportCard report={mockReport} {...mockHandlers} />);
    
    const viewButton = screen.getByText(/view details/i);
    fireEvent.click(viewButton);
    
    expect(mockHandlers.onViewDetails).toHaveBeenCalledWith(1);
  });

  it('shows edit and delete buttons when showEditDelete is true', () => {
    render(<ReportCard report={mockReport} {...mockHandlers} showEditDelete={true} />);
    
    expect(screen.getByText(/edit/i)).toBeInTheDocument();
    expect(screen.getByText(/delete/i)).toBeInTheDocument();
  });

  it('hides edit and delete buttons when showEditDelete is false', () => {
    render(<ReportCard report={mockReport} {...mockHandlers} showEditDelete={false} />);
    
    expect(screen.queryByText(/edit/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/delete/i)).not.toBeInTheDocument();
  });

  it('calls onEditReport when edit button is clicked', () => {
    render(<ReportCard report={mockReport} {...mockHandlers} showEditDelete={true} />);
    
    const editButton = screen.getByText(/edit/i);
    fireEvent.click(editButton);
    
    expect(mockHandlers.onEditReport).toHaveBeenCalledWith(mockReport);
  });

  it('calls onDeleteReport when delete button is clicked', () => {
    render(<ReportCard report={mockReport} {...mockHandlers} showEditDelete={true} />);
    
    const deleteButton = screen.getByText(/delete/i);
    fireEvent.click(deleteButton);
    
    expect(mockHandlers.onDeleteReport).toHaveBeenCalledWith(1);
  });

  it('displays AI recommendations when available', () => {
    const reportWithAI = {
      ...mockReport,
      ai_advice: 'Contact water authorities immediately'
    };
    
    render(<ReportCard report={reportWithAI} {...mockHandlers} showEditDelete={true} />);
    
    expect(screen.getByText(/AI Recommendations/i)).toBeInTheDocument();
    expect(screen.getByText(/contact water authorities/i)).toBeInTheDocument();
  });

  it('formats date correctly', () => {
    render(<ReportCard report={mockReport} {...mockHandlers} />);
    
    const dateElement = screen.getByText(/1\/15\/2024/);
    expect(dateElement).toBeInTheDocument();
  });

  it('displays reporter username', () => {
    render(<ReportCard report={mockReport} {...mockHandlers} />);
    
    expect(screen.getByText(/reported by testuser/i)).toBeInTheDocument();
  });

  it('shows Anonymous when user is not available', () => {
    const reportWithoutUser = { ...mockReport, user: null };
    
    render(<ReportCard report={reportWithoutUser} {...mockHandlers} />);
    
    expect(screen.getByText(/reported by anonymous/i)).toBeInTheDocument();
  });
});

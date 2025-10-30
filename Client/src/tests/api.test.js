import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import api from '../services/api';

vi.mock('axios');

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('creates axios instance with correct base URL', () => {
    expect(axios.create).toHaveBeenCalledWith(
      expect.objectContaining({
        baseURL: 'http://localhost:5001/api'
      })
    );
  });

  it('adds authorization header when token exists', () => {
    const mockRequest = { headers: {} };
    localStorage.getItem.mockReturnValue('test-token');

    const interceptor = axios.create.mock.results[0].value.interceptors.request.use.mock.calls[0][0];
    const result = interceptor(mockRequest);

    expect(result.headers.Authorization).toBe('Bearer test-token');
  });

  it('does not add authorization header when token does not exist', () => {
    const mockRequest = { headers: {} };
    localStorage.getItem.mockReturnValue(null);

    const interceptor = axios.create.mock.results[0].value.interceptors.request.use.mock.calls[0][0];
    const result = interceptor(mockRequest);

    expect(result.headers.Authorization).toBeUndefined();
  });

  it('redirects to login on 401 response', () => {
    const mockError = {
      response: { status: 401 }
    };

    delete window.location;
    window.location = { href: '' };

    const interceptor = axios.create.mock.results[0].value.interceptors.response.use.mock.calls[0][1];
    
    expect(() => interceptor(mockError)).rejects.toEqual(mockError);
    expect(localStorage.removeItem).toHaveBeenCalledWith('token');
    expect(window.location.href).toBe('/login');
  });

  it('does not redirect on non-401 errors', () => {
    const mockError = {
      response: { status: 500 }
    };

    delete window.location;
    window.location = { href: '' };

    const interceptor = axios.create.mock.results[0].value.interceptors.response.use.mock.calls[0][1];
    
    expect(() => interceptor(mockError)).rejects.toEqual(mockError);
    expect(window.location.href).toBe('');
  });
});

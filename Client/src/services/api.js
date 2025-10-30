import axios from 'axios';

const API_BASE_URL = 'https://earthlens-2.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE_URL
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export { API_BASE_URL };
export default api;

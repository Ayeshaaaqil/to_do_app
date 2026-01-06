// frontend/src/services/api.ts

import { getAuthToken } from './auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://to-do-app-4fak.vercel.app/';

// Generic API request function
const apiRequest = async (endpoint: string, options: RequestInit = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Add auth token if available - get the latest token
  const token = getAuthToken();
  if (token) {
    (headers as any)['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  // If we get a 401 or 403, clear auth and redirect to sign in
  if (response.status === 401 || response.status === 403) {
    const errorData = await response.json().catch(() => ({}));
    console.error('Authentication error:', errorData);

    // Clear authentication state
    await import('./auth').then(auth => auth.clearAuth());

    // Redirect to sign in (in a browser environment)
    if (typeof window !== 'undefined') {
      window.location.href = '/signin';
    }

    throw new Error(`Authentication failed: ${response.status} ${response.statusText}`);
  }

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

// Authentication API functions
export const authAPI = {
  signup: async (email: string, password: string, name?: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Signup failed: ${response.status} ${response.statusText}`);
      }

      return response.json();
    } catch (error: any) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Failed to connect to server. Please check your connection and try again.');
      }
      throw error;
    }
  },

  signin: async (email: string, password: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Signin failed: ${response.status} ${response.statusText}`);
      }

      return response.json();
    } catch (error: any) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Failed to connect to server. Please check your connection and try again.');
      }
      throw error;
    }
  },

  signout: async () => {
    const response = await fetch(`${API_BASE_URL}/auth/signout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Signout failed');
    }

    return response.json();
  },
};

// Todo API functions
export const todoAPI = {
  getTodos: async () => {
    return apiRequest('/todos');
  },

  createTodo: async (title: string, description?: string) => {
    return apiRequest('/todos', {
      method: 'POST',
      body: JSON.stringify({ title, description }),
    });
  },

  updateTodo: async (id: string, updates: { title?: string; description?: string }) => {
    return apiRequest(`/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  },

  toggleTodoComplete: async (id: string, isCompleted: boolean) => {
    return apiRequest(`/todos/${id}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ is_completed: isCompleted }),
    });
  },

  deleteTodo: async (id: string) => {
    return apiRequest(`/todos/${id}`, {
      method: 'DELETE',
    });
  },
};
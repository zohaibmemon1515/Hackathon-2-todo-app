// API service layer for frontend
import { User, UserLogin, UserRegister } from '@/types/user';
import { Task, TaskCreate, TaskUpdate } from '@/types/task';

// Base API configuration
const API_BASE_URL = 'http://localhost:8000';

// Base fetch function with error handling
const baseFetch = async (endpoint: string, options: RequestInit = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // Merge provided options with defaults
  const fetchOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };

  // Add auth token if available
  const token = localStorage.getItem('access_token');
  if (token && fetchOptions.headers) {
    (fetchOptions.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, fetchOptions);

    // Handle different response status codes
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

// Authentication API functions
export const authAPI = {
  register: async (userData: UserRegister): Promise<{ user: User; access_token: string; token_type: string }> => {
    return baseFetch('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  login: async (credentials: UserLogin): Promise<{ user: User; access_token: string; token_type: string }> => {
    return baseFetch('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },

  getProfile: async (): Promise<User> => {
    return baseFetch('/api/v1/auth/profile');
  },

  refreshToken: async (): Promise<{ access_token: string; token_type: string }> => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    return baseFetch('/api/v1/auth/refresh', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${refreshToken}`,
      },
    });
  },
};

// Task API functions
export const taskAPI = {
  getAll: async (): Promise<{ tasks: Task[]; total: number; limit: number; offset: number }> => {
    return baseFetch('/api/v1/tasks');
  },

  getById: async (id: string): Promise<Task> => {
    return baseFetch(`/api/v1/tasks/${id}`);
  },

  create: async (taskData: TaskCreate): Promise<Task> => {
    return baseFetch('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  },

  update: async (id: string, taskData: TaskUpdate): Promise<Task> => {
    return baseFetch(`/api/v1/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  },

  patch: async (id: string, taskData: Partial<TaskUpdate>): Promise<Task> => {
    return baseFetch(`/api/v1/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(taskData),
    });
  },

  delete: async (id: string): Promise<void> => {
    const url = `${API_BASE_URL}/api/v1/tasks/${id}`;

    const token = localStorage.getItem('access_token');
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, {
        method: 'DELETE',
        headers,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      // Delete operation returns no content, so just return
      return;
    } catch (error) {
      console.error('Delete API call failed:', error);
      throw error;
    }
  },
};

// Export the base API object
export const api = {
  auth: authAPI,
  tasks: taskAPI,
};

export default api;
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const credentials = localStorage.getItem('credentials');
    if (credentials) {
      config.headers.Authorization = `Basic ${credentials}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth functions
export const login = async (username, password) => {
  const credentials = btoa(`${username}:${password}`);

  try {
    // Test credentials by fetching datasets
    await axios.get(`${API_BASE_URL}/datasets/`, {
      headers: {
        Authorization: `Basic ${credentials}`,
      },
    });

    // Store credentials if successful
    localStorage.setItem('credentials', credentials);
    localStorage.setItem('username', username);

    return { success: true };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Invalid credentials'
    };
  }
};

export const logout = () => {
  localStorage.removeItem('credentials');
  localStorage.removeItem('username');
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('credentials');
};

export const getUsername = () => {
  return localStorage.getItem('username');
};

// Dataset API functions
export const getDatasets = async () => {
  const response = await api.get('/datasets/');
  return response.data;
};

export const getDataset = async (id) => {
  const response = await api.get(`/datasets/${id}/`);
  return response.data;
};

export const getDatasetAnalytics = async (id) => {
  const response = await api.get(`/datasets/${id}/analytics/`);
  return response.data;
};

export const uploadDataset = async (name, file) => {
  const formData = new FormData();
  formData.append('name', name);
  formData.append('file', file);

  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const deleteDataset = async (id) => {
  const response = await api.delete(`/datasets/${id}/`);
  return response.data;
};

export const downloadReport = async (id, datasetName) => {
  const credentials = localStorage.getItem('credentials');
  const response = await axios.get(
    `${API_BASE_URL}/datasets/${id}/download-report/`,
    {
      headers: {
        Authorization: `Basic ${credentials}`,
      },
      responseType: 'blob',
    }
  );

  // Create download link
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `report_${datasetName}.pdf`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};

export default api;

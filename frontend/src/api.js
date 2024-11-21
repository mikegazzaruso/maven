import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generateVideo = async (formData) => {
  try {
    const response = await api.post('/generate', formData);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Error generating video');
    }
    throw new Error('Network error occurred');
  }
};

export const checkStatus = async (taskId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/status/${taskId}`);
    return {
      status: response.data.status,
      current_step: response.data.current_step,
      progress: response.data.progress,
      error: response.data.error
    };
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Error checking video status');
    }
    throw new Error('Network error while checking video status');
  }
};

export const downloadVideo = async (taskId) => {
  try {
    const response = await api.get(`/video/${taskId}`, {
      responseType: 'blob',
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Error downloading video');
    }
    throw new Error('Network error occurred');
  }
};

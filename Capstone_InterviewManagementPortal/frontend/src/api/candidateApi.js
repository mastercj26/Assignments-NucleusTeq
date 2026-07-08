import api from './axiosConfig';

export const candidateApi = {
  list: (page = 1, perPage = 10) => 
    api.get(`/candidates?page=${page}&per_page=${perPage}`),
  get: (id) => api.get(`/candidates/${id}`),
  create: (data) => api.post('/candidates/', data),
  update: (id, data) => api.put(`/candidates/${id}`, data),

  uploadResume: (id, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/candidates/${id}/resume`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  downloadResume: (id) => {
    return api.get(`/candidates/${id}/resume`, { responseType: 'blob' });
  },
  updateStatus: (id, status, notes = '') => {
    return api.patch(`/candidates/${id}/status`, { status, notes });
  },
  getStatusHistory: (id) => {
    return api.get(`/candidates/${id}/status-history`);
  },
};
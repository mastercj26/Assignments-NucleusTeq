import api from './axiosConfig';

export const candidateApi = {
  list: (page = 1, perPage = 10) => 
    api.get(`/candidates?page=${page}&per_page=${perPage}`),
  get: (id) => api.get(`/candidates/${id}`),
  create: (data) => api.post('/candidates/', data),
  update: (id, data) => api.put(`/candidates/${id}`, data),
};
import api from './axiosConfig';

export const jobApi = {
  list: (page = 1, perPage = 10) => 
    api.get(`/jobs?page=${page}&per_page=${perPage}`),
  get: (id) => api.get(`/jobs/${id}`),
  create: (data) => api.post('/jobs/', data),
  update: (id, data) => api.put(`/jobs/${id}`, data),
};
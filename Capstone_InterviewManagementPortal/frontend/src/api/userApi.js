import api from './axiosConfig'

const userApi = {
  list: (page = 1, perPage = 10) => api.get(`/users?page=${page}&per_page=${perPage}`),
  get: (id) => api.get(`/users/${id}`),
  create: (data) => api.post('/users/', data),
  update: (id, data) => api.put(`/users/${id}`, data),
  listInterviewers: (params = {}) => api.get('/users/interviewers', { params }),
  toggleStatus: (id, active) => api.patch(`/users/${id}/disable?active=${active}`),
}

export default userApi

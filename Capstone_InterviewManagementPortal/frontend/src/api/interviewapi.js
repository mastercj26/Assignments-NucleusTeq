import api from './axiosConfig'

const interviewApi = {
  list: (page = 1, perPage = 10) => api.get(`/interviews?page=${page}&per_page=${perPage}`),
  get: (id) => api.get(`/interviews/${id}`),
  schedule: (data) => api.post('/interviews/', data),
  update: (id, data) => api.put(`/interviews/${id}`, data),
}

export default interviewApi

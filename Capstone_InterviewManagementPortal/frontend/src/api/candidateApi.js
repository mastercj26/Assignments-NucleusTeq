import api from './axiosConfig'

const candidateApi = {
  list: (page = 1, perPage = 10) => api.get(`/candidates?page=${page}&per_page=${perPage}`),
  get: (id) => api.get(`/candidates/${id}`),
  create: (data) => api.post('/candidates/', data),
  update: (id, data) => api.put(`/candidates/${id}`, data),
  uploadResume: (id, file) => {
    const form = new FormData()
    form.append('file', file)
    return api.post(`/candidates/${id}/resume`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  downloadResume: (id) => api.get(`/candidates/${id}/resume`, { responseType: 'blob' }),
  updateStatus: (id, status, notes = '') => api.patch(`/candidates/${id}/status`, { status, notes }),
  getStatusHistory: (id) => api.get(`/candidates/${id}/status-history`),
}

export default candidateApi

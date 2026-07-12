import api from './axiosConfig'

const dashboardApi = {
  getHR: () => api.get('/dashboard/hr'),
  getInterviewer: () => api.get('/dashboard/interviewer'),
}

export default dashboardApi

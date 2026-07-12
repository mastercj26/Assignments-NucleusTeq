import api from './axiosConfig'

const feedbackApi = {
  submit: (data) => api.post('/feedbacks/', data),
  getByInterview: (interviewId) => api.get(`/feedbacks/interview/${interviewId}`),
}

export default feedbackApi

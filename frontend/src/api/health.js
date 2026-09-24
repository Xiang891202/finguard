import apiClient from './client'

export const healthApi = {
  getProfile: () =>
    apiClient.get('/api/v1/app/health/profile').then((r) => r.data),

  createProfile: (payload) =>
    apiClient.post('/api/v1/app/health/profile', payload).then((r) => r.data),

  updateProfile: (payload) =>
    apiClient.put('/api/v1/app/health/profile', payload).then((r) => r.data),

  getCompletion: () =>
    apiClient.get('/api/v1/app/health/completion').then((r) => r.data),

  setConsent: (consent) =>
    apiClient.post('/api/v1/app/health/consent', { consent }).then((r) => r.data),

  listMarkers: () =>
    apiClient.get('/api/v1/app/health/genetic-markers').then((r) => r.data),

  listTests: () =>
    apiClient.get('/api/v1/app/health/genetic-tests').then((r) => r.data),

  addTest: (payload) =>
    apiClient.post('/api/v1/app/health/genetic-tests', payload).then((r) => r.data),

  deleteTest: (id) =>
    apiClient
      .delete(`/api/v1/app/health/genetic-tests/${id}`)
      .then((r) => r.data)
}
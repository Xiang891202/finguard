import apiClient from './client'

export const authApi = {
  // ─── User ───
  requestOTP: (email) =>
    apiClient.post('/api/v1/auth/otp/request', { email }).then((r) => r.data),

  verifyOTP: (email, otp) =>
    apiClient.post('/api/v1/auth/otp/verify', { email, otp }).then((r) => r.data),

  refresh: (refreshToken) =>
    apiClient
      .post('/api/v1/auth/refresh', { refresh_token: refreshToken })
      .then((r) => r.data),

  logout: (refreshToken) =>
    apiClient
      .post('/api/v1/auth/logout', { refresh_token: refreshToken })
      .then((r) => r.data),

  me: () => apiClient.get('/api/v1/auth/me').then((r) => r.data),

  // ─── Admin ───
  adminLogin: (email, password) =>
    apiClient
      .post('/api/v1/admin/auth/login', { email, password })
      .then((r) => r.data),

  adminLogout: (refreshToken) =>
    apiClient
      .post('/api/v1/admin/auth/logout', { refresh_token: refreshToken })
      .then((r) => r.data),

  adminMe: () => apiClient.get('/api/v1/admin/auth/me').then((r) => r.data)
}
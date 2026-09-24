import axios from 'axios'

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' }
})

// ─── 注入 access token（依 URL 自動判斷 user / admin）───
apiClient.interceptors.request.use((config) => {
  const url = config.url || ''
  const isAdmin = url.startsWith('/api/v1/admin/')
  const key = isAdmin ? 'auth_admin_access_token' : 'auth_user_access_token'
  const token = localStorage.getItem(key)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ─── 401 自動 refresh（含佇列，避免並發重複 refresh）───
let refreshing = false
let queue = []

function flushQueue(error, token = null) {
  queue.forEach(({ resolve, reject }) => (error ? reject(error) : resolve(token)))
  queue = []
}

apiClient.interceptors.response.use(
  (res) => res,
  async (err) => {
    const { config, response } = err
    const url = config?.url || ''
    const isAdmin = url.startsWith('/api/v1/admin/')
    const prefix = isAdmin ? 'admin' : 'user'

    if (
      response?.status !== 401 ||
      url.includes('/auth/refresh') ||
      url.includes('/auth/login') ||
      url.includes('/auth/otp/') ||
      config._retried
    ) {
      return Promise.reject(err)
    }

    if (refreshing) {
      return new Promise((resolve, reject) => {
        queue.push({ resolve, reject })
      }).then((token) => {
        config.headers.Authorization = `Bearer ${token}`
        config._retried = true
        return apiClient(config)
      })
    }

    refreshing = true
    const refreshToken = localStorage.getItem(`auth_${prefix}_refresh_token`)
    if (!refreshToken) {
      refreshing = false
      localStorage.removeItem(`auth_${prefix}_access_token`)
      return Promise.reject(err)
    }

    try {
      const { data } = await axios.post(`${baseURL}/api/v1/auth/refresh`, {
        refresh_token: refreshToken
      })
      const next = data.data
      localStorage.setItem(`auth_${prefix}_access_token`, next.access_token)
      localStorage.setItem(`auth_${prefix}_refresh_token`, next.refresh_token)

      flushQueue(null, next.access_token)
      config.headers.Authorization = `Bearer ${next.access_token}`
      config._retried = true
      return apiClient(config)
    } catch (e) {
      flushQueue(e)
      localStorage.removeItem(`auth_${prefix}_access_token`)
      localStorage.removeItem(`auth_${prefix}_refresh_token`)
      localStorage.removeItem(`auth_${prefix}_info`)
      return Promise.reject(e)
    } finally {
      refreshing = false
    }
  }
)

export default apiClient
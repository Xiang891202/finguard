import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'

const KEYS = {
  user:  { a: 'auth_user_access_token',  r: 'auth_user_refresh_token',  i: 'auth_user_info' },
  admin: { a: 'auth_admin_access_token', r: 'auth_admin_refresh_token', i: 'auth_admin_info' }
}

function read(role) {
  const k = KEYS[role]
  const infoRaw = localStorage.getItem(k.i)
  return {
    access: localStorage.getItem(k.a),
    refresh: localStorage.getItem(k.r),
    info: infoRaw ? JSON.parse(infoRaw) : null
  }
}

function write(role, access, refresh, info) {
  const k = KEYS[role]
  localStorage.setItem(k.a, access)
  localStorage.setItem(k.r, refresh)
  localStorage.setItem(k.i, JSON.stringify(info))
}

function wipe(role) {
  const k = KEYS[role]
  localStorage.removeItem(k.a)
  localStorage.removeItem(k.r)
  localStorage.removeItem(k.i)
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: read('user'),
    admin: read('admin')
  }),

  getters: {
    isAuthenticated: (s) => !!s.user.access,
    isAdmin: (s) => !!s.admin.access,
    currentUser: (s) => s.user.info,
    currentAdmin: (s) => s.admin.info
  },

  actions: {
    async login(email, otp) {
      const res = await authApi.verifyOTP(email, otp)
      const d = res.data
      write('user', d.access_token, d.refresh_token, d.user)
      this.user = read('user')
      return d
    },

    async logout() {
      const r = this.user.refresh
      if (r) {
        try { await authApi.logout(r) } catch (_) {}
      }
      wipe('user')
      this.user = { access: null, refresh: null, info: null }
    },

    async adminLogin(email, password) {
      const res = await authApi.adminLogin(email, password)
      const d = res.data
      write('admin', d.access_token, d.refresh_token, d.admin)
      this.admin = read('admin')
      return d
    },

    async adminLogout() {
      const r = this.admin.refresh
      if (r) {
        try { await authApi.adminLogout(r) } catch (_) {}
      }
      wipe('admin')
      this.admin = { access: null, refresh: null, info: null }
    }
  }
})
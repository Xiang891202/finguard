import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
  	path: '/',
  	name: 'home',
  	component: () => import('@/views/HomeView.vue')
	},

  // User
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/app/LoginView.vue'),
    meta: { public: true }
  },
  {
    path: '/app/account/health',
    name: 'health-profile',
    component: () => import('@/views/app/HealthProfileView.vue'),
    meta: { requiresUser: true }
  },

  // Admin
  {
    path: '/admin/login',
    name: 'admin-login',
    component: () => import('@/views/admin/AdminLoginView.vue'),
    meta: { public: true }
  },
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: () => import('@/views/HomeView.vue'),   // 佔位，Day 4+ 替換
    meta: { requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const userToken = localStorage.getItem('auth_user_access_token')
  const adminToken = localStorage.getItem('auth_admin_access_token')

  if (to.meta.requiresUser && !userToken) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
  if (to.meta.requiresAdmin && !adminToken) {
    return { path: '/admin/login' }
  }
  return true
})

export default router
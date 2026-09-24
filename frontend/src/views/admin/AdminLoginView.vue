<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseCard from '@/components/common/BaseCard.vue'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function submit() {
  if (!email.value || !password.value) return
  loading.value = true
  error.value = ''
  try {
    await auth.adminLogin(email.value, password.value)
    router.push('/admin/dashboard')
  } catch (e) {
    error.value = e.response?.data?.error?.message || e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-slate-900 px-4">
    <div class="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-800 p-8 shadow-xl">
      <div class="mb-8 text-center">
        <div class="text-3xl">🛡️</div>
        <h1 class="mt-2 text-2xl font-bold text-white">FinGuard 管理員</h1>
        <p class="mt-1 text-sm text-slate-400">Admin Console</p>
      </div>

      <form class="space-y-4" @submit.prevent="submit">
        <label class="block">
          <span class="mb-1 block text-sm font-medium text-slate-300">Email</span>
          <input
            v-model="email"
            type="email"
            class="w-full rounded-lg border border-slate-600 bg-slate-700 px-3 py-2
                   text-white transition duration-200 outline-none
                   focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30"
          />
        </label>
        <label class="block">
          <span class="mb-1 block text-sm font-medium text-slate-300">密碼</span>
          <input
            v-model="password"
            type="password"
            class="w-full rounded-lg border border-slate-600 bg-slate-700 px-3 py-2
                   text-white transition duration-200 outline-none
                   focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30"
          />
        </label>
        <button
          type="submit"
          :disabled="!email || !password || loading"
          class="w-full rounded-lg bg-sky-600 px-4 py-2.5 font-medium text-white
                 transition duration-200
                 hover:bg-sky-700
                 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ loading ? '登入中…' : '登入' }}
        </button>
      </form>

      <p v-if="error" class="mt-4 rounded-lg bg-red-950 px-3 py-2 text-sm text-red-300">
        {{ error }}
      </p>

      <div class="mt-6 border-t border-slate-700 pt-4 text-center text-xs text-slate-500">
        <router-link to="/login" class="transition hover:text-slate-300">
          ← 回用戶登入
        </router-link>
      </div>
    </div>
  </div>
</template>
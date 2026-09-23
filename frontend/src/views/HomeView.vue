<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full animate-fade-in">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-700 rounded-xl flex items-center justify-center text-2xl">
          🛡️
        </div>
        <div>
          <h1 class="text-2xl font-bold text-slate-900">FinGuard</h1>
          <p class="text-sm text-slate-500">個人 / 家庭財務安全儀表板</p>
        </div>
      </div>

      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
          <span class="text-sm text-slate-600">系統狀態</span>
          <span :class="statusClass">{{ statusText }}</span>
        </div>

        <div class="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
          <span class="text-sm text-slate-600">資料庫</span>
          <span :class="dbClass">{{ dbText }}</span>
        </div>

        <div class="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
          <span class="text-sm text-slate-600">Redis</span>
          <span :class="redisClass">{{ redisText }}</span>
        </div>

        <div class="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
          <span class="text-sm text-slate-600">版本</span>
          <span class="text-sm font-mono text-slate-700">{{ version }}</span>
        </div>
      </div>

      <button
        @click="fetchHealth"
        :disabled="loading"
        class="mt-6 w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
      >
        {{ loading ? '檢查中...' : '重新檢查' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '@/api/client'

const loading = ref(false)
const health = ref({ status: 'unknown', database: 'unknown', redis: 'unknown', version: '-' })

const statusText = computed(() => health.value.status === 'healthy' ? '✅ 正常' : '❌ 異常')
const statusClass = computed(() => health.value.status === 'healthy' ? 'text-green-600 font-semibold text-sm' : 'text-red-600 font-semibold text-sm')
const dbText = computed(() => health.value.database === 'connected' ? '✅ 已連線' : `❌ ${health.value.database}`)
const dbClass = computed(() => health.value.database === 'connected' ? 'text-green-600 font-semibold text-sm' : 'text-red-600 font-semibold text-sm')
const redisText = computed(() => health.value.redis === 'connected' ? '✅ 已連線' : `❌ ${health.value.redis}`)
const redisClass = computed(() => health.value.redis === 'connected' ? 'text-green-600 font-semibold text-sm' : 'text-red-600 font-semibold text-sm')
const version = computed(() => health.value.version)

async function fetchHealth() {
  loading.value = true
  try {
    const res = await apiClient.get('/health')
    health.value = res.data
  } catch (e) {
    health.value = { status: 'error', database: 'error', redis: 'error', version: '-' }
  } finally {
    loading.value = false
  }
}

onMounted(fetchHealth)
</script>
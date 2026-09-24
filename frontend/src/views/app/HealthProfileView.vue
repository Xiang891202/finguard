<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useHealthStore } from '@/stores/health'
import HealthProfileForm from '@/components/health/HealthProfileForm.vue'
import CompletionIndicator from '@/components/health/CompletionIndicator.vue'
import BaseCard from '@/components/common/BaseCard.vue'

const router = useRouter()
const auth = useAuthStore()
const health = useHealthStore()
const flash = ref('')

onMounted(async () => {
  await Promise.all([
    health.loadProfile(),
    health.loadCompletion(),
    health.loadMarkers(),
    health.loadTests()
  ])
})

async function onSubmit(payload) {
  flash.value = ''
  try {
    await health.submitAll(payload)
    flash.value = '健康檔案已儲存'
    setTimeout(() => (flash.value = ''), 2500)
  } catch (e) {
    flash.value = e.response?.data?.error?.message || e.message
  }
}

async function logout() {
  await auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <header class="border-b border-slate-200 bg-white">
      <div class="mx-auto flex max-w-3xl items-center justify-between px-6 py-4">
        <div class="flex items-center gap-2">
          <span class="text-xl">🛡️</span>
          <span class="font-bold text-slate-900">FinGuard</span>
        </div>
        <div class="flex items-center gap-4 text-sm">
          <span class="text-slate-600">{{ auth.currentUser?.email }}</span>
          <button
            class="text-slate-500 transition hover:text-slate-700"
            @click="logout"
          >
            登出
          </button>
        </div>
      </div>
    </header>

    <main class="mx-auto max-w-3xl px-6 py-10">
      <div class="mb-8 flex items-start justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">📋 健康檔案</h1>
          <p class="mt-1 text-sm text-slate-500">
            完成度越高，保險缺口與風險評估越精準
          </p>
        </div>
        <CompletionIndicator :percentage="health.completion.completion_rate" />
      </div>

      <div
        v-if="flash"
        class="mb-6 rounded-lg bg-emerald-50 px-4 py-2 text-sm text-emerald-700"
      >
        {{ flash }}
      </div>

      <BaseCard>
        <HealthProfileForm
          :profile="health.profile"
          :loading="health.loading"
          @submit="onSubmit"
        />
      </BaseCard>
    </main>
  </div>
</template>
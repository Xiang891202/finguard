<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseButton from '@/components/common/BaseButton.vue'

const router = useRouter()
const auth = useAuthStore()
const isDev = import.meta.env.DEV

const email = ref('')
const otp = ref('')
const step = ref('email')
const loading = ref(false)
const error = ref('')
const devCode = ref('')
const countdown = ref(0)
let timer = null

const emailValid = computed(() =>
  /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value)
)

async function sendOTP() {
  if (!emailValid.value) return
  loading.value = true
  error.value = ''
  try {
    const res = await authApi.requestOTP(email.value)
    const payload = res?.data ?? res
    devCode.value = payload?.dev_code || ''
    step.value = 'otp'
    startCountdown(60)
  } catch (e) {
    error.value = e.response?.data?.error?.message || e.message
  } finally {
    loading.value = false
  }
}

function startCountdown(sec) {
  countdown.value = sec
  clearInterval(timer)
  timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) clearInterval(timer)
  }, 1000)
}

async function resend() {
  if (countdown.value > 0) return
  await sendOTP()
}

async function verify() {
  if (otp.value.length < 4) return
  loading.value = true
  error.value = ''
  try {
    await auth.login(email.value, otp.value)
    router.push('/app/account/health')
  } catch (e) {
    error.value = e.response?.data?.error?.message || e.message
  } finally {
    loading.value = false
  }
}

onUnmounted(() => clearInterval(timer))
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-slate-50 px-4">
    <BaseCard class="w-full max-w-md">
      <div class="mb-8 text-center">
        <div class="text-3xl">🛡️</div>
        <h1 class="mt-2 text-2xl font-bold text-slate-900">FinGuard 財安</h1>
        <p class="mt-1 text-sm text-slate-500">登入 / 註冊 (Sign in / Sign up)</p>
      </div>

      <div v-if="step === 'email'" class="space-y-4">
        <BaseInput
          v-model="email"
          label="電子郵件 (Email)"
          type="email"
          placeholder="you@example.com"
          @keydown.enter="sendOTP"
        />
        <BaseButton
          block
          :disabled="!emailValid"
          :loading="loading"
          @click="sendOTP"
        >
          發送驗證碼 (Send OTP)
        </BaseButton>
      </div>

      <div v-else class="space-y-4">
        <div class="rounded-lg bg-slate-50 px-3 py-2 text-sm text-slate-600">
          驗證碼已寄至 <span class="font-medium text-slate-900">{{ email }}</span>
        </div>
        <div
          v-if="isDev && devCode"
          class="rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-800"
        >
          開發模式驗證碼 (Dev code)：
          <span class="font-mono font-bold">{{ devCode }}</span>
        </div>
        <BaseInput
          v-model="otp"
          label="驗證碼 (OTP)"
          placeholder="000000"
          maxlength="6"
          inputmode="numeric"
          center
          tracking
          @keydown.enter="verify"
        />
        <BaseButton
          block
          :disabled="otp.length < 4"
          :loading="loading"
          @click="verify"
        >
          登入 (Sign in)
        </BaseButton>
        <div class="flex items-center justify-between text-sm">
          <button
            type="button"
            class="text-slate-500 transition hover:text-slate-700"
            @click="step = 'email'"
          >
            ← 改用其他電子郵件 (Change email)
          </button>
          <button
            type="button"
            :disabled="countdown > 0"
            class="text-sky-600 transition hover:text-sky-700 disabled:text-slate-400"
            @click="resend"
          >
            {{ countdown > 0
              ? `重新發送 (Resend in ${countdown}s)`
              : '重新發送 (Resend)' }}
          </button>
        </div>
      </div>

      <p v-if="error" class="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
        {{ error }}
      </p>

      <div class="mt-6 border-t border-slate-200 pt-4 text-center text-xs text-slate-400">
        <router-link to="/admin/login" class="transition hover:text-slate-600">
          管理員登入 (Admin sign in) →
        </router-link>
      </div>
    </BaseCard>
  </div>
</template>
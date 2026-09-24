import { defineStore } from 'pinia'
import { healthApi } from '@/api/health'

export const useHealthStore = defineStore('health', {
  state: () => ({
    profile: null,
    completion: { completion_rate: 0, missing_fields: [], precision_level: 'none' },
    markers: [],
    tests: [],
    loading: false,
    error: null
  }),

  actions: {
    async loadProfile() {
      this.loading = true
      this.error = null
      try {
        const res = await healthApi.getProfile()
        this.profile = res.data
      } catch (e) {
        if (e.response?.status === 404) {
          this.profile = null
        } else {
          this.error = e.response?.data?.error?.message || e.message
        }
      } finally {
        this.loading = false
      }
    },

    async loadCompletion() {
      const res = await healthApi.getCompletion()
      this.completion = res.data
    },

    async loadMarkers() {
      const res = await healthApi.listMarkers()
      this.markers = res.data
    },

    async loadTests() {
      const res = await healthApi.listTests()
      this.tests = res.data
    },

    async deleteTest(id) {
      await healthApi.deleteTest(id)
      await Promise.all([this.loadTests(), this.loadCompletion()])
    },

    /**
     * 一次性提交：profile + 同意 + 所有新檢測
     */
    async submitAll({ profile, pendingTests }) {
      this.loading = true
      this.error = null
      try {
        // 1) 存 profile（含 consent_genetic）
        const fn = this.profile ? healthApi.updateProfile : healthApi.createProfile
        const res = await fn(profile)
        this.profile = res.data

        // 2) 逐個提交新的基因檢測
        for (const t of pendingTests || []) {
          await healthApi.addTest({
            marker_id: t.marker_id,
            result: t.result
          })
        }

        // 3) 重新載入
        await Promise.all([this.loadTests(), this.loadCompletion(), this.loadProfile()])
      } finally {
        this.loading = false
      }
    }
  }
})
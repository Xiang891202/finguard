<script setup>
import { computed } from 'vue'

const props = defineProps({
  percentage: { type: Number, default: 0 }
})

const radius = 28
const circumference = 2 * Math.PI * radius
const offset = computed(
  () => circumference * (1 - Math.min(props.percentage, 100) / 100)
)

const color = computed(() => {
  if (props.percentage >= 100) return '#10b981'
  if (props.percentage >= 80) return '#0ea5e9'
  if (props.percentage >= 40) return '#f59e0b'
  return '#ef4444'
})
</script>

<template>
  <div class="flex items-center gap-4">
    <svg width="72" height="72" viewBox="0 0 72 72" class="-rotate-90">
      <circle cx="36" cy="36" :r="radius" fill="none" stroke="#e2e8f0" stroke-width="6" />
      <circle
        cx="36"
        cy="36"
        :r="radius"
        fill="none"
        :stroke="color"
        stroke-width="6"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="offset"
        class="transition-all duration-300 ease-out"
      />
    </svg>
    <div>
      <div class="text-2xl font-bold text-slate-900">{{ percentage.toFixed(0) }}%</div>
      <div class="text-xs text-slate-500">完成度</div>
    </div>
  </div>
</template>
<script setup>
const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'secondary', 'ghost', 'danger'].includes(v)
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v)
  },
  type: { type: String, default: 'button' },
  disabled: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
  block: { type: Boolean, default: false }
})
defineEmits(['click'])

const variantClass = {
  primary: 'bg-sky-600 text-white hover:bg-sky-700 focus:ring-sky-200',
  secondary: 'bg-slate-100 text-slate-700 hover:bg-slate-200 focus:ring-slate-200',
  ghost: 'bg-transparent text-slate-600 hover:bg-slate-100 focus:ring-slate-200',
  danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-200'
}

const sizeClass = {
  sm: 'px-3 py-1 text-sm',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-2.5 text-base'
}
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    class="rounded-lg font-medium transition duration-200 outline-none
           focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
    :class="[
      variantClass[variant],
      sizeClass[size],
      block ? 'w-full' : ''
    ]"
    @click="$emit('click', $event)"
  >
    <span v-if="loading">處理中…</span>
    <slot v-else />
  </button>
</template>
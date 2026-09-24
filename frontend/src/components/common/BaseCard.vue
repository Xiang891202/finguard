<script setup>
defineProps({
  padding: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v)
  }
})

const paddingClass = {
  sm: 'p-4',
  md: 'p-8',
  lg: 'p-10'
}
</script>

<template>
  <div
    class="rounded-2xl border border-slate-200 bg-white shadow-sm"
    :class="paddingClass[padding]"
  >
    <slot />
  </div>
</template>
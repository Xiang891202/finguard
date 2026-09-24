<script setup>
defineProps({
  modelValue: { type: Boolean, default: false },
  label: { type: String, default: '' },
  description: { type: String, default: '' },
  disabled: { type: Boolean, default: false }
})
defineEmits(['update:modelValue'])
</script>

<template>
  <label
    class="group flex cursor-pointer select-none items-start gap-3"
    :class="{ 'cursor-not-allowed opacity-50': disabled }"
  >
    <input
      type="checkbox"
      :checked="modelValue"
      :disabled="disabled"
      class="mt-0.5 h-5 w-5 rounded border-slate-300 text-sky-600
             transition duration-200 focus:ring-sky-500"
      @change="$emit('update:modelValue', $event.target.checked)"
    />
    <span class="text-sm">
      <span class="block font-medium text-slate-800 transition group-hover:text-sky-700">
        {{ label }}
      </span>
      <span v-if="description" class="mt-0.5 block text-xs text-slate-500">
        {{ description }}
      </span>
    </span>
  </label>
</template>
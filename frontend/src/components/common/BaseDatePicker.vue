<script setup>
defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, default: '' },
  required: { type: Boolean, default: false },
  max: { type: String, default: '' }
})
defineEmits(['update:modelValue'])
</script>

<template>
  <label class="block">
    <span v-if="label" class="mb-1 block text-sm font-medium text-slate-700">
      {{ label }}<span v-if="required" class="ml-1 text-red-500">*</span>
    </span>
    <input
      type="date"
      :value="modelValue"
      :max="max"
      class="w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900
             transition duration-200 outline-none
             hover:border-slate-400
             focus:border-sky-500 focus:ring-2 focus:ring-sky-200"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </label>
</template>
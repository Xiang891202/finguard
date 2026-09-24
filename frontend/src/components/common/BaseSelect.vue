<script setup>
defineProps({
  modelValue: { type: [String, Number], default: '' },
  label: { type: String, default: '' },
  options: { type: Array, default: () => [] },   // [{value, label}]
  placeholder: { type: String, default: '請選擇' },
  required: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false }
})
defineEmits(['update:modelValue'])
</script>

<template>
  <label class="block">
    <span v-if="label" class="mb-1 block text-sm font-medium text-slate-700">
      {{ label }}<span v-if="required" class="ml-1 text-red-500">*</span>
    </span>
    <select
      :value="modelValue"
      :disabled="disabled"
      class="w-full rounded-lg border border-slate-300 bg-white px-3 py-2
             text-slate-900 transition duration-200 outline-none
             hover:border-slate-400
             focus:border-sky-500 focus:ring-2 focus:ring-sky-200
             disabled:cursor-not-allowed disabled:bg-slate-50"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option value="">{{ placeholder }}</option>
      <option v-for="o in options" :key="o.value" :value="o.value">
        {{ o.label }}
      </option>
    </select>
  </label>
</template>
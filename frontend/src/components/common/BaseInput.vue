<script setup>
defineProps({
  modelValue: { type: [String, Number], default: '' },
  label: { type: String, default: '' },
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  required: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  maxlength: { type: [String, Number], default: undefined },
  inputmode: { type: String, default: undefined },
  center: { type: Boolean, default: false },
  tracking: { type: Boolean, default: false }
})
defineEmits(['update:modelValue'])
</script>

<template>
  <label class="block">
    <span v-if="label" class="mb-1 block text-sm font-medium text-slate-700">
      {{ label }}<span v-if="required" class="ml-1 text-red-500">*</span>
    </span>
    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :maxlength="maxlength"
      :inputmode="inputmode"
      class="w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900
             transition duration-200 outline-none
             hover:border-slate-400
             focus:border-sky-500 focus:ring-2 focus:ring-sky-200
             disabled:cursor-not-allowed disabled:bg-slate-50"
      :class="[
        center ? 'text-center' : '',
        tracking ? 'text-lg tracking-[0.5em]' : ''
      ]"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </label>
</template>
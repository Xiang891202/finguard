<script setup>
import BaseCheckbox from '@/components/common/BaseCheckbox.vue'
import BaseInput from '@/components/common/BaseInput.vue'

defineProps({
  value: { type: Object, required: true },
  otherValue: { type: String, default: '' }
})
const emit = defineEmits(['update:value', 'update:otherValue'])

const ITEMS = [
  { key: 'cardiovascular', label: '心血管疾病' },
  { key: 'diabetes', label: '糖尿病' },
  { key: 'cancer', label: '癌症' },
  { key: 'stroke', label: '中風' },
  { key: 'hypertension', label: '高血壓' }
]
</script>

<template>
  <div class="space-y-3">
    <BaseCheckbox
      v-for="item in ITEMS"
      :key="item.key"
      :model-value="!!value[item.key]"
      :label="item.label"
      @update:model-value="(v) => emit('update:value', { ...value, [item.key]: v })"
    />
    <div class="pt-2">
      <BaseInput
        :model-value="otherValue"
        label="其他"
        placeholder="例如：甲狀腺疾病"
        @update:model-value="(v) => emit('update:otherValue', v)"
      />
    </div>
  </div>
</template>
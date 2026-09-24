<script setup>
import { ref, computed } from 'vue'
import BaseSelect from '@/components/common/BaseSelect.vue'
import BaseButton from '@/components/common/BaseButton.vue'

const props = defineProps({
  markers: { type: Array, default: () => [] },
  tests: { type: Array, default: () => [] }
})
const emit = defineEmits(['add', 'remove'])

const markerId = ref('')
const result = ref('high')

const RESULT_OPTIONS = [
  { value: 'high', label: '高風險' },
  { value: 'medium', label: '中風險' },
  { value: 'low', label: '低風險' }
]

const markerOptions = computed(() =>
  props.markers.map((m) => {
    const diseases = m.related_diseases || []
    const diseaseStr = diseases.length > 0 ? diseases.join('、') : m.marker_name
    return { value: m.id, label: `${diseaseStr}（${m.marker_code}）` }
  })
)

const canAdd = computed(() => !!markerId.value)

function onAdd() {
  if (!canAdd.value) return
  emit('add', { marker_id: markerId.value, result: result.value })
  markerId.value = ''
  result.value = 'high'
}

function resultLabel(v) {
  return RESULT_OPTIONS.find((o) => o.value === v)?.label || v
}
</script>

<template>
  <div class="space-y-3">
    <div class="grid gap-3 sm:grid-cols-[2fr,1fr,auto]">
      <BaseSelect
        v-model="markerId"
        label="基因點位"
        :options="markerOptions"
        placeholder="請選擇"
      />
      <BaseSelect
        v-model="result"
        label="結果"
        :options="RESULT_OPTIONS"
        placeholder=""
      />
      <div class="flex items-end">
        <BaseButton
          block
          :disabled="!canAdd"
          @click="onAdd"
        >
          新增
        </BaseButton>
      </div>
    </div>

    <p v-if="markers.length === 0" class="text-xs text-amber-700">
      ⚠️ 尚無基因點位資料，請聯絡管理員
    </p>

    <ul v-if="tests.length" class="divide-y divide-slate-200">
      <li
        v-for="t in tests"
        :key="t.id"
        class="flex items-center justify-between py-2"
      >
        <div>
          <div class="font-medium text-slate-800">
            {{ t.marker_name }}
            <span v-if="t.pending" class="ml-2 text-xs text-amber-600">（未儲存）</span>
          </div>
          <div class="text-xs text-slate-500">
            {{ resultLabel(t.result) }}
            <span v-if="t.risk_level_computed !== null && t.risk_level_computed !== undefined">
              · 風險倍數 {{ t.risk_level_computed }}
            </span>
          </div>
        </div>
        <button
          type="button"
          class="rounded-md px-3 py-1 text-sm text-red-600 transition duration-200
                 hover:bg-red-50"
          @click="emit('remove', t)"
        >
          刪除
        </button>
      </li>
    </ul>
    <p v-else class="text-sm text-slate-500">尚未新增任何檢測</p>
  </div>
</template>
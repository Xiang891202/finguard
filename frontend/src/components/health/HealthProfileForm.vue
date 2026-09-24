<script setup>
import { onMounted, watch, computed, ref } from 'vue'
import { useHealthProfile } from '@/composables/useHealthProfile'
import { useHealthStore } from '@/stores/health'
import BaseDatePicker from '@/components/common/BaseDatePicker.vue'
import BaseCheckbox from '@/components/common/BaseCheckbox.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import FamilyHistoryForm from './FamilyHistoryForm.vue'
import GeneticTestForm from './GeneticTestForm.vue'

const props = defineProps({
  profile: { type: Object, default: null },
  loading: { type: Boolean, default: false }
})
const emit = defineEmits(['submit'])

const health = useHealthStore()
const { form, completion, isValid, toPayload, fromProfile } = useHealthProfile()

const markers = computed(() => health.markers || [])
const existingTests = computed(() => health.tests || [])
const localConsent = ref(false)
const pendingTests = ref([])

let lastLoadedId = null
function syncFromProfile(p) {
  if (!p || p.id === lastLoadedId) return
  fromProfile(p)
  localConsent.value = !!p.consent_genetic
  lastLoadedId = p.id
}

onMounted(() => syncFromProfile(props.profile))
watch(() => props.profile?.id, () => syncFromProfile(props.profile))

const GENDERS = [
  { value: 'male', label: '男' },
  { value: 'female', label: '女' }
]

const allTests = computed(() => {
  const existing = existingTests.value.map((t) => ({ ...t, pending: false }))
  return [...existing, ...pendingTests.value]
})

function addPending({ marker_id, result }) {
  const m = markers.value.find((x) => x.id === marker_id)
  if (!m) return
  if (
    existingTests.value.some((t) => t.marker_id === marker_id) ||
    pendingTests.value.some((t) => t.marker_id === marker_id)
  ) return
  pendingTests.value.push({
    id: `pending-${Date.now()}-${marker_id}`,
    marker_id,
    marker_name: m.marker_name,
    result,
    risk_level_computed: null,
    pending: true
  })
}

async function removeTest(t) {
  if (t.pending) {
    pendingTests.value = pendingTests.value.filter((x) => x.id !== t.id)
  } else {
    await health.deleteTest(t.id)
  }
}

function onSubmit() {
  if (!isValid.value) return
  const payload = {
    ...toPayload(),
    consent_genetic: form.has_genetic_test ? localConsent.value : false
  }
  emit('submit', {
    profile: payload,
    pendingTests: pendingTests.value.map((t) => ({
      marker_id: t.marker_id,
      result: t.result
    }))
  })
}
</script>

<template>
  <form class="space-y-8" @submit.prevent="onSubmit">
    <section class="space-y-4">
      <h3 class="text-sm font-semibold uppercase tracking-wide text-slate-500">
        基本資料（必填）
      </h3>
      <BaseDatePicker
        v-model="form.birth_date"
        label="西元生日"
        required
        max="2100-12-31"
      />
      <div>
        <span class="mb-1 block text-sm font-medium text-slate-700">
          性別<span class="ml-1 text-red-500">*</span>
        </span>
        <div class="flex gap-2">
          <button
            v-for="g in GENDERS"
            :key="g.value"
            type="button"
            class="rounded-lg border px-4 py-2 text-sm transition duration-200"
            :class="form.gender === g.value
              ? 'border-sky-500 bg-sky-50 text-sky-700'
              : 'border-slate-300 text-slate-700 hover:border-slate-400'"
            @click="form.gender = g.value"
          >
            {{ g.label }}
          </button>
        </div>
      </div>
    </section>

    <section class="space-y-4">
      <h3 class="text-sm font-semibold uppercase tracking-wide text-slate-500">
        家族病史（選填）
      </h3>
      <FamilyHistoryForm
        :value="form.family_history"
        :other-value="form.other_history"
        @update:value="(v) => (form.family_history = v)"
        @update:other-value="(v) => (form.other_history = v)"
      />
    </section>

    <section class="space-y-4">
      <h3 class="text-sm font-semibold uppercase tracking-wide text-slate-500">
        基因檢測（選填）
      </h3>
      <BaseCheckbox
        v-model="form.has_genetic_test"
        label="我做過基因檢測"
      />
      <div
        v-if="form.has_genetic_test"
        class="rounded-xl border border-slate-200 bg-slate-50 p-4"
      >
        <BaseCheckbox
          v-model="localConsent"
          label="我同意 FinGuard 處理我的基因資料"
          description="依個人資料保護法第 6 條，基因資料屬特種個資，需獨立同意。資料將加密儲存，您可隨時刪除。"
        />
        <div
          v-if="localConsent"
          class="mt-4 rounded-lg border border-slate-200 bg-white p-4"
        >
          <GeneticTestForm
            :markers="markers"
            :tests="allTests"
            @add="addPending"
            @remove="removeTest"
          />
        </div>
      </div>
    </section>

    <div class="flex items-center justify-between border-t border-slate-200 pt-6">
      <div class="text-sm text-slate-500">
        目前完成度 <span class="font-semibold text-slate-700">{{ completion }}%</span>
      </div>
      <BaseButton
        type="submit"
        :disabled="!isValid"
        :loading="loading"
      >
        儲存
      </BaseButton>
    </div>
  </form>
</template>
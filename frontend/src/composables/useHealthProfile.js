import { reactive, computed } from 'vue'

const FAMILY_KEYS = ['cardiovascular', 'diabetes', 'cancer', 'stroke', 'hypertension']

export function useHealthProfile() {
  const form = reactive({
    birth_date: '',
    gender: '',
    family_history: {
      cardiovascular: false,
      diabetes: false,
      cancer: false,
      stroke: false,
      hypertension: false
    },
    other_history: '',
    has_genetic_test: false
  })

  const completion = computed(() => {
    let s = 0
    if (form.birth_date) s += 40
    if (form.gender) s += 40
    const hasFH = Object.values(form.family_history).some(Boolean) || !!form.other_history
    if (hasFH) s += 10
    if (form.has_genetic_test) s += 10
    return s
  })

  const isValid = computed(() => !!form.birth_date && !!form.gender)

  function toPayload() {
    const fh = { ...form.family_history }
    if (form.other_history) fh.other = form.other_history
    const hasFH = Object.values(form.family_history).some(Boolean) || !!form.other_history
    return {
      birth_date: form.birth_date,
      gender: form.gender,
      family_history: hasFH ? fh : null,
      has_genetic_test: form.has_genetic_test
    }
  }

  function fromProfile(p) {
    if (!p) return
    form.birth_date = p.birth_date || ''
    form.gender = p.gender || ''
    const fh = p.family_history || {}
    for (const k of FAMILY_KEYS) {
      form.family_history[k] = !!fh[k]
    }
    form.other_history = fh.other || ''
    form.has_genetic_test = !!p.has_genetic_test
  }

  return { form, completion, isValid, toPayload, fromProfile, FAMILY_KEYS }
}
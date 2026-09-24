import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import HealthProfileForm from '@/components/health/HealthProfileForm.vue'

describe('HealthProfileForm', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders empty form when no profile', () => {
    const wrapper = mount(HealthProfileForm, {
      global: { plugins: [createPinia()] }
    })
    expect(wrapper.find('form').exists()).toBe(true)
    expect(wrapper.text()).toContain('基本資料')
    expect(wrapper.text()).toContain('家族病史')
    expect(wrapper.text()).toContain('基因檢測')
  })

  it('fills fields from profile prop and updates completion', async () => {
    const wrapper = mount(HealthProfileForm, {
      props: {
        profile: {
          birth_date: '1985-06-15',
          gender: 'male',
          family_history: { cardiovascular: true },
          has_genetic_test: false
        }
      },
      global: { plugins: [createPinia()] }
    })
    await wrapper.vm.$nextTick()
    // 80 + 10（家族病史）= 90
    expect(wrapper.text()).toContain('90%')
  })

  it('disables submit button when required fields empty', () => {
    const wrapper = mount(HealthProfileForm, {
      global: { plugins: [createPinia()] }
    })
    const btn = wrapper.find('button[type="submit"]')
    expect(btn.attributes('disabled')).toBeDefined()
  })

    it('emits submit with correct payload', async () => {
    const wrapper = mount(HealthProfileForm, {
      props: {
        profile: {
          birth_date: '1985-06-15',
          gender: 'male',
          family_history: {},
          has_genetic_test: false
        }
      },
      global: { plugins: [createPinia()] }
    })
    await wrapper.vm.$nextTick()
    await wrapper.find('form').trigger('submit.prevent')

    const events = wrapper.emitted('submit')
    expect(events).toBeTruthy()
    expect(events[0][0].profile.birth_date).toBe('1985-06-15')
    expect(events[0][0].profile.gender).toBe('male')
    expect(events[0][0].profile.consent_genetic).toBe(false)
    expect(events[0][0].pendingTests).toEqual([])
  })
})
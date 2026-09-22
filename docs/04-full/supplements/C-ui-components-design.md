📚 Full P5.5 補充文件包（三份完整文件）

📄 文件 C：Full P5.5 詳細 UI 元件設計
版本：v1.0
適用範圍：Full P5.5 前端元件

C.1 元件總覽
C.1.1 元件層級
text
頁面層（5 個）
├── EnginesView.vue
├── EngineDetailView.vue
├── EngineEditorView.vue
├── ExecutionTracesView.vue
└── RecomputeJobsView.vue

引擎總覽（3 個）
├── EngineOverviewCard.vue
├── RecentExecutions.vue
└── RecomputeSummary.vue

版本管理（4 個）
├── VersionList.vue
├── VersionCard.vue
├── VersionCompare.vue
└── ActivationPanel.vue

編輯器（引用文件 B）
├── EditorPanel.vue
├── 6 種引擎編輯器
├── TestRunner.vue
└── SubmitPanel.vue

追蹤樹（3 個）
├── TraceFilter.vue
├── TraceTree.vue
└── TraceNode.vue

重算（4 個）
├── JobList.vue
├── JobCard.vue
├── RecomputeForm.vue
└── JobProgress.vue
C.1.2 元件依賴關係
text
EnginesView
├── EngineOverviewCard（x5）
├── RecentExecutions
└── RecomputeSummary

EngineDetailView
├── VersionList
│   └── VersionCard
├── VersionCompare
└── ActivationPanel

EngineEditorView
├── EditorPanel
│   └── 6 種編輯器（文件 B）
├── TestRunner
└── SubmitPanel

ExecutionTracesView
├── TraceFilter
└── TraceTree
    └── TraceNode

RecomputeJobsView
├── JobList
│   └── JobCard
├── RecomputeForm
└── JobProgress
C.2 頁面層元件
C.2.1 EnginesView.vue
職責：引擎總覽頁，顯示 5 大引擎的狀態。

Props：無（從 store 讀取）

Emits：無

內部狀態：

狀態	型別	說明
engines	ref	從 store 讀取
loading	ref	載入中
error	ref	錯誤訊息
生命週期：

onMounted：呼叫 enginesStore.fetchAll()

子元件：

EngineOverviewCard（x5）

RecentExecutions

RecomputeSummary

路由：/admin/engines

C.2.2 EngineDetailView.vue
職責：單一引擎的版本管理頁。

Props：

Prop	型別	必填	說明
（從 route.params 讀取）	-	-	engineType
內部狀態：

狀態	型別	說明
engineType	computed	從 route 取得
versions	ref	版本列表
selectedVersion	ref	當前選中版本
生命週期：

onMounted：呼叫 enginesStore.fetchVersions(engineType)

子元件：

VersionList

VersionCompare

ActivationPanel

路由：/admin/engines/:type

C.2.3 EngineEditorView.vue
職責：引擎編輯器頁。

Props：

Prop	型別	必填	說明
（從 route.params 讀取）	-	-	engineType, version
內部狀態：

狀態	型別	說明
config	ref	當前編輯的設定
isDirty	computed	是否有未儲存變更
isTesting	ref	測試中
生命週期：

onMounted：呼叫 enginesStore.fetchVersion(engineType, version)

onBeforeRouteLeave：若有未儲存變更，提示使用者

子元件：

EditorPanel（分派到 6 種編輯器）

TestRunner

SubmitPanel

路由：/admin/engines/:type/edit/:version

C.2.4 ExecutionTracesView.vue
職責：執行追蹤列表頁。

Props：無

內部狀態：

狀態	型別	說明
traces	ref	追蹤列表
filters	ref	篩選條件
selectedSnapshotId	ref	選中的快照 ID
生命週期：

onMounted：呼叫 enginesStore.fetchTraces()

子元件：

TraceFilter

TraceTree

路由：/admin/traces

C.2.5 RecomputeJobsView.vue
職責：重算任務管理頁。

Props：無

內部狀態：

狀態	型別	說明
jobs	ref	重算任務列表
showForm	ref	是否顯示新增表單
生命週期：

onMounted：呼叫 enginesStore.fetchRecomputeJobs()

子元件：

JobList

RecomputeForm

JobProgress

路由：/admin/recompute

C.3 引擎總覽相關元件
C.3.1 EngineOverviewCard.vue
職責：顯示單一引擎的狀態卡片。

Props：

Prop	型別	必填	說明
engine	Object	✅	引擎資訊
engine 物件結構：

javascript
{
  engine_type: 'crawler',
  name: '爬蟲引擎',
  active_version: 'v1.2',
  version_count: 3,
  last_execution: '2026-09-22T06:00:00Z',
  status: 'healthy'
}
Emits：

事件	參數	說明
edit	-	點擊編輯
versions	-	點擊版本
traces	-	點擊追蹤
內部狀態：

狀態	型別	說明
statusColor	computed	依 status 計算顏色
子元件：

BaseCard

BaseButton（x3）

測試案例：

javascript
it('emits edit when edit button clicked', async () => {
  const wrapper = mount(EngineOverviewCard, {
    props: { engine: mockEngine }
  })
  await wrapper.find('[data-testid="edit-btn"]').trigger('click')
  expect(wrapper.emitted('edit')).toBeTruthy()
})

it('shows green status for healthy', () => {
  const wrapper = mount(EngineOverviewCard, {
    props: { engine: { ...mockEngine, status: 'healthy' } }
  })
  expect(wrapper.find('.status-healthy').exists()).toBe(true)
})
C.3.2 RecentExecutions.vue
職責：顯示最近執行紀錄。

Props：

Prop	型別	必填	說明
executions	Array	✅	執行紀錄
execution 物件結構：

javascript
{
  execution_snapshot_id: 'uuid',
  execution_date: '2026-09-22',
  status: 'success',
  duration_ms: 3200
}
Emits：

事件	參數	說明
view-trace	snapshotId	查看追蹤樹
子元件：

BaseTable

C.3.3 RecomputeSummary.vue
職責：顯示重算任務統計。

Props：

Prop	型別	必填	說明
summary	Object	✅	統計資料
summary 物件結構：

javascript
{
  running: 0,
  pending: 0,
  completed: 3,
  failed: 0
}
子元件：

BaseCard（x4）

C.4 版本管理相關元件
C.4.1 VersionList.vue
職責：版本列表。

Props：

Prop	型別	必填	說明
versions	Array	✅	版本清單
Emits：

事件	參數	說明
select	versionId	選中版本
activate	versionId	啟用
archive	versionId	封存
delete	versionId	刪除
compare	[v1, v2]	比較
內部狀態：

狀態	型別	說明
compareMode	ref	是否為比較模式
selectedForCompare	ref	選中的版本（最多 2 個）
子元件：

VersionCard（xN）

BaseButton（比較）

C.4.2 VersionCard.vue
職責：單一版本卡片。

Props：

Prop	型別	必填	說明
version	Object	✅	版本資訊
compareMode	Boolean	❌	是否為比較模式
version 物件結構：

javascript
{
  id: 'uuid',
  engine_type: 'llm',
  version: 'v1.4',
  status: 'draft',  // draft/testing/active/archived
  description: '優化市場情緒解讀語氣',
  created_at: '2026-09-22T10:00:00Z',
  activated_at: null,
  usage_count: 0,
  avg_duration_ms: null
}
Emits：

事件	參數	說明
select	-	選中
activate	-	啟用
archive	-	封存
delete	-	刪除
compare-select	-	比較選中
內部狀態：

狀態	型別	說明
statusBadge	computed	依 status 顯示徽章
canActivate	computed	是否可啟用（僅 testing/draft）
canDelete	computed	是否可刪除（僅 draft）
子元件：

BaseCard

BaseButton（依狀態顯示不同按鈕）

測試案例：

javascript
it('shows activate button for draft', () => {
  const wrapper = mount(VersionCard, {
    props: { version: { ...mockVersion, status: 'draft' } }
  })
  expect(wrapper.find('[data-testid="activate-btn"]').exists()).toBe(true)
})

it('hides delete button for active', () => {
  const wrapper = mount(VersionCard, {
    props: { version: { ...mockVersion, status: 'active' } }
  })
  expect(wrapper.find('[data-testid="delete-btn"]').exists()).toBe(false)
})
C.4.3 VersionCompare.vue
職責：比較兩個版本的差異。

Props：

Prop	型別	必填	說明
v1	Object	✅	版本 1
v2	Object	✅	版本 2
內部狀態：

狀態	型別	說明
diff	computed	差異清單
差異顯示：

text
┌─────────────────────────────────────────────────────────────┐
│  📊 版本比較                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  欄位             v1.3           v1.4        差異           │
│  ─────────────────────────────────────────────────────     │
│  model            qwen2.5:7b     qwen2.5:7b  -             │
│  temperature      0.3            0.3         -             │
│  max_tokens       200            200         -             │
│  system_prompt    「你是一位...」 「你是...」  ✏️ 修改       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
子元件：

BaseTable

C.4.4 ActivationPanel.vue
職責：啟用版本的確認面板。

Props：

Prop	型別	必填	說明
version	Object	✅	待啟用版本
Emits：

事件	參數	說明
confirm	-	確認啟用
cancel	-	取消
內部狀態：

狀態	型別	說明
showConfirm	ref	是否顯示確認對話框
子元件：

BaseModal

BaseButton

C.5 編輯器相關元件
編輯器子元件詳見文件 B。

C.5.1 EditorPanel.vue
職責：根據引擎類型分派到對應編輯器。

Props：

Prop	型別	必填	說明
engineType	String	✅	crawler / normalizer / ...
config	Object	✅	當前設定
disabled	Boolean	❌	是否唯讀
Emits：

事件	參數	說明
update:config	Object	設定變更
validate	Boolean	驗證結果
內部邏輯：

javascript
const editorComponent = computed(() => {
  return {
    crawler: CrawlerEditor,
    normalizer: NormalizerEditor,
    validator: ValidatorEditor,
    matcher: MatcherEditor,
    monte_carlo: MonteCarloEditor,
    llm: LLMEditor
  }[props.engineType]
})
C.5.2 TestRunner.vue
職責：測試執行器，用測試輸入驗證設定。

Props：

Prop	型別	必填	說明
engineType	String	✅	引擎類型
config	Object	✅	當前設定
Emits：

事件	參數	說明
tested	result	測試完成
內部狀態：

狀態	型別	說明
testInput	ref	測試輸入（JSON）
testing	ref	測試中
result	ref	測試結果
error	ref	錯誤訊息
子元件：

BaseInput（testInput）

BaseButton（執行測試）

ResultDisplay（測試結果）

測試案例：

javascript
it('runs test and emits result', async () => {
  const wrapper = mount(TestRunner, {
    props: { engineType: 'llm', config: mockConfig }
  })
  await wrapper.find('[name="test_input"]').setValue('{"score": 62}')
  await wrapper.find('[data-testid="run-test"]').trigger('click')
  await flushPromises()
  expect(wrapper.emitted('tested')).toBeTruthy()
})
C.5.3 SubmitPanel.vue
職責：提交面板，管理版本提交。

Props：

Prop	型別	必填	說明
engineType	String	✅	引擎類型
config	Object	✅	當前設定
currentVersion	String	❌	當前版本（若為編輯）
Emits：

事件	參數	說明
submit-draft	data	提交為草稿
submit-testing	data	提交為測試版
submit-active	data	直接啟用
內部狀態：

狀態	型別	說明
description	ref	變更說明
nextVersion	computed	下一個版本號
submitting	ref	提交中
子元件：

BaseInput（description）

VersionBadge（nextVersion）

BaseButton（x3）

版本號自動遞增邏輯：

javascript
const nextVersion = computed(() => {
  const match = props.currentVersion?.match(/v(\d+)\.(\d+)/)
  if (!match) return 'v1.0'
  const [, major, minor] = match
  return `v${major}.${parseInt(minor) + 1}`
})
C.6 追蹤樹相關元件
C.6.1 TraceFilter.vue
職責：追蹤篩選器。

Props：

Prop	型別	必填	說明
filters	Object	✅	當前篩選條件
Emits：

事件	參數	說明
update:filters	Object	篩選變更
篩選欄位：

日期範圍

引擎類型

狀態（success/failed/skipped）

子元件：

BaseDatePicker（x2）

BaseSelect（engineType）

BaseSelect（status）

C.6.2 TraceTree.vue
職責：樹狀追蹤顯示。

Props：

Prop	型別	必填	說明
trace	Object	✅	追蹤樹根節點
trace 物件結構：

javascript
{
  engine_type: 'crawler',
  step_name: 'daily_crawl',
  status: 'success',
  duration_ms: 3200,
  input_data: {...},
  output_data: {...},
  children: [...]
}
Emits：

事件	參數	說明
node-click	node	節點被點擊
內部狀態：

狀態	型別	說明
expandedNodes	ref(Set)	已展開節點
子元件：

TraceNode（遞迴）

C.6.3 TraceNode.vue
職責：單一追蹤節點。

Props：

Prop	型別	必填	說明
node	Object	✅	節點資料
depth	Number	❌	縮排深度（預設 0）
expanded	Boolean	❌	是否展開
Emits：

事件	參數	說明
toggle	-	展開/收合
click	node	點擊
內部狀態：

狀態	型別	說明
statusColor	computed	依 status 計算顏色
hasChildren	computed	是否有子節點
渲染邏輯：

vue
<template>
  <div class="trace-node" :style="{ paddingLeft: `${depth * 20}px` }">
    <div @click="$emit('click', node)">
      <span v-if="hasChildren" @click.stop="$emit('toggle')">
        {{ expanded ? '▼' : '▶' }}
      </span>
      <span :class="statusColor">●</span>
      <span>{{ node.step_name }}</span>
      <span>{{ node.duration_ms }}ms</span>
    </div>
    <div v-if="expanded && hasChildren">
      <TraceNode
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        :depth="depth + 1"
      />
    </div>
  </div>
</template>
C.7 重算相關元件
C.7.1 JobList.vue
職責：重算任務列表。

Props：

Prop	型別	必填	說明
jobs	Array	✅	任務列表
Emits：

事件	參數	說明
view	jobId	查看任務
子元件：

JobCard（xN）

C.7.2 JobCard.vue
職責：單一重算任務卡片。

Props：

Prop	型別	必填	說明
job	Object	✅	任務資訊
job 物件結構：

javascript
{
  id: 'uuid',
  engine_type: 'monte_carlo',
  from_version: 'v1.0.0',
  to_version: 'v1.1.0',
  status: 'running',
  affected_records: 30,
  total_records: 100,
  started_at: '2026-09-22T10:00:00Z',
  completed_at: null
}
內部狀態：

狀態	型別	說明
progress	computed	進度 %
statusColor	computed	狀態顏色
子元件：

BaseCard

JobProgress

C.7.3 RecomputeForm.vue
職責：新增重算任務表單。

Props：無

Emits：

事件	參數	說明
submit	data	提交表單
cancel	-	取消
內部狀態：

狀態	型別	說明
form	ref	表單資料
versions	ref	可選版本
errors	ref	驗證錯誤
表單欄位：

engine_type（Select）

from_version_id（Select）

to_version_id（Select）

start_date（DatePicker）

end_date（DatePicker）

子元件：

BaseSelect（x3）

BaseDatePicker（x2）

BaseButton（x2）

驗證規則：

欄位	規則
engine_type	必填
from_version_id	必填、不等於 to_version_id
to_version_id	必填
start_date	必填、≤ end_date
end_date	必填、≥ start_date
C.7.4 JobProgress.vue
職責：顯示任務進度條。

Props：

Prop	型別	必填	說明
current	Number	✅	當前進度
total	Number	✅	總數
內部狀態：

狀態	型別	說明
percentage	computed	百分比
color	computed	依進度顯示顏色
C.8 狀態管理與資料流
C.8.1 Pinia Store
javascript
// frontend/src/stores/engines.js

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import enginesApi from '@/api/engines'

export const useEnginesStore = defineStore('engines', () => {
  // State
  const engines = ref([])
  const versions = ref({})  // { [engineType]: [...] }
  const traces = ref([])
  const recomputeJobs = ref([])
  const loading = ref(false)
  
  // Getters
  const getActiveVersion = computed(() => (engineType) => {
    return versions.value[engineType]?.find(v => v.status === 'active')
  })
  
  // Actions
  async function fetchAll() {
    loading.value = true
    try {
      engines.value = await enginesApi.getAll()
    } finally {
      loading.value = false
    }
  }
  
  async function fetchVersions(engineType) {
    versions.value[engineType] = await enginesApi.getVersions(engineType)
  }
  
  async function activateVersion(engineType, versionId) {
    await enginesApi.activate(engineType, versionId)
    await fetchVersions(engineType)
  }
  
  async function createRecomputeJob(data) {
    const job = await enginesApi.createRecompute(data)
    recomputeJobs.value.push(job)
    return job
  }
  
  return {
    engines, versions, traces, recomputeJobs, loading,
    getActiveVersion,
    fetchAll, fetchVersions, activateVersion, createRecomputeJob
  }
})
C.8.2 資料流範例：啟用版本
text
1. 使用者點擊「啟用」按鈕
    ↓
2. VersionCard 發出 activate 事件
    ↓
3. VersionList 轉發至 EngineDetailView
    ↓
4. EngineDetailView 呼叫 enginesStore.activateVersion()
    ↓
5. Store 呼叫 API
    ↓
6. API 回應成功
    ↓
7. Store 重新 fetchVersions
    ↓
8. 所有相關元件自動更新
C.9 測試策略
C.9.1 單元測試覆蓋
元件	測試案例數	重點
EngineOverviewCard	5	Props 渲染、Emits
VersionCard	8	狀態顯示、按鈕可見性
VersionCompare	3	差異計算
EditorPanel	4	分派邏輯
TestRunner	5	測試執行、錯誤處理
SubmitPanel	6	版本遞增、提交
TraceNode	4	展開、點擊
JobCard	4	進度顯示
RecomputeForm	8	驗證規則
C.9.2 整合測試
javascript
// frontend/tests/integration/engine-lifecycle.spec.js

describe('Engine Lifecycle', () => {
  it('full lifecycle: create → test → activate', async () => {
    const wrapper = mount(EngineEditorView, {
      global: {
        plugins: [createTestingPinia()]
      }
    })
    
    // 1. 編輯設定
    await wrapper.find('[name="temperature"]').setValue(0.5)
    
    // 2. 測試
    await wrapper.find('[data-testid="run-test"]').trigger('click')
    await flushPromises()
    expect(wrapper.find('[data-testid="test-result"]').text()).toContain('success')
    
    // 3. 提交為測試版
    await wrapper.find('[data-testid="submit-testing"]').trigger('click')
    expect(wrapper.emitted('submit')).toBeTruthy()
  })
})
C.9.3 E2E 測試（Playwright）
javascript
// e2e/engine-management.spec.js

test('admin can manage engine versions', async ({ page }) => {
  await page.goto('/admin/engines')
  await expect(page.locator('[data-testid="engine-card"]')).toHaveCount(5)
  
  await page.click('[data-testid="engine-card-llm"] [data-testid="edit-btn"]')
  await expect(page).toHaveURL(/\/admin\/engines\/llm/)
  
  await page.click('[data-testid="new-version-btn"]')
  await page.fill('[name="temperature"]', '0.5')
  await page.click('[data-testid="run-test"]')
  await expect(page.locator('[data-testid="test-result"]')).toBeVisible()
})
C.10 實作檢查清單
□ 5 個頁面層元件
□ 3 個引擎總覽元件
□ 4 個版本管理元件
□ 3 個編輯器相關元件
□ 3 個追蹤樹元件
□ 4 個重算元件
□ 6 種引擎編輯器（文件 B）
□ Pinia Store 完整
□ 路由設定完整
□ 單元測試 ≥ 80%
□ 整合測試通過
□ E2E 測試通過
□ 響應式設計（3 裝置）
□ 無障礙（a11y）檢查
文件 C 結束
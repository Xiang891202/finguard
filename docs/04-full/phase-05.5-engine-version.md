# Full Phase 5.5：引擎版本管理系統

**版本**：v1.0
**所屬**：完整版
**依賴 Phase**：
- Full P1（多租戶）
- MVP P7（爬蟲）、MVP P9（蒙地卡羅）
**預計工時**：8 天

---

## ⚠️ 本 Phase 的完整版約束

- 完整版專屬（MVP 不納入）
- 支援 5 大引擎的版本管理
- Redis Pub/Sub 快取失效
- 圖形化編輯器

---

## 🔗 依賴 MVP 哪個 Phase

- **依賴 MVP P0**：`engine_versions` 等表已建立（空表）
- **依賴 MVP P7**：爬蟲引擎已運作
- **依賴 MVP P9**：蒙地卡羅引擎已運作
- **依賴 Full P1**：多租戶架構已完成

---

## 🔄 與 MVP 的差異

| 項目 | MVP | 完整版 |
| :--- | :--- | :--- |
| 版本管理 | 無（硬編碼） | 完整版本系統 |
| 編輯器 | 無 | 圖形化編輯器 |
| 快取失效 | 無 | Redis Pub/Sub |
| 重算 | 無 | 支援 |
| 追蹤樹 | 無 | 完整追蹤 |
| 引擎數量 | 0（無管理） | 5 引擎 |

---

## 📂 前置檔案檢查

| 檔案路徑 | 來源 | 用途 |
| :--- | :--- | :--- |
| docs/01-framework/01-shared-framework.md | 第一批 | 架構 |
| docs/02-reference/01-database-schema.md | 第二批 | 引擎表 |
| docs/02-reference/02-api-spec.md | 第二批 | API |
| docs/03-mvp/phase-07-crawler.md | 第三批 | 爬蟲實作 |
| docs/03-mvp/phase-09-forecast.md | 第三批 | 蒙地卡羅實作 |

---

## 📦 本 Phase 產出檔案

### 後端

| 檔案路徑 | 動作 | 說明 |
| :--- | :--- | :--- |
| backend/app/api/v1/admin_engines.py | 新增 | 引擎管理 API |
| backend/app/services/engine/version_service.py | 新增 | 版本 CRUD |
| backend/app/services/engine/snapshot_service.py | 新增 | 快照管理 |
| backend/app/services/engine/trace_service.py | 新增 | 追蹤樹 |
| backend/app/services/engine/recompute_service.py | 新增 | 重算任務 |
| backend/app/services/engine/cache_service.py | 新增 | 快取失效 |
| backend/app/services/engine/editor_service.py | 新增 | 編輯器邏輯 |
| backend/app/services/engine/llm_usage_service.py | 新增 | LLM 成本追蹤 |
| backend/app/core/cache_pubsub.py | 新增 | Redis Pub/Sub |
| backend/app/models/engine.py | 新增 | ORM 模型 |
| backend/app/schemas/engine.py | 新增 | DTO |
| backend/app/workers/recompute_worker.py | 新增 | 重算 Worker |

### 前端

| 檔案路徑 | 動作 | 說明 |
| :--- | :--- | :--- |
| frontend/src/views/admin/EnginesView.vue | 新增 | 引擎總覽 |
| frontend/src/views/admin/EngineDetailView.vue | 新增 | 版本管理 |
| frontend/src/views/admin/EngineEditorView.vue | 新增 | 編輯器 |
| frontend/src/views/admin/ExecutionTracesView.vue | 新增 | 追蹤樹 |
| frontend/src/views/admin/RecomputeJobsView.vue | 新增 | 重算任務 |
| frontend/src/components/engine/EngineOverviewCard.vue | 新增 | 引擎卡片 |
| frontend/src/components/engine/VersionList.vue | 新增 | 版本列表 |
| frontend/src/components/engine/VersionCard.vue | 新增 | 單一版本 |
| frontend/src/components/engine/VersionCompare.vue | 新增 | 版本比較 |
| frontend/src/components/engine/TraceTree.vue | 新增 | 樹狀追蹤 |
| frontend/src/components/engine/TraceNode.vue | 新增 | 追蹤節點 |
| frontend/src/components/engine/EditorPanel.vue | 新增 | 編輯面板 |
| frontend/src/components/engine/TestRunner.vue | 新增 | 測試執行器 |
| frontend/src/components/engine/SubmitPanel.vue | 新增 | 提交面板 |
| frontend/src/components/engine/RecomputeForm.vue | 新增 | 重算表單 |
| frontend/src/api/engines.js | 新增 | API |
| frontend/src/stores/engines.js | 新增 | Store |
| frontend/src/composables/useEngineEditor.js | 新增 | Composable |

### 測試

| 檔案路徑 | 動作 |
| :--- | :--- |
| backend/tests/unit/test_version_service.py | 新增 |
| backend/tests/unit/test_cache_pubsub.py | 新增 |
| backend/tests/unit/test_trace_service.py | 新增 |
| backend/tests/integration/test_engine_versions.py | 新增 |
| backend/tests/integration/test_recompute_flow.py | 新增 |
| frontend/tests/EngineEditor.spec.js | 新增 |

---

## 1. 目標

建立跨引擎的版本管理系統，支援：
- 5 大引擎版本 CRUD 與生命週期
- 執行快照記錄
- 追蹤樹視覺化
- 重算任務
- Redis Pub/Sub 快取失效
- 圖形化編輯器

---

## 2. 前置條件

- [ ] Full P1 完成
- [ ] MVP P7, P9 完成
- [ ] Redis Pub/Sub 已設定
- [ ] 6 張引擎管理表已建立

---

## 3. 前端畫面

### 3.1 頁面清單

| 頁面 | 路由 | 說明 |
| :--- | :--- | :--- |
| EnginesView | /admin/engines | 引擎總覽 |
| EngineDetailView | /admin/engines/:type | 版本管理 |
| EngineEditorView | /admin/engines/:type/edit/:version | 編輯器 |
| ExecutionTracesView | /admin/traces | 追蹤列表 |
| RecomputeJobsView | /admin/recompute | 重算任務 |

### 3.2 UI 草圖

**EnginesView**：
┌─────────────────────────────────────────────────────────────┐
│ ⚙️ 引擎管理中心 │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 🕷️ 爬蟲引擎 v1.2 ✅ [編輯] [版本] [追蹤] │ │
│ │ 🧹 資料整理 v1.1 ✅ [編輯] [版本] [追蹤] │ │
│ │ 🎯 用戶比對 v1.0 ✅ [編輯] [版本] [追蹤] │ │
│ │ 🎲 蒙地卡羅 v1.0 ✅ [編輯] [版本] [追蹤] │ │
│ │ 🧠 LLM v1.3 ✅ [編輯] [版本] [追蹤] │ │
│ └─────────────────────────────────────────────────────┘ │
│ │
│ 【最近執行】 │
│ 2026-09-22 06:00 ✅ 成功 │
│ [展開追蹤樹] │
│ │
│ 【重算任務】 │
│ 進行中：0 | 待處理：0 | 完成：3 │
│ │
└─────────────────────────────────────────────────────────────┘

text

**EngineDetailView**：
┌─────────────────────────────────────────────────────────────┐
│ 🎲 蒙地卡羅引擎 — 版本管理 │
├─────────────────────────────────────────────────────────────┤
│ │
│ 【版本列表】 │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ v1.0.0 ✅ 使用中 │ │
│ │ 建立：2026-09-01 │ │
│ │ 使用次數：22 次 │ │
│ │ 平均耗時：3.2s │ │
│ │ 模擬次數：10,000 │ │
│ │ [檢視設定] [封存] │ │
│ ├─────────────────────────────────────────────────────┤ │
│ │ v0.9.0 📦 已封存 │ │
│ │ 建立：2026-08-15 │ │
│ │ 使用次數：17 次 │ │
│ │ [檢視設定] [切換為使用中] [重算歷史] │ │
│ └─────────────────────────────────────────────────────┘ │
│ │
│ 【版本比較】 │
│ 選擇兩個版本 → [比較] │
│ │
│ 【重算任務】 │
│ ● 只算未來（預設） │
│ ○ 重算最近 30 天 │
│ ○ 全歷史重算 │
│ │
└─────────────────────────────────────────────────────────────┘

text

**EngineEditorView（LLM 為例）**：
┌─────────────────────────────────────────────────────────────┐
│ 🧠 LLM 引擎編輯器 — prompt-v1.4（草稿） │
├─────────────────────────────────────────────────────────────┤
│ │
│ 【基本設定】 │
│ 模型：[qwen2.5:7b ▼] Temperature：0.3 │
│ Max Tokens：200 │
│ │
│ 【System Prompt】 │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 你是一位財務分析師... │ │
│ └─────────────────────────────────────────────────────┘ │
│ │
│ 【User Prompt 模板】 │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 市場情緒分數：{{ sentiment_score }} │ │
│ │ 市場狀態：{{ state }} │ │
│ │ 波動率：{{ volatility }} │ │
│ │ 回撤：{{ drawdown }} │ │
│ └─────────────────────────────────────────────────────┘ │
│ │
│ 【本地測試】 │
│ 測試輸入： │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ { "sentiment_score": 62, "state": "elevated", ... } │ │
│ └─────────────────────────────────────────────────────┘ │
│ [▶ 執行測試] │
│ │
│ 結果：目前市場情緒分數為 62... │
│ 耗時：850ms | Tokens：45/200 │
│ │
│ [儲存草稿] [提交為測試版] [直接啟用] │
└─────────────────────────────────────────────────────────────┘

text

### 3.3 Vue 元件結構
EnginesView.vue
├── EngineOverviewCard.vue（5 個引擎）
├── RecentExecutions.vue
└── RecomputeSummary.vue

EngineDetailView.vue
├── VersionList.vue
│ └── VersionCard.vue
├── VersionCompare.vue
└── ActivationPanel.vue

EngineEditorView.vue
├── EditorPanel.vue
│ ├── BasicSettingsForm.vue
│ ├── SystemPromptEditor.vue
│ └── UserPromptEditor.vue
├── TestRunner.vue
└── SubmitPanel.vue

ExecutionTracesView.vue
├── TraceFilter.vue
└── TraceTree.vue
└── TraceNode.vue

RecomputeJobsView.vue
├── JobList.vue
├── RecomputeForm.vue
└── JobProgress.vue

text

**元件職責**：

| 元件 | 職責 | Props | Emits |
| :--- | :--- | :--- | :--- |
| EnginesView | 引擎總覽 | - | - |
| EngineOverviewCard | 單一引擎卡片 | engine: Object | edit, versions, traces |
| VersionList | 版本列表 | versions: Array | select, activate, archive |
| VersionCard | 單一版本 | version: Object | click |
| VersionCompare | 版本比較 | v1, v2 | - |
| EditorPanel | 編輯面板 | config: Object | update:config |
| TestRunner | 測試執行 | endpoint: String | result |
| SubmitPanel | 提交面板 | version: Object | submit |
| TraceTree | 追蹤樹 | trace: Object | node-click |
| TraceNode | 追蹤節點 | node: Object, depth: Number | click |

**狀態管理**：

| 類型 | 檔案 | 用途 |
| :--- | :--- | :--- |
| Store | stores/engines.js | 引擎、版本、追蹤 |
| Composable | composables/useEngineEditor.js | 編輯器邏輯 |

### 3.4 樣式規範

- **風格**：Emil Kowalski
- **動畫**：卡片過場 200ms
- **編輯器**：等寬字體
- **追蹤樹**：可展開 / 收合，節點顏色依狀態

### 3.5 響應式設計

| 裝置 | 佈局 |
| :--- | :--- |
| 電腦 | 左右佈局（版本列表 + 編輯器） |
| 平板 | 上下佈局 |
| 手機 | 單欄，分頁切換 |

---

## 4. 後端邏輯

### 4.1 API 端點

| 方法 | 路徑 | 說明 |
| :--- | :--- | :--- |
| GET | /api/v1/admin/engines | 引擎總覽 |
| GET | /api/v1/admin/engines/{type}/versions | 版本列表 |
| GET | /api/v1/admin/engines/{type}/versions/{id} | 版本詳情 |
| POST | /api/v1/admin/engines/{type}/versions | 新增版本 |
| PUT | /api/v1/admin/engines/{type}/versions/{id} | 更新版本 |
| POST | /api/v1/admin/engines/{type}/versions/{id}/test | 測試版本 |
| POST | /api/v1/admin/engines/{type}/versions/{id}/activate | 啟用 |
| POST | /api/v1/admin/engines/{type}/versions/{id}/archive | 封存 |
| DELETE | /api/v1/admin/engines/{type}/versions/{id} | 刪除草稿 |
| GET | /api/v1/admin/engines/traces | 追蹤列表 |
| GET | /api/v1/admin/engines/traces/{snapshot_id} | 追蹤樹 |
| POST | /api/v1/admin/engines/recompute | 建立重算任務 |
| GET | /api/v1/admin/engines/recompute/{job_id} | 查詢重算 |
| GET | /api/v1/admin/engines/recompute | 重算列表 |
| GET | /api/v1/admin/engines/llm-usage | LLM 使用統計 |

### 4.2 請求/回應範例

**POST /api/v1/admin/engines/llm/versions**：

請求：
```json
{
  "version": "v1.4",
  "config": {
    "model": "qwen2.5:7b",
    "temperature": 0.3,
    "max_tokens": 200,
    "system_prompt": "你是一位財務分析師...",
    "user_prompt_template": "市場情緒分數：{{ sentiment_score }}..."
  },
  "description": "優化市場情緒解讀語氣"
}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "version": "v1.4",
    "status": "draft"
  }
}
POST /api/v1/admin/engines/{type}/versions/{id}/activate：

回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "status": "active",
    "activated_at": "2026-09-22T10:00:00Z",
    "cache_invalidation_published": true
  }
}
POST /api/v1/admin/engines/recompute：

請求：

json
{
  "engine_type": "monte_carlo",
  "from_version_id": "uuid-v1.0.0",
  "to_version_id": "uuid-v1.1.0",
  "start_date": "2026-08-23",
  "end_date": "2026-09-22"
}
回應：

json
{
  "success": true,
  "data": {
    "job_id": "uuid",
    "status": "pending",
    "estimated_records": 30
  }
}
GET /api/v1/admin/engines/traces/{snapshot_id}：

回應：

json
{
  "success": true,
  "data": {
    "execution_snapshot_id": "uuid",
    "execution_date": "2026-09-22",
    "root": {
      "engine_type": "crawler",
      "step_name": "daily_crawl",
      "status": "success",
      "duration_ms": 3200,
      "children": [
        {
          "engine_type": "crawler",
          "step_name": "fetch_twse",
          "status": "success",
          "duration_ms": 320,
          "input_data": { "symbol": "0050" },
          "output_data": { "price": 155.20 }
        }
      ]
    }
  }
}
4.3 資料庫變更
使用表：

engine_versions

execution_snapshots

engine_traces

recompute_jobs

llm_usage_logs

engine_cache_invalidations

4.4 環境變數
變數	說明	預設
REDIS_PUBSUB_CHANNEL	快取失效頻道	engine_updated
CACHE_TTL_SECONDS	快取 TTL	300
RECOMPUTE_BATCH_SIZE	重算批次	100
5. 單元測試
5.1 後端測試（pytest）
python
# tests/unit/test_version_service.py
def test_create_version():
    result = service.create("llm", {
        "version": "v1.4",
        "config": {"model": "qwen2.5:7b"}
    })
    assert result["status"] == "draft"

def test_activate_version():
    v = service.create("llm", {"version": "v1.4", "config": {}})
    service.activate(v["id"])
    assert service.get(v["id"])["status"] == "active"

def test_only_one_active_per_engine():
    v1 = service.create("llm", {"version": "v1.3", "config": {}})
    v2 = service.create("llm", {"version": "v1.4", "config": {}})
    service.activate(v1["id"])
    service.activate(v2["id"])
    assert service.get(v1["id"])["status"] == "archived"
    assert service.get(v2["id"])["status"] == "active"

def test_cannot_edit_active():
    v = service.create("llm", {"version": "v1.4", "config": {}})
    service.activate(v["id"])
    with pytest.raises(EngineCannotEditActive):
        service.update(v["id"], {"config": {}})
python
# tests/unit/test_cache_pubsub.py
@patch("app.core.cache_pubsub.redis_client")
def test_publish_invalidation(mock_redis):
    cache_service.publish_invalidation("llm", "v1.4")
    mock_redis.publish.assert_called_once()
    args = mock_redis.publish.call_args
    assert args[0][0] == "engine_updated"
python
# tests/unit/test_trace_service.py
def test_trace_tree_structure():
    snapshot = create_test_snapshot()
    tree = trace_service.get_tree(snapshot["id"])
    assert tree["root"]["engine_type"] == "crawler"
    assert len(tree["root"]["children"]) > 0
5.2 前端測試（vitest）
javascript
// frontend/tests/EngineEditor.spec.js
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import EngineEditorView from '@/views/admin/EngineEditorView.vue'

describe('EngineEditorView', () => {
  it('submits version as draft', async () => {
    const wrapper = mount(EngineEditorView)
    await wrapper.find('[data-testid="submit-draft"]').trigger('click')
    expect(wrapper.emitted('submit')).toBeTruthy()
  })

  it('runs test with sample input', async () => {
    const wrapper = mount(EngineEditorView)
    await wrapper.find('[data-testid="run-test"]').trigger('click')
    await flushPromises()
    expect(wrapper.find('[data-testid="test-result"]').exists()).toBe(true)
  })

  it('shows validation error for invalid config', async () => {
    const wrapper = mount(EngineEditorView)
    await wrapper.find('[name="temperature"]').setValue(5.0)
    await wrapper.find('form').trigger('submit')
    expect(wrapper.text()).toContain('Temperature 必須介於 0 到 2 之間')
  })
})

describe('TraceTree', () => {
  it('expands node on click', async () => {
    const wrapper = mount(TraceTree, {
      props: { trace: mockTrace }
    })
    await wrapper.find('[data-testid="trace-node-root"]').trigger('click')
    expect(wrapper.findAll('[data-testid="trace-node"]').length).toBeGreaterThan(1)
  })
})
5.3 整合測試
python
# tests/integration/test_engine_versions.py
def test_full_version_lifecycle(auth_admin_client):
    # 1. 建立草稿
    response = auth_admin_client.post(
        "/api/v1/admin/engines/llm/versions",
        json={"version": "v1.4", "config": {...}}
    )
    version_id = response.json()["data"]["id"]
    
    # 2. 測試
    response = auth_admin_client.post(
        f"/api/v1/admin/engines/llm/versions/{version_id}/test",
        json={"test_input": {...}}
    )
    assert response.status_code == 200
    
    # 3. 啟用
    response = auth_admin_client.post(
        f"/api/v1/admin/engines/llm/versions/{version_id}/activate"
    )
    assert response.json()["data"]["status"] == "active"
    
    # 4. 驗證快取失效被發布
    assert response.json()["data"]["cache_invalidation_published"] is True
python
# tests/integration/test_recompute_flow.py
def test_recompute_job(auth_admin_client):
    response = auth_admin_client.post(
        "/api/v1/admin/engines/recompute",
        json={
            "engine_type": "monte_carlo",
            "from_version_id": "uuid-v1.0.0",
            "to_version_id": "uuid-v1.1.0",
            "start_date": "2026-08-23",
            "end_date": "2026-09-22"
        }
    )
    job_id = response.json()["data"]["job_id"]
    assert response.json()["data"]["status"] == "pending"
    
    # 等待完成
    time.sleep(2)
    response = auth_admin_client.get(f"/api/v1/admin/engines/recompute/{job_id}")
    assert response.json()["data"]["status"] in ["running", "completed"]
6. 驗收標準
□ 5 大引擎版本管理可用
□ 版本生命週期正確（draft → testing → active → archived）
□ 同一引擎同時只有一個 active
□ 執行快照正確記錄
□ 追蹤樹可視覺化
□ 重算任務可執行
□ Redis Pub/Sub 快取失效生效（延遲 < 1 秒）
□ 圖形化編輯器可即時測試
□ 響應式設計（3 裝置）
□ 權限控制正確（僅管理員）
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
類型	檔案	狀態
後端	admin_engines.py	✅
後端	version_service.py, snapshot_service.py	✅
後端	trace_service.py, recompute_service.py	✅
後端	cache_service.py, editor_service.py	✅
後端	llm_usage_service.py	✅
後端	cache_pubsub.py	✅
後端	engine.py (model), engine.py (schema)	✅
後端	recompute_worker.py	✅
前端	EnginesView, EngineDetailView, EngineEditorView	✅
前端	ExecutionTracesView, RecomputeJobsView	✅
前端	EngineOverviewCard, VersionList, VersionCard	✅
前端	VersionCompare, TraceTree, TraceNode	✅
前端	EditorPanel, TestRunner, SubmitPanel	✅
前端	RecomputeForm	✅
前端	engines.js (api), engines.js (store)	✅
前端	useEngineEditor.js	✅
測試	6 個測試檔	✅
8. 版本紀錄
版本	日期	變更
v1.0	2026-09-22	初版建立（v1.5 新增）
📄 文件 3：Phase 模板
版本：v1.5
適用範圍：所有 Phase 規劃書
最後更新：2026-09-22

模板使用說明
每個 Phase 獨立規劃書必須包含以下結構：

markdown
# Phase {N}：{名稱}

## ⚠️ 本 Phase 的 MVP/完整版約束

## 📂 前置檔案檢查（請提供以下檔案）
| 檔案路徑 | 來源 | 用途 |

## 📦 本 Phase 產出檔案
| 檔案路徑 | 動作 | 說明 |

## 1. 目標
## 2. 前置條件
## 3. 前端畫面
### 3.1 頁面清單
### 3.2 UI 草圖
### 3.3 Vue 元件結構
### 3.4 樣式規範
### 3.5 響應式設計
## 4. 後端邏輯
### 4.1 API 端點
### 4.2 請求/回應範例
### 4.3 資料庫變更
### 4.4 環境變數
## 5. 單元測試
### 5.1 後端測試（pytest）
### 5.2 前端測試（vitest）
### 5.3 整合測試
## 6. 驗收標準
## 7. 交付物清單
完整模板
markdown
# Phase {N}：{名稱}

**版本**：v1.0
**所屬**：MVP / 完整版
**依賴 Phase**：{前一個 Phase 編號}
**預計工時**：{天數}

---

## ⚠️ 本 Phase 的 MVP/完整版約束

- {約束 1}
- {約束 2}

---

## 📂 前置檔案檢查（請提供以下檔案）

| 檔案路徑 | 來源 | 用途 |
| :--- | :--- | :--- |
| docs/01-framework/01-shared-framework.md | 第一批 | 架構與設計原則 |
| docs/02-reference/01-database-schema.md | 第二批 | 表結構 |
| docs/02-reference/02-api-spec.md | 第二批 | API 定義 |
| docs/03-mvp/00-overview.md | 第三批 | Phase 總覽 |
| docs/03-mvp/phase-{N-1}.md | 第三批 | 前一個 Phase |

---

## 📦 本 Phase 產出檔案

| 檔案路徑 | 動作 | 說明 |
| :--- | :--- | :--- |
| backend/app/api/v1/{name}.py | 新增 | API 路由 |
| backend/app/services/{name}_service.py | 新增 | 商業邏輯 |
| backend/app/models/{name}.py | 新增 | ORM 模型 |
| backend/app/schemas/{name}.py | 新增 | Pydantic DTO |
| frontend/src/views/{Name}View.vue | 新增 | 頁面 |
| frontend/src/components/{Name}.vue | 新增 | 子元件 |
| frontend/src/api/{name}.js | 新增 | API 呼叫 |
| frontend/src/stores/{name}.js | 新增 | Pinia Store |
| frontend/src/composables/use{Name}.js | 新增 | Composable |
| backend/tests/unit/test_{name}.py | 新增 | 單元測試 |
| backend/tests/integration/test_{name}.py | 新增 | 整合測試 |
| frontend/tests/{name}.spec.js | 新增 | 前端測試 |

---

## 1. 目標

{本 Phase 要達成的具體目標}

---

## 2. 前置條件

- [ ] {前置條件 1}
- [ ] {前置條件 2}

---

## 3. 前端畫面

### 3.1 頁面清單

| 頁面 | 路由 | 說明 |
| :--- | :--- | :--- |
| {PageName} | /{path} | {說明} |

### 3.2 UI 草圖
┌─────────────────────────────────────┐
│ {頁面標題} │
├─────────────────────────────────────┤
│ {區塊 1} │
│ {區塊 2} │
└─────────────────────────────────────┘

text

### 3.3 Vue 元件結構
{PageName}View.vue（頁面層）
├── {ComponentA}.vue（區塊 A）
│ ├── BaseButton.vue（共用元件）
│ └── BaseInput.vue（共用元件）
├── {ComponentB}.vue（區塊 B）
│ └── BaseModal.vue（共用元件）
└── {ComponentC}.vue（區塊 C）

text

**元件職責**：

| 元件 | 職責 | Props | Emits |
| :--- | :--- | :--- | :--- |
| {PageName}View.vue | 頁面組裝、路由 | - | - |
| {ComponentA}.vue | {職責} | {props} | {emits} |

**狀態管理**：

| 類型 | 檔案 | 用途 |
| :--- | :--- | :--- |
| Store | stores/{name}.js | {跨頁面狀態} |
| Composable | composables/use{Name}.js | {無狀態邏輯} |

### 3.4 樣式規範

- **風格**：Emil Kowalski
- **動畫**：流暢過場（200-300ms）
- **互動**：懸停、點擊回饋
- **顏色**：參考 `styles/variables.css`

### 3.5 響應式設計

| 裝置 | 斷點 | 佈局 |
| :--- | :--- | :--- |
| 電腦 | ≥ 1024px | {佈局說明} |
| 平板 | 768px ~ 1023px | {佈局說明} |
| 手機 | < 768px | {佈局說明} |

---

## 4. 後端邏輯

### 4.1 API 端點

| 方法 | 路徑 | 說明 | 認證 |
| :--- | :--- | :--- | :--- |
| GET | /api/v1/{resource} | 列表 | ✅ |
| POST | /api/v1/{resource} | 新增 | ✅ |
| PUT | /api/v1/{resource}/{id} | 更新 | ✅ |
| DELETE | /api/v1/{resource}/{id} | 刪除 | ✅ |

### 4.2 請求/回應範例

**請求**：
```json
{
  "field1": "value1"
}
回應：

json
{
  "success": true,
  "data": {
    "id": 1,
    "field1": "value1"
  }
}
4.3 資料庫變更
表名	變更	說明
{table}	新增/修改	{說明}
4.4 環境變數
變數	說明	預設值
{VAR}	{說明}	{預設}
5. 單元測試
5.1 後端測試（pytest）
python
# tests/unit/test_{name}.py
def test_{function}_success():
    # Arrange
    # Act
    # Assert
    pass

def test_{function}_failure():
    pass
測試涵蓋：

成功情境

失敗情境

邊界情境

Fallback 情境

5.2 前端測試（vitest）
javascript
// tests/{name}.spec.js
import { describe, it, expect } from 'vitest'

describe('{Component}', () => {
  it('renders correctly', () => {
    expect(true).toBe(true)
  })
})
測試涵蓋：

元件渲染

使用者互動

狀態變化

5.3 整合測試
python
# tests/integration/test_{name}.py
def test_{name}_crud_integration():
    # POST → Service → DB
    response = client.post("/api/v1/{resource}", json={...})
    assert response.status_code == 201

    # GET → 驗證
    response = client.get("/api/v1/{resource}")
    assert len(response.json()["data"]) == 1
Critical Path 必過：

API → Service → DB

DB → Service → API

6. 驗收標準
□ 前端畫面可操作
□ 後端 API 端點正常
□ 單元測試全部通過（覆蓋率 ≥ 80%）
□ Critical Integration Test 通過
□ 資料庫變更已套用
□ 環境變數已設定
□ 健康檢查端點回應正常（若適用）
□ 異常情境已記錄至 incidents 表（若適用）
□ 管理員通知機制已驗證（若適用）
□ 響應式設計（電腦/平板/手機）已驗證
□ 權限控制正確（管理員 / 一般用戶 / tenant_id）
□ 模型上限正確（管理員 10 / 一般用戶 2）
□ 基因資料加密驗證（若適用）
□ 健康檔案完成度計算正確（若適用）
□ Coverage Ratio 計算正確（若適用）
□ 引擎版本管理驗證（若適用）（v1.5 新增）
□ Redis Pub/Sub 快取失效驗證（若適用）（v1.5 新增）
□ LLM Provider 路由正確（若適用）（v1.5 新增）
□ {自訂驗收項目}
7. 交付物清單
類型	檔案	狀態
後端	backend/app/api/v1/{name}.py	✅
後端	backend/app/services/{name}_service.py	✅
後端	backend/app/models/{name}.py	✅
後端	backend/app/schemas/{name}.py	✅
前端	frontend/src/views/{Name}View.vue	✅
前端	frontend/src/components/{Name}.vue	✅
前端	frontend/src/api/{name}.js	✅
前端	frontend/src/stores/{name}.js	✅
前端	frontend/src/composables/use{Name}.js	✅
測試	backend/tests/unit/test_{name}.py	✅
測試	backend/tests/integration/test_{name}.py	✅
測試	frontend/tests/{name}.spec.js	✅
文件	docs/03-mvp/phase-{N}.md	✅
版本紀錄
版本	日期	變更
v1.0	{日期}	初版建立
text

---

## 完整版 Phase 額外要求

完整版 Phase 必須額外包含：

```markdown
## 🔄 與 MVP 的差異

| 項目 | MVP | 完整版 |
| :--- | :--- | :--- |
| {項目} | {MVP 做法} | {完整版做法} |

## 🔗 依賴 MVP 哪個 Phase

- 依賴 MVP Phase {N}：{說明}

## 🆕 新增功能

- {新增功能 1}
- {新增功能 2}

## 💰 金流狀態

- 本 Phase 是否涉及金流：是 / 否
- 若涉及，金流開關狀態：開啟 / 關閉

## 🧬 健康檔案相關

- 本 Phase 是否涉及健康檔案：是 / 否
- 若涉及，涉及哪些欄位：{欄位}

## ⚙️ 引擎版本管理相關（v1.5 新增）

- 本 Phase 是否涉及引擎版本管理：是 / 否
- 若涉及，涉及哪些引擎：{crawler/normalizer/validator/matcher/monte_carlo/llm}
- 是否需要快取失效：是 / 否

## 🧠 LLM 相關（v1.5 新增）

- 本 Phase 是否涉及 LLM：是 / 否
- 若涉及，使用哪個 Provider：{template/groq/gemini/openai/ollama}
Phase 前端顆粒度要求
每個 Phase 的「3. 前端畫面」章節必須細化到：

頁面層級：完整 .vue 頁面檔案

元件層級：所有子元件

共用元件：引用哪些 Base*

Props / Emits：介面定義

狀態管理：store、composable

互動行為：懸停、點擊、動畫

響應式斷點：三裝置佈局

UI 草圖：ASCII 或文字

文件 3 結束
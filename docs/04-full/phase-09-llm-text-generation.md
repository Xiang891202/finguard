📄 更新文件 3：Full Phase 9 LLM Provider 抽象層 + 編輯器
版本：v2.0
所屬：完整版
依賴 Phase：

Full P5.5（引擎版本管理）

MVP P9（市場情緒數值化）

MVP P10（Email 模板）
預計工時：10 天（v1.4：6 天）

⚠️ 本 Phase 的完整版約束
LLM 為可選加值功能

依方案路由（免費版用模板）

整合 Full P5.5 的編輯器框架

🔗 依賴 MVP 哪個 Phase
依賴 MVP P9：市場情緒數值化（sentiment_score）

依賴 MVP P10：Email 模板已建立

依賴 Full P5.5：引擎版本管理系統

🔄 與 MVP 的差異
項目	MVP	完整版
文字生成	Jinja2 模板	Provider 抽象層
Provider	無	Template/Groq/Gemini/OpenAI/Ollama
用戶選擇	無	依方案路由
編輯器	無	圖形化編輯器（整合 P5.5）
成本追蹤	無	llm_usage_logs
🔄 與 v1.4 的差異
項目	v1.4	v1.5
LLM 定位	核心	可選加值
Provider 層級	無	5 層抽象
MVP 使用	✅	❌ MVP 用模板
編輯器	無	整合 P5.5
工時	6 天	10 天
📂 前置檔案檢查
檔案路徑	來源	用途
docs/01-framework/01-shared-framework.md	第一批	架構
docs/02-reference/01-database-schema.md	第二批	表結構
docs/02-reference/02-api-spec.md	第二批	API
docs/04-full/phase-05.5-engine-version.md	第四批	引擎版本管理
docs/03-mvp/phase-09-forecast.md	第三批	市場情緒
📦 本 Phase 產出檔案
後端
檔案路徑	動作	說明
backend/app/services/llm/base_provider.py	新增	抽象類
backend/app/services/llm/template_provider.py	新增	免費用戶
backend/app/services/llm/groq_provider.py	新增	專業版
backend/app/services/llm/gemini_provider.py	新增	專業+
backend/app/services/llm/openai_provider.py	新增	未來付費
backend/app/services/llm/ollama_provider.py	新增	管理員
backend/app/services/llm/provider_factory.py	新增	路由
backend/app/services/llm/prompt_builder.py	新增	Prompt 組裝
backend/app/api/v1/admin_llm.py	新增	LLM 管理 API
backend/app/api/v1/user_llm.py	新增	用戶偏好 API
backend/app/schemas/llm.py	新增	DTO
前端
檔案路徑	動作	說明
frontend/src/views/admin/LLMSettingsView.vue	新增	LLM 設定
frontend/src/views/admin/LLMEditorView.vue	新增	LLM 編輯器（整合 P5.5）
frontend/src/views/app/AccountLLMView.vue	新增	用戶 LLM 偏好
frontend/src/components/llm/ProviderCard.vue	新增	Provider 卡片
frontend/src/components/llm/ProviderConfigForm.vue	新增	Provider 設定
frontend/src/components/llm/RoutingTable.vue	新增	路由表
frontend/src/api/llm.js	新增	API
frontend/src/stores/llm.js	新增	Store
測試
檔案路徑	動作
backend/tests/unit/test_providers.py	新增
backend/tests/unit/test_provider_factory.py	新增
backend/tests/integration/test_llm_routing.py	新增
1. 目標
建立 5 層 LLM Provider 抽象層，依方案路由：

TemplateProvider（免費用戶）

GroqProvider（專業版）

GeminiProvider（專業+）

OpenAIProvider（未來付費）

OllamaProvider（管理員）

整合 Full P5.5 的編輯器框架，讓管理員可視覺化編輯 Prompt。

2. 前置條件
□ Full P5.5 完成
□ MVP P9, P10 完成
□ 至少一個付費 Provider API Key 已設定（Groq / Gemini）
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
LLMSettingsView	/admin/llm	LLM 設定
LLMEditorView	/admin/engines/llm/edit/:version	LLM 編輯器（P5.5）
AccountLLMView	/app/account/llm	用戶 LLM 偏好
3.2 UI 草圖
LLMSettingsView：

text
┌─────────────────────────────────────────────────────────────┐
│  🧠 LLM 設定                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【Provider 狀態】                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ✅ Template      (內建)  [測試]                     │   │
│  │ ✅ Groq          (已設定) [測試] [設定]              │   │
│  │ ✅ Gemini        (已設定) [測試] [設定]              │   │
│  │ ⚪ OpenAI        (未設定) [設定]                    │   │
│  │ ⚪ Ollama        (離線)  [測試] [設定]              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  【方案路由】                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 免費版    →  Template                               │   │
│  │ 專業版    →  Groq                                   │   │
│  │ 專業+     →  Gemini                                 │   │
│  │ 管理員    →  Ollama                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│  [編輯路由]                                                  │
│                                                             │
│  【成本統計】                                                │
│  本月使用：1,500 次 / 0 USD                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
AccountLLMView（用戶端）：

text
┌─────────────────────────────────────────────────────────────┐
│  🧠 LLM 偏好                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  目前方案：免費版                                            │
│  LLM Provider：Template（純模板）                           │
│                                                             │
│  升級專業版解鎖：                                            │
│  ✅ Groq 個人化解讀                                          │
│  ✅ 更自然的文字                                              │
│                                                             │
│  [升級專業版]                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
3.3 Vue 元件結構
text
LLMSettingsView.vue
├── ProviderList.vue
│   └── ProviderCard.vue
│       └── ProviderConfigForm.vue
├── RoutingTable.vue
└── UsageStats.vue

LLMEditorView.vue
└── （整合 Full P5.5 的 EditorPanel）

AccountLLMView.vue
├── PlanCard.vue
├── CurrentProvider.vue
└── UpgradeCTA.vue
元件職責：

元件	職責	Props	Emits
LLMSettingsView	頁面	-	-
ProviderCard	Provider 卡片	provider: Object	test, config
ProviderConfigForm	設定表單	provider: String	save
RoutingTable	路由表	routing: Object	edit
UsageStats	使用統計	stats: Object	-
AccountLLMView	用戶端	-	-
狀態管理：

類型	檔案	用途
Store	stores/llm.js	Provider、路由、統計
3.4 樣式規範
沿用 Full P5.5 編輯器風格。

3.5 響應式設計
裝置	佈局
電腦	雙欄
平板	單欄
手機	單欄
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/admin/llm/providers	Provider 列表
POST	/api/v1/admin/llm/providers/{provider}/test	測試連線
PUT	/api/v1/admin/llm/providers/{provider}/config	設定金鑰
GET	/api/v1/admin/llm/routing	查看路由
PUT	/api/v1/admin/llm/routing	修改路由
GET	/api/v1/admin/llm/usage	使用統計
GET	/api/v1/app/account/llm	用戶偏好
PUT	/api/v1/app/account/llm	更新偏好
4.2 請求/回應範例
POST /api/v1/admin/llm/providers/groq/test：

json
{
  "test_prompt": "請用一句話說明市場狀態"
}
回應：

json
{
  "success": true,
  "data": {
    "provider": "groq",
    "status": "healthy",
    "latency_ms": 420,
    "output": "目前市場波動程度相對提高。"
  }
}
PUT /api/v1/admin/llm/routing：

json
{
  "routing": {
    "free": "template",
    "pro": "groq",
    "pro_plus": "gemini",
    "admin": "ollama"
  }
}
4.3 資料庫變更
使用表：

users（llm_provider 欄位）

engine_versions（engine_type='llm'）

llm_usage_logs

engine_traces

無新增表。

4.4 環境變數
變數	說明
GROQ_API_KEY	Groq API Key
GEMINI_API_KEY	Gemini API Key
OPENAI_API_KEY	OpenAI API Key（未來）
OLLAMA_HOST	Ollama 主機（RunPod）
LLM_TIMEOUT_SECONDS	逾時（30）
5. 單元測試
5.1 後端測試
python
# tests/unit/test_providers.py
def test_template_provider_no_api_call():
    provider = TemplateProvider()
    result = provider.generate("市場情緒分數：62", {})
    assert result.text  # 模板文字
    assert result.cost_usd == 0
    assert result.tokens_input == 0

@patch("app.services.llm.groq_provider.groq_client")
def test_groq_provider(mock_groq):
    mock_groq.chat.completions.create.return_value = ...
    provider = GroqProvider()
    result = provider.generate("...", {})
    assert result.provider == "groq"

def test_provider_factory_free_user():
    user = MockUser(plan='free')
    provider = ProviderFactory().get_provider(user)
    assert isinstance(provider, TemplateProvider)

def test_provider_factory_pro_user():
    user = MockUser(plan='pro')
    provider = ProviderFactory().get_provider(user)
    assert isinstance(provider, GroqProvider)

def test_provider_factory_admin():
    user = MockUser(role='admin')
    provider = ProviderFactory().get_provider(user)
    assert isinstance(provider, OllamaProvider)

# tests/unit/test_provider_factory.py
def test_provider_offline_fallback():
    # 若 Groq 離線，降級為 Template
    with patch.object(GroqProvider, 'is_available', return_value=False):
        user = MockUser(plan='pro')
        provider = ProviderFactory().get_provider(user)
        assert isinstance(provider, TemplateProvider)
5.2 前端測試
javascript
describe('LLMSettingsView', () => {
  it('renders 5 providers', () => {
    const wrapper = mount(LLMSettingsView, {
      props: { providers: mockProviders }
    })
    expect(wrapper.findAll('[data-testid="provider-card"]').length).toBe(5)
  })

  it('shows routing table', () => {
    const wrapper = mount(LLMSettingsView)
    expect(wrapper.find('[data-testid="routing-table"]').exists()).toBe(true)
  })
})
5.3 整合測試
python
def test_llm_routing_by_plan(auth_client, admin_client, test_models):
    # 免費用戶 → template
    response = auth_client.get("/api/v1/app/account/llm")
    assert response.json()["data"]["provider"] == "template"
    
    # 管理員 → ollama
    response = admin_client.get("/api/v1/app/account/llm")
    assert response.json()["data"]["provider"] == "ollama"

def test_llm_usage_logged(auth_client):
    # 觸發一次 LLM 呼叫
    auth_client.post("/api/v1/app/forecast/run", json={...})
    
    # 驗證 llm_usage_logs 有記錄
    response = admin_client.get("/api/v1/admin/llm/usage")
    assert response.json()["data"]["total_requests"] > 0
6. 驗收標準
□ 5 個 Provider 實作完成
□ Provider 依方案路由
□ Provider 可切換（管理員 UI）
□ 成本追蹤正確
□ 整合引擎版本管理
□ 圖形化編輯器可用（整合 P5.5）
□ 快取失效生效
□ Provider 離線時降級為 Template
□ 用戶可查看自己使用的 Provider
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
類型	檔案	狀態
後端	base_provider.py + 5 個 Provider	✅
後端	provider_factory.py, prompt_builder.py	✅
後端	admin_llm.py, user_llm.py	✅
後端	llm.py (schema)	✅
前端	LLMSettingsView, LLMEditorView, AccountLLMView	✅
前端	ProviderCard, ProviderConfigForm, RoutingTable	✅
前端	llm.js (api), llm.js (store)	✅
測試	test_providers.py, test_provider_factory.py	✅
測試	test_llm_routing.py	✅
8. 版本紀錄
版本	日期	變更
v1.0	2026-09-20	初版（LLM 為核心）
v2.0	2026-09-22	改為 Provider 抽象層、整合 P5.5 編輯器、工時 6→10 天
文件結束
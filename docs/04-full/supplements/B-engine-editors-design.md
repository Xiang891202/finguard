📚 Full P5.5 補充文件包（三份完整文件）

📄 文件 B：6 種引擎編輯器設計
版本：v1.0
適用範圍：Full P5.5 引擎編輯器

B.0 共用架構
B.0.1 編輯器架構
所有編輯器遵循同一模式：

text
EngineEditorView.vue（頁面層）
├── EditorPanel.vue（分派器）
│   ├── CrawlerEditor.vue
│   ├── NormalizerEditor.vue
│   ├── ValidatorEditor.vue
│   ├── MatcherEditor.vue
│   ├── MonteCarloEditor.vue
│   └── LLMEditor.vue
├── TestRunner.vue（共用）
└── SubmitPanel.vue（共用）
B.0.2 共用 Props / Emits
所有 Editor 子元件都遵循：

Props：

Prop	型別	必填	說明
config	Object	✅	當前設定
disabled	Boolean	❌	是否唯讀
Emits：

事件	參數	說明
update:config	Object	設定變更
validate	Boolean	驗證結果
B.0.3 共用驗證機制
javascript
// composables/useEngineEditor.js

export function useEngineEditor(engineType) {
  const config = ref({})
  const errors = ref({})
  const isValid = computed(() => Object.keys(errors.value).length === 0)
  
  function validate() {
    errors.value = validators[engineType](config.value)
    emit('validate', isValid.value)
  }
  
  watch(config, validate, { deep: true })
  
  return { config, errors, isValid }
}
B.1 CrawlerEditor（爬蟲）
B.1.1 用途
編輯爬蟲引擎的來源設定（source_config）。

B.1.2 可編輯欄位
欄位	型別	說明
primary.provider	Select	twse / yfinance / cnyes / cbc
primary.endpoint	Input	API 網址
primary.params	KeyValue	動態參數
fallbacks	Array	備援來源清單
validation.tolerance_pct	Number	容忍值 %
validation.min_sources	Number	最少來源數
update_frequency	Select	daily / weekly
B.1.3 UI 草圖
text
┌─────────────────────────────────────────────────────────────┐
│  🕷️ 爬蟲引擎編輯器                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【主要來源】                                                │
│  Provider：[twse ▼]                                         │
│  Endpoint：[https://openapi.twse.com.tw/v1/...]              │
│  參數：                                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ symbol  [0050]                     [刪除]            │   │
│  │ [+ 新增參數]                                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  【備援來源】                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. yfinance  ticker: 0050.TW   [編輯] [刪除]        │   │
│  │ 2. cnyes     symbol: 0050      [編輯] [刪除]        │   │
│  └─────────────────────────────────────────────────────┘   │
│  [+ 新增備援來源]                                            │
│                                                             │
│  【驗證設定】                                                │
│  容忍值：   [0.5] %                                          │
│  最少來源數：[2]                                             │
│                                                             │
│  【更新頻率】                                                │
│  [daily ▼]                                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
B.1.4 Vue 元件結構
text
CrawlerEditor.vue
├── PrimarySourceForm.vue
│   ├── BaseSelect.vue（provider）
│   ├── BaseInput.vue（endpoint）
│   └── KeyValueEditor.vue（params）
├── FallbackSourceList.vue
│   └── FallbackSourceRow.vue
│       └── BaseInput.vue
├── ValidationConfigForm.vue
│   ├── BaseInput.vue（tolerance_pct）
│   └── BaseInput.vue（min_sources）
└── BaseSelect.vue（update_frequency）
B.1.5 驗證規則
欄位	規則
provider	必填
endpoint	必填、URL 格式
tolerance_pct	0 ~ 100
min_sources	≥ 1
update_frequency	必選
B.1.6 測試案例
javascript
describe('CrawlerEditor', () => {
  it('validates endpoint is URL', async () => {
    const wrapper = mount(CrawlerEditor)
    await wrapper.find('[name="endpoint"]').setValue('not-a-url')
    expect(wrapper.text()).toContain('請輸入有效的網址')
  })
  
  it('adds fallback source', async () => {
    const wrapper = mount(CrawlerEditor)
    await wrapper.find('[data-testid="add-fallback"]').trigger('click')
    expect(wrapper.findAll('[data-testid="fallback-row"]').length).toBe(2)
  })
})
B.2 NormalizerEditor（正規化）
B.2.1 用途
編輯正規化引擎的欄位映射規則。

B.2.2 可編輯欄位
欄位	型別	說明
rules	Array	正規化規則清單
rules[].source	Select	來源名稱
rules[].mappings	KeyValue	欄位映射
B.2.3 UI 草圖
text
┌─────────────────────────────────────────────────────────────┐
│  🧹 正規化引擎編輯器                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【正規化規則】                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. TWSE → 標準格式                                   │   │
│  │    欄位映射：                                        │   │
│  │      z → close                                       │   │
│  │      o → open                                        │   │
│  │      h → high                                        │   │
│  │      l → low                                         │   │
│  │    [編輯] [刪除]                                     │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ 2. yfinance → 標準格式                              │   │
│  │    [編輯] [刪除]                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│  [+ 新增規則]                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
B.2.4 Vue 元件結構
text
NormalizerEditor.vue
├── RuleList.vue
│   └── RuleCard.vue
│       ├── BaseSelect.vue（source）
│       └── MappingEditor.vue（欄位映射）
└── AddRuleButton.vue
B.2.5 驗證規則
欄位	規則
rules	至少 1 條
source	必填
mappings	至少 1 組
B.3 ValidatorEditor（驗證）
B.3.1 用途
編輯三源驗證的判定規則。

B.3.2 可編輯欄位
欄位	型別	說明
level1_threshold	Number	Level 1 容忍值 %
level2_min_sources	Number	Level 2 最少來源數
conflict_actions	Checkbox	衝突處理動作
B.3.3 UI 草圖
text
┌─────────────────────────────────────────────────────────────┐
│  ✅ 驗證引擎編輯器                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【Level 1 判定】                                            │
│  所有來源差異 ≤ [0.5] %                                      │
│                                                             │
│  【Level 2 判定】                                            │
│  至少 [2] 個來源差異 ≤ [0.5] %                               │
│                                                             │
│  【Level 3 判定】                                            │
│  A ≠ B ≠ C → 標記 DATA_CONFLICT                             │
│                                                             │
│  【衝突處理】                                                │
│  ☑ 觸發管理員通知                                            │
│  ☑ 標記 STALE                                                │
│  ☑ 使用前一日資料                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
B.3.4 Vue 元件結構
text
ValidatorEditor.vue
├── Level1Config.vue
│   └── BaseInput.vue（threshold）
├── Level2Config.vue
│   ├── BaseInput.vue（min_sources）
│   └── BaseInput.vue（threshold）
├── Level3Info.vue
└── ConflictActions.vue
    └── BaseCheckbox.vue（3 個）
B.3.5 驗證規則
欄位	規則
level1_threshold	0 ~ 100
level2_min_sources	≥ 2
conflict_actions	至少 1 項
B.4 MatcherEditor（比對）
B.4.1 用途
編輯用戶比對引擎的邏輯。

B.4.2 可編輯欄位
欄位	型別	說明
mode	Radio	user_only / all_assets
skip_unheld	Checkbox	跳過未持有
cache_results	Checkbox	快取結果
frequency	Select	daily / weekly
B.4.3 UI 草圖
text
┌─────────────────────────────────────────────────────────────┐
│  🎯 比對引擎編輯器                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【比對邏輯】                                                │
│  ● 只比對用戶持有的資產（預設）                              │
│  ○ 比對所有資產                                              │
│                                                             │
│  【最佳化選項】                                              │
│  ☑ 跳過未持有的資產類別                                      │
│  ☑ 快取已計算結果                                            │
│                                                             │
│  【比對頻率】                                                │
│  [daily ▼]                                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
B.4.4 Vue 元件結構
text
MatcherEditor.vue
├── ModeSelector.vue（Radio）
├── OptimizationOptions.vue（Checkbox x2）
└── BaseSelect.vue（frequency）
B.5 MonteCarloEditor（蒙地卡羅）
B.5.1 用途
編輯蒙地卡羅模型的參數。

B.5.2 可編輯欄位
欄位	型別	說明
model_version	Input	模型版本
simulation_count	Slider	模擬次數 1000 ~ 100000
random_seed	Input	隨機種子
horizon_months	Checkbox	3 / 6
volatility_source	Radio	30d / 60d / custom
convergence_check	Checkbox	收斂檢查
confidence_interval	Checkbox	信賴區間
B.5.3 UI 草圖
text
┌─────────────────────────────────────────────────────────────┐
│  🎲 蒙地卡羅引擎編輯器                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【模型參數】                                                │
│  模型版本：[v1.0.0]                                          │
│  模擬次數：[10000]  [━━━━●━━━━━]                            │
│  隨機種子：[42]                                              │
│  預測期間：☑ 3 個月  ☑ 6 個月                                │
│                                                             │
│  【波動率來源】                                              │
│  ○ 歷史波動率（30 天）                                       │
│  ● 歷史波動率（60 天）                                       │
│  ○ 自訂                                                      │
│                                                             │
│  【進階選項】                                                │
│  ☑ 收斂檢查                                                  │
│  ☑ 信賴區間計算                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
B.5.4 Vue 元件結構
text
MonteCarloEditor.vue
├── ModelParamsForm.vue
│   ├── BaseInput.vue（model_version）
│   ├── SimulationCountSlider.vue
│   ├── BaseInput.vue（random_seed）
│   └── HorizonCheckboxes.vue
├── VolatilitySourceSelector.vue（Radio x3）
└── AdvancedOptions.vue
    └── BaseCheckbox.vue（x2）
B.5.5 驗證規則
欄位	規則
model_version	必填、語意化版本格式
simulation_count	1000 ~ 100000
random_seed	整數
horizon_months	至少選 1 個
B.6 LLMEditor（LLM）
B.6.1 用途
編輯 LLM 引擎的 Prompt 與模型參數。

B.6.2 可編輯欄位
欄位	型別	說明
provider	Select	template / groq / gemini / openai / ollama
model	Select	依 provider 動態
temperature	Slider	0 ~ 2
max_tokens	Input	1 ~ 4000
system_prompt	Textarea	System Prompt
user_prompt_template	Textarea	User Prompt 模板
test_input	JSON	測試輸入
B.6.3 UI 草圖
text
┌─────────────────────────────────────────────────────────────┐
│  🧠 LLM 引擎編輯器                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【基本設定】                                                │
│  Provider：[ollama ▼]                                       │
│  模型：[qwen2.5:7b ▼]                                       │
│  Temperature：[0.3] [━━●━━━━━━]                             │
│  Max Tokens：[200]                                           │
│                                                             │
│  【System Prompt】                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 你是一位財務分析師，請根據以下數值，用繁體中文      │   │
│  │ 以客觀、中性的語氣解釋市場狀態。                    │   │
│  │                                                     │   │
│  │ 禁止：                                              │   │
│  │ - 提供投資建議                                      │   │
│  │ - 預測未來走勢                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  【User Prompt 模板】                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 市場情緒分數：{{ sentiment_score }}                 │   │
│  │ 市場狀態：{{ state }}                               │   │
│  │ 波動率：{{ volatility }}                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  【可用變數】                                                │
│  [sentiment_score] [state] [volatility] [drawdown]          │
│                                                             │
│  【測試輸入】                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ { "sentiment_score": 62, "state": "elevated" }      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
B.6.4 Vue 元件結構
text
LLMEditor.vue
├── ProviderSelector.vue
│   ├── BaseSelect.vue（provider）
│   └── BaseSelect.vue（model，動態）
├── ModelParamsForm.vue
│   ├── TemperatureSlider.vue
│   └── BaseInput.vue（max_tokens）
├── SystemPromptEditor.vue（Textarea）
├── UserPromptEditor.vue（Textarea）
├── VariableChips.vue（可用變數）
└── TestInputEditor.vue（JSON）
B.6.5 驗證規則
欄位	規則
provider	必填
model	若 provider 非 template，必填
temperature	0 ~ 2
max_tokens	1 ~ 4000
system_prompt	必填、≤ 2000 字
user_prompt_template	必填
user_prompt_template	變數必須在可用清單內
B.6.6 測試案例
javascript
describe('LLMEditor', () => {
  it('validates temperature range', async () => {
    const wrapper = mount(LLMEditor)
    await wrapper.find('[name="temperature"]').setValue(3.0)
    expect(wrapper.text()).toContain('Temperature 必須介於 0 到 2 之間')
  })
  
  it('shows model selector when provider is not template', async () => {
    const wrapper = mount(LLMEditor)
    await wrapper.find('[name="provider"]').setValue('ollama')
    expect(wrapper.find('[name="model"]').exists()).toBe(true)
  })
  
  it('validates prompt variables', async () => {
    const wrapper = mount(LLMEditor)
    await wrapper.find('[name="user_prompt_template"]')
      .setValue('{{ unknown_var }}')
    expect(wrapper.text()).toContain('未知變數：unknown_var')
  })
})
文件 B 結束
📄 更新文件 2：Phase 9 蒙地卡羅 + 風險計算（移除 LLM）
版本：v2.0
所屬：MVP
依賴 Phase：P7
預計工時：3 天（v1.4：5 天）

⚠️ 本 Phase 的 MVP/完整版約束（v1.5 更新）
MVP：3 個月與 6 個月預測

NumPy 純數學計算

不使用 LLM（v1.5）

市場情緒用規則式解讀（v1.5）

LLM 延後至 Full P9

🔄 與 v1.4 的差異
項目	v1.4	v1.5
LLM 整合	✅ 有	❌ 移除
市場情緒解讀	LLM 生成	規則式（if/elif）
Ollama 依賴	✅	❌ 移除
工時	5 天	3 天
📂 前置檔案檢查
檔案路徑	來源	用途
docs/01-framework/01-shared-framework.md	第一批	架構
docs/02-reference/01-database-schema.md	第二批	表結構
docs/02-reference/02-api-spec.md	第二批	API
docs/03-mvp/phase-07-crawler.md	第三批	爬蟲實作
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/forecast.py	新增	預測端點
backend/app/services/forecast/monte_carlo.py	新增	蒙地卡羅引擎
backend/app/services/forecast/risk_calculator.py	新增	風險計算
backend/app/services/forecast/sentiment_calculator.py	新增	市場情緒數值化
backend/app/services/forecast/sentiment_interpreter.py	新增（v1.5）	規則式解讀
backend/app/workers/forecast_worker.py	新增	Celery Worker
frontend/src/views/app/DashboardView.vue	修改	加入預測
frontend/src/components/dashboard/ForecastCard.vue	新增	預測卡片
frontend/src/components/charts/PieChart.vue	新增	圓餅圖
frontend/src/api/forecast.js	新增	API
frontend/src/stores/forecast.js	新增	Store
backend/tests/unit/test_monte_carlo.py	新增	測試
backend/tests/unit/test_sentiment_interpreter.py	新增（v1.5）	規則測試
backend/tests/integration/test_forecast_flow.py	新增	整合
移除檔案（v1.5）：

~~backend/app/services/llm/ollama_client.py~~

~~backend/app/services/llm/prompt_builder.py~~

1. 目標
建立蒙地卡羅模擬與風險計算系統。

v1.5 變更：市場情緒解讀改用規則式邏輯，不依賴 LLM。

2. 前置條件
□ P7 完成
□ NumPy 已安裝
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
DashboardView	/app/dashboard	加入預測區塊
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  📊 儀表板                           │
├─────────────────────────────────────┤
│  🔮 風險預測                         │
│                                     │
│  3 個月後：                          │
│  ├── 儲備金跌破安全線：14.5%         │
│  └── 破產機率：3.2%                  │
│                                     │
│  6 個月後：                          │
│  ├── 儲備金跌破安全線：23.1%         │
│  └── 破產機率：7.2%                  │
│                                     │
│  📈 市場情緒                         │
│  分數：62 / 100（elevated）          │
│  ⚠️ 目前市場波動程度相對提高。        │
│  （規則式解讀，非 LLM）              │
│                                     │
│  [ 重新預測 ]                        │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
DashboardView.vue
├── ForecastCard.vue
│   ├── PieChart.vue（儲備金）
│   └── LineChart.vue（走勢）
├── SentimentCard.vue
│   ├── SentimentScore.vue
│   └── SentimentExplanation.vue
└── BaseButton.vue
元件職責：

元件	職責	Props	Emits
DashboardView	頁面組裝	-	-
ForecastCard	預測卡片	forecast: Object	refresh
SentimentCard	市場情緒	score: Number, state: String, explanation: String	-
PieChart	圓餅圖	data: Array	-
LineChart	折線圖	data: Array	-
狀態管理：

類型	檔案	用途
Store	stores/forecast.js	預測結果、市場情緒
Composable	composables/useForecast.js	API 呼叫
3.4 樣式規範
圖表：Emil Kowalski 風格動畫

數字：等寬字體

情緒標示：三色（正常 / elevated / high）

3.5 響應式設計
裝置	佈局
電腦	雙欄（圖表 + 數字）
平板	單欄
手機	單欄全寬
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
POST	/api/v1/app/forecast/run	執行預測
GET	/api/v1/app/forecast/latest	查詢最新
4.2 請求/回應範例
POST /api/v1/app/forecast/run：

json
{
  "model_id": "uuid",
  "horizon_months": 6,
  "simulation_count": 10000
}
回應：

json
{
  "success": true,
  "data": {
    "run_id": "uuid",
    "model_version": "v1.0.0",
    "horizon_months": 6,
    "results": {
      "bankruptcy_probability": 0.072,
      "reserve_breach_probability": 0.145,
      "volatility_level": "elevated"
    },
    "sentiment": {
      "score": 62,
      "state": "elevated",
      "explanation": "目前市場波動程度相對提高。",
      "provider": "rule_based"
    },
    "generated_at": "2026-09-22T07:00:00Z"
  }
}
4.3 資料庫變更
使用表：forecast_runs, forecast_results, forecast_inputs

4.4 環境變數
變數	說明	預設值
SIMULATION_COUNT	預設模擬次數	10000
FORECAST_MODEL_VERSION	模型版本	v1.0.0
RANDOM_SEED	隨機種子	42
v1.5 移除：

~~OLLAMA_HOST~~

~~OLLAMA_MODEL~~

5. 單元測試
5.1 後端測試
python
# tests/unit/test_monte_carlo.py
def test_monte_carlo_deterministic():
    engine = MonteCarloEngine(seed=42)
    result = engine.run(
        initial_assets=1000000,
        monthly_expenses=50000,
        volatility=0.15,
        horizon_months=6,
        simulation_count=1000
    )
    assert 0 <= result["bankruptcy_probability"] <= 1
    assert 0 <= result["reserve_breach_probability"] <= 1

def test_monte_carlo_zero_volatility():
    engine = MonteCarloEngine(seed=42)
    result = engine.run(
        initial_assets=1000000,
        monthly_expenses=10000,
        volatility=0.0,
        horizon_months=6,
        simulation_count=1000
    )
    assert result["bankruptcy_probability"] == 0.0

# tests/unit/test_sentiment_interpreter.py（v1.5 新增）
def test_sentiment_high():
    result = interpret_sentiment(score=75)
    assert "明顯提高" in result

def test_sentiment_elevated():
    result = interpret_sentiment(score=62)
    assert "相對提高" in result

def test_sentiment_normal():
    result = interpret_sentiment(score=40)
    assert "中等" in result

def test_sentiment_low():
    result = interpret_sentiment(score=20)
    assert "相對平穩" in result
5.2 前端測試
javascript
describe('SentimentCard', () => {
  it('displays rule-based explanation', () => {
    const wrapper = mount(SentimentCard, {
      props: {
        score: 62,
        state: 'elevated',
        explanation: '目前市場波動程度相對提高。'
      }
    })
    expect(wrapper.text()).toContain('相對提高')
    expect(wrapper.text()).toContain('規則式解讀')
  })
})
5.3 整合測試
python
def test_forecast_flow(auth_client, test_model_with_holdings):
    response = auth_client.post("/api/v1/app/forecast/run", json={
        "model_id": test_model_with_holdings["id"],
        "horizon_months": 6,
        "simulation_count": 1000
    })
    assert response.status_code == 200
    data = response.json()["data"]
    assert "bankruptcy_probability" in data["results"]
    assert data["sentiment"]["provider"] == "rule_based"
6. 驗收標準（v1.5 更新）
□ 蒙地卡羅引擎實作
□ 3 個月與 6 個月預測
□ 破產機率計算正確
□ 儲備金跌破機率計算正確
□ 市場情緒數值化（sentiment_score）
□ 規則式解讀正確（v1.5）
□ 無 LLM 依賴（v1.5）
□ 圖表顯示正確
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
類型	檔案	狀態
後端	forecast.py	✅
後端	monte_carlo.py, risk_calculator.py	✅
後端	sentiment_calculator.py	✅
後端	sentiment_interpreter.py（v1.5）	✅
後端	forecast_worker.py	✅
前端	DashboardView, ForecastCard, SentimentCard	✅
前端	PieChart, LineChart	✅
測試	test_monte_carlo.py	✅
測試	test_sentiment_interpreter.py（v1.5）	✅
測試	test_forecast_flow.py	✅
8. 版本紀錄
版本	日期	變更
v1.0	2026-09-20	初版（含 LLM）
v2.0	2026-09-22	移除 LLM，改用規則式解讀，工時 5→3 天
文件結束
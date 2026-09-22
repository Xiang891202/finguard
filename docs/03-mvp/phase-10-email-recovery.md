📄 更新文件 3：Phase 10 Email 報告 + 自癒機制（改用模板）
版本：v2.0
所屬：MVP
依賴 Phase：P9
預計工時：4 天（v1.4：6 天）

⚠️ 本 Phase 的 MVP/完整版約束（v1.5 更新）
MVP：基礎自癒（Level 1）

Email 為 6 區塊合併

Email 文字用 Jinja2 模板生成（v1.5）

不使用 LLM（v1.5）

LLM 延後至 Full P9

🔄 與 v1.4 的差異
項目	v1.4	v1.5
文字生成	靜態模板 + LLM	純 Jinja2 模板
市場情緒	LLM 生成	規則式解讀
保險缺口說明	LLM 生成	模板生成
Ollama 依賴	✅	❌ 移除
工時	6 天	4 天
📂 前置檔案檢查
檔案路徑	來源	用途
docs/02-reference/01-database-schema.md	第二批	表結構
docs/03-mvp/phase-09-forecast.md	第三批	預測結果
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/email_preview.py	新增	Email 預覽
backend/app/api/v1/admin_system.py	新增	管理員系統
backend/app/api/v1/admin_incidents.py	新增	管理員異常
backend/app/services/email_service.py	新增	Email 發送
backend/app/services/email_builder.py	新增（v1.5）	模板組裝
backend/app/services/health_service.py	新增	健康檢查
backend/app/services/recovery_service.py	新增	自動修復
backend/app/services/incident_service.py	新增	異常記錄
backend/app/workers/email_worker.py	新增	Email Worker
backend/app/workers/recovery_worker.py	新增	修復 Worker
backend/app/templates/emails/daily_report.html	新增	主模板
backend/app/templates/emails/sections/financial.html	新增（v1.5）	金融區塊
backend/app/templates/emails/sections/market_sentiment.html	新增（v1.5）	情緒區塊
backend/app/templates/emails/sections/forecast.html	新增（v1.5）	預測區塊
backend/app/templates/emails/sections/insurance_gap.html	新增（v1.5）	保險區塊
backend/app/templates/emails/sections/comic.html	新增（v1.5）	漫畫區塊
backend/app/templates/emails/sections/disclaimer.html	新增（v1.5）	免責區塊
backend/app/templates/emails/admin_alert.html	新增	管理員警報
frontend/src/views/app/EmailPreviewView.vue	新增	Email 預覽
frontend/src/views/admin/AdminDashboardView.vue	新增	管理員儀表板
frontend/src/views/admin/IncidentsView.vue	新增	異常列表
frontend/src/api/emailPreview.js	新增	API
frontend/src/api/admin.js	新增	API
backend/tests/unit/test_email_service.py	新增	測試
backend/tests/unit/test_email_builder.py	新增（v1.5）	模板測試
backend/tests/unit/test_recovery_service.py	新增	測試
backend/tests/integration/test_email_flow.py	新增	整合
移除檔案（v1.5）：

~~backend/app/services/llm/text_generator.py~~

1. 目標
建立每日 Email 合併報告與基礎自癒機制。

v1.5 變更：Email 文字用 Jinja2 模板生成，不依賴 LLM。

2. 前置條件
□ P9 完成
□ SMTP 已設定
□ Jinja2 已安裝
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
EmailPreviewView	/app/email-preview	預覽 Email
AdminDashboardView	/admin/dashboard	系統狀態
IncidentsView	/admin/incidents	異常列表
3.2 UI 草圖
EmailPreviewView：

text
┌─────────────────────────────────────┐
│  📧 Email 預覽                       │
├─────────────────────────────────────┤
│  📊 你的每日財務安全報告              │
│                                     │
│  【區塊 1】金融水位                  │
│  儲備金：5 個月 / 目標 6 個月        │
│  淨值：1,200,000                     │
│                                     │
│  【區塊 2】市場情緒                  │
│  sentiment_score: 62 (elevated)     │
│  ⚠️ 目前市場波動程度相對提高。        │
│                                     │
│  【區塊 3】AI 風險預測               │
│  3 個月：14.5% / 6 個月：23.1%      │
│                                     │
│  【區塊 4】保險缺口                  │
│  🟢 2 | 🟡 3 | 🔴 3                  │
│                                     │
│  【區塊 5】漫畫                      │
│  [圖]                                │
│                                     │
│  【區塊 6】免責聲明                  │
│                                     │
│  [ 寄送測試 Email ]                  │
└─────────────────────────────────────┘
AdminDashboardView：

text
┌─────────────────────────────────────┐
│  🎛️ 系統儀表板                       │
├─────────────────────────────────────┤
│  健康狀態：                          │
│  🟢 資料庫 | 🟢 Redis | 🟡 API       │
│                                     │
│  佇列：crawl(0) forecast(0) email(2)│
│                                     │
│  今日異常：1 件                      │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
EmailPreviewView.vue
├── EmailSection.vue（6 個）
│   ├── FinancialSection.vue
│   ├── MarketSentimentSection.vue
│   ├── ForecastSection.vue
│   ├── InsuranceGapSection.vue
│   ├── ComicSection.vue
│   └── DisclaimerSection.vue
└── BaseButton.vue

AdminDashboardView.vue
├── HealthIndicator.vue
├── QueueStatus.vue
├── IncidentSummary.vue
└── ManualControls.vue

IncidentsView.vue
├── IncidentList.vue
│   └── IncidentRow.vue
└── IncidentDetail.vue
元件職責：

元件	職責	Props	Emits
EmailPreviewView	頁面組裝	-	-
EmailSection	通用區塊	title, content	-
MarketSentimentSection	情緒區塊	score, state, explanation	-
AdminDashboardView	管理員儀表板	-	-
HealthIndicator	健康燈號	services: Object	-
狀態管理：

類型	檔案	用途
Store	stores/emailPreview.js	Email 預覽
Store	stores/admin.js	系統狀態
3.4 樣式規範
Email 預覽：模擬 Email 版面

管理員：深色主題

3.5 響應式設計
裝置	佈局
電腦	雙欄
平板	單欄
手機	單欄
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/app/email-preview	Email 預覽
POST	/api/v1/app/email-preview/send-test	寄送測試
GET	/api/v1/admin/dashboard	系統狀態
GET	/api/v1/admin/users	用戶列表
GET	/api/v1/admin/incidents	異常列表
GET	/api/v1/admin/incidents/{id}	異常詳情
POST	/api/v1/admin/incidents/{id}/resolve	標記解決
4.2 請求/回應範例
GET /api/v1/app/email-preview：

json
{
  "success": true,
  "data": {
    "date": "2026-09-22",
    "sections": {
      "financial": {
        "reserve_months": 5,
        "target_months": 6,
        "net_worth": 1200000,
        "debt_ratio": 0.35
      },
      "market_sentiment": {
        "score": 62,
        "state": "elevated",
        "explanation": "目前市場波動程度相對提高。",
        "provider": "rule_based"
      },
      "forecast": {
        "3_months": {"bankruptcy": 0.032, "reserve_breach": 0.145},
        "6_months": {"bankruptcy": 0.072, "reserve_breach": 0.231}
      },
      "insurance_gap": {
        "green": 2, "yellow": 3, "red": 3
      },
      "comic": {"template": "default", "text": "..."},
      "disclaimer": "..."
    }
  }
}
4.3 資料庫變更
使用表：email_logs, incidents, audit_logs

4.4 環境變數
變數	說明
SMTP_HOST	SMTP 主機
SMTP_PORT	SMTP 埠
SMTP_USER	Gmail 帳號
SMTP_PASSWORD	Gmail 應用密碼
ADMIN_ALERT_EMAIL	管理員 Email
INCIDENT_RATE_LIMIT_HOUR	同服務限制（預設 1）
INCIDENT_RATE_LIMIT_DAILY	同類型限制（預設 3）
v1.5 移除：

~~OLLAMA_HOST~~

~~OLLAMA_MODEL~~

5. 單元測試
5.1 後端測試
python
# tests/unit/test_email_builder.py（v1.5 新增）
def test_build_all_sections():
    report = email_builder.build(user_id)
    assert "financial" in report["sections"]
    assert "market_sentiment" in report["sections"]
    assert "forecast" in report["sections"]
    assert "insurance_gap" in report["sections"]
    assert "comic" in report["sections"]
    assert "disclaimer" in report["sections"]

def test_sentiment_uses_rule_based():
    report = email_builder.build(user_id)
    assert report["sections"]["market_sentiment"]["provider"] == "rule_based"

def test_no_llm_dependency():
    # 驗證 email_builder 不匯入任何 LLM 模組
    import app.services.email_builder as eb
    source = inspect.getsource(eb)
    assert "ollama" not in source.lower()
    assert "llm" not in source.lower()

# tests/unit/test_email_service.py
def test_email_send_success(mock_smtp):
    result = email_service.send(user_id, report)
    assert result["status"] == "sent"

# tests/unit/test_recovery_service.py
def test_level_1_retry_success():
    with patch("app.services.recovery_service.retry_api", return_value=True):
        result = recovery_service.recover("api_timeout")
        assert result["success"] is True
        assert result["level"] == 1

def test_level_3_stops_and_notifies():
    with patch("app.services.recovery_service.send_admin_email") as mock_email:
        result = recovery_service.recover("data_corruption")
        assert result["level"] == 3
        assert mock_email.called
5.2 前端測試
javascript
describe('EmailPreviewView', () => {
  it('renders 6 sections', async () => {
    const wrapper = mount(EmailPreviewView, {
      props: { sections: mockSections }
    })
    expect(wrapper.findAll('[data-testid="email-section"]').length).toBe(6)
  })

  it('displays rule-based sentiment', async () => {
    const wrapper = mount(EmailPreviewView, {
      props: { 
        sections: { 
          market_sentiment: { 
            score: 62, 
            state: 'elevated', 
            explanation: '目前市場波動程度相對提高。',
            provider: 'rule_based'
          } 
        } 
      }
    })
    expect(wrapper.text()).toContain('相對提高')
  })
})
5.3 整合測試
python
def test_email_preview_integration(auth_client):
    response = auth_client.get("/api/v1/app/email-preview")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "sections" in data
    assert data["sections"]["market_sentiment"]["provider"] == "rule_based"
6. 驗收標準（v1.5 更新）
□ Email 6 區塊齊全
□ 保險缺口顯示 Coverage Ratio（非商品）
□ 市場情緒用規則式解讀（v1.5）
□ 無 LLM 依賴（v1.5）
□ 管理員可收到異常警報
□ Level 1 修復不通知
□ Level 2 記錄 Incident
□ Level 3 停止並通知
□ 通知頻率控制生效
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
類型	檔案	狀態
後端	email_preview.py, admin_system.py, admin_incidents.py	✅
後端	email_service.py	✅
後端	email_builder.py（v1.5）	✅
後端	health_service.py, recovery_service.py, incident_service.py	✅
後端	email_worker.py, recovery_worker.py	✅
模板	daily_report.html + 6 個 sections	✅
模板	admin_alert.html	✅
前端	EmailPreviewView, EmailSection 相關元件	✅
前端	AdminDashboardView, IncidentsView	✅
測試	test_email_service.py	✅
測試	test_email_builder.py（v1.5）	✅
測試	test_recovery_service.py	✅
測試	test_email_flow.py	✅
8. 版本紀錄
版本	日期	變更
v1.0	2026-09-20	初版（含 LLM）
v2.0	2026-09-22	改用 Jinja2 模板，移除 LLM，工時 6→4 天
文件結束
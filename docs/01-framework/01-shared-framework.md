📄 文件 1：共用框架規劃書
版本：v1.5
適用範圍：MVP 與完整版共用
最後更新：2026-09-22

1. 專案概述
1.1 專案定位
一套結合「理財模型」、「保險保障」與「健康風險」的個人財務風險管理系統。

短期目標：個人與家人使用（MVP）

長期目標：多租戶 SaaS（完整版）

設計原則：個人優先、商業就緒、免費優先、插件化、15 年長期運作

1.2 核心價值
價值	說明
風險可視化	將財務與保險風險轉為直覺的機率與水位狀態
資料可信	多源交叉比對，Level 1/2/3 驗證
插件化擴充	管理員動態新增資產與保單
版本可追溯（v1.5）	5 大引擎獨立版本、可還原、可重算
相容升級	MVP 與完整版採相容資料模型，降低升級重構成本
免費優先	自建 LLM、本地 Strix、開源工具
自癒能力	系統自動排查、自動修復、必要時通知管理員
精準保險	納入年齡、性別、家族病史、基因，精算覆蓋率
1.3 重要限制（System Output 邊界）
系統允許輸出（Allowed）：

✓ 歷史資料、當前資料

✓ 風險指標、機率

✓ 保障覆蓋狀態（Coverage Ratio）

✓ 儲備金水位

✓ 情境模擬

✓ 資料品質狀態

✓ 醫療費用參考區間

系統禁止輸出（Not Allowed）：

✗ 買進、賣出、持有建議

✗ 具體投資配置建議

✗ 具體保險商品推薦

✗ 具體業務員推薦

✗ 任何操作做法

✗ 「建議你提高保額」等結論性語句

核心原則：只呈現數據，不下結論。

1.4 十一大核心需求總覽
編號	需求	說明
1	理財模型：三源比對	TWSE、yfinance、鉅亨網 → Level 1/2/3
2	保險：雙源比對	Finfo、保險公司官網
3	技術分工	Node.js / Python / Java
4	多租戶架構	tenant_id + user_id，PostgreSQL
5	自建 LLM	Ollama + Llama / Qwen（完整版）
6	Emil Kowalski 風格	流暢動畫、細膩互動
7	本地 Strix	AI 模擬攻擊測試
8	Email + OTP 登入	用戶端無密碼
9	資料流程	爬蟲 → 比對 → 整理 → 用戶比對 → Email
10	健康檔案	生日、性別、家族病史、基因
11	精準保險預測	醫療開銷 × 覆蓋率
12	引擎版本管理（v1.5）	5 大引擎獨立版本、可還原、可重算
2. 系統架構
2.1 三層架構總覽
text
前端 (Vue 3 + Vite + Tailwind CSS)
    ↓
Node.js (API Gateway / BFF) ── MVP 階段省略
    ├── 用戶認證
    ├── JWT 頒發與驗證
    ├── Rate Limiting / CORS
    └── 請求路由與聚合
            ↓
Python FastAPI (核心業務服務)
    ├── 財務引擎
    ├── 爬蟲 (金融三源 + 保險雙源)
    ├── AI 預測 (蒙地卡羅)
    ├── 保險模組
    ├── 健康檔案模組
    ├── 醫療費用參考
    ├── 引擎版本管理（v1.5）
    ├── 自癒機制
    └── Email 派送
            ↓
Java Spring Boot (金流微服務)
    └── 訂閱、自動扣款、Stripe Webhook
2.2 MVP 簡化架構
text
前端 (Vue 3)
    ↓
Python FastAPI (單一後端)
    ├── 認證
    ├── 財務引擎
    ├── 爬蟲（3 個 Handler）
    ├── AI 預測（不含 LLM）
    ├── 保險模組
    ├── 健康檔案
    ├── 自癒機制
    └── Email 派送（模板生成）
    ↓
PostgreSQL (MVP 即用)
2.3 完整版架構
text
前端 (Vue 3)
    ↓
Node.js (API Gateway / BFF)
    ↓
    ┌───────┴───────┐
    ↓               ↓
Python FastAPI   Java Spring Boot
(核心業務)        (金流微服務)
    ↓               ↓
    └───────┬───────┘
            ↓
    Supabase (PostgreSQL)
            ↓
    LLM Provider 抽象層（v1.5）
    ├── TemplateProvider（免費用戶）
    ├── GroqProvider（專業版）
    ├── GeminiProvider（專業+）
    ├── OpenAIProvider（未來）
    └── OllamaProvider（管理員）
2.4 架構決策（嚴格遵守）
Node.js = API Gateway / BFF；Python FastAPI = 核心業務；Java = 金流微服務

source_config 支援多來源（primary + fallbacks）

每個 Handler 必須有獨立單元測試

Plugin 是功能模組層級，Handler 是資產類別層級

前端 composable 放無狀態邏輯，store 放跨頁面狀態

MVP 管理員後台僅唯讀清單，Full P2 才做 CRUD

保險模組使用獨立 BaseInsuranceHandler

金流 Java 模組獨立目錄

MVP 資料庫 = PostgreSQL

MVP 僅實作必要 Handler

市場情緒必須先數值化，LLM 僅負責文字解釋

資料刪除分級處理

基因資料加密處理

保險覆蓋率納入健康檔案

只呈現數據，不下結論

5 大引擎獨立版本管理（v1.5）

設定變更即時生效（Redis Pub/Sub）（v1.5）

LLM 免費為主，付費解鎖（v1.5）

3. 技術棧總覽
組件	選擇	說明
主框架	Node.js	API Gateway / BFF（完整版）
核心業務	Python FastAPI	財務、保險、爬蟲、AI、健康檔案
爬蟲	Python	金融三源 + 保險雙源 + 醫療費用
AI 預測	Python + NumPy	蒙地卡羅模擬
LLM Provider（v1.5）	5 層抽象	Template / Groq / Gemini / OpenAI / Ollama
金流	Java Spring Boot	訂閱與自動扣款（MVP 完全關閉）
前端	Vue 3 + Vite + Tailwind CSS	Emil Kowalski 風格
資料庫	PostgreSQL（MVP 與完整版一致）	MVP 為自架；完整版為 Supabase
快取 / Queue	Redis	Celery Broker
快取失效（v1.5）	Redis Pub/Sub	引擎設定即時生效
安全掃描	Strix（本地）	AI 模擬攻擊測試
登入（管理員）	Email + 密碼	bcrypt
登入（用戶）	Email + OTP	OTP 只存 hash
基因資料加密	Fernet / AES-256	-
GPU 推論（v1.5）	RunPod / Vast.ai（按需）	完整版 Ollama 部署
部署	Render（MVP）→ AWS / GCP（完整版）	免費優先
4. 角色與權限決策表
4.1 角色定義
角色	登入方式	可進入頁面	說明
管理員	Email + 密碼	/admin/* + /app/*	你本人
一般用戶	Email + OTP	僅 /app/*	家人 / 未來租戶
4.2 模型上限
階段	金流狀態	管理員	一般用戶
MVP	關閉	10	2
完整版	開啟（免費）	10	2
完整版	開啟（專業版）	10	4
完整版	開啟（專業版+擴充）	10	4 + 加購數
4.3 LLM Provider 對應方案（v1.5）
方案	價格	LLM Provider	說明
免費版	$0	TemplateProvider	純模板
專業版	NT$299/月	GroqProvider	免費 API
專業版+擴充	NT$398/月	GeminiProvider	更強模型
付費選項（未來）	TBD	OpenAIProvider	可切換
管理員	-	OllamaProvider	自建
4.4 金流 UI
階段	金流 UI
MVP	❌ 完全不出現
完整版	✅ 管理員後台可開關
4.5 Phase 數量（v1.5 更新）
版本	Phase 數量	金流	健康檔案	引擎管理
MVP	12（P0 ~ P11）	❌	✅	❌
完整版	20（P1 ~ P19 + P5.5）	✅ P18	✅	✅ P5.5
5. 資料庫架構原則
5.1 多租戶設計
租戶（Tenant）與用戶（User）是兩個不同概念：

text
tenant（租戶 = 一個家庭 / 一個組織）
  ├── user_1（家人 A）
  ├── user_2（家人 B）
  └── user_3（家人 C）
核心表必須同時具備：

欄位	用途
tenant_id	隔離不同租戶
user_id	標示資料擁有者
created_by	記錄建立者
5.2 資料庫選擇
階段	資料庫	說明
MVP	PostgreSQL（自架）	與完整版同一體系
完整版	Supabase（PostgreSQL）	託管服務
5.3 「零遷移成本」精確定義
MVP 與完整版採用相容的資料模型設計，降低升級時的 Schema 重構成本；完整版仍需執行資料庫遷移與資料搬遷程序。

✅ 零 Schema 重構

⚠️ 仍需資料遷移（資料搬遷、驗證、rollback）

5.4 表分類
分類	說明	MVP 寫入	完整版寫入
租戶表	tenants	✅	✅
核心表	用戶、管理員、模型、金庫、持有部位、負債	✅	✅
認證表	OTP、Refresh Token	✅	✅
健康檔案表	健康檔案、基因、醫療費用	✅	✅
保險表	保單、缺口、人體圖譜	✅（部分）	✅
預測表	Forecast 三表	✅	✅
插件表	資產類別、資產標的	✅（唯讀）	✅（CRUD）
引擎管理表（v1.5）	版本、快照、追蹤、重算	❌	✅
金流表	訂閱、付款紀錄	❌	✅
審計表	操作日誌、告警、incidents	✅	✅
5.5 表清單（36 張，v1.5 更新）
#	表名	分類	MVP	完整版
1	tenants	租戶	✅	✅
2	users	核心	✅	✅
3	admin_users	核心	✅	✅
4	otp_tokens	認證	✅	✅
5	refresh_tokens	認證	✅	✅
6	financial_models	核心	✅	✅
7	vaults	核心	✅	✅
8	holdings	核心	✅	✅
9	liabilities	核心	✅	✅
10	asset_classes	插件	✅（唯讀）	✅
11	asset_definitions	插件	✅（唯讀）	✅
12	market_prices	資料	✅	✅
13	market_snapshots	資料	✅	✅
14	forecast_runs	預測	✅	✅
15	forecast_results	預測	✅	✅
16	forecast_inputs	預測	✅	✅
17	insurance_policies	保險	✅	✅
18	insurance_products	保險	✅	✅
19	insurance_products_history	保險	✅	✅
20	body_part_mapping	保險	✅	✅
21	insurance_gap_snapshots	保險	✅	✅
22	email_logs	審計	✅	✅
23	incidents	審計	✅	✅
24	subscriptions	金流	❌	✅
25	audit_logs	審計	✅	✅
26	user_health_profiles	健康	✅	✅
27	genetic_markers	健康	✅	✅
28	user_genetic_tests	健康	✅	✅
29	medical_cost_references	健康	✅	✅
30	disease_risk_mapping	健康	✅	✅
31	engine_versions	引擎管理	❌	✅
32	execution_snapshots	引擎管理	❌	✅
33	engine_traces	引擎管理	❌	✅
34	recompute_jobs	引擎管理	❌	✅
35	llm_usage_logs	引擎管理	❌	✅
36	engine_cache_invalidations	引擎管理	❌	✅
5.6 market_prices 與 market_snapshots 職責定義
market_prices（最新 canonical 價格）：

symbol、price、currency、price_date、source_status、updated_at

用途：查詢「現在價格」

market_snapshots（某一天完整市場狀態）：

snapshot_date、symbol、OHLC、volume、source、validation_status

用途：Forecast 取歷史資料

5.7 forecast 三表
forecast_runs：每次預測的執行紀錄（model_version、input_snapshot_id）

forecast_results：預測結果（metric、value、confidence_interval）

forecast_inputs：預測輸入（snapshot_date、user_snapshot）

5.8 健康檔案相關表
user_health_profiles：生日、性別、家族病史、基因同意

genetic_markers：基因點位清單（管理員可擴充）

user_genetic_tests：用戶基因檢測結果（原始資料加密）

medical_cost_references：醫療費用參考

disease_risk_mapping：疾病風險映射

5.9 引擎管理相關表（v1.5 新增）
engine_versions：5 大引擎的版本管理

execution_snapshots：每次執行的版本組合

engine_traces：引擎追蹤樹

recompute_jobs：重算任務

llm_usage_logs：LLM 使用紀錄（成本追蹤）

engine_cache_invalidations：快取失效紀錄

5.10 資料保留與刪除政策
資料類型	處理方式
用戶財務資料	可刪除 / 匿名化
用戶保單資料	可刪除 / 匿名化
用戶健康檔案	可刪除
付款紀錄	保留（法定保存期限）
發票	保留（稅務法規）
審計日誌	保留
Incidents	保留
引擎版本 / 快照（v1.5）	保留（系統維運）
6. API 設計原則
6.1 版本控制
所有端點前綴 /api/v1/

6.2 路徑區隔
路徑前綴	角色	說明
/api/v1/auth/*	通用	用戶 OTP 認證
/api/v1/admin/auth/*	管理員	Email + 密碼
/api/v1/app/*	用戶端	財務、保險、儀表板
/api/v1/app/health/*	用戶端	健康檔案
/api/v1/admin/*	管理員	系統監控、資產管理
/api/v1/admin/engines/*（v1.5）	管理員	引擎版本管理
/api/v1/billing/*	金流	訂閱、付款（Full P18）
6.3 請求 / 回應格式
成功回應：

json
{
  "success": true,
  "data": { },
  "meta": { "page": 1, "total": 100 }
}
錯誤回應：

json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用戶不存在"
  }
}
6.4 錯誤碼規範
前綴	類別	範例
AUTH_	認證	AUTH_INVALID_OTP
USER_	用戶	USER_NOT_FOUND
MODEL_	模型	MODEL_LIMIT_EXCEEDED
CRAWL_	爬蟲	CRAWL_SOURCE_FAILED
FORECAST_	預測	FORECAST_INSUFFICIENT_DATA
INSURANCE_	保險	INSURANCE_POLICY_EXPIRED
HEALTH_	健康	HEALTH_CONSENT_REQUIRED
ENGINE_（v1.5）	引擎管理	ENGINE_VERSION_NOT_FOUND
BILLING_	金流	BILLING_PAYMENT_FAILED
SYSTEM_	系統	SYSTEM_SERVICE_UNAVAILABLE
INCIDENT_	異常	INCIDENT_RECOVERY_FAILED
6.5 認證機制
管理員：Email + 密碼（bcrypt）→ JWT
一般用戶：Email + OTP → JWT

Access Token：15 分鐘

Refresh Token：7 天

Refresh Token Rotation

Token Revoke（登出時撤銷）

OTP 只存 hash

6.6 OTP 防濫用機制
限制	值
OTP 有效期	5 分鐘
OTP 重試次數	3 次
同 Email 重發間隔	60 秒
同 Email 每日上限	10 次
同 IP 每分鐘上限	5 次
同 IP 每日上限	50 次
7. 插件化架構
7.1 三層抽象
text
AssetClass（資產類別）
    ↓ 綁定 handler_class
AssetDefinition（資產標的）
    ↓ 關聯
Holding（用戶持有部位）
7.2 Plugin 與 Handler 層級
text
Plugin Registry
  ├── Finance Plugin
  │     ├── EquityHandler（MVP）
  │     ├── ForexHandler（MVP）
  │     ├── MoneyMarketHandler（MVP）
  │     ├── BondHandler（Full）
  │     ├── MetalHandler（Full）
  │     └── CryptoHandler（Full）
  ├── Insurance Plugin
  │     ├── LifeInsuranceHandler（Full）
  │     └── PropertyInsuranceHandler（Full）
  └── Forecast Plugin
        └── MonteCarloEngine（MVP）
7.3 MVP Handler 範圍
Handler	用途
EquityHandler	股票
ForexHandler	外匯
MoneyMarketHandler	貨幣基金
7.4 Handler 策略模式
python
class BaseAssetHandler(ABC):
    def __init__(self, asset_definition: dict):
        self.asset = asset_definition
        self.source_config = asset_definition.get('source_config', {})

    @abstractmethod
    def fetch_price(self, date) -> float: pass

    @abstractmethod
    def calculate_volatility(self, lookback_days=30) -> float: pass

    def validate_price(self, price: float) -> bool:
        return price > 0

    def resolve_sources(self) -> list:
        sources = [self.source_config.get('primary')]
        sources.extend(self.source_config.get('fallbacks', []))
        return [s for s in sources if s]
7.5 source_config Schema
json
{
  "primary": {
    "provider": "twse",
    "endpoint": "https://...",
    "params": { "symbol": "0050" }
  },
  "fallbacks": [
    { "provider": "yfinance", "ticker": "0050.TW" },
    { "provider": "cnyes", "endpoint": "..." }
  ],
  "validation": {
    "tolerance_pct": 0.5,
    "min_sources": 2
  },
  "update_frequency": "daily"
}
8. 三源驗證機制
8.1 流程
text
Source A, B, C
    ↓
Normalization
    ↓
Validation（Level 1 / 2 / 3）
    ↓
Canonical Value
8.2 驗證分級
Level	情境	處理
Level 1	A ≈ B ≈ C	接受，取加權平均
Level 2	A ≈ B，C 異常	排除 C
Level 3	A ≠ B ≠ C	標記 DATA_CONFLICT
8.3 DATA_CONFLICT 處理
該資產當日不更新 canonical value

標記 source_status = CONFLICT

觸發管理員通知

Forecast 使用前一日資料，標記 STALE

8.4 各資料類型適用驗證
資料類型	適用驗證
股票收盤價	Level 1/2/3
匯率	Level 1/2/3
ETF NAV	Level 1/2/3
成交量	單源為主
股利 / 除權息	單源 + 人工覆核
9. 單一責任原則（SRP）
9.1 後端目錄結構
text
backend/
├── app/
│   ├── api/v1/
│   │   ├── auth.py
│   │   ├── admin_auth.py
│   │   ├── models.py
│   │   ├── vaults.py
│   │   ├── holdings.py
│   │   ├── liabilities.py
│   │   ├── crawler.py
│   │   ├── forecast.py
│   │   ├── insurance.py
│   │   ├── body_map.py
│   │   ├── health.py
│   │   ├── admin_system.py
│   │   ├── admin_assets.py
│   │   ├── admin_incidents.py
│   │   ├── admin_engines.py          # v1.5 新增
│   │   └── health_check.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── encryption.py
│   │   ├── cache_pubsub.py           # v1.5 新增
│   │   ├── events.py
│   │   ├── exceptions.py
│   │   ├── constants.py
│   │   └── logging.py
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── migrations/
│   ├── models/
│   │   ├── tenant.py
│   │   ├── user.py
│   │   ├── admin_user.py
│   │   ├── otp_token.py
│   │   ├── refresh_token.py
│   │   ├── financial_model.py
│   │   ├── vault.py
│   │   ├── holding.py
│   │   ├── liability.py
│   │   ├── asset.py
│   │   ├── forecast.py
│   │   ├── insurance.py
│   │   ├── body_part.py
│   │   ├── health_profile.py
│   │   ├── genetic_marker.py
│   │   ├── medical_cost.py
│   │   ├── engine.py                 # v1.5 新增
│   │   └── incident.py
│   ├── schemas/
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── admin_auth_service.py
│   │   ├── model_service.py
│   │   ├── vault_service.py
│   │   ├── holding_service.py
│   │   ├── liability_service.py
│   │   ├── crawler/
│   │   ├── forecast/
│   │   ├── insurance/
│   │   ├── health/
│   │   ├── llm/                      # v1.5 新增
│   │   │   ├── base_provider.py
│   │   │   ├── template_provider.py
│   │   │   ├── groq_provider.py
│   │   │   ├── gemini_provider.py
│   │   │   ├── openai_provider.py
│   │   │   ├── ollama_provider.py
│   │   │   └── provider_factory.py
│   │   ├── engine/                   # v1.5 新增
│   │   │   ├── version_service.py
│   │   │   ├── snapshot_service.py
│   │   │   ├── trace_service.py
│   │   │   ├── recompute_service.py
│   │   │   ├── cache_service.py
│   │   │   └── editor_service.py
│   │   ├── health_service.py
│   │   ├── recovery_service.py
│   │   ├── incident_service.py
│   │   ├── data_retention_service.py
│   │   └── email_service.py
│   ├── handlers/
│   │   ├── base_handler.py
│   │   ├── equity_handler.py
│   │   ├── forex_handler.py
│   │   └── money_market_handler.py
│   ├── workers/
│   │   ├── crawl_worker.py
│   │   ├── forecast_worker.py
│   │   ├── email_worker.py
│   │   ├── recovery_worker.py
│   │   ├── recompute_worker.py       # v1.5 新增
│   │   └── cleanup_worker.py
│   ├── plugins/
│   ├── utils/
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── alembic/
├── requirements.txt
└── Dockerfile
9.2 前端目錄結構
text
frontend/
├── src/
│   ├── api/
│   │   ├── client.js
│   │   ├── auth.js
│   │   ├── adminAuth.js
│   │   ├── models.js
│   │   ├── vaults.js
│   │   ├── holdings.js
│   │   ├── liabilities.js
│   │   ├── crawler.js
│   │   ├── forecast.js
│   │   ├── insurance.js
│   │   ├── bodyMap.js
│   │   ├── health.js
│   │   ├── engines.js                # v1.5 新增
│   │   └── admin.js
│   ├── components/
│   │   ├── common/
│   │   ├── charts/
│   │   ├── body-map/
│   │   ├── health/
│   │   └── engine/                   # v1.5 新增
│   │       ├── VersionList.vue
│   │       ├── VersionCompare.vue
│   │       ├── TraceTree.vue
│   │       ├── EditorPanel.vue
│   │       └── TestRunner.vue
│   ├── views/
│   │   ├── admin/
│   │   │   ├── AdminLoginView.vue
│   │   │   ├── AdminDashboardView.vue
│   │   │   ├── AssetClassesView.vue
│   │   │   ├── AssetDefinitionsView.vue
│   │   │   ├── UsersView.vue
│   │   │   ├── IncidentsView.vue
│   │   │   ├── EnginesView.vue       # v1.5 新增
│   │   │   ├── EngineDetailView.vue  # v1.5 新增
│   │   │   ├── EngineEditorView.vue  # v1.5 新增
│   │   │   ├── ExecutionTracesView.vue # v1.5 新增
│   │   │   ├── RecomputeJobsView.vue # v1.5 新增
│   │   │   ├── BillingView.vue
│   │   │   └── SettingsView.vue
│   │   └── app/
│   │       ├── LoginView.vue
│   │       ├── DashboardView.vue
│   │       ├── ModelsView.vue
│   │       ├── VaultsView.vue
│   │       ├── HoldingsView.vue
│   │       ├── LiabilitiesView.vue
│   │       ├── InsuranceView.vue
│   │       ├── BodyMapView.vue
│   │       ├── EmailPreviewView.vue
│   │       ├── AccountView.vue
│   │       └── HealthProfileView.vue
│   ├── composables/
│   │   ├── useAuth.js
│   │   ├── useModels.js
│   │   ├── useVaults.js
│   │   ├── useForecast.js
│   │   ├── useBodyMap.js
│   │   ├── useHealthProfile.js
│   │   └── useEngineEditor.js        # v1.5 新增
│   ├── stores/
│   │   ├── auth.js
│   │   ├── adminAuth.js
│   │   ├── models.js
│   │   ├── vaults.js
│   │   ├── health.js
│   │   ├── engines.js                # v1.5 新增
│   │   └── ui.js
│   ├── router/
│   ├── styles/
│   ├── utils/
│   └── App.vue
├── tests/
├── package.json
└── vite.config.js
9.3 金流 Java 模組目錄結構
text
billing-service/
├── src/main/java/com/example/billing/
│   ├── controller/
│   ├── service/
│   ├── repository/
│   ├── model/
│   ├── dto/
│   ├── config/
│   └── BillingApplication.java
├── src/main/resources/
│   ├── application.yml
│   └── templates/
├── src/test/java/com/example/billing/
├── pom.xml
└── Dockerfile
9.4 SRP 實作規範
層級	責任	禁止事項
API 層	接收請求、呼叫 Service、回傳回應	❌ 不寫商業邏輯
Service 層	商業邏輯、資料處理	❌ 不直接寫 SQL
Model 層	定義表結構、關聯	❌ 不寫商業邏輯
Handler 層	特定資產類型的爬取與計算	❌ 不處理用戶資料
Worker 層	非同步任務調度	❌ 不寫商業邏輯
Util 層	無狀態工具函數	❌ 不依賴資料庫
9.5 共用邏輯抽離清單
共用邏輯	抽離位置
JWT 產生與驗證	core/security.py
密碼哈希	core/security.py
基因資料加密	core/encryption.py
Redis Pub/Sub（v1.5）	core/cache_pubsub.py
金錢精度處理	utils/decimal_utils.py
日期處理	utils/date_utils.py
錯誤回應格式	core/exceptions.py
分頁邏輯	services/base_service.py
資產驗證	handlers/base_handler.py
資料庫 Session	db/session.py
API 回應格式	schemas/base.py
日誌記錄	core/logging.py
健康檢查	services/health_service.py
異常記錄	services/incident_service.py
9.6 前端 composable 與 store 邊界
類型	用途	範例
Composable	無狀態、可重用邏輯	useApi()、useForm()、useBodyMapInteraction()、useEngineEditor()
Store (Pinia)	跨頁面共享狀態	authStore、modelStore、enginesStore、uiStore
判斷準則：

邏輯需被多個元件使用，且不涉及共享狀態 → composable

狀態需跨頁面保留 → store

禁止在 composable 中直接修改 store

10. 安全性設計
10.1 認證與授權
管理員：Email + 密碼（bcrypt）→ JWT

一般用戶：Email + OTP → JWT

JWT Token（Access + Refresh）

Refresh Token Rotation

Token Revoke 機制

Rate Limiting（每 IP 每分鐘 60 次）

CORS 白名單

10.2 資料隔離
所有查詢強制帶 tenant_id + user_id 條件

Service 層統一注入

禁止跨租戶查詢

管理員端與用戶端 JWT 不相容

10.3 基因資料特殊處理
法律依據：

台灣《個人資料保護法》第 6 條（特種個資）

GDPR Art. 9

處理原則：

項目	做法
同意	獨立同意書
存儲	原始點位加密
查詢	僅查計算後風險等級
刪除	用戶絕對刪除權
稽核	每次存取記錄
加密	Fernet / AES-256
10.4 本地 Strix 模擬攻擊
使用本地 Strix 進行 AI 模擬攻擊測試

由本地 Ollama 驅動

測試範圍：SQL Injection、XSS、CSRF、越權存取

每次部署前自動執行

10.5 敏感資料處理
OTP 有效期：5 分鐘，只存 hash

JWT Secret 存放環境變數

管理員密碼 bcrypt（cost = 12）

金流相關資料加密

基因原始資料加密

11. AI 與計算引擎分離
11.1 分離原則
組件	責任	技術
蒙地卡羅模擬	純數學計算	NumPy
市場情緒計算	規則 + 數值指標	NumPy
保險覆蓋率計算	規則 + 精算表	NumPy
LLM	僅文字解釋	Provider 抽象層
11.2 市場情緒流程
text
市場資料
    ↓
規則 / 數值指標
    ↓
Market Sentiment Score（0-100）
    ↓
sentiment_state = "normal" / "elevated" / "high"
    ↓
LLM（若啟用）僅負責文字解釋
LLM 只能說：「目前市場波動程度相對提高……」
LLM 不能說：「市場很危險。」

11.3 資料流
text
數值計算 (NumPy) → 結構化結果 → LLM 解讀 → 文字輸出
LLM 僅接收計算後的結構化結果

LLM 不參與任何數值運算

LLM 輸出不影響計算結果

12. Email 設計
12.1 每日合併發送
一封 Email 包含六個區塊：

text
┌─────────────────────────────────────────────────────────────┐
│  📊 你的每日財務安全報告 (YYYY-MM-DD)                       │
├─────────────────────────────────────────────────────────────┤
│  區塊 1：金融水位                                            │
│  區塊 2：市場情緒（sentiment_score + 解釋）                  │
│  區塊 3：AI 風險預測（3 個月 / 6 個月）                      │
│  區塊 4：保險缺口（Coverage Ratio）                          │
│  區塊 5：漫畫（4-6 格）                                     │
│  區塊 6：免責聲明                                            │
└─────────────────────────────────────────────────────────────┘
12.2 Email 服務
階段	服務
MVP	SMTP（Gmail），每日上限 500 封
完整版	AWS SES
12.3 文字生成策略（v1.5 更新）
階段	策略
MVP	Jinja2 模板（規則式解讀）
完整版（免費）	TemplateProvider
完整版（專業）	GroqProvider
完整版（專業+）	GeminiProvider
完整版（管理員）	OllamaProvider
12.4 停發規則
用戶進入寬限期時，Email 停止發送

12.5 保險區塊詳細規則
顯示：

保障類型、缺口程度、現有保障 vs 需求基準

Coverage Ratio

醫療費用參考區間

不顯示：

具體商品名稱、保險公司名稱、推薦原因

行動呼籲：「如有需要，請洽詢你的保險業務員進行詳細討論。」

13. 保險模組設計
13.1 人體剖面圖
左右半身：左為外觀，右為內部

SVG 繪製：支援無限縮放

動態渲染：由 body_part_mapping.ui_config 驅動

管理員擴充：新增身體部位時，僅需後台新增資料

13.2 三色狀態規則
顏色	狀態	Coverage Ratio
🟢 綠色	完全覆蓋	≥ 100%
🟡 黃色	部分覆蓋	50% ~ <100%
🔴 紅色	嚴重缺口	< 50%
13.3 Coverage Ratio 精準化計算
基礎公式：

text
Coverage Ratio = 實際保障 / 精準需求基準
精準需求基準計算：

text
需求基準 = 基礎醫療費用
         × 年齡風險乘數
         × 性別風險乘數
         × 家族病史乘數
         × 基因風險乘數
13.4 健康檔案的資料來源
資料	來源	必填
西元生日	用戶輸入	✅
性別	用戶輸入	✅
家族病史	用戶輸入	選填
基因檢測	用戶輸入	選填
13.5 基因點位清單（MVP 預設 8 個）
基因	關聯疾病
BRCA1 / BRCA2	乳癌、卵巢癌
APOE	阿茲海默症
LDLR	家族性高膽固醇
TP53	多種癌症
HFE	血色素沉著症
MTHFR	血栓、葉酸代謝
ALDH2	酒精代謝、食道癌
HLA-B*1502	藥物過敏
13.6 醫療費用參考
MVP：人工 Seed（8 疾病）

完整版：衛福部爬蟲（100+ 疾病）

13.7 互動行為
行為	效果
點擊部位	該部位高亮，其餘變暗
點擊部位後	右側面板更新
再次點擊	取消選取
懸停	邊框變粗
13.8 響應式設計
裝置	佈局
電腦（≥ 1024px）	左右佈局
平板（768-1023px）	上下佈局
手機（< 768px）	上下佈局，面板底部彈窗
13.9 人體部位清單（預設）
部位代碼	部位名稱	分類
brain	大腦 / 神經	internal
heart	心臟 / 心血管	internal
eyes	雙眼 / 視力	external
limbs	四肢 / 骨骼	external
liver	肝臟 / 消化	internal
lungs	肺 / 呼吸	internal
skin	皮膚 / 外觀	external
reproductive	生殖系統	internal
14. 健康檔案模組
14.1 會員中心流程
text
新用戶 Email 登入
    ↓
強制導向會員中心 /app/account/health
    ↓
填寫健康檔案
├── 西元生日（必填）
├── 性別（必填）
├── 家族病史（選填）
└── 基因檢測（選填）
    ↓
儲存
    ↓
進入儀表板
舊用戶：

導覽列新增「會員中心 → 健康檔案」入口

儀表板顯示「完成度」提示

14.2 API 端點
方法	路徑	說明
GET	/api/v1/app/health/profile	查詢健康檔案
POST	/api/v1/app/health/profile	新增
PUT	/api/v1/app/health/profile	更新
POST	/api/v1/app/health/consent	基因同意
GET	/api/v1/app/health/genetic-markers	基因點位清單
GET	/api/v1/app/health/genetic-tests	基因檢測結果
POST	/api/v1/app/health/genetic-tests	新增檢測
DELETE	/api/v1/app/health/genetic-tests/{id}	刪除檢測
GET	/api/v1/app/health/completion	完成度
14.3 完成度計算
欄位	權重
西元生日	40%
性別	40%
家族病史	10%
基因檢測	10%
15. 資料流程
text
定時爬蟲（MVP：手動觸發）
    ↓
Normalization
    ↓
Validation（Level 1/2/3）
    ↓
Canonical Value
    ↓
比對用戶（只比對用戶「有的」資產）
    ↓
Forecast（使用 forecast_inputs 記錄）
    ↓
保險覆蓋率計算（納入健康檔案）
    ↓
發送 Email（模板或 LLM）
15.1 資源優化原則
用戶有股票但沒有債券 → 只比對股票

用戶有心血管保單但無家族病史 → 仍計算（精準度較低）

15.2 資料更新頻率
資料類型	頻率
金融市場資料	每日一次
保險商品目錄	每週一次
保險缺口分析	每日執行
醫療費用參考	每年（MVP 人工）
Email 發送	每日合併
15.3 STALE 資料處理
text
canonical_value = 昨日價格
value_date = 昨日
data_status = STALE
    ↓
Forecast 知道資料過期
    ↓
降低可信度 / 停止該資產預測
明確原則：不使用過期資料偽裝為當日資料。

16. 管理員與用戶端區隔
16.1 兩種登入方式
角色	登入方式	路徑前綴
管理員	Email + 密碼	/admin/*
一般用戶	Email + OTP	/app/*
16.2 頁面區隔
頁面類型	路徑前綴	功能範圍
管理員後台	/admin/*	系統監控、資產管理、用戶管理、金流開關、引擎管理
用戶端	/app/*	財務模型、保險、健康檔案、儀表板
16.3 管理員頁面清單（v1.5 更新）
頁面	路徑	功能	MVP
管理員登入	/admin/login	Email + 密碼	✅
系統儀表板	/admin/dashboard	系統健康	✅
資產類別管理	/admin/asset-classes	CRUD（唯讀 in MVP）	✅（唯讀）
資產標的管理	/admin/asset-definitions	CRUD（唯讀 in MVP）	✅（唯讀）
用戶管理	/admin/users	用戶清單	✅
異常事件	/admin/incidents	歷史異常	✅
基因點位管理	/admin/genetic-markers	新增/編輯	✅
醫療費用管理	/admin/medical-costs	新增/編輯	✅
引擎管理中心（v1.5）	/admin/engines	5 引擎版本管理	❌
引擎編輯器（v1.5）	/admin/engines/:type/edit	圖形化編輯	❌
追蹤樹（v1.5）	/admin/traces	執行追蹤	❌
重算任務（v1.5）	/admin/recompute	重算管理	❌
金流開關	/admin/billing	開啟/關閉金流	❌
系統設定	/admin/settings	Feature Flags	❌
16.4 用戶端頁面清單
頁面	路徑	功能
用戶登入	/login	Email + OTP
儀表板	/app/dashboard	財務水位、保險缺口、AI 預測
財務模型	/app/models	模型、金庫、持有部位、負債
保險模組	/app/insurance	保單管理、人體剖面圖
Email 預覽	/app/email-preview	預覽當日報告
會員中心	/app/account	帳號設定
健康檔案	/app/account/health	生日、性別、家族病史、基因
17. 自癒機制
17.1 核心流程
text
問題發生
    ↓
自動排查
    ↓
自動修復
    ↓
修復成功？
├── 是 → 記錄日誌，不通知管理員
└── 否 → 發送管理員 Email
17.2 自動排查項目
排查項目	檢查內容
環境檢查	資料庫、Redis、外部 API
程式碼檢查	最近部署版本、錯誤日誌
業務檢查	用戶資料完整性、異常值
17.3 自動修復動作
問題類型	自動修復動作	通知管理員
API 逾時	重試 3 次	失敗才通知
資料庫連線失敗	重新建立連線池	失敗才通知
Redis 連線失敗	重啟 Redis 客戶端	失敗才通知
爬蟲資料異常	使用昨日資料（標記 STALE）	通知
Worker 當機	自動重啟 Worker	失敗才通知
前端渲染錯誤	顯示錯誤提示	失敗才通知
資料不一致	觸發重新計算	通知
17.4 修復分級
級別	適用範圍	系統行為	通知管理員
Level 1	無副作用	自動修復	❌
Level 2	可能資料變更	重試 + 降級	⚠️ 記錄 Incident
Level 3	可能資料損壞	停止 + 發送 Email	✅ 立即通知
17.5 incidents 表
sql
CREATE TABLE incidents (
    id CHAR(36) PRIMARY KEY,
    incident_number VARCHAR(20) NOT NULL UNIQUE,
    service_name VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    trigger_event VARCHAR(50) NOT NULL,
    diagnosis_report TEXT,
    possible_causes JSONB,
    auto_recovery_attempted BOOLEAN DEFAULT FALSE,
    auto_recovery_success BOOLEAN DEFAULT FALSE,
    recovery_action_taken VARCHAR(100),
    recovery_error TEXT,
    engineer_email_sent BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'open',
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);
17.6 管理員通知 Email 結構
主旨：🚨 [系統異常] {service_name} - {severity} - {incident_number}

內容區塊：異常摘要、自動排查結果、可能原因分析、自動修復嘗試、建議下一步

17.7 通知頻率控制
情境	頻率限制
同一服務連續異常	1 小時內最多 1 次
同一類型異常	24 小時內最多 3 次
Critical 異常	立即通知
18. 金流完整規格（MVP 完全關閉）
18.1 金流開關行為
開關狀態	系統行為
關閉（預設）	無「升級」按鈕；管理員 10 模型、一般用戶 2 模型；不扣款
開啟	顯示「升級」按鈕；免費用戶 2 模型；試用期 30 天
18.2 金流完整流程
text
[點擊「升級」] → [付款頁面] → [Stripe 處理]
    ↓
[付款成功 → 發送 Email → 訂閱生效]
    ↓
[每月自動扣款]
    ↓
[連續 3 次失敗 → 唯讀寬限期 30 天]
    ↓
[寬限期結束 → 資料分級處理]
18.3 金流規則總表
規則	內容
試用期	30 天，全功能，2 模型
專業版	NT$299/月，4 模型
專業版+擴充	NT$99/月，+2 模型（可至 8）
自動扣款	用戶需勾選
扣款失敗	3 次重試，間隔 24 小時
寬限期	30 天
退款政策	7 天內全額退款
18.4 金流 Email 模板清單
#	模板名稱	觸發時機
1	付款成功	首次付款
2	扣款成功	每月扣款
3-5	扣款失敗（1-3 次）	失敗時
6	進入寬限期	第 3 次失敗後
7	寬限期倒數	第 27 天
8	資料清除通知	寬限期結束
9	手動續訂通知	管理員延長
10	退款確認	退款完成
18.5 服務條款與合約
文件	位置
服務條款	/terms
隱私政策	/privacy
退款政策	/refund-policy
訂閱條款	/subscription-terms
基因資料同意書	/genetic-consent
18.6 發票與收據
項目	處理方式
發票開立	付款成功後自動開立
發票寄送	隨 Email 附 PDF
發票查詢	會員中心
統一編號	可於付款時填寫
18.7 金流相關 API
方法	路徑
POST	/api/v1/billing/checkout
POST	/api/v1/billing/webhook
GET	/api/v1/billing/subscription
GET	/api/v1/billing/invoices
POST	/api/v1/billing/cancel
POST	/api/v1/billing/refund
18.8 金流與 MVP 的關係
階段	金流狀態
MVP	完全關閉，UI 不出現
完整版	管理員可開關
19. MVP 部署限制
19.1 Render 免費方案限制
服務	限制	建議
Web Service	15 分鐘無請求會休眠	UptimeRobot 喚醒
PostgreSQL	90 天限制	定期備份
Redis	需外部服務	Upstash
Background Worker	需付費	MVP 改用同步
SMTP	Gmail 每日 500 封	足夠 MVP
19.2 MVP 部署建議
服務	選擇
主應用	Render Web Service
資料庫	Render PostgreSQL 或 Neon
Redis	Upstash
Celery Worker	MVP 不啟用自動排程
Email	Gmail SMTP
LLM（v1.5）	不使用（模板生成）
19.3 不可依賴的項目
❌ Ephemeral disk

❌ 本地檔案系統持久化

❌ In-memory 快取

19.4 必須外部持久化
✅ 資料庫（PostgreSQL）

✅ Redis（Upstash）

✅ 檔案儲存（S3 / R2）

✅ Email 記錄（DB）

20. 預設決策表
項目	決策
目標用戶規模	MVP：1-5 人；完整版：100-1000 租戶
資料庫	PostgreSQL（MVP 與完整版一致）
金融資料更新頻率	每日一次
保險商品目錄更新頻率	每週一次
保險缺口分析頻率	每日執行
醫療費用更新頻率	MVP：每年人工 / 完整版：爬蟲
Email 服務	MVP：SMTP（Gmail）；完整版：AWS SES
備用金定義	現金儲備＋緊急預備金，以「月數」為單位
風險指標	儲備金跌破安全線機率、破產風險機率、市場波動水位
漫畫風格	靜態模板＋文字（完整版可選 LLM）
管理員範圍	MVP：唯讀清單；完整版：CRUD＋金流開關
管理員登入	Email + 密碼（bcrypt）
用戶登入	Email + OTP（只存 hash）
自癒機制	Level 1 自動、Level 2 重試降級、Level 3 停止並通知
部署環境	MVP：Render 免費；完整版：AWS / GCP
測試標準	Unit ≥ 80%、Critical Integration 必過、E2E 延後
管理員模型上限	10
一般用戶模型上限（MVP）	2
一般用戶模型上限（完整版免費）	2
一般用戶模型上限（完整版專業）	4
付費擴充	+2 模型 NT$99/月
三源驗證	Level 1/2/3，衝突標記 DATA_CONFLICT
保險覆蓋	Coverage Ratio（含健康檔案）
商品推薦	不顯示具體商品，只顯示保障類型缺口
資料刪除	分級處理
MVP Handler	僅 Equity / Forex / MoneyMarket
健康檔案必填	生日、性別
健康檔案選填	家族病史、基因檢測
基因資料處理	加密存儲、獨立同意、可刪除
基因點位數量	MVP 預設 8 個，管理員可擴充
醫療費用來源	MVP：人工 Seed；完整版：爬蟲
MVP LLM（v1.5）	不使用（模板生成）
完整版 LLM（v1.5）	Provider 抽象層
免費版 LLM（v1.5）	TemplateProvider
專業版 LLM（v1.5）	GroqProvider
專業+ LLM（v1.5）	GeminiProvider
管理員 LLM（v1.5）	OllamaProvider（RunPod 按需）
引擎版本管理（v1.5）	5 引擎獨立版本
快取失效（v1.5）	Redis Pub/Sub（< 1 秒）
21. MVP 與完整版關係
21.1 共用基礎
同一套資料庫（PostgreSQL）

同一套 Schema（36 張表）

同一套 API 規格

同一套目錄結構

同一套插件化架構

同一套自癒框架

同一套健康檔案架構

21.2 MVP 範圍
項目	內容
Phase 數量	12（P0～P11）
資料庫	PostgreSQL（自架）
爬蟲觸發	手動
Handler	3 個
Email 服務	SMTP（Gmail）
Email 生成	Jinja2 模板（v1.5）
LLM（v1.5）	❌ 不使用
管理員後台	登入、儀表板、資產唯讀、用戶清單、異常事件、基因點位、醫療費用
自癒機制	基礎
金流	完全關閉
模型上限	管理員 10、一般用戶 2
健康檔案	✅
醫療費用	人工 Seed
部署	Render 免費
21.3 完整版範圍
項目	內容
Phase 數量	20（P1~P19 + P5.5）
資料庫	Supabase（PostgreSQL）
爬蟲觸發	自動排程
Handler	6 個
Email 服務	AWS SES
Email 生成	Provider 抽象層
LLM（v1.5）	5 層 Provider
管理員後台	完整 + 引擎管理
自癒機制	完整三級
金流	管理員開關
模型上限	管理員 10、免費 2、專業 4、擴充
引擎版本管理（v1.5）	✅ 5 引擎
快取失效（v1.5）	Redis Pub/Sub
部署	AWS / GCP
21.4 升級路徑
text
MVP Phase 0-11（PostgreSQL）
    ↓
完整版 Phase 1-19 + P5.5（Supabase PostgreSQL）
    ↓
仍需執行：資料搬遷、驗證、rollback
    ↓
零 Schema 重構 ≠ 零資料遷移
21.5 MVP Phase 清單（12 個）
Phase	名稱
P0	基礎建設
P1	用戶認證 + 會員中心健康檔案
P2	財務模型 + 金庫
P3	持有部位（EquityHandler）
P4	負債
P5	外匯（ForexHandler）
P6	貨幣基金（MoneyMarketHandler）
P7	爬蟲調度 + 三源驗證
P8	保險保單 CRUD
P9	蒙地卡羅 + 風險計算（無 LLM）
P10	Email 報告 + 自癒機制（模板生成）
P11	醫療費用 + 覆蓋率精算
21.6 完整版 Phase 清單（20 個）
Phase	名稱
P1	多租戶架構
P2	資產類別 + 標的管理（CRUD）
P3	更多 Handler（Bond / Metal / Crypto）
P4	自動排程爬蟲
P5	人體剖面圖
P5.5	引擎版本管理系統（新增）
P6	保險商品爬蟲
P7	保險缺口分析
P8	保險保單擴充子分類
P9	LLM Provider 抽象層 + 編輯器
P10	漫畫生成
P11	保險缺口精算
P12	Report Aggregator
P13	多語言支援
P14	效能優化
P15	指揮中心
P16	資料匯出 / 匯入
P17	API 開放
P18	金流模組
P19	醫療費用爬蟲
22. 引擎版本管理系統（v1.5 新增）
22.1 設計理念
「如果無法追蹤版本、無法還原、無法重算，那歷史資料就只是死的數字。」

FinGuard 的五大引擎各自有獨立的版本維度，每次執行都記錄「當下用了哪些版本」。

22.2 五大引擎的版本維度
引擎	版本維度	版本範例
爬蟲引擎	腳本版本 + 來源配置	crawler-v1.2 + source-twse-v3
資料整理引擎	驗證規則 + 正規化	validator-v1.1 + normalizer-v1.0
用戶比對引擎	比對邏輯	matcher-v1.0
蒙地卡羅引擎	模型 + 參數	mc-v1.0.0 + params-2026Q3
LLM 引擎	Prompt + 模型 + 參數	prompt-v1.3 + qwen2.5:7b + temp-0.3
22.3 核心機制
機制 1：版本快照（Snapshot）
每次每日任務執行時，記錄當下的版本組合，所有當天產出的資料都掛上 execution_snapshot_id。

機制 2：可還原（Rollback）
任一引擎可切回舊版本：

版本列表顯示：使用中 / 測試中 / 已封存

一鍵切換：下次任務即使用新版本

切換不需重新部署應用

機制 3：可重算（Recompute）
換版本後可選擇重算範圍：

只算未來（預設）

重算最近 N 天

全歷史重算

重算時舊資料標記為「已棄用」，保留對照。

22.4 版本生命週期
text
草稿（draft） → 測試版（testing） → 啟用中（active） → 已封存（archived）
22.5 圖形化編輯器
每個引擎一個編輯器，支援：

視覺化編輯設定（Prompt / 參數 / 規則）

本地測試（用測試 API 立即看結果）

提交為測試版

管理員確認後啟用

22.6 快取失效機制
問題：應用層快取會擋住「改了馬上生效」。

解法：Redis Pub/Sub 通知所有服務清快取。

text
管理員改設定
    ↓
寫入 PostgreSQL / Supabase
    ↓
發布 Redis Pub/Sub：engine_updated
    ↓
所有服務清本地快取
    ↓
下次請求自動載入新版本（延遲 < 1 秒）
降級機制：

Redis 不可用 → 退回 TTL（最長 5 分鐘延遲）

Supabase Realtime 可用 → 額外訂閱作為備援

22.7 設定變更 vs 程式碼變更
變更類型	範例	儲存位置	生效方式
設定變更（80%）	Prompt、參數、容忍值	資料庫	即時生效（< 1 秒）
程式碼變更（20%）	新增 Handler、邏輯修改	Git 倉庫	Git push → 重新部署
23. LLM 部署策略（v1.5 新增）
23.1 五層 LLM Provider 抽象層
text
應用層（FastAPI）
    ↓
LLM Provider 抽象層（策略模式）
├── TemplateProvider    ← 免費用戶預設（純模板，零成本）
├── GroqProvider        ← 專業版（免費 API）
├── GeminiProvider      ← 專業+（免費 API）
├── OpenAIProvider      ← 未來付費選項
└── OllamaProvider      ← 管理員 / 自建
23.2 方案與 LLM 對應表
方案	價格	LLM Provider
免費版	$0	TemplateProvider
專業版	NT$299/月	GroqProvider
專業版+擴充	NT$398/月	GeminiProvider
付費選項（未來）	TBD	OpenAIProvider
管理員	-	OllamaProvider
23.3 為什麼 MVP 不用 LLM？
原因	說明
80% 的內容可用模板	金融水位、風險數字、免責聲明
成本	即使免費 API 也有 rate limit
延遲	850ms vs 模板 < 10ms
幻覺	需要嚴格限制
MVP 簡單	零 GPU、零 API Key、零成本
23.4 LLM 真正加值的地方
區塊	模板	LLM
金融水位	✅	❌
市場情緒分數	✅	❌
市場情緒深度解讀	⚠️	✅
風險數字	✅	❌
保險缺口數字	✅	❌
保險缺口個人化說明	⚠️	✅
漫畫文字	✅	⚠️
免責聲明	✅	❌
23.5 部署架構
text
MVP 階段
├── Render Web Service
├── PostgreSQL（自架）
├── Redis（Upstash）
└── LLM：TemplateProvider（零成本）

完整版階段
├── Render / AWS / GCP
├── Supabase（PostgreSQL）
├── Redis（Upstash）
├── LLM Provider 依方案路由
└── Ollama 部署於 GPU 平台（RunPod / Vast.ai）
    └── 按需啟動（每日 1-2 小時）
23.6 LLM 使用成本追蹤
sql
CREATE TABLE llm_usage_logs (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) REFERENCES users(id),
    provider VARCHAR(30) NOT NULL,
    tokens_input INT,
    tokens_output INT,
    cost_usd NUMERIC(10, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
23.7 用戶 LLM 偏好
sql
ALTER TABLE users ADD COLUMN llm_provider VARCHAR(30) DEFAULT 'template';
24. 版本紀錄
版本	日期	變更
v1.0	2026-09-20	初版
v1.1	2026-09-20	新增管理員區隔、自癒機制
v1.2	2026-09-20	新增角色權限、金流規格
v1.3	2026-09-20	修正零遷移、PostgreSQL、Level 1/2/3、Coverage Ratio、資料刪除分級、tenant_id
v1.4	2026-09-21	新增健康檔案模組、基因資料處理、醫療費用參考、精準保險覆蓋率
v1.5	2026-09-22	新增引擎版本管理、LLM Provider 抽象層、Redis Pub/Sub 快取失效、MVP 移除 LLM
文件 1 結束
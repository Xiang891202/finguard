📄 文件 6：API 與 Phase 對應表
版本：v1.5
適用範圍：MVP 12 個 Phase、完整版 20 個 Phase

1. MVP Phase 與 API 對應
Phase 0：基礎建設
方法	路徑	說明
GET	/health	健康檢查
GET	/health/ready	就緒檢查
GET	/health/live	存活檢查
資料庫：建立所有 36 張表（空表）

Phase 1：用戶認證 + 會員中心健康檔案
方法	路徑	說明
POST	/auth/otp/request	請求 OTP
POST	/auth/otp/verify	驗證 OTP
POST	/auth/refresh	刷新 Token
POST	/auth/logout	登出
POST	/admin/auth/login	管理員登入
POST	/admin/auth/logout	管理員登出
GET	/app/health/profile	查詢健康檔案
POST	/app/health/profile	新增
PUT	/app/health/profile	更新
POST	/app/health/consent	基因同意
GET	/app/health/genetic-markers	基因點位清單
GET	/app/health/genetic-tests	基因檢測結果
POST	/app/health/genetic-tests	新增檢測
DELETE	/app/health/genetic-tests/{id}	刪除檢測
GET	/app/health/completion	完成度
資料表：tenants, users, admin_users, otp_tokens, refresh_tokens, user_health_profiles, genetic_markers, user_genetic_tests

Phase 2：財務模型 + 金庫
方法	路徑
GET	/app/models
POST	/app/models
PUT	/app/models/{id}
DELETE	/app/models/{id}
GET	/app/vaults
POST	/app/vaults
PUT	/app/vaults/{id}
DELETE	/app/vaults/{id}
資料表：financial_models, vaults

Phase 3：持有部位（EquityHandler）
方法	路徑
GET	/app/holdings
POST	/app/holdings
PUT	/app/holdings/{id}
DELETE	/app/holdings/{id}
資料表：holdings, asset_classes, asset_definitions

Handler：EquityHandler

Phase 4：負債
方法	路徑
GET	/app/liabilities
POST	/app/liabilities
PUT	/app/liabilities/{id}
DELETE	/app/liabilities/{id}
資料表：liabilities

Phase 5：外匯（ForexHandler）
（沿用 Phase 3）

Handler：ForexHandler

Phase 6：貨幣基金（MoneyMarketHandler）
（沿用 Phase 3）

Handler：MoneyMarketHandler

Phase 7：爬蟲調度 + 三源驗證
方法	路徑
POST	/app/crawler/trigger
GET	/app/crawler/status/{task_id}
資料表：market_prices, market_snapshots

Service：CrawlerDispatcher, Normalizer, Validator, DataCleaner

Phase 8：保險保單 CRUD
方法	路徑
GET	/app/insurance/policies
POST	/app/insurance/policies
PUT	/app/insurance/policies/{id}
DELETE	/app/insurance/policies/{id}
GET	/app/insurance/body-map
資料表：insurance_policies, body_part_mapping

Phase 9：蒙地卡羅 + 風險計算（無 LLM）
方法	路徑
POST	/app/forecast/run
GET	/app/forecast/latest
資料表：forecast_runs, forecast_results, forecast_inputs

Service：MonteCarloEngine, RiskCalculator, SentimentCalculator

⚠️ v1.5 變更：移除 LLM 相關邏輯，市場情緒用規則式解讀

Phase 10：Email 報告 + 自癒機制（模板生成）
方法	路徑
GET	/app/email-preview
GET	/admin/dashboard
GET	/admin/users
GET	/admin/incidents
GET	/admin/incidents/{id}
POST	/admin/incidents/{id}/resolve
資料表：email_logs, incidents, audit_logs

Service：EmailService, HealthService, RecoveryService, IncidentService

⚠️ v1.5 變更：Email 用 Jinja2 模板生成

Phase 11：醫療費用 + 保險覆蓋率精算
方法	路徑
GET	/app/insurance/gap
GET	/admin/genetic-markers
POST	/admin/genetic-markers
GET	/admin/medical-costs
POST	/admin/medical-costs
資料表：medical_cost_references, disease_risk_mapping, insurance_gap_snapshots

Service：CoverageCalculator, MedicalCostService

2. 完整版 Phase 與 API 對應
Full P1：多租戶架構
GET /admin/tenants

POST /admin/tenants

PUT /admin/tenants/{id}

DELETE /admin/tenants/{id}

POST /tenants/register

GET /tenants/me

Full P2：資產類別 + 標的管理（CRUD）
POST /admin/asset-classes

PUT /admin/asset-classes/{id}

DELETE /admin/asset-classes/{id}

POST /admin/asset-definitions

PUT /admin/asset-definitions/{id}

DELETE /admin/asset-definitions/{id}

Full P3：更多 Handler
BondHandler, MetalHandler, CryptoHandler

Full P4：自動排程爬蟲
GET /admin/schedules

PUT /admin/schedules/{name}

POST /admin/schedules/{name}/trigger

Full P5：人體剖面圖
擴充 /app/insurance/body-map（SVG 互動）

Full P5.5：引擎版本管理系統（v1.5 新增）
API 端點（全部新增）：

方法	路徑	說明
GET	/admin/engines	引擎總覽
GET	/admin/engines/{type}/versions	版本列表
GET	/admin/engines/{type}/versions/{id}	版本詳情
POST	/admin/engines/{type}/versions	新增版本
PUT	/admin/engines/{type}/versions/{id}	更新版本
POST	/admin/engines/{type}/versions/{id}/test	測試版本
POST	/admin/engines/{type}/versions/{id}/activate	啟用
POST	/admin/engines/{type}/versions/{id}/archive	封存
DELETE	/admin/engines/{type}/versions/{id}	刪除草稿
GET	/admin/engines/traces	追蹤列表
GET	/admin/engines/traces/{snapshot_id}	追蹤樹
POST	/admin/engines/recompute	建立重算
GET	/admin/engines/recompute/{job_id}	查詢重算
GET	/admin/engines/recompute	重算列表
GET	/admin/engines/llm-usage	LLM 使用統計
資料表：engine_versions, execution_snapshots, engine_traces, recompute_jobs, llm_usage_logs, engine_cache_invalidations

前端頁面：

/admin/engines

/admin/engines/:type

/admin/engines/:type/edit/:version

/admin/traces

/admin/recompute

Full P6：保險商品爬蟲
擴充保險商品表

Full P7：保險缺口分析
擴充 /app/insurance/gap

Full P8：保險保單擴充子分類
Full P9：LLM Provider 抽象層 + 編輯器（v1.5 擴充）
新增 API 端點：

方法	路徑	說明
GET	/admin/llm/providers	Provider 列表
POST	/admin/llm/providers/{provider}/test	測試 Provider
PUT	/admin/llm/providers/{provider}/config	設定 Provider
GET	/admin/llm/routing	查看路由
PUT	/admin/llm/routing	修改路由
整合引擎版本管理：

LLM 編輯器使用 Full P5.5 的編輯器框架

版本存於 engine_versions（engine_type='llm'）

每次呼叫產生 engine_traces

成本記錄到 llm_usage_logs

Full P10：漫畫生成
Full P11：保險缺口精算
Full P12：Report Aggregator
Full P13：多語言支援
Full P14：效能優化
Full P15：指揮中心（整合引擎管理）
Full P16：資料匯出 / 匯入
GET /app/export

POST /app/import

Full P17：API 開放
GET /app/api-keys

POST /app/api-keys

DELETE /app/api-keys/{id}

Full P18：金流模組
POST /billing/checkout

POST /billing/webhook

GET /billing/subscription

GET /billing/invoices

POST /billing/cancel

POST /billing/refund

GET /admin/billing

POST /admin/billing/toggle

Full P19：醫療費用爬蟲
3. 資料庫表與 Phase 對應（v1.5 更新）
表	MVP Phase	Full Phase
tenants	P0	P1
users	P1	-
admin_users	P1	-
otp_tokens	P1	-
refresh_tokens	P1	-
financial_models	P2	-
vaults	P2	-
holdings	P3	P3
liabilities	P4	-
asset_classes	P0	P2
asset_definitions	P0	P2
market_prices	P7	P4
market_snapshots	P7	P4
forecast_runs	P9	P9
forecast_results	P9	P9
forecast_inputs	P9	P9
insurance_policies	P8	P8
insurance_products	-	P6
insurance_products_history	-	P6
body_part_mapping	P8	P5
insurance_gap_snapshots	P11	P7
email_logs	P10	P12
incidents	P10	P15
subscriptions	-	P18
audit_logs	P0	-
user_health_profiles	P1	-
genetic_markers	P1	-
user_genetic_tests	P1	-
medical_cost_references	P11	P19
disease_risk_mapping	P11	P11
engine_versions（v1.5）	-	P5.5
execution_snapshots（v1.5）	-	P5.5
engine_traces（v1.5）	-	P5.5
recompute_jobs（v1.5）	-	P5.5
llm_usage_logs（v1.5）	-	P5.5
engine_cache_invalidations（v1.5）	-	P5.5
4. MVP API 統計（v1.5）
Phase	API 數	資料表數
P0	3	36
P1	15	8
P2	8	2
P3	4	3
P4	4	1
P5	0（複用 P3）	0
P6	0（複用 P3）	0
P7	2	2
P8	5	2
P9	2	3
P10	6	3
P11	5	3
總計	54	36
5. 完整版 API 統計（v1.5）
Phase	新增 API 數
P1	5
P2	6
P3	0
P4	3
P5	0
P5.5	15
P6	0
P7	0
P8	0
P9	+5（Provider 相關）
P10	0
P11	0
P12	0
P13	0
P14	0
P15	5
P16	2
P17	3
P18	8
P19	0
總計	52
完整版總 API 數：54 + 52 = 106

6. 引擎管理 API 詳細對應（v1.5 新增）
引擎	版本管理	追蹤	重算	編輯器
crawler	✅	✅	✅	✅
normalizer	✅	✅	✅	✅
validator	✅	✅	✅	✅
matcher	✅	✅	✅	✅
monte_carlo	✅	✅	✅	✅
llm	✅	✅	✅	✅
編輯器支援的設定類型：

引擎	可編輯設定
crawler	source_config、選擇器
normalizer	正規化規則
validator	容忍值、min_sources
matcher	比對邏輯
monte_carlo	模型參數、模擬次數
llm	Prompt、模型、temperature
7. LLM Provider 與 Phase 對應（v1.5）
Provider	MVP	Full P9	說明
TemplateProvider	✅	✅	MVP 唯一使用
GroqProvider	❌	✅	專業版
GeminiProvider	❌	✅	專業+
OpenAIProvider	❌	✅	未來付費
OllamaProvider	❌	✅	管理員
文件 6 結束


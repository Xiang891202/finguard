# 📚 文件導航

本目錄包含 FinGuard 專案的所有規劃書。

## 🗂️ 文件結構

### 第一批：框架層（v1.5）

| 文件 | 說明 | 狀態 |
| :--- | :--- | :---: |
| [01-shared-framework.md](./01-framework/01-shared-framework.md) | 共用框架規劃書 | ✅ v1.5 |
| [02-operations-manual.md](./01-framework/02-operations-manual.md) | 操作手冊 | ✅ v1.5 |
| [03-phase-template.md](./01-framework/03-phase-template.md) | Phase 模板 | ✅ v1.5 |

### 第二批：參考文件（v1.5）

| 文件 | 說明 | 狀態 |
| :--- | :--- | :---: |
| [01-database-schema.md](./02-reference/01-database-schema.md) | 資料庫完整 Schema（36 張表） | ✅ v1.5 |
| [02-api-spec.md](./02-reference/02-api-spec.md) | API 完整規格（106 端點） | ✅ v1.5 |
| [03-api-phase-mapping.md](./02-reference/03-api-phase-mapping.md) | API 與 Phase 對應表 | ✅ v1.5 |

### 第三批：MVP 規劃（v1.5）

| 文件 | 說明 | 狀態 |
| :--- | :--- | :---: |
| [00-overview.md](./03-mvp/00-overview.md) | MVP 功能規劃書 | ✅ v1.5 |
| [phase-00-setup.md](./03-mvp/phase-00-setup.md) | Phase 0：基礎建設 | ✅ v1.4 |
| [phase-01-auth.md](./03-mvp/phase-01-auth.md) | Phase 1：用戶認證 + 健康檔案 | ✅ v1.4 |
| [phase-02-models.md](./03-mvp/phase-02-models.md) | Phase 2：財務模型 + 金庫 | ✅ v1.4 |
| [phase-03-holdings.md](./03-mvp/phase-03-holdings.md) | Phase 3：持有部位（Equity） | ✅ v1.4 |
| [phase-04-liabilities.md](./03-mvp/phase-04-liabilities.md) | Phase 4：負債 | ✅ v1.4 |
| [phase-05-forex.md](./03-mvp/phase-05-forex.md) | Phase 5：外匯（Forex） | ✅ v1.4 |
| [phase-06-money-market.md](./03-mvp/phase-06-money-market.md) | Phase 6：貨幣基金 | ✅ v1.4 |
| [phase-07-crawler.md](./03-mvp/phase-07-crawler.md) | Phase 7：爬蟲調度 + 三源驗證 | ✅ v1.4 |
| [phase-08-insurance.md](./03-mvp/phase-08-insurance.md) | Phase 8：保險保單 CRUD | ✅ v1.4 |
| [phase-09-forecast.md](./03-mvp/phase-09-forecast.md) | Phase 9：蒙地卡羅 + 風險計算 | ✅ v2.0（移除 LLM） |
| [phase-10-email-recovery.md](./03-mvp/phase-10-email-recovery.md) | Phase 10：Email 報告 + 自癒 | ✅ v2.0（改用模板） |
| [phase-11-medical-cost.md](./03-mvp/phase-11-medical-cost.md) | Phase 11：醫療費用 + 覆蓋率精算 | ✅ v1.4 |

### 第四批：完整版規劃（v1.5）

| 文件 | 說明 | 狀態 |
| :--- | :--- | :---: |
| [00-overview.md](./04-full/00-overview.md) | 完整版功能規劃書（20 Phase） | ✅ v1.5 |
| [phase-01-tenant-architecture.md](./04-full/phase-01-tenant-architecture.md) | P1：多租戶架構 | ✅ v1.4 |
| [phase-02-asset-management.md](./04-full/phase-02-asset-management.md) | P2：資產類別 + 標的管理 | ✅ v1.4 |
| [phase-03-more-handlers.md](./04-full/phase-03-more-handlers.md) | P3：更多 Handler | ✅ v1.4 |
| [phase-04-scheduled-crawler.md](./04-full/phase-04-scheduled-crawler.md) | P4：自動排程爬蟲 | ✅ v1.4 |
| [phase-05-body-map.md](./04-full/phase-05-body-map.md) | P5：人體剖面圖 | ✅ v1.4 |
| [phase-05.5-engine-version.md](./04-full/phase-05.5-engine-version.md) | **P5.5：引擎版本管理系統** | 🆕 v1.5 |
| [phase-06-insurance-crawler.md](./04-full/phase-06-insurance-crawler.md) | P6：保險商品爬蟲 | ✅ v1.4 |
| [phase-07-insurance-gap.md](./04-full/phase-07-insurance-gap.md) | P7：保險缺口分析 | ✅ v1.4 |
| [phase-08-insurance-subcategories.md](./04-full/phase-08-insurance-subcategories.md) | P8：保險保單擴充子分類 | ✅ v1.4 |
| [phase-09-llm-text-generation.md](./04-full/phase-09-llm-text-generation.md) | P9：LLM Provider 抽象層 | ✅ v2.0（Provider 抽象） |
| [phase-10-comic-generation.md](./04-full/phase-10-comic-generation.md) | P10：漫畫生成 | ✅ v1.4 |
| [phase-11-advanced-coverage.md](./04-full/phase-11-advanced-coverage.md) | P11：保險缺口精算 | ✅ v1.4 |
| [phase-12-report-aggregator.md](./04-full/phase-12-report-aggregator.md) | P12：Report Aggregator | ✅ v1.4 |
| [phase-13-i18n.md](./04-full/phase-13-i18n.md) | P13：多語言支援 | ✅ v1.4 |
| [phase-14-performance.md](./04-full/phase-14-performance.md) | P14：效能優化 | ✅ v1.4 |
| [phase-15-command-center.md](./04-full/phase-15-command-center.md) | P15：指揮中心 | ✅ v2.0（整合引擎管理） |
| [phase-16-export-import.md](./04-full/phase-16-export-import.md) | P16：資料匯出 / 匯入 | ✅ v1.4 |
| [phase-17-api-open.md](./04-full/phase-17-api-open.md) | P17：API 開放 | ✅ v1.4 |
| [phase-18-billing.md](./04-full/phase-18-billing.md) | P18：金流模組 | ✅ v1.4 |
| [phase-19-medical-cost-crawler.md](./04-full/phase-19-medical-cost-crawler.md) | P19：醫療費用爬蟲 | ✅ v1.4 |

### 補充文件（v1.5）

| 文件 | 說明 | 狀態 |
| :--- | :--- | :---: |
| [A-redis-pubsub-guide.md](./04-full/supplements/A-redis-pubsub-guide.md) | Redis Pub/Sub 實作指南 | ✅ v1.5 |
| [B-engine-editors-design.md](./04-full/supplements/B-engine-editors-design.md) | 6 種引擎編輯器設計 | ✅ v1.5 |
| [C-ui-components-design.md](./04-full/supplements/C-ui-components-design.md) | UI 元件詳細設計 | ✅ v1.5 |

### 實作指南（v1.5）

| 文件 | 說明 | 狀態 |
| :--- | :--- | :---: |
| [01-implementation-order.md](./05-implementation-guide/01-implementation-order.md) | 實作順序指南 | ✅ v1.0 |
| [02-daily-workflow.md](./05-implementation-guide/02-daily-workflow.md) | 每日工作流程 | ✅ v1.0 |
| [03-verification-checklist.md](./05-implementation-guide/03-verification-checklist.md) | 驗證清單 | ✅ v1.0 |


## 🔄 閱讀順序

1. 先讀 `01-framework/` 了解整體架構
2. 再讀 `02-reference/` 了解資料庫與 API
3. 讀 `03-mvp/` 了解 MVP 實作順序
4. 讀 `04-full/` 了解完整版擴充
5. 需要實作細節時查閱 `04-full/supplements/`

## 📌 版本對照

| 版本 | 日期 | 變更 |
| :--- | :--- | :--- |
| **v1.5** | **2026-09-22** | **新增引擎版本管理、LLM Provider 抽象層、Redis Pub/Sub、MVP 移除 LLM** |
| v1.4 | 2026-09-21 | 新增健康機制（年紀、家族病史、基因風險）、醫療費用參考、精準保險覆蓋率 |
| v1.3 | 2026-09-20 | 修正 21 項架構問題（零遷移、PostgreSQL、三源驗證等） |
| v1.2 | 2026-09-20 | 新增金流規格、角色權限 |
| v1.1 | 2026-09-20 | 新增管理員區隔、自癒機制 |
| v1.0 | 2026-09-20 | 初版 |

## 📊 v1.5 專案規模

| 項目 | v1.4 | v1.5 |
| :--- | :---: | :---: |
| 資料表 | 30 | **36** |
| MVP Phase | 12 | 12 |
| 完整版 Phase | 19 | **20** |
| 總 Phase | 31 | **32** |
| MVP API | 54 | 54 |
| 完整版 API | 29 | **52** |
| 總 API | 83 | **106** |
| MVP 工時 | 48 天 | **44 天** |
| 完整版工時 | 114 天 | **121 天** |
| 總工時 | 162 天 | **165 天** |

## 🎯 五大核心變更（v1.5）

| # | 變更 | 說明 |
| :---: | :--- | :--- |
| 1 | **引擎版本管理系統** | 5 大引擎獨立版本、可還原、可重算 |
| 2 | **LLM Provider 抽象層** | Template / Groq / Gemini / OpenAI / Ollama |
| 3 | **免費為主 LLM 策略** | MVP 用模板，付費解鎖 LLM |
| 4 | **Redis Pub/Sub 快取失效** | 設定變更即時生效（< 1 秒） |
| 5 | **圖形化引擎編輯器** | 本地編輯 → 測試 → 提交 → 部署 |
# FinGuard（財安）

> 個人 / 家庭財務安全儀表板
> Personal & Family Financial Safety Dashboard

## 📖 專案簡介

一套結合「理財模型 × 保險保障 × 健康風險 × AI 預測」的個人財務風險管理系統。

- **短期目標**：個人與家人使用（MVP）
- **長期目標**：多租戶 SaaS（完整版）
- **設計原則**：個人優先、商業就緒、免費優先、插件化、15 年長期運作

## 📚 文件導航

所有規劃書位於 [`docs/`](./docs/)，請從 [`docs/README.md`](./docs/README.md) 開始閱讀。

| 批次 | 文件 | 說明 |
| :--- | :--- | :--- |
| 第一批 | [框架層](./docs/01-framework/) | 共用框架、操作手冊、Phase 模板 |
| 第二批 | [參考文件](./docs/02-reference/) | 資料庫 Schema、API 規格 |
| 第三批 | [MVP 規劃](./docs/03-mvp/) | MVP 功能規劃與各 Phase（12 個） |
| 第四批 | [完整版規劃](./docs/04-full/) | 完整版功能規劃與各 Phase（20 個） |
| 第五批 | [實作指南](./docs/05-implementation-guide/) | 實作順序、每日流程、驗證清單 |

## 🏗️ 技術棧

| 組件 | 選擇 |
| :--- | :--- |
| 主框架 | Node.js（完整版 BFF） |
| 核心業務 | Python FastAPI |
| 金流 | Java Spring Boot |
| 前端 | Vue 3 + Vite + Tailwind CSS |
| 資料庫 | PostgreSQL（MVP 與完整版一致） |
| 快取 / Queue | Redis / Upstash |
| AI 預測 | Python + NumPy（蒙地卡羅） |
| LLM Provider | Template / Groq / Gemini / OpenAI / Ollama（5 層抽象） |
| 安全掃描 | Strix（本地） |
| 部署 | Render（MVP）→ AWS / GCP（完整版） |

## 📊 專案規模

| 項目 | 數量 |
| :--- | :---: |
| 開發階段（Phase） | 32（MVP 12 + 完整版 20） |
| 資料表 | 36 |
| API 端點 | 106 |
| 預估工時 | 165 天 |
| 架構層級 | 7 層 |
| 程式語言 | 4（Vue / Node / Python / Java） |
| 引擎 | 5（爬蟲 / 正規化 / 驗證 / 比對 / 蒙地卡羅 / LLM） |

## 📌 文件版本

- 目前版本：**v1.5**
- 最後更新：2026-09-22
- 版本紀錄：見 [docs/README.md](./docs/README.md)

## ✨ v1.5 核心亮點

- **引擎版本管理系統**：5 大引擎獨立版本、可還原、可重算
- **LLM Provider 抽象層**：免費為主、付費解鎖
- **Redis Pub/Sub 快取失效**：設定變更即時生效（< 1 秒）
- **圖形化引擎編輯器**：本地編輯 → 測試 → 提交 → 部署
- **健康檔案精算**：納入年齡、性別、家族病史、基因

## 🚫 重要限制

- ❌ 不提供投資建議
- ❌ 不提供操作做法
- ❌ 不推薦具體保險商品
- ✅ 僅提供「風險機率」與「水位狀態」
- ✅ 只呈現數據，不下結論

## 📄 授權

（待補）
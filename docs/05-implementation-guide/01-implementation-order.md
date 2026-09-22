📘 實作順序指南
版本：v1.0
最後更新：2026-09-22
適用範圍：從 MVP 到完整版的實作順序

📁 檔案位置
text
docs/
└── 05-implementation-guide/
    ├── 01-implementation-order.md          ← 本文件
    ├── 02-daily-workflow.md                ← 每日工作流程（可選）
    └── 03-verification-checklist.md        ← 驗證清單（可選）
建立指令：

powershell
# 建立目錄
New-Item -ItemType Directory -Force -Path docs\05-implementation-guide

# 建立主文件
New-Item -ItemType File -Force -Path docs\05-implementation-guide\01-implementation-order.md

Write-Host "✅ 實作順序指南目錄建立完成！" -ForegroundColor Green
📄 主文件完整內容
markdown
# 實作順序指南（Implementation Order Guide）

**版本**：v1.0
**最後更新**：2026-09-22
**適用範圍**：從 MVP 到完整版的實作順序

---

## 1. 為什麼需要這份指南？

規劃書有 32 個 Phase，但**不是照順序做就好**。本指南說明：

- ✅ **該從哪個 Phase 開始**
- ✅ **哪些 Phase 可以並行**
- ✅ **每個 Phase 的完成標準**
- ✅ **遇到問題時的處理方式**
- ✅ **如何驗證「整體系統」可用**

---

## 2. 總體實作順序（4 個階段）
┌─────────────────────────────────────────────────────────────┐
│ 階段 1：MVP 基礎（44 天） │
│ P0 → P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8 → P9 → P10 → P11│
└─────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│ 階段 2：完整版核心（約 40 天） │
│ F1 → F2 → F3 → F4 → F5 → F5.5 │
└─────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│ 階段 3：完整版擴充（約 50 天） │
│ F6 → F7 → F8 → F9 → F10 → F11 → F12 │
└─────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│ 階段 4：完整版收尾（約 31 天） │
│ F13 → F14 → F15 → F16 → F17 → F18 → F19 │
└─────────────────────────────────────────────────────────────┘

text

---

## 3. MVP 實作順序（詳細）

### 3.1 MVP 12 個 Phase 順序

| 順序 | Phase | 名稱 | 工時 | 依賴 |
| :---: | :---: | :--- | :---: | :--- |
| 1 | P0 | 基礎建設 | 3 天 | - |
| 2 | P1 | 用戶認證 + 健康檔案 | 5 天 | P0 |
| 3 | P2 | 財務模型 + 金庫 | 4 天 | P1 |
| 4 | P3 | 持有部位（Equity） | 4 天 | P2 |
| 5 | P4 | 負債 | 2 天 | P2 |
| 6 | P5 | 外匯（Forex） | 3 天 | P3 |
| 7 | P6 | 貨幣基金 | 2 天 | P3 |
| 8 | P7 | 爬蟲調度 + 三源驗證 | 5 天 | P3, P5, P6 |
| 9 | P8 | 保險保單 CRUD | 4 天 | P2 |
| 10 | P9 | 蒙地卡羅 + 風險計算 | 3 天 | P7 |
| 11 | P10 | Email 報告 + 自癒 | 4 天 | P9 |
| 12 | P11 | 醫療費用 + 覆蓋率精算 | 5 天 | P8, P9 |
| **總計** | - | - | **44 天** | - |

### 3.2 可並行的 Phase
P2 完成後：
├── P3（持有部位） ─── P5（外匯） ─── P6（貨幣基金）
└── P4（負債）

P7 完成後：
└── P9（蒙地卡羅）

P2 完成後：
└── P8（保險保單） ─── P11（醫療費用）

text

**建議並行順序**：
- **Week 1-2**：P0 → P1 → P2
- **Week 3**：P3 + P4（並行）
- **Week 4**：P5 + P6（並行）
- **Week 5**：P7
- **Week 6**：P8 + P9（並行）
- **Week 7**：P10 + P11（並行）
- **Week 8-9**：整合測試 + 修正

---

## 4. MVP 各 Phase 實作細節

### 4.1 Phase 0：基礎建設（3 天）

**目標**：專案骨架、DB、CI/CD

**每日進度**：
| 天數 | 任務 |
| :---: | :--- |
| Day 1 | 建立專案結構、套件安裝 |
| Day 2 | 建立 36 張表、Alembic 遷移 |
| Day 3 | 健康檢查端點、CI/CD 設定 |

**完成標準**：
- [ ] `docker-compose up` 可執行
- [ ] 36 張表建立完成
- [ ] `GET /health` 回應 200
- [ ] CI 可執行（lint + test）

**驗證指令**：
```bash
curl http://localhost:8000/health
# 應回應 {"status": "healthy", "version": "1.5.0"}
4.2 Phase 1：用戶認證 + 健康檔案（5 天）
目標：Email OTP 登入、管理員登入、健康檔案 CRUD

每日進度：

天數	任務
Day 1	OTP 請求/驗證 API
Day 2	JWT + Refresh Token Rotation
Day 3	管理員登入（bcrypt）
Day 4	健康檔案 CRUD
Day 5	基因資料（加密 + 同意）
完成標準：

□ 用戶可用 Email + OTP 登入
□ 管理員可用 Email + 密碼登入
□ OTP 防濫用生效
□ 基因資料加密存儲
□ 健康檔案完成度計算正確
驗證指令：

bash
# 1. 請求 OTP
curl -X POST http://localhost:8000/api/v1/auth/otp/request \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# 2. 驗證 OTP（從 DB 查）
curl -X POST http://localhost:8000/api/v1/auth/otp/verify \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "otp": "123456"}'
4.3 Phase 2：財務模型 + 金庫（4 天）
目標：模型 CRUD、金庫 CRUD、模型上限

每日進度：

天數	任務
Day 1	模型 CRUD API
Day 2	金庫 CRUD API
Day 3	模型上限驗證（一般用戶 2、管理員 10）
Day 4	前端頁面整合
完成標準：

□ 模型 CRUD 完整
□ 金庫 CRUD 完整
□ 模型上限生效
□ 軟刪除（is_archived）
4.4 Phase 3：持有部位（EquityHandler）（4 天）
目標：股票 CRUD、EquityHandler

每日進度：

天數	任務
Day 1	BaseAssetHandler 抽象類
Day 2	EquityHandler 實作
Day 3	持有部位 CRUD API
Day 4	前端頁面整合
完成標準：

□ EquityHandler 實作完成
□ 持有部位 CRUD 完整
□ 損益計算正確
□ Handler 單元測試通過
關鍵測試：

python
def test_equity_handler_fetch_price(mock_twse):
    mock_twse.return_value = 155.20
    handler = EquityHandler({"symbol": "0050.TW", ...})
    assert handler.fetch_price("2026-09-22") == 155.20
4.5 Phase 4：負債（2 天）
目標：負債 CRUD

完成標準：

□ 負債 CRUD 完整
□ 剩餘金額不可超過總額
4.6 Phase 5：外匯（ForexHandler）（3 天）
目標：ForexHandler、外匯 CRUD

完成標準：

□ ForexHandler 實作完成
□ Fallback 機制測試通過
□ 外匯 Seed 資料建立
4.7 Phase 6：貨幣基金（MoneyMarketHandler）（2 天）
目標：MoneyMarketHandler

完成標準：

□ MoneyMarketHandler 實作完成
□ 固定低波動率正確
4.8 Phase 7：爬蟲調度 + 三源驗證（5 天）
目標：CrawlerDispatcher、Normalizer、Validator

每日進度：

天數	任務
Day 1	CrawlerDispatcher 動態載入
Day 2	Normalizer 正規化
Day 3	Validator Level 1/2/3
Day 4	DATA_CONFLICT 處理
Day 5	手動觸發 API + 前端
完成標準：

□ 手動觸發爬蟲
□ 三源驗證 Level 1/2/3 正確
□ DATA_CONFLICT 觸發 Incident
□ STALE 標記正確
關鍵測試：

python
def test_level_3_conflict():
    result = validator.validate([100.0, 120.0, 140.0], tolerance=0.5)
    assert result["level"] == "LEVEL_3"
    assert result["status"] == "DATA_CONFLICT"
4.9 Phase 8：保險保單 CRUD（4 天）
目標：保單 CRUD、body_part_mapping

完成標準：

□ 保單 CRUD 完整
□ 人身 / 財產分類正確
□ Body Part Selector 可用
□ body_part_mapping Seed 完成（8 部位）
4.10 Phase 9：蒙地卡羅 + 風險計算（3 天）
目標：蒙地卡羅、風險計算、市場情緒（規則式）

⚠️ v1.5 變更：移除 LLM，改用規則式解讀

完成標準：

□ 蒙地卡羅引擎實作
□ 3 個月與 6 個月預測
□ 破產機率計算正確
□ 市場情緒規則式解讀正確
□ 無 LLM 依賴
關鍵測試：

python
def test_monte_carlo_deterministic():
    engine = MonteCarloEngine(seed=42)
    result = engine.run(initial_assets=1000000, ...)
    assert 0 <= result["bankruptcy_probability"] <= 1
4.11 Phase 10：Email 報告 + 自癒（4 天）
目標：Email 6 區塊、自癒 Level 1

⚠️ v1.5 變更：Email 用 Jinja2 模板生成

完成標準：

□ Email 6 區塊齊全
□ 市場情緒用規則式解讀
□ 無 LLM 依賴
□ Level 1 修復不通知
□ Level 2/3 記錄 Incident
4.12 Phase 11：醫療費用 + 覆蓋率精算（5 天）
目標：醫療費用 Seed、Coverage Ratio

完成標準：

□ 醫療費用 Seed 完成（≥ 8 疾病）
□ 疾病風險映射 Seed 完成
□ Coverage Ratio 計算正確
□ 不顯示具體商品推薦
關鍵測試：

python
def test_coverage_basic():
    result = coverage_calc.calculate(
        base_cost=500000,
        age=55, gender="male",
        family_history=True, genetic_positive=True
    )
    # 500000 × 1.5 × 1.3 × 1.5 × 1.8 = 2632500
    assert result["required_coverage"] == 2632500
5. MVP 整合測試（Week 8-9）
5.1 整合測試清單
測試	說明
E2E-01	新用戶註冊 → 健康檔案 → 建立模型 → 新增持有部位
E2E-02	手動觸發爬蟲 → 三源驗證 → 更新價格
E2E-03	建立保單 → 計算 Coverage Ratio
E2E-04	執行蒙地卡羅 → 產生 Email 預覽
E2E-05	系統異常 → 自動修復 → 通知管理員
5.2 完整流程驗證
bash
# 1. 註冊新用戶
curl -X POST /auth/otp/request -d '{"email": "new@example.com"}'
curl -X POST /auth/otp/verify -d '{"email": "new@example.com", "otp": "..."}'

# 2. 填寫健康檔案
curl -X POST /app/health/profile -H "Authorization: Bearer $TOKEN" \
  -d '{"birth_date": "1985-06-15", "gender": "male"}'

# 3. 建立模型
curl -X POST /app/models -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "我的家庭財務", "emergency_fund_months": 6}'

# 4. 新增持有部位
curl -X POST /app/holdings -H "Authorization: Bearer $TOKEN" \
  -d '{"model_id": "...", "asset_definition_id": "...", "quantity": 100}'

# 5. 觸發爬蟲
curl -X POST /app/crawler/trigger -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"asset_class": "equity"}'

# 6. 執行預測
curl -X POST /app/forecast/run -H "Authorization: Bearer $TOKEN" \
  -d '{"model_id": "...", "horizon_months": 6}'

# 7. 查看 Email 預覽
curl /app/email-preview -H "Authorization: Bearer $TOKEN"
6. 完整版實作順序（詳細）
6.1 完整版 20 個 Phase 順序
順序	Phase	名稱	工時	依賴
1	F1	多租戶架構	5 天	MVP
2	F2	資產類別 + 標的管理	6 天	F1
3	F3	更多 Handler	6 天	F1
4	F4	自動排程爬蟲	4 天	F3
5	F5	人體剖面圖	7 天	F2
6	F5.5	引擎版本管理	8 天	F4, F5
7	F6	保險商品爬蟲	8 天	F5.5
8	F7	保險缺口分析	5 天	F6
9	F8	保險保單擴充子分類	4 天	F7
10	F9	LLM Provider 抽象層	10 天	F5.5
11	F10	漫畫生成	5 天	F9
12	F11	保險缺口精算	7 天	F8
13	F12	Report Aggregator	4 天	F10
14	F13	多語言支援	4 天	F12
15	F14	效能優化	5 天	F13
16	F15	指揮中心	9 天	F14
17	F16	資料匯出 / 匯入	5 天	F15
18	F17	API 開放	5 天	F16
19	F18	金流模組	12 天	F17
20	F19	醫療費用爬蟲	6 天	F18
總計	-	-	121 天	-
6.2 關鍵里程碑
text
F1（多租戶）─── 系統可支援多租戶
F5.5（引擎版本管理）─── 所有引擎可追蹤版本
F9（LLM Provider）─── LLM 可切換
F15（指揮中心）─── 完整自癒上線
F18（金流）─── 可收費
7. 實作注意事項
7.1 版本鎖定規則
Phase 開始後，不得直接修改 Framework。

若必須修改：

text
Framework v1.5
    ↓
Phase P3 進行中
    ↓
發現需要修改
    ↓
Framework v1.5 → v1.6
    ↓
影響分析：
├── 哪些 Phase 受影響？
├── 是否需要重做？
└── 是否需要補測試？
7.2 每個 Phase 的完成定義（DoD）
□ 前端畫面可操作
□ 後端 API 端點正常
□ 單元測試通過（≥ 80%）
□ Critical Integration Test 通過
□ 驗收標準全部勾選
□ 交付物清單已產出
7.3 測試策略
測試類型	時機	範圍
單元測試	每個 PR	Service、Handler
整合測試	每個 Phase 完成	API → Service → DB
E2E 測試	MVP 完成、完整版完成	全流程
效能測試	F14	API < 200ms
8. 每週工作節奏建議
8.1 每日工作流程
text
早上（2-3 小時）：
├── 檢視昨日進度
├── 確認今日任務
└── 開始實作

下午（3-4 小時）：
├── 繼續實作
├── 撰寫單元測試
└── 提交 PR

晚上（1-2 小時）：
├── Code Review
├── 修正問題
└── 更新文件
8.2 每週檢核
週幾	任務
週一	開始新 Phase
週三	中期檢查
週五	Phase 完成驗收
週末	整合測試 / 文件更新
9. 遇到問題的處理方式
9.1 問題分類
類型	處理方式
規格不清	查閱框架規劃書 → 若仍不清，記錄並討論
技術卡關	查閱相關文件 → 問 AI → 暫時跳過
測試失敗	先修測試 → 若測試有誤，修測試
架構衝突	停止 → 分析 → 修改 Framework 版本
9.2 緊急處理順序
text
1. 記錄問題（建立 Issue）
2. 評估影響範圍
3. 決定：立即修 / 延後修 / 修改架構
4. 執行
5. 更新文件
10. 快速查閱表
10.1 MVP 快速查閱
想做的事	查這個
從哪開始？	P0（基礎建設）
怎麼登入？	P1（認證）
怎麼加資產？	P3（持有部位）
怎麼抓價格？	P7（爬蟲）
怎麼算保費？	P11（覆蓋率精算）
怎麼寄 Email？	P10（Email）
10.2 完整版快速查閱
想做的事	查這個
怎麼多租戶？	F1
怎麼加新資產？	F2（管理員 UI）
怎麼自動化？	F4（排程）
怎麼管版本？	F5.5
怎麼換 LLM？	F9
怎麼收費？	F18
11. 實作順序檢查清單
11.1 開始 MVP 前
□ 讀完 01-shared-framework.md
□ 讀完 02-reference/01-database-schema.md
□ 讀完 02-reference/02-api-spec.md
□ 環境準備（Node.js 20+、Python 3.11+、PostgreSQL）
□ Git 專案建立
11.2 每個 Phase 開始前
□ 前一個 Phase 已完成
□ 前置檔案已備妥
□ 該 Phase 規劃書已讀
□ 測試環境已就緒
11.3 每個 Phase 完成後
□ 所有測試通過
□ 驗收標準勾選
□ 交付物清單確認
□ Git commit
□ 更新文件
12. 版本紀錄
版本	日期	變更
v1.0	2026-09-22	初版建立
文件結束
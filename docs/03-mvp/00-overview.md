📄 更新文件 1：MVP 功能規劃書（00-overview.md）
版本：v1.5
所屬：MVP
Phase 數量：12（P0 ~ P11）

1. MVP 目標
建立一套可在 1-5 人環境運作的個人 / 家庭財務安全儀表板，包含：

用戶認證（Email + OTP）

健康檔案（生日、性別、家族病史、基因）

財務模型（模型、金庫、持有部位、負債）

保險保單與缺口分析

蒙地卡羅風險預測

每日 Email 合併報告（模板生成，v1.5）

基礎自癒機制

2. MVP 範圍界定（v1.5 更新）
項目	納入	不納入
用戶認證	✅	-
健康檔案	✅	-
財務模型	✅	-
持有部位	✅（3 Handler）	❌（Bond/Metal/Crypto）
負債	✅	-
保險保單	✅	-
保險缺口	✅（基礎）	❌（完整精算）
預測	✅	-
Email 報告	✅（模板生成）	-
自癒機制	✅（基礎）	❌（完整三級）
LLM（v1.5）	❌ 不納入	-
多租戶 UI	❌	-
金流	❌	-
人體剖面圖	❌	❌（Full P5）
漫畫生成	❌	❌（Full P10）
引擎版本管理（v1.5）	❌ 不納入	❌（Full P5.5）
3. 12 個 Phase 總覽（v1.5 更新）
Phase	名稱	主要產出	依賴
P0	基礎建設	專案骨架、DB、CI/CD	-
P1	用戶認證 + 健康檔案	Email OTP、會員中心	P0
P2	財務模型 + 金庫	模型、金庫 CRUD	P1
P3	持有部位（Equity）	股票 CRUD、EquityHandler	P2
P4	負債	負債 CRUD	P2
P5	外匯（Forex）	外匯 CRUD、ForexHandler	P3
P6	貨幣基金（MoneyMarket）	貨幣基金、MoneyMarketHandler	P3
P7	爬蟲調度 + 三源驗證	Crawler、Validator	P3, P5, P6
P8	保險保單 CRUD	保單管理、body_part_mapping	P2
P9	蒙地卡羅 + 風險計算	MonteCarlo、Sentiment（無 LLM）	P7
P10	Email 報告 + 自癒	Email（模板）、Incidents、Dashboard	P9
P11	醫療費用 + 覆蓋率精算	medical_cost、CoverageCalculator	P8, P9
4. Phase 依賴圖
text
P0（基礎建設）
    ↓
P1（認證 + 健康檔案）
    ↓
P2（模型 + 金庫）
    ├── P3（持有部位 Equity）
    │       ├── P5（外匯 Forex）
    │       ├── P6（貨幣基金）
    │       └── P7（爬蟲調度）
    │               ↓
    │           P9（蒙地卡羅）
    │               ↓
    │           P10（Email + 自癒）
    │               ↑
    └── P4（負債）   │
                     │
        P8（保險保單）┘
            ↓
        P11（醫療費用 + 覆蓋率精算）
5. 每 Phase 的完成定義（DoD）
每個 Phase 必須滿足：

□ 前端畫面可操作（Vue 3）
□ 後端 API 端點正常
□ 單元測試通過（覆蓋率 ≥ 80%）
□ Critical Integration Test 通過
□ 驗收標準全部勾選
□ 交付物清單已產出
6. Phase 工時預估（v1.5 更新）
Phase	名稱	預估工時
P0	基礎建設	3 天
P1	用戶認證 + 健康檔案	5 天
P2	財務模型 + 金庫	4 天
P3	持有部位（Equity）	4 天
P4	負債	2 天
P5	外匯（Forex）	3 天
P6	貨幣基金	2 天
P7	爬蟲調度 + 三源驗證	5 天
P8	保險保單 CRUD	4 天
P9	蒙地卡羅 + 風險計算	3 天（v1.4：5 天）
P10	Email 報告 + 自癒	4 天（v1.4：6 天）
P11	醫療費用 + 覆蓋率精算	5 天
總計	-	44 天（v1.4：48 天）
v1.5 工時變化：-4 天（移除 LLM）

7. MVP 整體驗收（v1.5 更新）
MVP 完成時，系統必須能夠：

用戶以 Email + OTP 登入

填寫健康檔案（生日、性別、家族病史、基因）

建立財務模型、金庫、持有部位、負債

手動觸發爬蟲，取得三源驗證後的價格

建立保險保單，計算 Coverage Ratio

執行蒙地卡羅預測（3 個月、6 個月）

發送每日 Email 報告（6 區塊，模板生成）（v1.5）

系統異常時自動排查、修復、通知管理員

8. 與完整版的銜接（v1.5）
項目	MVP	完整版
文字生成	Jinja2 模板	Provider 抽象層
引擎版本管理	❌	✅ Full P5.5
LLM Provider	❌	✅ Full P9
快取失效	❌	✅ Full P5.5
升級路徑：

text
MVP P9（模板解讀）
    ↓
Full P5.5（引擎版本管理）
    ↓
Full P9（Provider 抽象層，可切換 LLM）
9. 版本紀錄
版本	日期	變更
v1.0	2026-09-20	初版
v1.1	2026-09-20	新增健康檔案相關
v1.2	2026-09-20	更新角色權限
v1.3	2026-09-20	修正零遷移、PostgreSQL
v1.4	2026-09-21	新增醫療費用、覆蓋率精算
v1.5	2026-09-22	移除 LLM（P9、P10）、工時 48→44 天
文件結束


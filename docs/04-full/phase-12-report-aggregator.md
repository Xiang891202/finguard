Full Phase 12：Report Aggregator
版本：v1.0
所屬：完整版
依賴 MVP Phase：MVP P10（Email）
預計工時：4 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P10：Email 已可發送

依賴 Full P9, P10：LLM、漫畫已可生成

🔄 與 MVP 的差異
項目	MVP	完整版
報告	6 區塊	6 區塊 + LLM + 漫畫
個人化	基本	高度個人化
語言	中文	多語言
格式	HTML	HTML + PDF
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/services/report_aggregator.py	新增	報告聚合
backend/app/services/pdf_service.py	新增	PDF 生成
backend/app/workers/report_worker.py	新增	Worker
frontend/src/views/app/ReportHistoryView.vue	新增	歷史報告
backend/tests/unit/test_report_aggregator.py	新增	測試
1. 目標
建立完整報告聚合，合併金融 + 保險 + LLM + 漫畫。

2. 前置條件
□ MVP P10 完成
□ Full P9, P10 完成
3. 前端畫面
3.1 頁面清單
頁面	路由
ReportHistoryView	/app/reports
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  📧 歷史報告                         │
├─────────────────────────────────────┤
│  2026-09-21 ✅ 已寄送                │
│  2026-09-20 ✅ 已寄送                │
│  2026-09-19 ⚠️ 部分失敗              │
│                                     │
│  [查看] [下載 PDF]                   │
└─────────────────────────────────────┘
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/app/reports	歷史報告
GET	/api/v1/app/reports/{id}	報告詳情
GET	/api/v1/app/reports/{id}/pdf	下載 PDF
4.2 請求/回應範例
（略）

4.3 資料庫變更
新增表：

sql
CREATE TABLE report_archives (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL REFERENCES users(id),
    report_date DATE NOT NULL,
    content JSONB NOT NULL,
    pdf_path VARCHAR(255),
    sent_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
4.4 環境變數
無新增。

5. 單元測試
python
def test_aggregate_all_sections():
    report = aggregator.build(user_id, date="2026-09-21")
    assert "financial" in report
    assert "market_sentiment" in report
    assert "forecast" in report
    assert "insurance_gap" in report
    assert "comic" in report
    assert "disclaimer" in report
6. 驗收標準
□ 6 區塊完整
□ LLM 文字整合
□ 漫畫整合
□ PDF 生成
□ 歷史可查
□ 單元測試 ≥ 80%
7. 交付物清單
（略）
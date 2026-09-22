Full Phase 19：醫療費用爬蟲
版本：v1.0
所屬：完整版
依賴 MVP Phase：MVP P11（醫療費用）
預計工時：6 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P11：medical_cost_references 表已建立

依賴 MVP P7：爬蟲框架已建立

🔄 與 MVP 的差異
項目	MVP	完整版
醫療費用來源	人工 Seed	衛福部爬蟲
更新頻率	每年	每月
疾病數	8	100+
自動化	手動	自動
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/services/crawler/medical_cost_crawler.py	新增	爬蟲
backend/app/services/crawler/medical_cost_parser.py	新增	解析
backend/app/workers/medical_cost_worker.py	新增	Worker
backend/app/api/v1/admin_medical.py	修改	加入爬蟲觸發
backend/tests/unit/test_medical_cost_crawler.py	新增	測試
1. 目標
建立醫療費用爬蟲（衛福部公開資料）。

2. 前置條件
□ MVP P11 完成
□ 衛福部爬蟲目標 URL 已確認
3. 前端畫面
沿用 MVP P11 MedicalCostsView，加入「重新爬取」按鈕。

3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  💊 醫療費用管理  [重新爬取]         │
├─────────────────────────────────────┤
│  最近更新：2026-09-01（衛福部）      │
│  疾病數：127                         │
│                                     │
│  [檢視] [編輯]                       │
└─────────────────────────────────────┘
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
POST	/api/v1/admin/medical-costs/crawl	觸發爬蟲
GET	/api/v1/admin/medical-costs/crawl/status	狀態
4.2 請求/回應範例
POST /api/v1/admin/medical-costs/crawl：

json
{
  "source": "mohw",
  "force": false
}
回應：

json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "status": "running"
  }
}
4.3 資料庫變更
擴充 medical_cost_references：

sql
ALTER TABLE medical_cost_references
ADD COLUMN source_url TEXT,
ADD COLUMN crawled_at TIMESTAMP;
4.4 環境變數
變數	說明
MOHW_CRAWL_URL	衛福部 URL
MOHW_CRAWL_SCHEDULE	0 3 1 * * （每月 1 日 03:00）
5. 單元測試
python
def test_medical_cost_crawler_parses_data(mock_response):
    mock_response.return_value = MOCK_MOHW_HTML
    result = crawler.crawl()
    assert len(result) > 0
    assert "disease_code" in result[0]
    assert "cost_min" in result[0]

def test_medical_cost_deduplication():
    # 爬取兩次，不應重複
    crawler.crawl()
    crawler.crawl()
    count = db.query(MedicalCostReference).filter_by(disease_code="HEART_SURGERY").count()
    assert count == 1
6. 驗收標準
□ 衛福部爬蟲運作
□ 100+ 疾病
□ 每月自動更新
□ 去重邏輯正確
□ 管理員可手動觸發
□ 單元測試 ≥ 80%
7. 交付物清單
（略）


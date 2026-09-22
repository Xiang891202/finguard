Phase 7：爬蟲調度 + 三源驗證
版本：v1.0
所屬：MVP
依賴 Phase：P3, P5, P6
預計工時：5 天

⚠️ 本 Phase 的 MVP/完整版約束
MVP：手動觸發（非自動排程）

支援三源驗證（Level 1/2/3）

DATA_CONFLICT 觸發 Incident

📂 前置檔案檢查
檔案路徑	來源
docs/01-framework/01-shared-framework.md	第一批
docs/02-reference/01-database-schema.md	第二批
docs/03-mvp/phase-03-holdings.md	第三批
docs/03-mvp/phase-05-forex.md	第三批
docs/03-mvp/phase-06-money-market.md	第三批
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/crawler.py	新增	爬蟲端點
backend/app/services/crawler/dispatcher.py	新增	調度器
backend/app/services/crawler/normalizer.py	新增	正規化
backend/app/services/crawler/validator.py	新增	驗證
backend/app/services/crawler/data_cleaner.py	新增	清理
backend/app/workers/crawl_worker.py	新增	Celery Worker
frontend/src/views/admin/CrawlerView.vue	新增	管理員爬蟲頁
frontend/src/api/crawler.js	新增	API
backend/tests/unit/test_normalizer.py	新增	測試
backend/tests/unit/test_validator.py	新增	測試
backend/tests/unit/test_dispatcher.py	新增	測試
backend/tests/integration/test_crawler_flow.py	新增	整合
1. 目標
建立爬蟲調度與三源驗證機制。

2. 前置條件
□ P3, P5, P6 完成
□ Redis 已就緒
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
CrawlerView	/admin/crawler	手動觸發爬蟲
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  🕷️ 爬蟲管理                         │
├─────────────────────────────────────┤
│  類別：[全部 ▼]                      │
│  [ 立即執行 ]                        │
├─────────────────────────────────────┤
│  最近執行：                          │
│  2026-09-21 10:05                    │
│  ✅ 成功 5 / 失敗 0 / 衝突 0         │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
CrawlerView.vue
├── CrawlerTrigger.vue
├── CrawlerStatus.vue
└── CrawlerHistory.vue
3.4 樣式規範
沿用 P2。

3.5 響應式設計
裝置	佈局
電腦	雙欄
平板	單欄
手機	單欄
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
POST	/api/v1/app/crawler/trigger	觸發爬蟲
GET	/api/v1/app/crawler/status/{task_id}	查詢狀態
4.2 請求/回應範例
POST /api/v1/app/crawler/trigger：

json
{
  "asset_class": "equity",
  "force": false
}
回應：

json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "status": "running",
    "assets_count": 5
  }
}
4.3 資料庫變更
使用表：market_prices, market_snapshots

4.4 環境變數
變數	說明
REDIS_URL	Celery Broker
CRAWL_TOLERANCE_PCT	容忍差異 % (預設 0.5)
5. 單元測試
5.1 後端測試
python
# tests/unit/test_validator.py
def test_level_1_all_match():
    result = validator.validate([100.0, 100.1, 99.9], tolerance=0.5)
    assert result["level"] == "LEVEL_1"
    assert 99.9 <= result["value"] <= 100.1

def test_level_2_one_outlier():
    result = validator.validate([100.0, 100.1, 150.0], tolerance=0.5)
    assert result["level"] == "LEVEL_2"
    assert result["excluded_source"] == "source_c"

def test_level_3_conflict():
    result = validator.validate([100.0, 120.0, 140.0], tolerance=0.5)
    assert result["level"] == "LEVEL_3"
    assert result["status"] == "DATA_CONFLICT"
5.2 前端測試
javascript
// tests/CrawlerView.spec.js
describe('CrawlerView', () => {
  it('triggers crawl on button click', async () => {
    const wrapper = mount(CrawlerView)
    await wrapper.find('[data-testid="trigger-btn"]').trigger('click')
    expect(wrapper.emitted('trigger')).toBeTruthy()
  })
})
5.3 整合測試
python
# tests/integration/test_crawler_flow.py
@patch("app.handlers.equity_handler.get_stock_price")
def test_full_crawl_flow(mock_price, auth_admin_client):
    mock_price.side_effect = [100.0, 100.1, 99.9]  # 三源
    response = auth_admin_client.post("/api/v1/app/crawler/trigger", json={
        "asset_class": "equity"
    })
    task_id = response.json()["data"]["task_id"]
    
    # 等待完成
    time.sleep(1)
    response = auth_admin_client.get(f"/api/v1/app/crawler/status/{task_id}")
    assert response.json()["data"]["status"] == "completed"
6. 驗收標準
□ 手動觸發爬蟲
□ 三源驗證 Level 1/2/3 正確
□ DATA_CONFLICT 觸發 Incident
□ STALE 標記正確
□ 管理員可查看歷史
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
（略）
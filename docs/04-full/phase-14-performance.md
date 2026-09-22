Full Phase 14：效能優化
版本：v1.0
所屬：完整版
依賴 MVP Phase：全部
預計工時：5 天

🔗 依賴 MVP 哪個 Phase
依賴所有 MVP Phase：需完整系統

🔄 與 MVP 的差異
項目	MVP	完整版
API 回應	未優化	< 200ms
快取	無	Redis
索引	基本	最佳化
N+1 查詢	可能有	無
分頁	基本	Cursor
CDN	無	Cloudflare
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/core/cache.py	新增	Redis 快取
backend/app/middleware/timing.py	新增	效能監控
backend/app/db/indexes.sql	新增	索引優化
frontend/vite.config.js	修改	建置優化
backend/tests/performance/	新增	效能測試
1. 目標
優化系統效能至 API < 200ms。

2. 前置條件
□ MVP 完成
3. 前端畫面
無新增頁面。

4. 後端邏輯
4.1 API 端點
沿用。

4.2 請求/回應範例
沿用。

4.3 資料庫變更
新增複合索引：

sql
CREATE INDEX idx_holdings_model_asset ON holdings(model_id, asset_definition_id);
CREATE INDEX idx_market_snapshots_date_symbol ON market_snapshots(snapshot_date DESC, symbol);
CREATE INDEX idx_forecast_runs_user_date ON forecast_runs(user_id, generated_at DESC);
4.4 環境變數
變數	說明
REDIS_CACHE_TTL	快取 TTL (300)
SLOW_QUERY_THRESHOLD	慢查詢閾值 (100ms)
5. 單元測試
5.3 效能測試
python
def test_api_response_time(benchmark):
    result = benchmark(lambda: client.get("/api/v1/app/models"))
    assert result.stats.mean < 0.2  # 200ms
6. 驗收標準
□ API 平均 < 200ms
□ Redis 快取生效
□ 無 N+1 查詢
□ 索引優化完成
□ CDN 設定
□ 效能測試通過
7. 交付物清單
（略）
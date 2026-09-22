Phase 5：外匯（ForexHandler）
版本：v1.0
所屬：MVP
依賴 Phase：P3
預計工時：3 天

⚠️ 本 Phase 的 MVP/完整版約束
MVP：實作 ForexHandler

支援 USD/TWD、JPY/TWD 等

📂 前置檔案檢查
檔案路徑	來源
docs/02-reference/01-database-schema.md	第二批
docs/03-mvp/phase-03-holdings.md	第三批
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/handlers/forex_handler.py	新增	外匯處理器
backend/app/services/asset_service.py	修改	支援外匯
backend/tests/unit/test_forex_handler.py	新增	Handler 測試
backend/app/db/seeds/forex_assets.py	新增	Seed 外匯
1. 目標
實作 ForexHandler，支援外匯資產。

2. 前置條件
□ P3 完成
3. 前端畫面
3.1 頁面清單
沿用 HoldingsView（透過 asset_class 篩選外匯）。

3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  📈 持有部位                         │
│  類別：[外匯 ▼]                      │
├─────────────────────────────────────┤
│  USD/TWD 美元兌台幣                  │
│  10,000 USD @ 31.50                  │
│  現值：315,200 TWD                   │
└─────────────────────────────────────┘
3.3 Vue 元件結構
（沿用 P3 的元件）

狀態管理：新增 useForex Composable

3.4 樣式規範
沿用 P3。

3.5 響應式設計
沿用 P3。

4. 後端邏輯
4.1 API 端點
（沿用 P3，透過 asset_class 篩選）

4.2 請求/回應範例
POST /api/v1/app/holdings（外匯）：

json
{
  "model_id": "uuid",
  "asset_definition_id": "usd-twd-uuid",
  "quantity": 10000,
  "average_cost": 31.50
}
4.3 資料庫變更
新增 Seed 資料：

sql
INSERT INTO asset_definitions (asset_class_id, symbol, display_name, source_config)
SELECT 
    (SELECT id FROM asset_classes WHERE code = 'forex'),
    'JPY/TWD',
    '日元兌台幣',
    '{"primary": {"provider": "cbc", "pair": "JPY/TWD"}}'::jsonb;
4.4 環境變數
無新增。

5. 單元測試
5.1 後端測試
python
# tests/unit/test_forex_handler.py
@patch("app.handlers.forex_handler.get_forex_rate")
def test_forex_fetch_price(mock_rate):
    mock_rate.return_value = 32.45
    handler = ForexHandler({
        "symbol": "USD/TWD",
        "source_config": {"primary": {"provider": "cbc", "pair": "USD/TWD"}}
    })
    price = handler.fetch_price("2026-09-21")
    assert price == 32.45

@patch("app.handlers.forex_handler.get_forex_rate")
def test_forex_fallback(mock_rate):
    mock_rate.side_effect = [Exception("primary failed"), 32.50]
    handler = ForexHandler({
        "symbol": "USD/TWD",
        "source_config": {
            "primary": {"provider": "cbc"},
            "fallbacks": [{"provider": "cnyes"}]
        }
    })
    price = handler.fetch_price("2026-09-21")
    assert price == 32.50
5.2 前端測試
（沿用 P3）

5.3 整合測試
python
def test_forex_holding_crud(auth_client, test_model, test_usd_twd):
    response = auth_client.post("/api/v1/app/holdings", json={
        "model_id": test_model["id"],
        "asset_definition_id": test_usd_twd["id"],
        "quantity": 10000,
        "average_cost": 31.50
    })
    assert response.status_code == 201
6. 驗收標準
□ ForexHandler 實作完成
□ ForexHandler 單元測試通過（含 fallback）
□ 外匯 Seed 資料建立
□ 可透過 HoldingsView 管理
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
（略）
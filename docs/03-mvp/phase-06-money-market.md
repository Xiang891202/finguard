Phase 6：貨幣基金（MoneyMarketHandler）
版本：v1.0
所屬：MVP
依賴 Phase：P3
預計工時：2 天

⚠️ 本 Phase 的 MVP/完整版約束
MVP：實作 MoneyMarketHandler

貨幣基金淨值變動極小，可手動或低頻更新

📂 前置檔案檢查
檔案路徑	來源
docs/02-reference/01-database-schema.md	第二批
docs/03-mvp/phase-03-holdings.md	第三批
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/handlers/money_market_handler.py	新增	貨幣基金處理器
backend/tests/unit/test_money_market_handler.py	新增	Handler 測試
backend/app/db/seeds/money_market_assets.py	新增	Seed
1. 目標
實作 MoneyMarketHandler，支援貨幣基金。

2. 前置條件
□ P3 完成
3. 前端畫面
沿用 HoldingsView。

4. 後端邏輯
4.1 API 端點
沿用 P3。

4.2 請求/回應範例
同 P5。

4.3 資料庫變更
Seed 資料：

sql
INSERT INTO asset_definitions (asset_class_id, symbol, display_name, source_config)
SELECT 
    (SELECT id FROM asset_classes WHERE code = 'money_market'),
    'USD_MMF',
    '美元貨幣基金',
    '{"primary": {"provider": "manual", "nav": 1.0}}'::jsonb;
4.4 環境變數
無新增。

5. 單元測試
5.1 後端測試
python
# tests/unit/test_money_market_handler.py
def test_mmf_fixed_volatility():
    handler = MoneyMarketHandler({...})
    volatility = handler.calculate_volatility()
    assert volatility == 0.015  # 固定低波動率

def test_mmf_fetch_price_from_config():
    handler = MoneyMarketHandler({
        "source_config": {"primary": {"provider": "manual", "nav": 1.0}}
    })
    price = handler.fetch_price("2026-09-21")
    assert price == 1.0
5.2 前端測試
沿用 P3。

5.3 整合測試
同 P5 格式。

6. 驗收標準
□ MoneyMarketHandler 實作完成
□ 固定低波動率正確
□ Seed 資料建立
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
（略）
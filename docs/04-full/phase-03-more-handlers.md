Full Phase 3：更多 Handler（Bond / Metal / Crypto）
版本：v1.0
所屬：完整版
依賴 MVP Phase：MVP P3（Handler 基礎）
預計工時：6 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P3：BaseAssetHandler 已建立

依賴 MVP P5, P6：ForexHandler、MoneyMarketHandler 已實作

🔄 與 MVP 的差異
項目	MVP	完整版
Handler 數	3 個	6 個
BondHandler	❌	✅
MetalHandler	❌	✅
CryptoHandler	❌	✅
外部 API	無	Yahoo Finance / CoinGecko
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/handlers/bond_handler.py	新增	債券
backend/app/handlers/metal_handler.py	新增	貴金屬
backend/app/handlers/crypto_handler.py	新增	虛擬貨幣
backend/app/db/seeds/bond_assets.py	新增	Seed
backend/app/db/seeds/metal_assets.py	新增	Seed
backend/app/db/seeds/crypto_assets.py	新增	Seed
backend/tests/unit/test_bond_handler.py	新增	測試
backend/tests/unit/test_metal_handler.py	新增	測試
backend/tests/unit/test_crypto_handler.py	新增	測試
1. 目標
實作 BondHandler、MetalHandler、CryptoHandler。

2. 前置條件
□ MVP P3, P5, P6 完成
□ Yahoo Finance API 已設定
□ CoinGecko API 已設定
3. 前端畫面
沿用 HoldingsView（透過 asset_class 篩選）。

3.3 Vue 元件結構
沿用 MVP P3。

4. 後端邏輯
4.1 API 端點
沿用 MVP P3。

4.2 請求/回應範例
POST /api/v1/app/holdings（債券）：

json
{
  "model_id": "uuid",
  "asset_definition_id": "us-treasury-uuid",
  "quantity": 10000,
  "average_cost": 100.0
}
4.3 資料庫變更
新增 Seed：

sql
-- 債券
INSERT INTO asset_definitions (asset_class_id, symbol, display_name, source_config)
SELECT (SELECT id FROM asset_classes WHERE code = 'bond'),
    'US10Y',
    '美國 10 年期公債',
    '{"primary": {"provider": "yfinance", "ticker": "^TNX"}}'::jsonb;

-- 貴金屬
INSERT INTO asset_definitions (asset_class_id, symbol, display_name, source_config)
SELECT (SELECT id FROM asset_classes WHERE code = 'metal'),
    'XAU/USD',
    '黃金',
    '{"primary": {"provider": "yfinance", "ticker": "GC=F"}}'::jsonb;

-- 虛擬貨幣
INSERT INTO asset_definitions (asset_class_id, symbol, display_name, source_config)
SELECT (SELECT id FROM asset_classes WHERE code = 'crypto'),
    'BTC-USD',
    '比特幣',
    '{"primary": {"provider": "coingecko", "coin_id": "bitcoin"}}'::jsonb;
4.4 環境變數
變數	說明
COINGECKO_API_KEY	CoinGecko API Key
5. 單元測試
5.1 後端測試
python
# tests/unit/test_bond_handler.py
@patch("app.handlers.bond_handler.get_bond_price")
def test_bond_fetch_price(mock_price):
    mock_price.return_value = 98.5
    handler = BondHandler({"symbol": "US10Y", ...})
    assert handler.fetch_price("2026-09-21") == 98.5

def test_bond_volatility():
    handler = BondHandler({...})
    assert handler.calculate_volatility() == 0.05

# tests/unit/test_crypto_handler.py
def test_crypto_validate_price_zero():
    handler = CryptoHandler({...})
    # 虛擬貨幣允許 0（放寬驗證）
    assert handler.validate_price(0) is True

def test_crypto_high_volatility():
    handler = CryptoHandler({...})
    assert handler.calculate_volatility() == 0.65
5.2 前端測試
（略）

5.3 整合測試
python
def test_all_handlers_registered():
    from app.services.crawler.handler_registry import get_all_handlers
    handlers = get_all_handlers()
    assert "EquityHandler" in handlers
    assert "ForexHandler" in handlers
    assert "MoneyMarketHandler" in handlers
    assert "BondHandler" in handlers
    assert "MetalHandler" in handlers
    assert "CryptoHandler" in handlers
6. 驗收標準
□ BondHandler 實作完成
□ MetalHandler 實作完成
□ CryptoHandler 實作完成
□ 每個 Handler 有獨立單元測試
□ Seed 資料建立
□ 可透過 HoldingsView 管理
□ 單元測試 ≥ 80%
7. 交付物清單
（略）


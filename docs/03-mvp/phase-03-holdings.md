Phase 3：持有部位（EquityHandler）
版本：v1.0
所屬：MVP
依賴 Phase：P2
預計工時：4 天

⚠️ 本 Phase 的 MVP/完整版約束
MVP：僅實作 EquityHandler

支援股票（0050.TW 等）

未接爬蟲（價格先用手動輸入或假資料）

📂 前置檔案檢查
檔案路徑	來源
docs/01-framework/01-shared-framework.md	第一批
docs/02-reference/01-database-schema.md	第二批
docs/02-reference/02-api-spec.md	第二批
docs/03-mvp/phase-02-models.md	第三批
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/holdings.py	新增	持有部位 CRUD
backend/app/api/v1/assets.py	新增	資產類別 / 標的查詢
backend/app/services/holding_service.py	新增	持有部位邏輯
backend/app/services/asset_service.py	新增	資產查詢
backend/app/handlers/base_handler.py	新增	Handler 抽象類
backend/app/handlers/equity_handler.py	新增	股票處理器
backend/app/schemas/holding.py	新增	DTO
frontend/src/views/app/HoldingsView.vue	新增	持有部位頁
frontend/src/components/holdings/HoldingList.vue	新增	列表
frontend/src/components/holdings/HoldingForm.vue	新增	表單
frontend/src/components/holdings/AssetSelector.vue	新增	資產選擇
frontend/src/api/holdings.js	新增	API
frontend/src/api/assets.js	新增	API
frontend/src/stores/holdings.js	新增	Store
backend/tests/unit/test_equity_handler.py	新增	Handler 測試
backend/tests/unit/test_holding_service.py	新增	服務測試
backend/tests/integration/test_holdings_crud.py	新增	整合
frontend/tests/HoldingForm.spec.js	新增	前端測試
1. 目標
建立持有部位系統，實作 EquityHandler，支援股票 CRUD。

2. 前置條件
□ P2 完成
□ asset_classes 與 asset_definitions 已 Seed
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
HoldingsView	/app/holdings?model_id=uuid	持有部位管理
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  📈 持有部位         [+ 新增]        │
├─────────────────────────────────────┤
│  模型：[我的家庭財務 ▼]              │
│  類別：[全部 ▼]                      │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │ 0050.TW 元大台灣50             │  │
│  │ 100 股 @ 150.50                │  │
│  │ 現值：15,520                   │  │
│  │ 損益：+470 (+3.1%)             │  │
│  │ [編輯] [刪除]                  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
HoldingsView.vue
├── ModelSelector.vue（共用）
├── AssetClassFilter.vue
├── HoldingList.vue
│   └── HoldingCard.vue
├── HoldingForm.vue（Modal）
│   ├── AssetSelector.vue
│   │   ├── BaseInput.vue（搜尋）
│   │   └── AssetList.vue
│   ├── BaseInput.vue（數量）
│   └── BaseInput.vue（成本）
└── DeleteConfirmModal.vue
元件職責：

元件	職責	Props	Emits
HoldingsView	頁面	-	-
HoldingList	列表	holdings: Array	edit, delete
HoldingCard	卡片	holding: Object	edit, delete
HoldingForm	表單	holding?: Object	submit, cancel
AssetSelector	資產選擇	assetClass?: String	select
狀態管理：

類型	檔案	用途
Store	stores/holdings.js	持有部位
Composable	composables/useHoldings.js	API 邏輯
3.4 樣式規範
沿用 P2 風格

3.5 響應式設計
裝置	佈局
電腦	表格 + 側欄
平板	卡片列表
手機	卡片列表，全寬
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/app/assets/classes	資產類別列表
GET	/api/v1/app/assets/definitions	資產標的列表
GET	/api/v1/app/holdings	持有部位列表
POST	/api/v1/app/holdings	新增
PUT	/api/v1/app/holdings/{id}	更新
DELETE	/api/v1/app/holdings/{id}	刪除
4.2 請求/回應範例
POST /api/v1/app/holdings：

json
{
  "model_id": "uuid",
  "asset_definition_id": "uuid",
  "quantity": 100,
  "average_cost": 150.50
}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "asset": {
      "symbol": "0050.TW",
      "display_name": "元大台灣50",
      "asset_class": "equity"
    },
    "quantity": 100,
    "average_cost": 150.50,
    "current_price": 155.20,
    "current_value": 15520.00,
    "unrealized_gain": 470.00
  }
}
4.3 資料庫變更
使用表：holdings, asset_classes, asset_definitions

4.4 環境變數
無新增。

5. 單元測試
5.1 後端測試
python
# tests/unit/test_equity_handler.py
def test_equity_handler_fetch_price(mock_yfinance):
    handler = EquityHandler({
        "symbol": "0050.TW",
        "source_config": {"primary": {"provider": "twse"}}
    })
    mock_yfinance.return_value = 155.20
    price = handler.fetch_price("2026-09-21")
    assert price == 155.20

def test_equity_handler_validate_price():
    handler = EquityHandler({...})
    assert handler.validate_price(155.20) is True
    assert handler.validate_price(-1) is False
5.2 前端測試
javascript
// tests/HoldingForm.spec.js
describe('HoldingForm', () => {
  it('validates quantity is positive', async () => {
    const wrapper = mount(HoldingForm)
    await wrapper.find('[name="quantity"]').setValue(-1)
    await wrapper.find('form').trigger('submit')
    expect(wrapper.text()).toContain('數量必須大於 0')
  })
})
5.3 整合測試
python
# tests/integration/test_holdings_crud.py
def test_holdings_crud(auth_client, test_model, test_asset):
    response = auth_client.post("/api/v1/app/holdings", json={
        "model_id": test_model["id"],
        "asset_definition_id": test_asset["id"],
        "quantity": 100,
        "average_cost": 150.50
    })
    assert response.status_code == 201
6. 驗收標準
□ 持有部位 CRUD 完整
□ EquityHandler 實作完成
□ EquityHandler 單元測試通過
□ 資產下拉選擇可用
□ 損益計算正確
□ 響應式設計
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
（略，格式同 P1）
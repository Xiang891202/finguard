Full Phase 2：資產類別 + 標的管理（CRUD）
版本：v1.0
所屬：完整版
依賴 MVP Phase：MVP P3（資產查詢）
預計工時：6 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P3：資產類別 / 標的查詢已存在

依賴 MVP P0：asset_classes, asset_definitions 表已建立

🔄 與 MVP 的差異
項目	MVP	完整版
管理員頁面	唯讀清單	完整 CRUD
新增資產標的	需 Seed	管理員 UI 新增
新增資產類別	需寫程式	管理員 UI 新增（若有 Handler）
動態載入驗證	無	有（驗證 Handler 存在）
source_config 驗證	無	JSON Schema 驗證
📂 前置檔案檢查
（略）

📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/admin_assets.py	新增	資產管理 CRUD
backend/app/services/asset_admin_service.py	新增	邏輯
backend/app/services/crawler/handler_registry.py	新增	Handler 註冊表
backend/app/schemas/asset_admin.py	新增	DTO
backend/app/utils/source_config_validator.py	新增	驗證器
frontend/src/views/admin/AssetClassesView.vue	修改	加入 CRUD
frontend/src/views/admin/AssetDefinitionsView.vue	修改	加入 CRUD
frontend/src/components/admin/AssetClassForm.vue	新增	表單
frontend/src/components/admin/AssetDefinitionForm.vue	新增	表單
frontend/src/components/admin/SourceConfigEditor.vue	新增	source_config 編輯
backend/tests/unit/test_asset_admin_service.py	新增	測試
1. 目標
提供管理員完整的資產類別 / 標的 CRUD，並驗證 Handler 存在與 source_config 格式。

2. 前置條件
□ MVP P3 完成
□ Handler 策略模式已實作
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
AssetClassesView	/admin/asset-classes	類別 CRUD
AssetDefinitionsView	/admin/asset-definitions	標的 CRUD
3.2 UI 草圖
AssetDefinitionsView：

text
┌─────────────────────────────────────┐
│  📦 資產標的管理     [+ 新增]        │
├─────────────────────────────────────┤
│  類別：[全部 ▼]                      │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │ 0050.TW                        │  │
│  │ 元大台灣50 | equity            │  │
│  │ source: twse + yfinance + cnyes│  │
│  │ [編輯] [停用]                  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
AssetDefinitionsView.vue
├── AssetDefinitionList.vue
├── AssetDefinitionForm.vue（Modal）
│   ├── BaseSelect.vue（類別）
│   ├── BaseInput.vue（symbol）
│   └── SourceConfigEditor.vue
│       ├── PrimarySourceForm.vue
│       ├── FallbackSourceList.vue
│       └── ValidationConfigForm.vue
3.4 樣式規範
沿用 MVP 管理員頁面風格。

3.5 響應式設計
裝置	佈局
電腦	表格
平板	卡片
手機	單欄
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/admin/asset-classes	列表
POST	/api/v1/admin/asset-classes	新增
PUT	/api/v1/admin/asset-classes/{id}	更新
DELETE	/api/v1/admin/asset-classes/{id}	刪除（軟）
GET	/api/v1/admin/asset-definitions	列表
POST	/api/v1/admin/asset-definitions	新增
PUT	/api/v1/admin/asset-definitions/{id}	更新
DELETE	/api/v1/admin/asset-definitions/{id}	刪除（軟）
GET	/api/v1/admin/handlers	可用 Handler 列表
4.2 請求/回應範例
POST /api/v1/admin/asset-definitions：

json
{
  "asset_class_id": "uuid",
  "symbol": "JPY/TWD",
  "display_name": "日元兌台幣",
  "currency": "TWD",
  "source_config": {
    "primary": {"provider": "cbc", "pair": "JPY/TWD"},
    "fallbacks": [{"provider": "cnyes", "pair": "JPYTWD"}],
    "validation": {"tolerance_pct": 0.5, "min_sources": 2}
  }
}
錯誤（Handler 不存在）：

json
{
  "success": false,
  "error": {
    "code": "HANDLER_NOT_FOUND",
    "message": "資產類別對應的 Handler 不存在"
  }
}
4.3 資料庫變更
使用表：asset_classes, asset_definitions

4.4 環境變數
無新增。

5. 單元測試
5.1 後端測試
python
# tests/unit/test_asset_admin_service.py
def test_create_asset_definition_valid_handler():
    # 外匯類別有 ForexHandler
    result = service.create_definition({
        "asset_class_id": "forex-uuid",
        "symbol": "JPY/TWD",
        "source_config": {...}
    })
    assert result["symbol"] == "JPY/TWD"

def test_create_asset_definition_no_handler():
    # 新增類別但無 Handler
    with pytest.raises(HandlerNotFoundError):
        service.create_definition({
            "asset_class_id": "new-class-uuid",
            "symbol": "XYZ",
            "source_config": {...}
        })

def test_source_config_validation():
    with pytest.raises(ValidationError):
        service.create_definition({
            "symbol": "TEST",
            "source_config": {"primary": "invalid"}
        })
5.2 前端測試
javascript
describe('SourceConfigEditor', () => {
  it('adds fallback source', async () => {
    const wrapper = mount(SourceConfigEditor)
    await wrapper.find('[data-testid="add-fallback"]').trigger('click')
    expect(wrapper.findAll('[data-testid="fallback-row"]').length).toBe(2)
  })
})
5.3 整合測試
python
def test_asset_definition_crud(auth_admin_client):
    # 新增
    response = auth_admin_client.post("/api/v1/admin/asset-definitions", json={...})
    assert response.status_code == 201
    asset_id = response.json()["data"]["id"]
    
    # 更新
    response = auth_admin_client.put(f"/api/v1/admin/asset-definitions/{asset_id}", json={...})
    assert response.status_code == 200
    
    # 刪除
    response = auth_admin_client.delete(f"/api/v1/admin/asset-definitions/{asset_id}")
    assert response.status_code == 200
6. 驗收標準
□ 類別 CRUD 完整
□ 標的 CRUD 完整
□ Handler 存在驗證
□ source_config 格式驗證
□ 軟刪除
□ 響應式設計
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
（略）
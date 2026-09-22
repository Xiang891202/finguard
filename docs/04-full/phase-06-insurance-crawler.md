Full Phase 6：保險商品爬蟲
版本：v1.0
所屬：完整版
依賴 MVP Phase：MVP P8（保險保單）
預計工時：8 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P7：爬蟲調度框架

依賴 MVP P8：insurance_products 表已建立

🔄 與 MVP 的差異
項目	MVP	完整版
保險商品	無	雙源爬蟲
來源	-	Finfo + 官網
生命週期	-	上架 / 改版 / 下架
資料量	0	數百筆
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/handlers/insurance_handler.py	新增	保險爬蟲基礎
backend/app/services/crawler/insurance_crawler.py	新增	爬蟲
backend/app/services/crawler/insurance_validator.py	新增	雙源比對
backend/app/services/insurance/product_service.py	新增	商品邏輯
backend/app/services/insurance/lifecycle_service.py	新增	生命週期
backend/app/workers/insurance_crawl_worker.py	新增	Worker
frontend/src/views/admin/InsuranceProductsView.vue	新增	商品管理
backend/tests/unit/test_insurance_validator.py	新增	測試
backend/tests/integration/test_insurance_crawl.py	新增	整合
1. 目標
建立保險商品雙源爬蟲與生命週期管理。

2. 前置條件
□ MVP P7, P8 完成
□ Finfo 爬蟲已設定
□ 保險公司官網爬蟲已設定
3. 前端畫面
3.1 頁面清單
頁面	路由
InsuranceProductsView	/admin/insurance-products
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  🛡️ 保險商品     [重新爬取]         │
├─────────────────────────────────────┤
│  類別：[全部 ▼] 狀態：[已上架 ▼]    │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │ XX 終身醫療險                  │  │
│  │ XX 人壽 | 疾病險 | 上架        │  │
│  │ 來源：Finfo ✅ | 官網 ✅       │  │
│  │ [檢視] [下架]                  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
InsuranceProductsView.vue
├── ProductFilter.vue
├── ProductList.vue
│   └── ProductCard.vue
└── ProductDetailModal.vue
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/admin/insurance-products	列表
POST	/api/v1/admin/insurance-products/crawl	觸發爬蟲
GET	/api/v1/admin/insurance-products/{id}	詳情
GET	/api/v1/admin/insurance-products/{id}/history	生命週期
PUT	/api/v1/admin/insurance-products/{id}/deactivate	下架
4.2 請求/回應範例
GET /api/v1/admin/insurance-products：

json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "product_code": "XX-MED-001",
      "product_name": "XX 終身醫療險",
      "insurer_name": "XX 人壽",
      "category": "life",
      "subcategory": "disease",
      "covered_body_parts": ["heart", "brain"],
      "is_active": true,
      "sources": ["finfo", "official"]
    }
  ]
}
4.3 資料庫變更
使用表：insurance_products, insurance_products_history

4.4 環境變數
變數	說明
FINFO_CRAWL_ENABLED	true
OFFICIAL_CRAWL_ENABLED	true
5. 單元測試
5.1 後端測試
python
# tests/unit/test_insurance_validator.py
def test_double_source_match():
    result = validator.validate(
        finfo={"product_name": "XX 醫療險", "coverage": 1000000},
        official={"product_name": "XX 醫療險", "coverage": 1000000}
    )
    assert result["status"] == "MATCH"

def test_double_source_conflict():
    result = validator.validate(
        finfo={"coverage": 1000000},
        official={"coverage": 1500000}
    )
    assert result["status"] == "CONFLICT"
5.2 前端測試
（略）

5.3 整合測試
python
def test_insurance_crawl_flow(auth_admin_client, mock_finfo, mock_official):
    response = auth_admin_client.post("/api/v1/admin/insurance-products/crawl")
    assert response.status_code == 200
    # 驗證商品已寫入
    products = db.query(InsuranceProduct).all()
    assert len(products) > 0
6. 驗收標準
□ Finfo 爬蟲運作
□ 官網爬蟲運作
□ 雙源比對
□ 生命週期記錄（上架 / 改版 / 下架）
□ 已下架商品不推薦
□ 管理員可查看商品
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
（略）
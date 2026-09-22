Phase 4：負債
版本：v1.0
所屬：MVP
依賴 Phase：P2
預計工時：2 天

⚠️ 本 Phase 的 MVP/完整版約束
MVP：支援房貸、車貸、信用卡、學貸、其他

📂 前置檔案檢查
檔案路徑	來源
docs/02-reference/01-database-schema.md	第二批
docs/03-mvp/phase-02-models.md	第三批
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/liabilities.py	新增	負債 CRUD
backend/app/services/liability_service.py	新增	邏輯
backend/app/schemas/liability.py	新增	DTO
frontend/src/views/app/LiabilitiesView.vue	新增	頁面
frontend/src/components/liabilities/LiabilityList.vue	新增	列表
frontend/src/components/liabilities/LiabilityForm.vue	新增	表單
frontend/src/api/liabilities.js	新增	API
frontend/src/stores/liabilities.js	新增	Store
backend/tests/unit/test_liability_service.py	新增	測試
backend/tests/integration/test_liabilities_crud.py	新增	整合
1. 目標
提供負債的完整 CRUD。

2. 前置條件
□ P2 完成
3. 前端畫面
3.1 頁面清單
頁面	路由
LiabilitiesView	/app/liabilities?model_id=uuid
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  💳 負債            [+ 新增]         │
├─────────────────────────────────────┤
│  模型：[我的家庭財務 ▼]              │
├─────────────────────────────────────┤
│  房貸                                │
│  總額 1000 萬 | 剩餘 800 萬          │
│  利率 1.85% | 月付 45,000            │
│  [編輯] [刪除]                       │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
LiabilitiesView.vue
├── ModelSelector.vue
├── LiabilityList.vue
│   └── LiabilityCard.vue
└── LiabilityForm.vue（Modal）
    ├── BaseSelect.vue（類型）
    ├── BaseInput.vue（金額）
    └── BaseButton.vue
3.4 樣式規範
沿用 P2。

3.5 響應式設計
裝置	佈局
電腦	卡片列表 2 欄
平板	卡片列表
手機	全寬卡片
4. 後端邏輯
4.1 API 端點
方法	路徑
GET	/api/v1/app/liabilities
POST	/api/v1/app/liabilities
PUT	/api/v1/app/liabilities/{id}
DELETE	/api/v1/app/liabilities/{id}
4.2 請求/回應範例
POST /api/v1/app/liabilities：

json
{
  "model_id": "uuid",
  "name": "房貸",
  "liability_type": "mortgage",
  "total_amount": 10000000,
  "remaining_amount": 8000000,
  "interest_rate": 0.0185,
  "monthly_payment": 45000
}
4.3 資料庫變更
使用表：liabilities

4.4 環境變數
無新增。

5. 單元測試
5.1 後端測試
python
# tests/unit/test_liability_service.py
def test_create_liability():
    result = service.create(user_id, {...})
    assert result["name"] == "房貸"

def test_remaining_cannot_exceed_total():
    with pytest.raises(ValueError):
        service.create(user_id, {"total_amount": 100, "remaining_amount": 200})
5.2 前端測試
（略）

5.3 整合測試
python
def test_liabilities_crud(auth_client, test_model):
    response = auth_client.post("/api/v1/app/liabilities", json={...})
    assert response.status_code == 201
6. 驗收標準
□ 負債 CRUD 完整
□ 剩餘金額不可超過總額
□ 響應式設計
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
（略，格式同 P1）
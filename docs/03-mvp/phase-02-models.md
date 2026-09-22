Phase 2：財務模型 + 金庫
版本：v1.0
所屬：MVP
依賴 Phase：P1
預計工時：4 天

⚠️ 本 Phase 的 MVP/完整版約束
MVP：一般用戶最多 2 個模型

管理員：10 個

軟刪除（is_archived）

📂 前置檔案檢查
檔案路徑	來源
docs/01-framework/01-shared-framework.md	第一批
docs/02-reference/01-database-schema.md	第二批
docs/02-reference/02-api-spec.md	第二批
docs/03-mvp/phase-01-auth.md	第三批
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/models.py	新增	模型 CRUD
backend/app/api/v1/vaults.py	新增	金庫 CRUD
backend/app/services/model_service.py	新增	模型邏輯
backend/app/services/vault_service.py	新增	金庫邏輯
backend/app/services/base_service.py	新增	共用分頁
backend/app/schemas/model.py	新增	模型 DTO
backend/app/schemas/vault.py	新增	金庫 DTO
frontend/src/views/app/ModelsView.vue	新增	模型頁
frontend/src/views/app/VaultsView.vue	新增	金庫頁
frontend/src/components/models/ModelList.vue	新增	模型列表
frontend/src/components/models/ModelForm.vue	新增	模型表單
frontend/src/components/vaults/VaultList.vue	新增	金庫列表
frontend/src/components/vaults/VaultForm.vue	新增	金庫表單
frontend/src/api/models.js	新增	API
frontend/src/api/vaults.js	新增	API
frontend/src/stores/models.js	新增	Store
frontend/src/stores/vaults.js	新增	Store
backend/tests/unit/test_model_service.py	新增	測試
backend/tests/unit/test_vault_service.py	新增	測試
backend/tests/integration/test_models_crud.py	新增	整合
frontend/tests/ModelForm.spec.js	新增	前端測試
1. 目標
提供財務模型與金庫的完整 CRUD，並實作模型數量上限。

2. 前置條件
□ P1 完成
□ 用戶可登入
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
ModelsView	/app/models	模型列表 + CRUD
VaultsView	/app/vaults?model_id=uuid	金庫列表 + CRUD
3.2 UI 草圖
ModelsView：

text
┌─────────────────────────────────────┐
│  📊 財務模型         [+ 新增]        │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │ 我的家庭財務（預設）           │  │
│  │ TWD | 備用金 6 個月            │  │
│  │ [編輯] [刪除] [檢視]           │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ 個人投資                       │  │
│  │ TWD | 備用金 3 個月            │  │
│  │ [編輯] [刪除] [檢視]           │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
ModelsView.vue
├── ModelList.vue
│   └── ModelCard.vue
├── ModelForm.vue（Modal）
│   ├── BaseInput.vue
│   └── BaseButton.vue
└── DeleteConfirmModal.vue
    └── BaseModal.vue
元件職責：

元件	職責	Props	Emits
ModelsView	頁面組裝	-	-
ModelList	列表	models: Array	edit, delete, view
ModelForm	表單	model?: Object	submit, cancel
ModelCard	卡片	model: Object	edit, delete, view
狀態管理：

類型	檔案	用途
Store	stores/models.js	模型列表、當前模型
Composable	composables/useModels.js	表單驗證、API
3.4 樣式規範
卡片：Emil Kowalski 風格（微陰影、流暢懸停）

Modal：淡入 + 縮放動畫（200ms）

3.5 響應式設計
裝置	佈局
電腦	Grid 3 欄
平板	Grid 2 欄
手機	單欄全寬
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/app/models	列表
POST	/api/v1/app/models	新增
PUT	/api/v1/app/models/{id}	更新
DELETE	/api/v1/app/models/{id}	刪除（軟刪除）
GET	/api/v1/app/vaults	列表
POST	/api/v1/app/vaults	新增
PUT	/api/v1/app/vaults/{id}	更新
DELETE	/api/v1/app/vaults/{id}	刪除
4.2 請求/回應範例
POST /api/v1/app/models：

json
{
  "name": "我的家庭財務",
  "base_currency": "TWD",
  "emergency_fund_months": 6
}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "我的家庭財務",
    "is_default": true,
    "created_at": "2026-09-21T10:00:00Z"
  }
}
錯誤（超過上限）：

json
{
  "success": false,
  "error": {
    "code": "MODEL_LIMIT_EXCEEDED",
    "message": "已達模型數量上限（2）"
  }
}
4.3 資料庫變更
使用表：financial_models, vaults

4.4 環境變數
無新增。

5. 單元測試
5.1 後端測試
python
# tests/unit/test_model_service.py
def test_create_model_success():
    result = service.create(user_id, {"name": "M1", "emergency_fund_months": 6})
    assert result["name"] == "M1"

def test_create_model_limit_exceeded():
    service.create(user_id, {"name": "M1"})
    service.create(user_id, {"name": "M2"})
    with pytest.raises(ModelLimitExceeded):
        service.create(user_id, {"name": "M3"})

def test_admin_no_limit():
    # 管理員可建立 10 個
    for i in range(10):
        service.create(admin_id, {"name": f"M{i}"})
    # 11 個才失敗
5.2 前端測試
javascript
// tests/ModelForm.spec.js
describe('ModelForm', () => {
  it('emits submit with form data', async () => {
    const wrapper = mount(ModelForm)
    await wrapper.find('[name="name"]').setValue('Test')
    await wrapper.find('form').trigger('submit')
    expect(wrapper.emitted('submit')).toBeTruthy()
  })
})
5.3 整合測試
python
# tests/integration/test_models_crud.py
def test_models_crud_integration(auth_client):
    # POST
    response = auth_client.post("/api/v1/app/models", json={"name": "M1"})
    assert response.status_code == 201
    
    # GET
    response = auth_client.get("/api/v1/app/models")
    assert len(response.json()["data"]) == 1
    
    # PUT
    model_id = response.json()["data"][0]["id"]
    response = auth_client.put(f"/api/v1/app/models/{model_id}", json={"name": "M1-updated"})
    assert response.status_code == 200
    
    # DELETE
    response = auth_client.delete(f"/api/v1/app/models/{model_id}")
    assert response.status_code == 200
6. 驗收標準
□ 模型 CRUD 完整
□ 金庫 CRUD 完整
□ 模型上限生效（一般用戶 2、管理員 10）
□ 軟刪除（is_archived）
□ 預設模型只能一個
□ 響應式設計
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
（略，格式同 P1）


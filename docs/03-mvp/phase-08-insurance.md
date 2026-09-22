Phase 8：保險保單 CRUD
版本：v1.0
所屬：MVP
依賴 Phase：P2
預計工時：4 天

⚠️ 本 Phase 的 MVP/完整版約束
MVP：保單 CRUD，分類（人身 / 財產）

不實作人體剖面圖（Full P5）

不實作精算（Full P11）

📂 前置檔案檢查
檔案路徑	來源
docs/02-reference/01-database-schema.md	第二批
docs/02-reference/02-api-spec.md	第二批
docs/03-mvp/phase-02-models.md	第三批
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/insurance.py	新增	保單 CRUD
backend/app/api/v1/body_map.py	新增	人體圖譜（唯讀）
backend/app/services/insurance/policy_service.py	新增	保單邏輯
backend/app/services/insurance/body_map_service.py	新增	部位查詢
backend/app/schemas/insurance.py	新增	DTO
frontend/src/views/app/InsuranceView.vue	新增	保單頁
frontend/src/components/insurance/PolicyList.vue	新增	列表
frontend/src/components/insurance/PolicyForm.vue	新增	表單
frontend/src/components/insurance/BodyPartSelector.vue	新增	部位選擇
frontend/src/api/insurance.js	新增	API
frontend/src/stores/insurance.js	新增	Store
backend/tests/unit/test_policy_service.py	新增	測試
backend/tests/integration/test_policies_crud.py	新增	整合
frontend/tests/PolicyForm.spec.js	新增	前端測試
1. 目標
提供保險保單 CRUD，支援人身 / 財產分類，並 Seed body_part_mapping。

2. 前置條件
□ P2 完成
3. 前端畫面
3.1 頁面清單
頁面	路由
InsuranceView	/app/insurance?model_id=uuid
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  🛡️ 保險保單         [+ 新增]        │
├─────────────────────────────────────┤
│  模型：[我的家庭財務 ▼]              │
│  分類：[全部 ▼]                      │
├─────────────────────────────────────┤
│  終身醫療險                          │
│  XX 人壽                             │
│  保障 100 萬 | 年繳 30,000           │
│  涵蓋：心臟、大腦                    │
│  [編輯] [刪除]                       │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
InsuranceView.vue
├── ModelSelector.vue
├── CategoryFilter.vue
├── PolicyList.vue
│   └── PolicyCard.vue
├── PolicyForm.vue（Modal）
│   ├── BaseSelect.vue（分類）
│   ├── BaseSelect.vue（子分類）
│   ├── BaseInput.vue（保額）
│   ├── BodyPartSelector.vue
│   └── BaseButton.vue
元件職責：

元件	職責	Props	Emits
InsuranceView	頁面	-	-
PolicyList	列表	policies: Array	edit, delete
PolicyForm	表單	policy?: Object	submit, cancel
BodyPartSelector	部位選擇	selected: Array	update:selected
3.4 樣式規範
沿用 P2。

3.5 響應式設計
裝置	佈局
電腦	卡片 3 欄
平板	卡片 2 欄
手機	單欄全寬
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/app/insurance/policies	列表
POST	/api/v1/app/insurance/policies	新增
PUT	/api/v1/app/insurance/policies/{id}	更新
DELETE	/api/v1/app/insurance/policies/{id}	刪除
GET	/api/v1/app/insurance/body-map	部位清單
4.2 請求/回應範例
POST /api/v1/app/insurance/policies：

json
{
  "model_id": "uuid",
  "category": "life",
  "subcategory": "disease",
  "policy_name": "終身醫療險",
  "insurer_name": "XX 人壽",
  "coverage_amount": 1000000,
  "annual_premium": 30000,
  "covered_body_parts": ["heart", "brain"]
}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "policy_name": "終身醫療險",
    "coverage_amount": 1000000,
    "covered_body_parts": ["heart", "brain"]
  }
}
4.3 資料庫變更
使用表：insurance_policies, body_part_mapping

Seed body_part_mapping（8 個部位）。

4.4 環境變數
無新增。

5. 單元測試
5.1 後端測試
python
# tests/unit/test_policy_service.py
def test_create_policy():
    result = service.create(user_id, {
        "category": "life",
        "policy_name": "終身醫療險",
        "coverage_amount": 1000000
    })
    assert result["policy_name"] == "終身醫療險"

def test_invalid_category():
    with pytest.raises(ValueError):
        service.create(user_id, {"category": "invalid"})
5.2 前端測試
javascript
describe('PolicyForm', () => {
  it('requires policy name', async () => {
    const wrapper = mount(PolicyForm)
    await wrapper.find('form').trigger('submit')
    expect(wrapper.text()).toContain('請輸入保單名稱')
  })
})
5.3 整合測試
python
def test_policies_crud(auth_client, test_model):
    response = auth_client.post("/api/v1/app/insurance/policies", json={
        "model_id": test_model["id"],
        "category": "life",
        "policy_name": "終身醫療險",
        "coverage_amount": 1000000
    })
    assert response.status_code == 201
6. 驗收標準
□ 保單 CRUD 完整
□ 人身 / 財產分類正確
□ 子分類正確
□ Body Part Selector 可用
□ body_part_mapping Seed 完成
□ 響應式設計
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
（略）
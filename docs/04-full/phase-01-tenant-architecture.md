Full Phase 1：多租戶架構
版本：v1.0
所屬：完整版
依賴 MVP Phase：P1（用戶認證）、P0（資料庫 Schema 已預留 tenant_id）
預計工時：5 天

⚠️ 本 Phase 的完整版約束
完整版：多租戶隔離

每個租戶獨立資料

管理員可管理所有租戶

🔗 依賴 MVP 哪個 Phase
依賴 MVP P0：資料庫 Schema 已預留 tenant_id

依賴 MVP P1：用戶認證系統已完成

🔄 與 MVP 的差異
項目	MVP	完整版
租戶數	1（預設租戶）	多租戶
租戶註冊	無	有（自助或邀請）
租戶隔離	無強制	所有查詢強制 tenant_id
租戶方案	無	free / pro / pro_plus
管理員範圍	全部資料	可跨租戶管理
📂 前置檔案檢查
檔案路徑	來源	用途
docs/01-framework/01-shared-framework.md	第一批	架構
docs/02-reference/01-database-schema.md	第二批	tenants 表
docs/02-reference/02-api-spec.md	第二批	API
docs/03-mvp/phase-01-auth.md	第三批	MVP 認證
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/admin_tenants.py	新增	租戶管理
backend/app/api/v1/tenant_register.py	新增	租戶註冊
backend/app/services/tenant_service.py	新增	租戶邏輯
backend/app/core/tenant_context.py	新增	租戶上下文
backend/app/middleware/tenant_middleware.py	新增	租戶注入
backend/app/schemas/tenant.py	新增	DTO
frontend/src/views/admin/TenantsView.vue	新增	租戶管理
frontend/src/views/TenantRegisterView.vue	新增	租戶註冊
frontend/src/api/tenants.js	新增	API
frontend/src/stores/tenant.js	新增	Store
backend/tests/unit/test_tenant_service.py	新增	測試
backend/tests/integration/test_tenant_isolation.py	新增	隔離測試
1. 目標
建立多租戶架構，實現租戶隔離、租戶管理、租戶註冊。

2. 前置條件
□ MVP 完成
□ tenants 表已存在（MVP P0 已建）
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
TenantRegisterView	/register	新租戶註冊
TenantsView	/admin/tenants	租戶列表（管理員）
3.2 UI 草圖
TenantsView：

text
┌─────────────────────────────────────┐
│  🏢 租戶管理                         │
├─────────────────────────────────────┤
│  [+ 新增租戶]                        │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │ 預設租戶                       │  │
│  │ plan: free | users: 1 / 5     │  │
│  │ [檢視] [停用]                  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
TenantsView.vue
├── TenantList.vue
│   └── TenantCard.vue
├── TenantForm.vue（Modal）
│   └── BaseInput.vue
└── DeleteConfirmModal.vue

TenantRegisterView.vue
├── TenantRegisterForm.vue
│   ├── BaseInput.vue（租戶名稱）
│   ├── BaseInput.vue（Email）
│   └── BaseButton.vue
3.4 樣式規範
沿用 MVP P2 風格。

3.5 響應式設計
裝置	佈局
電腦	卡片 3 欄
平板	卡片 2 欄
手機	單欄
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/admin/tenants	租戶列表
POST	/api/v1/admin/tenants	新增租戶
PUT	/api/v1/admin/tenants/{id}	更新
DELETE	/api/v1/admin/tenants/{id}	停用
POST	/api/v1/tenants/register	自助註冊
GET	/api/v1/tenants/me	當前租戶
4.2 請求/回應範例
POST /api/v1/admin/tenants：

json
{
  "name": "王家",
  "slug": "wang-family",
  "plan": "free",
  "max_users": 5,
  "max_models": 2
}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "王家",
    "slug": "wang-family",
    "plan": "free"
  }
}
4.3 資料庫變更
新增欄位（若有需要）：

sql
ALTER TABLE tenants ADD COLUMN IF NOT EXISTS owner_user_id CHAR(36);
ALTER TABLE tenants ADD COLUMN IF NOT EXISTS billing_email VARCHAR(255);
4.4 環境變數
變數	說明
TENANT_ISOLATION_ENABLED	true
DEFAULT_TENANT_ID	預設租戶 ID
5. 單元測試
5.1 後端測試
python
# tests/unit/test_tenant_service.py
def test_create_tenant():
    result = service.create({"name": "王家", "slug": "wang"})
    assert result["slug"] == "wang"

def test_slug_unique():
    service.create({"name": "A", "slug": "test"})
    with pytest.raises(ValueError):
        service.create({"name": "B", "slug": "test"})
5.2 前端測試
javascript
describe('TenantForm', () => {
  it('validates slug format', async () => {
    const wrapper = mount(TenantForm)
    await wrapper.find('[name="slug"]').setValue('王 家')
    await wrapper.find('form').trigger('submit')
    expect(wrapper.text()).toContain('slug 只能包含英數字和連字號')
  })
})
5.3 整合測試
python
# tests/integration/test_tenant_isolation.py
def test_tenant_isolation():
    # 建立兩個租戶
    t1 = create_tenant("tenant1")
    t2 = create_tenant("tenant2")
    
    # tenant1 的用戶
    u1 = create_user(t1["id"], "user1@t1.com")
    token1 = login(u1)
    
    # tenant2 的用戶
    u2 = create_user(t2["id"], "user2@t2.com")
    token2 = login(u2)
    
    # u1 建立模型
    client_with_token(token1).post("/api/v1/app/models", json={"name": "M1"})
    
    # u2 查詢模型，應看不到 u1 的
    response = client_with_token(token2).get("/api/v1/app/models")
    assert len(response.json()["data"]) == 0
6. 驗收標準
□ 多租戶隔離生效
□ 所有查詢帶 tenant_id
□ 管理員可跨租戶管理
□ 租戶註冊流程可用
□ 租戶方案限制生效
□ 響應式設計
□ 單元測試 ≥ 80%
□ 整合測試（隔離）通過
7. 交付物清單
（略，格式同 MVP P1）
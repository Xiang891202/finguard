Phase 1：用戶認證 + 會員中心健康檔案
版本：v1.0
所屬：MVP
依賴 Phase：P0
預計工時：5 天

⚠️ 本 Phase 的 MVP/完整版約束
MVP：健康檔案為必填（新用戶強制導向）

基因資料加密儲存

獨立基因同意書

舊用戶可跳過

📂 前置檔案檢查
檔案路徑	來源	用途
docs/01-framework/01-shared-framework.md	第一批	架構
docs/02-reference/01-database-schema.md	第二批	表結構
docs/02-reference/02-api-spec.md	第二批	API 規格
docs/03-mvp/phase-00-setup.md	第三批	P0 產出
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/auth.py	新增	OTP 認證
backend/app/api/v1/admin_auth.py	新增	管理員登入
backend/app/api/v1/health.py	修改	加入健康檔案端點
backend/app/services/auth_service.py	新增	認證邏輯
backend/app/services/admin_auth_service.py	新增	管理員認證
backend/app/services/health/health_profile_service.py	新增	健康檔案
backend/app/services/health/genetic_service.py	新增	基因資料
backend/app/core/security.py	新增	JWT、bcrypt
backend/app/core/encryption.py	新增	基因加密
backend/app/schemas/auth.py	新增	認證 DTO
backend/app/schemas/health.py	新增	健康檔案 DTO
frontend/src/views/app/LoginView.vue	新增	用戶登入
frontend/src/views/admin/AdminLoginView.vue	新增	管理員登入
frontend/src/views/app/HealthProfileView.vue	新增	健康檔案
frontend/src/components/health/HealthProfileForm.vue	新增	主表單
frontend/src/components/health/FamilyHistoryForm.vue	新增	家族病史
frontend/src/components/health/GeneticTestForm.vue	新增	基因檢測
frontend/src/components/health/CompletionIndicator.vue	新增	完成度
frontend/src/components/common/BaseDatePicker.vue	新增	日期選擇
frontend/src/components/common/BaseCheckbox.vue	新增	勾選框
frontend/src/api/auth.js	新增	認證 API
frontend/src/api/health.js	新增	健康檔案 API
frontend/src/stores/auth.js	新增	認證 Store
frontend/src/stores/health.js	新增	健康 Store
frontend/src/composables/useHealthProfile.js	新增	Composable
backend/tests/unit/test_auth.py	新增	認證測試
backend/tests/unit/test_health_profile.py	新增	健康檔案測試
backend/tests/integration/test_auth_flow.py	新增	認證整合測試
frontend/tests/HealthProfileForm.spec.js	新增	表單測試
1. 目標
建立完整的用戶認證系統（Email + OTP）與健康檔案模組。

2. 前置條件
□ P0 完成
□ 資料庫表已建立
□ SMTP 服務已設定
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
LoginView	/login	用戶 OTP 登入
AdminLoginView	/admin/login	管理員登入
HealthProfileView	/app/account/health	健康檔案
3.2 UI 草圖
LoginView：

text
┌─────────────────────────────────────┐
│  🛡️ FinGuard                        │
├─────────────────────────────────────┤
│                                     │
│  登入 / 註冊                         │
│                                     │
│  Email: [________________]          │
│                                     │
│  [ 發送驗證碼 ]                      │
│                                     │
│  （發送後顯示）                      │
│  驗證碼: [______]                    │
│  [ 登入 ]                            │
│                                     │
└─────────────────────────────────────┘
HealthProfileView：

text
┌─────────────────────────────────────┐
│  📋 健康檔案         完成度 80%      │
├─────────────────────────────────────┤
│                                     │
│  基本資料（必填）                    │
│  ├── 西元生日 [____/__/__] *        │
│  └── 性別 [○男 ○女 ○其他] *        │
│                                     │
│  家族病史（選填）                    │
│  ├── ☐ 心血管疾病                    │
│  ├── ☐ 糖尿病                        │
│  ├── ☐ 癌症                          │
│  └── ☐ 其他 [____]                   │
│                                     │
│  基因檢測（選填）                    │
│  ├── 是否做過基因檢測？[○是 ○否]    │
│  └── 若勾選「是」：                  │
│      需勾選同意書 ☐                  │
│      ├── ☐ BRCA1 / BRCA2            │
│      ├── ☐ APOE                     │
│      └── ...                         │
│                                     │
│  [儲存] [稍後填寫]                   │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
LoginView.vue
├── BaseInput.vue
├── BaseButton.vue
└── BaseCard.vue

HealthProfileView.vue
├── HealthProfileForm.vue
│   ├── BaseDatePicker.vue
│   ├── BaseSelect.vue
│   ├── FamilyHistoryForm.vue
│   │   └── BaseCheckbox.vue
│   └── GeneticTestForm.vue
│       ├── BaseCheckbox.vue
│       └── BaseInput.vue
├── CompletionIndicator.vue
└── BaseButton.vue
元件職責：

元件	職責	Props	Emits
LoginView	登入頁組裝	-	-
HealthProfileView	健康檔案頁	-	-
HealthProfileForm	主表單	profile: Object	submit, cancel
FamilyHistoryForm	家族病史	value: Object	update:value
GeneticTestForm	基因檢測	value: Object	update:value
CompletionIndicator	完成度	percentage: Number	-
BaseDatePicker	日期選擇	modelValue: String	update:modelValue
狀態管理：

類型	檔案	用途
Store	stores/auth.js	登入狀態、Token
Store	stores/health.js	健康檔案、完成度
Composable	composables/useHealthProfile.js	表單驗證、API
3.4 樣式規範
風格：Emil Kowalski

動畫：切換 250ms

互動：懸停、聚焦效果

3.5 響應式設計
裝置	佈局
電腦	居中卡片，寬 480px
平板	居中卡片，寬 90%
手機	全寬，填滿螢幕
4. 後端邏輯
4.1 API 端點
方法	路徑	說明	認證
POST	/api/v1/auth/otp/request	請求 OTP	❌
POST	/api/v1/auth/otp/verify	驗證 OTP	❌
POST	/api/v1/auth/refresh	刷新 Token	❌
POST	/api/v1/auth/logout	登出	✅
POST	/api/v1/admin/auth/login	管理員登入	❌
POST	/api/v1/admin/auth/logout	管理員登出	✅
GET	/api/v1/app/health/profile	查詢健康檔案	✅
POST	/api/v1/app/health/profile	新增健康檔案	✅
PUT	/api/v1/app/health/profile	更新健康檔案	✅
POST	/api/v1/app/health/consent	基因同意	✅
GET	/api/v1/app/health/genetic-markers	基因點位清單	✅
GET	/api/v1/app/health/genetic-tests	基因檢測結果	✅
POST	/api/v1/app/health/genetic-tests	新增檢測	✅
DELETE	/api/v1/app/health/genetic-tests/{id}	刪除檢測	✅
GET	/api/v1/app/health/completion	完成度	✅
4.2 請求/回應範例
POST /api/v1/auth/otp/request：

json
{
  "email": "user@example.com"
}
回應：

json
{
  "success": true,
  "data": {
    "message": "驗證碼已寄出",
    "expires_in": 300
  }
}
POST /api/v1/auth/otp/verify：

json
{
  "email": "user@example.com",
  "otp": "123456"
}
回應：

json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "is_new_user": true,
      "health_profile_completed": false
    }
  }
}
POST /api/v1/app/health/profile：

json
{
  "birth_date": "1985-06-15",
  "gender": "male",
  "family_history": {
    "cardiovascular": true,
    "diabetes": false
  }
}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "completion_rate": 90.00
  }
}
4.3 資料庫變更
使用表：users, admin_users, otp_tokens, refresh_tokens, user_health_profiles, genetic_markers, user_genetic_tests, tenants

4.4 環境變數
變數	說明	預設值
SMTP_HOST	SMTP 主機	smtp.gmail.com
SMTP_PORT	SMTP 埠	587
SMTP_USER	Gmail 帳號	（必填）
SMTP_PASSWORD	Gmail 應用密碼	（必填）
OTP_EXPIRY_SECONDS	OTP 有效期	300
JWT_ACCESS_EXPIRY	Access Token	900
JWT_REFRESH_EXPIRY	Refresh Token	604800
ENCRYPTION_KEY	基因加密金鑰	（必填）
5. 單元測試
5.1 後端測試
python
# tests/unit/test_auth.py
def test_otp_request_success():
    response = client.post("/api/v1/auth/otp/request", json={
        "email": "test@example.com"
    })
    assert response.status_code == 200
    assert "expires_in" in response.json()["data"]

def test_otp_rate_limited():
    # 60 秒內第二次請求
    client.post("/api/v1/auth/otp/request", json={"email": "test@example.com"})
    response = client.post("/api/v1/auth/otp/request", json={"email": "test@example.com"})
    assert response.status_code == 429
    assert response.json()["error"]["code"] == "AUTH_OTP_RATE_LIMITED"

def test_health_profile_completion():
    # 生日 + 性別 = 80%
    profile = {"birth_date": "1985-06-15", "gender": "male"}
    response = client.post("/api/v1/app/health/profile", json=profile)
    assert response.json()["data"]["completion_rate"] == 80.0
5.2 前端測試
javascript
// tests/HealthProfileForm.spec.js
import { mount } from '@vue/test-utils'
import HealthProfileForm from '@/components/health/HealthProfileForm.vue'

describe('HealthProfileForm', () => {
  it('shows consent when genetic test enabled', async () => {
    const wrapper = mount(HealthProfileForm)
    await wrapper.find('[data-testid="genetic-toggle"]').setValue(true)
    expect(wrapper.find('[data-testid="genetic-consent"]').exists()).toBe(true)
  })
})
5.3 整合測試
python
# tests/integration/test_auth_flow.py
def test_full_auth_flow():
    # 1. 請求 OTP
    client.post("/api/v1/auth/otp/request", json={"email": "test@example.com"})
    
    # 2. 從 DB 取得 OTP（測試用）
    otp = get_test_otp("test@example.com")
    
    # 3. 驗證 OTP
    response = client.post("/api/v1/auth/otp/verify", json={
        "email": "test@example.com",
        "otp": otp
    })
    assert response.status_code == 200
    assert "access_token" in response.json()["data"]
6. 驗收標準
□ 用戶可用 Email + OTP 登入
□ 管理員可用 Email + 密碼登入
□ OTP 防濫用機制生效（60 秒、每日上限）
□ Refresh Token Rotation 生效
□ 新用戶登入後強制導向健康檔案
□ 健康檔案完成度計算正確
□ 基因資料加密存儲
□ 基因同意書獨立顯示
□ 舊用戶可跳過健康檔案
□ 響應式設計（3 裝置）
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
類型	檔案	狀態
後端	auth.py, admin_auth.py, health.py	✅
後端	auth_service.py, admin_auth_service.py	✅
後端	health_profile_service.py, genetic_service.py	✅
後端	security.py, encryption.py	✅
前端	LoginView, AdminLoginView, HealthProfileView	✅
前端	HealthProfileForm, FamilyHistoryForm, GeneticTestForm	✅
測試	test_auth.py, test_health_profile.py, test_auth_flow.py	✅



## 8. 實作 vs 規劃的差異（2026-09-24 完成）

| 規劃書 | 實際實作 | 原因 |
|---|---|---|
| `services/auth_service.py` | `services/otp_service.py` + `services/token_service.py` | SRP 拆分，職責分離 |
| `api/v1/health.py`（改） | `api/v1/health_profile.py` + `api/v1/genetic.py` | 原 `health.py` 為 P0 健康檢查端點 |
| `services/health/health_profile_service.py` | `services/health_profile_service.py` | 簡化目錄（暫無 `health/` 子目錄） |
| `services/health/genetic_service.py` | `services/genetic_service.py` | 同上 |
| `tests/unit/test_auth.py` | `test_auth_otp.py` + `test_auth_token.py` + `test_admin_auth.py` | 依功能拆分 |
| `tests/integration/test_auth_flow.py` | ✅ 建立 | 涵蓋 3 條 Critical Path |

## 9. 驗收結果（2026-09-24）

| 項目 | 結果 |
|---|---|
| 後端單元 + 整合測試 | 55 passed |
| 後端測試覆蓋率 | 84% |
| 前端 E2E（Playwright） | 6 passed |
| 前端單元測試（Vitest） | 4 passed |
| 資料庫 migration | `b93f21a4aec3` (head) |

## 10. 已知延後項目

| 項目 | 延後至 | 原因 |
|---|---|---|
| 舊用戶跳過健康檔案 | Phase 9-10 | 需先有 Dashboard |
| BaseInput/BaseButton/BaseCard/BaseSelect 抽取 | Phase 2 前 | 重構性質，獨立 commit |
| Emil Kowalski 風格 polish | Phase 11 | UI 定型後統一處理 |
| 響應式 3 裝置截圖 | Phase 1 收尾 | 本節補做 |
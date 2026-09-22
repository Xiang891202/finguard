Phase 0：基礎建設
版本：v1.0
所屬：MVP
依賴 Phase：無
預計工時：3 天

⚠️ 本 Phase 的 MVP/完整版約束
MVP：建立所有 30 張表（空表），但不寫入完整版資料

金流相關表建立但不使用

只實作 Python FastAPI 單一後端（Node.js 延後）

📂 前置檔案檢查
檔案路徑	來源	用途
docs/01-framework/01-shared-framework.md	第一批	架構與設計原則
docs/01-framework/03-phase-template.md	第一批	Phase 格式
docs/02-reference/01-database-schema.md	第二批	30 張表 DDL
docs/02-reference/02-api-spec.md	第二批	API 規格
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/main.py	新增	FastAPI 入口
backend/app/core/config.py	新增	環境變數
backend/app/core/logging.py	新增	日誌設定
backend/app/core/exceptions.py	新增	自訂例外
backend/app/core/constants.py	新增	常數
backend/app/db/base.py	新增	SQLAlchemy Base
backend/app/db/session.py	新增	Session 管理
backend/app/db/migrations/	新增	Alembic migrations
backend/app/models/*.py	新增	所有 ORM 模型
backend/app/api/v1/health.py	新增	健康檢查
backend/app/schemas/base.py	新增	通用 DTO
backend/app/services/health_service.py	新增	健康檢查
backend/requirements.txt	新增	Python 依賴
backend/Dockerfile	新增	Docker 映像
backend/.env.example	新增	環境變數範本
frontend/package.json	新增	前端依賴
frontend/vite.config.js	新增	Vite 設定
frontend/src/App.vue	新增	根元件
frontend/src/main.js	新增	入口
frontend/src/router/index.js	新增	路由
frontend/src/api/client.js	新增	Axios 封裝
frontend/src/styles/main.css	新增	全域樣式
frontend/src/styles/variables.css	新增	CSS 變數
docker-compose.yml	新增	本地開發
.github/workflows/ci.yml	新增	CI
1. 目標
建立專案骨架、資料庫、CI/CD，為後續 Phase 打好基礎。

2. 前置條件
□ Git 專案已初始化
□ PostgreSQL 已就緒
□ Node.js 20+、Python 3.11+ 已安裝
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
HomeView	/	首頁（顯示系統狀態）
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  🛡️ FinGuard（財安）                │
├─────────────────────────────────────┤
│                                     │
│  系統狀態：                          │
│  ✅ 資料庫連線正常                   │
│  ✅ Redis 連線正常                   │
│  📌 版本：v1.4.0                     │
│                                     │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
App.vue
└── HomeView.vue
    └── BaseCard.vue（共用元件）
元件職責：

元件	職責	Props	Emits
App.vue	根元件	-	-
HomeView.vue	首頁	-	-
BaseCard.vue	通用卡片	title, content	-
3.4 樣式規範
風格：Emil Kowalski

顏色：深色 / 淺色模式

動畫：200ms 過場

3.5 響應式設計
裝置	斷點	佈局
電腦	≥ 1024px	居中卡片
平板	768-1023px	居中卡片
手機	< 768px	全寬卡片
4. 後端邏輯
4.1 API 端點
方法	路徑	說明	認證
GET	/health	健康檢查	❌
GET	/health/ready	就緒檢查	❌
GET	/health/live	存活檢查	❌
4.2 請求/回應範例
請求：GET /health

回應：

json
{
  "status": "healthy",
  "version": "1.4.0",
  "database": "connected",
  "redis": "connected",
  "timestamp": "2026-09-21T10:00:00Z"
}
4.3 資料庫變更
建立所有 30 張表（見第二批文件 4）。

4.4 環境變數
變數	說明	預設值
DATABASE_URL	PostgreSQL 連線	postgresql://...
REDIS_URL	Redis 連線	redis://...
JWT_SECRET	JWT 密鑰	（必填）
ENCRYPTION_KEY	基因加密金鑰	（必填）
ENV	環境	development
5. 單元測試
5.1 後端測試
python
# tests/unit/test_health.py
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
5.2 前端測試
javascript
// tests/HomeView.spec.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import HomeView from '@/views/HomeView.vue'

describe('HomeView', () => {
  it('renders version', () => {
    const wrapper = mount(HomeView)
    expect(wrapper.text()).toContain('v1.4.0')
  })
})
5.3 整合測試
python
# tests/integration/test_health.py
def test_health_integration():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["database"] == "connected"
6. 驗收標準
□ 專案可執行（docker-compose up）
□ 資料庫 30 張表建立完成
□ GET /health 回應 200
□ 前端可訪問（顯示版本）
□ CI 可執行（lint + test）
□ 單元測試通過（≥ 80%）
□ 整合測試通過
7. 交付物清單
類型	檔案	狀態
後端	backend/app/main.py	✅
後端	backend/app/api/v1/health.py	✅
後端	backend/app/models/*.py（30 個）	✅
前端	frontend/src/views/HomeView.vue	✅
設定	docker-compose.yml	✅
CI	.github/workflows/ci.yml	✅
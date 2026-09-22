Full Phase 4：自動排程爬蟲
版本：v1.0
所屬：完整版
依賴 MVP Phase：MVP P7（爬蟲調度）
預計工時：4 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P7：CrawlerDispatcher、三源驗證已完成

🔄 與 MVP 的差異
項目	MVP	完整版
觸發方式	手動	自動排程
Celery Beat	❌	✅
排程頻率	-	每日 / 每週
失敗重試	手動	自動重試
監控	基本	完整
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/workers/celery_app.py	修改	加入 Beat
backend/app/workers/schedules.py	新增	排程定義
backend/app/api/v1/admin_schedules.py	新增	排程管理
frontend/src/views/admin/SchedulesView.vue	新增	排程頁
backend/tests/unit/test_schedules.py	新增	測試
1. 目標
建立自動排程爬蟲系統。

2. 前置條件
□ MVP P7 完成
□ Redis 已就緒
□ Celery Beat 已設定
3. 前端畫面
3.1 頁面清單
頁面	路由
SchedulesView	/admin/schedules
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  ⏰ 排程管理                         │
├─────────────────────────────────────┤
│  金融市場：每日 06:00 ✅ 啟用        │
│  保險目錄：每週一 08:00 ✅ 啟用       │
│  預測：每日 07:00 ✅ 啟用            │
│  Email：每日 08:00 ✅ 啟用           │
│                                     │
│  [編輯排程]                          │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
SchedulesView.vue
├── ScheduleList.vue
│   └── ScheduleCard.vue
└── ScheduleForm.vue
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/admin/schedules	排程列表
PUT	/api/v1/admin/schedules/{name}	更新排程
POST	/api/v1/admin/schedules/{name}/trigger	手動觸發
4.2 請求/回應範例
PUT /api/v1/admin/schedules/daily_crawl：

json
{
  "cron": "0 6 * * *",
  "enabled": true
}
4.3 資料庫變更
新增表：

sql
CREATE TABLE schedules (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    cron VARCHAR(50) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    last_run_at TIMESTAMP,
    next_run_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
4.4 環境變數
變數	說明
CELERY_BEAT_ENABLED	true
CRAWL_SCHEDULE	0 6 * * *
INSURANCE_SCHEDULE	0 8 * * 1
5. 單元測試
python
# tests/unit/test_schedules.py
def test_register_schedules():
    schedules = get_all_schedules()
    assert "daily_crawl" in schedules
    assert "weekly_insurance" in schedules
    assert "daily_forecast" in schedules
    assert "daily_email" in schedules

def test_disable_schedule():
    service.update("daily_crawl", {"enabled": False})
    schedule = service.get("daily_crawl")
    assert schedule["enabled"] is False
6. 驗收標準
□ Celery Beat 運作
□ 4 個排程（爬蟲、保險、預測、Email）
□ 可啟用 / 停用
□ 可手動觸發
□ 失敗自動重試
□ 單元測試 ≥ 80%
7. 交付物清單
（略）


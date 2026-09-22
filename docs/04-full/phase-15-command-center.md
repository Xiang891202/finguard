📄 更新文件 4：Full Phase 15 指揮中心
版本：v2.0
所屬：完整版
依賴 Phase：

MVP P10（基礎自癒）

Full P5.5（引擎版本管理）
預計工時：9 天（v1.4：8 天）

⚠️ 本 Phase 的完整版約束
完整三級修復

Incident 管理

整合引擎版本管理（v1.5）

🔗 依賴 MVP 哪個 Phase
依賴 MVP P10：Level 1 自癒、Incidents 表已存在

依賴 Full P5.5：引擎版本管理系統

🔄 與 MVP 的差異
項目	MVP	完整版
修復級別	Level 1	Level 1/2/3
指揮中心	無	完整 UI
Incident 管理	基本	完整
手動控制	無	有
頻率控制	基本	完整
引擎健康監控（v1.5）	無	整合
🔄 與 v1.4 的差異
項目	v1.4	v1.5
引擎管理整合	❌	✅
引擎追蹤入口	無	✅
工時	8 天	9 天
📂 前置檔案檢查
檔案路徑	來源	用途
docs/01-framework/01-shared-framework.md	第一批	架構
docs/03-mvp/phase-10-email-recovery.md	第三批	MVP 自癒
docs/04-full/phase-05.5-engine-version.md	第四批	引擎版本管理
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/services/recovery_service.py	修改	三級修復
backend/app/services/command_center_service.py	新增	指揮中心
backend/app/services/engine_health_service.py	新增（v1.5）	引擎健康檢查
backend/app/api/v1/admin_command.py	新增	指揮 API
backend/app/workers/recovery_worker.py	修改	擴充
frontend/src/views/admin/CommandCenterView.vue	新增	指揮中心
frontend/src/components/admin/HealthLights.vue	新增	健康燈號
frontend/src/components/admin/QueuePanel.vue	新增	佇列
frontend/src/components/admin/IncidentPanel.vue	新增	異常
frontend/src/components/admin/ManualControls.vue	新增	手動控制
frontend/src/components/admin/EngineHealthPanel.vue	新增（v1.5）	引擎健康
backend/tests/unit/test_recovery_3_levels.py	新增	測試
backend/tests/unit/test_engine_health.py	新增（v1.5）	測試
1. 目標
建立完整指揮中心，支援三級修復與手動控制，整合引擎版本管理。

2. 前置條件
□ MVP P10 完成
□ Full P5.5 完成
3. 前端畫面
3.1 頁面清單
頁面	路由
CommandCenterView	/admin/command-center
3.2 UI 草圖
text
┌─────────────────────────────────────────────────────────────┐
│  🎛️ 指揮中心                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【系統健康】                                                │
│  🟢 資料庫  🟢 Redis  🟡 API                                │
│                                                             │
│  【引擎健康】（v1.5 新增）                                   │
│  🟢 🕷️ crawler    🟢 🧹 normalizer                          │
│  🟢 🎯 matcher    🟢 🎲 monte_carlo                         │
│  🟡 🧠 llm        (延遲偏高)                                │
│  [查看引擎詳情] [追蹤樹]                                     │
│                                                             │
│  【佇列】                                                    │
│  crawl(0) forecast(0) email(2)                              │
│                                                             │
│  【今日異常】                                                │
│  INC-001 HIGH 已解決                                         │
│                                                             │
│  【手動控制】                                                │
│  [切換降級模式] [重啟 Worker]                               │
│  [清除快取] [觸發爬蟲] [重算任務]                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
3.3 Vue 元件結構
text
CommandCenterView.vue
├── HealthLights.vue
├── EngineHealthPanel.vue         # v1.5 新增
│   ├── EngineHealthCard.vue（5 個引擎）
│   └── EngineTraceLink.vue
├── QueuePanel.vue
├── IncidentPanel.vue
└── ManualControls.vue
元件職責：

元件	職責	Props	Emits
CommandCenterView	頁面	-	-
HealthLights	系統健康	services: Object	-
EngineHealthPanel	引擎健康	engines: Array	view-detail
EngineHealthCard	單一引擎	engine: Object	click
QueuePanel	佇列	queues: Object	-
IncidentPanel	異常	incidents: Array	resolve
ManualControls	手動控制	-	action
狀態管理：

類型	檔案	用途
Store	stores/admin.js	系統健康、引擎狀態
3.4 樣式規範
沿用 MVP P10 的管理員風格。

3.5 響應式設計
裝置	佈局
電腦	雙欄
平板	單欄
手機	單欄
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/admin/command/health	系統健康
GET	/api/v1/admin/command/engine-health	引擎健康（v1.5）
GET	/api/v1/admin/command/queues	佇列
GET	/api/v1/admin/command/incidents	異常
POST	/api/v1/admin/command/degrade	切換降級
POST	/api/v1/admin/command/restart-worker	重啟 Worker
POST	/api/v1/admin/command/clear-cache	清除快取
POST	/api/v1/admin/command/recompute	觸發重算（v1.5）
4.2 請求/回應範例
GET /api/v1/admin/command/engine-health（v1.5 新增）：

json
{
  "success": true,
  "data": {
    "engines": [
      {
        "engine_type": "crawler",
        "active_version": "v1.2",
        "status": "healthy",
        "last_execution": "2026-09-22T06:00:00Z",
        "success_rate_24h": 0.98,
        "avg_duration_ms": 3200
      },
      {
        "engine_type": "llm",
        "active_version": "v1.3",
        "status": "degraded",
        "last_execution": "2026-09-22T08:00:00Z",
        "success_rate_24h": 0.95,
        "avg_duration_ms": 1250,
        "note": "延遲偏高"
      }
    ]
  }
}
4.3 資料庫變更
新增表：

sql
CREATE TABLE system_settings (
    key VARCHAR(50) PRIMARY KEY,
    value JSONB,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO system_settings (key, value) VALUES
('degrade_mode', '{"enabled": false}'),
('maintenance_mode', '{"enabled": false}');
4.4 環境變數
變數	說明
COMMAND_CENTER_ENABLED	true
ENGINE_HEALTH_CHECK_INTERVAL	300（秒）
5. 單元測試
5.1 後端測試
python
# tests/unit/test_recovery_3_levels.py
def test_level_2_degrade():
    result = recovery.recover("crawl_failed")
    assert result["level"] == 2
    assert result["action"] == "use_yesterday_data"
    assert db.query(Incident).count() == 1

def test_level_3_stops_and_notifies():
    with patch("app.services.recovery_service.send_admin_email") as mock:
        result = recovery.recover("data_corruption")
        assert result["level"] == 3
        assert mock.called

# tests/unit/test_engine_health.py（v1.5 新增）
def test_engine_health_aggregation():
    health = engine_health_service.check_all()
    assert len(health["engines"]) == 5
    for e in health["engines"]:
        assert e["engine_type"] in ["crawler", "normalizer", "validator", 
                                     "matcher", "monte_carlo", "llm"]
        assert e["status"] in ["healthy", "degraded", "down"]

def test_engine_degraded_by_latency():
    # 延遲 > 1000ms 標記為 degraded
    with patch("app.services.engine_health_service.get_avg_latency", return_value=1200):
        result = engine_health_service.check_engine("llm")
        assert result["status"] == "degraded"
5.2 前端測試
javascript
describe('CommandCenterView', () => {
  it('renders engine health panel', () => {
    const wrapper = mount(CommandCenterView, {
      props: { engineHealth: mockEngineHealth }
    })
    expect(wrapper.findAll('[data-testid="engine-health-card"]').length).toBe(5)
  })

  it('shows degraded badge for slow engine', () => {
    const wrapper = mount(CommandCenterView, {
      props: { engineHealth: { engines: [{ engine_type: 'llm', status: 'degraded' }] } }
    })
    expect(wrapper.find('.engine-degraded').exists()).toBe(true)
  })
})
5.3 整合測試
python
def test_command_center_engine_integration(admin_client, test_engine_versions):
    response = admin_client.get("/api/v1/admin/command/engine-health")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["engines"]) == 5
    # 驗證與 Full P5.5 的版本一致
    for engine in data["engines"]:
        versions = admin_client.get(
            f"/api/v1/admin/engines/{engine['engine_type']}/versions?status=active"
        ).json()["data"]
        assert len(versions) == 1
        assert versions[0]["version"] == engine["active_version"]
6. 驗收標準
□ 三級修復正確
□ Level 1 不通知
□ Level 2 記錄 Incident
□ Level 3 立即通知
□ 手動控制可用
□ 頻率控制生效
□ 引擎健康面板顯示 5 引擎（v1.5）
□ 引擎健康與版本管理一致（v1.5）
□ 可從指揮中心跳轉到追蹤樹（v1.5）
□ 可從指揮中心觸發重算（v1.5）
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
類型	檔案	狀態
後端	command_center_service.py	✅
後端	engine_health_service.py（v1.5）	✅
後端	admin_command.py	✅
後端	recovery_service.py（修改）	✅
前端	CommandCenterView	✅
前端	HealthLights, QueuePanel, IncidentPanel, ManualControls	✅
前端	EngineHealthPanel（v1.5）	✅
測試	test_recovery_3_levels.py	✅
測試	test_engine_health.py（v1.5）	✅
8. 版本紀錄
版本	日期	變更
v1.0	2026-09-20	初版
v2.0	2026-09-22	整合引擎版本管理、工時 8→9 天
文件結束
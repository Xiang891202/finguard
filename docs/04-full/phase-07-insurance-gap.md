Full Phase 7：保險缺口分析
版本：v1.0
所屬：完整版
依賴 MVP Phase：MVP P11（覆蓋率精算）
預計工時：5 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P8：保單已可管理

依賴 MVP P11：Coverage Ratio 已可計算

🔄 與 MVP 的差異
項目	MVP	完整版
快照	即時計算	每日快照
歷史	無	可查歷史
趨勢	無	缺口趨勢圖
排程	手動	自動
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/insurance_gap.py	修改	加入歷史查詢
backend/app/services/insurance/gap_analyzer.py	修改	擴充
backend/app/workers/gap_snapshot_worker.py	新增	快照 Worker
frontend/src/views/app/InsuranceGapView.vue	新增	缺口頁
frontend/src/components/insurance/GapTrendChart.vue	新增	趨勢
backend/tests/unit/test_gap_analyzer.py	修改	擴充
backend/tests/integration/test_gap_snapshots.py	新增	整合
1. 目標
建立保險缺口每日快照與歷史分析。

2. 前置條件
□ MVP P11 完成
□ insurance_gap_snapshots 表已建立
3. 前端畫面
3.1 頁面清單
頁面	路由
InsuranceGapView	/app/insurance/gap
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  📊 保險缺口分析                     │
├─────────────────────────────────────┤
│  🟢 2 | 🟡 3 | 🔴 3                  │
│                                     │
│  缺口趨勢（30 天）：                  │
│  [折線圖]                            │
│                                     │
│  部位清單：                          │
│  ├── 心臟 🔴 38%                    │
│  ├── 大腦 🟡 65%                    │
│  └── ...                             │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
InsuranceGapView.vue
├── GapSummary.vue
├── GapTrendChart.vue
└── GapPartList.vue
    └── GapPartRow.vue
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/app/insurance/gap	當前缺口
GET	/api/v1/app/insurance/gap/history	歷史快照
4.2 請求/回應範例
GET /api/v1/app/insurance/gap/history?days=30：

json
{
  "success": true,
  "data": {
    "snapshots": [
      {
        "snapshot_date": "2026-09-21",
        "summary": {"green": 2, "yellow": 3, "red": 3},
        "parts": [...]
      }
    ]
  }
}
4.3 資料庫變更
使用表：insurance_gap_snapshots

4.4 環境變數
變數	說明
GAP_SNAPSHOT_SCHEDULE	0 7 * * *
5. 單元測試
python
def test_gap_snapshot_created_daily():
    run_gap_snapshot_worker(user_id)
    snapshots = db.query(InsuranceGapSnapshot).filter_by(user_id=user_id).all()
    assert len(snapshots) > 0
6. 驗收標準
□ 每日快照自動執行
□ 歷史快照可查
□ 趨勢圖顯示
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
（略）


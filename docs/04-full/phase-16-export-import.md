Full Phase 16：資料匯出 / 匯入
版本：v1.0
所屬：完整版
依賴 MVP Phase：全部
預計工時：5 天

🔗 依賴 MVP 哪個 Phase
依賴所有 MVP Phase

🔄 與 MVP 的差異
項目	MVP	完整版
匯出	無	CSV / JSON
匯入	無	CSV / JSON
備份	無	自動
還原	無	可選
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/export.py	新增	匯出 API
backend/app/api/v1/import_.py	新增	匯入 API
backend/app/services/export_service.py	新增	匯出邏輯
backend/app/services/import_service.py	新增	匯入邏輯
frontend/src/views/app/DataManagementView.vue	新增	資料管理
backend/tests/unit/test_export.py	新增	測試
1. 目標
提供資料匯出 / 匯入功能。

2. 前置條件
□ MVP 完成
3. 前端畫面
3.1 頁面清單
頁面	路由
DataManagementView	/app/data
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  💾 資料管理                         │
├─────────────────────────────────────┤
│  【匯出】                            │
│  [匯出全部（JSON）]                  │
│  [匯出財務（CSV）]                   │
│  [匯出保險（CSV）]                   │
│                                     │
│  【匯入】                            │
│  選擇檔案：[選擇]                    │
│  格式：[○JSON ○CSV]                 │
│  [匯入]                              │
└─────────────────────────────────────┘
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/app/export	匯出
POST	/api/v1/app/import	匯入
4.2 請求/回應範例
GET /api/v1/app/export?type=all&format=json：回傳檔案

POST /api/v1/app/import：

text
Content-Type: multipart/form-data
file: [檔案]
format: json
4.3 資料庫變更
無需新增。

4.4 環境變數
變數	說明
MAX_IMPORT_SIZE	10MB
5. 單元測試
python
def test_export_json():
    data = export_service.export_all(user_id)
    assert "models" in data
    assert "holdings" in data
    assert "insurance_policies" in data

def test_import_validates_schema():
    invalid_data = {"models": [{"invalid_field": "x"}]}
    with pytest.raises(ValidationError):
        import_service.import_data(user_id, invalid_data)
6. 驗收標準
□ 匯出 JSON
□ 匯出 CSV
□ 匯入驗證
□ 匯入衝突處理
□ 單元測試 ≥ 80%
7. 交付物清單
（略）


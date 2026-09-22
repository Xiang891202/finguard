Full Phase 17：API 開放
版本：v1.0
所屬：完整版
依賴 MVP Phase：全部
預計工時：5 天

🔗 依賴 MVP 哪個 Phase
依賴所有 MVP Phase

🔄 與 MVP 的差異
項目	MVP	完整版
API Key	無	有
速率限制	IP	API Key
文件	內部	公開
沙盒	無	有
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/api_keys.py	新增	API Key 管理
backend/app/middleware/api_key_auth.py	新增	認證
backend/app/services/api_key_service.py	新增	邏輯
frontend/src/views/app/ApiKeysView.vue	新增	API Key 頁
backend/tests/unit/test_api_keys.py	新增	測試
1. 目標
開放 API 給付費用戶，提供 API Key。

2. 前置條件
□ MVP 完成
3. 前端畫面
3.1 頁面清單
頁面	路由
ApiKeysView	/app/api-keys
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  🔑 API 金鑰                         │
├─────────────────────────────────────┤
│  [新增 API Key]                      │
│                                     │
│  Key: sk_live_xxx...                 │
│  建立：2026-09-21                    │
│  權限：read                          │
│  [複製] [撤銷]                       │
│                                     │
│  速率限制：1000 / 小時               │
└─────────────────────────────────────┘
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/app/api-keys	列表
POST	/api/v1/app/api-keys	新增
DELETE	/api/v1/app/api-keys/{id}	撤銷
4.2 請求/回應範例
POST /api/v1/app/api-keys：

json
{
  "name": "My Integration",
  "scope": "read"
}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "key": "sk_live_xxx...",
    "name": "My Integration",
    "scope": "read",
    "rate_limit": 1000
  }
}
4.3 資料庫變更
新增表：

sql
CREATE TABLE api_keys (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL REFERENCES users(id),
    key_hash VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    scope VARCHAR(20) DEFAULT 'read',
    rate_limit INT DEFAULT 1000,
    last_used_at TIMESTAMP,
    revoked_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
4.4 環境變數
變數	說明
API_KEY_PREFIX	sk_live_
5. 單元測試
python
def test_api_key_generation():
    result = service.create(user_id, {"name": "Test"})
    assert result["key"].startswith("sk_live_")

def test_api_key_revoked():
    key = service.create(user_id, {"name": "Test"})
    service.revoke(user_id, key["id"])
    with pytest.raises(Unauthorized):
        authenticate(key["key"])
6. 驗收標準
□ API Key 可生成
□ API Key 可撤銷
□ 速率限制生效
□ 文件公開
□ 單元測試 ≥ 80%
7. 交付物清單
（略）
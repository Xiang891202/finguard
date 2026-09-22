Full Phase 13：多語言支援
版本：v1.0
所屬：完整版
依賴 MVP Phase：無直接依賴
預計工時：4 天

🔗 依賴 MVP 哪個 Phase
依賴所有 MVP Phase：需所有頁面已完成

🔄 與 MVP 的差異
項目	MVP	完整版
語言	中文	中文 / 英文 / 日文
i18n	無	vue-i18n
Email	中文	多語言
錯誤訊息	中文	多語言
📦 本 Phase 產出檔案
檔案路徑	動作	說明
frontend/src/locales/zh-TW.json	新增	中文
frontend/src/locales/en.json	新增	英文
frontend/src/locales/ja.json	新增	日文
frontend/src/plugins/i18n.js	新增	i18n 設定
backend/app/locales/	新增	後端翻譯
backend/app/services/i18n_service.py	新增	後端 i18n
frontend/src/components/common/LanguageSwitcher.vue	新增	語言切換
backend/tests/unit/test_i18n.py	新增	測試
1. 目標
支援中文、英文、日文。

2. 前置條件
□ MVP 完成
3. 前端畫面
3.2 UI 草圖
LanguageSwitcher：

text
┌──────────────┐
│ 🌐 語言       │
├──────────────┤
│ ✓ 繁體中文    │
│   English    │
│   日本語      │
└──────────────┘
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
PUT	/api/v1/app/account/language	更新語言偏好
4.2 請求/回應範例
PUT /api/v1/app/account/language：

json
{
  "language": "en"
}
4.3 資料庫變更
新增欄位：

sql
ALTER TABLE users ADD COLUMN language VARCHAR(5) DEFAULT 'zh-TW';
4.4 環境變數
變數	說明
DEFAULT_LANGUAGE	zh-TW
SUPPORTED_LANGUAGES	zh-TW,en,ja
5. 單元測試
python
def test_i18n_email_language():
    # 用戶語言為英文，Email 應為英文
    user = create_user(language="en")
    email = email_service.build_daily_report(user["id"])
    assert "Financial" in email["subject"]
6. 驗收標準
□ 3 種語言可切換
□ Email 支援多語言
□ 錯誤訊息多語言
□ 單元測試 ≥ 80%
7. 交付物清單
（略）


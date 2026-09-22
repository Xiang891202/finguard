Full Phase 10：漫畫生成
版本：v1.0
所屬：完整版
依賴 MVP Phase：MVP P10（Email）
預計工時：5 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P10：Email 模板已建立

依賴 Full P9：LLM 已可生成文字

🔄 與 MVP 的差異
項目	MVP	完整版
漫畫	靜態佔位	動態生成
圖庫	無	固定圖庫
文字	靜態	LLM 生成
格數	無	4-6 格
涵蓋	無	金融 + 保險
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/services/comic/comic_generator.py	新增	漫畫生成
backend/app/services/comic/template_loader.py	新增	模板載入
backend/app/services/comic/text_generator.py	新增	文字生成
backend/app/assets/comics/	新增	圖庫
backend/app/api/v1/email_preview.py	修改	加入漫畫
frontend/src/components/email/ComicPanel.vue	新增	漫畫面板
backend/tests/unit/test_comic_generator.py	新增	測試
1. 目標
建立動態漫畫生成系統，涵蓋金融水位與保險缺口。

2. 前置條件
□ MVP P10 完成
□ Full P9 完成
□ 圖庫已準備
3. 前端畫面
3.2 UI 草圖
EmailPreviewView（更新）：

text
┌─────────────────────────────────────┐
│  【區塊 5】漫畫                      │
│  ┌───────────┬───────────┐         │
│  │  [圖 1]    │  [圖 2]   │         │
│  │ 儲備金下降 │ 保險缺口  │         │
│  ├───────────┼───────────┤         │
│  │  [圖 3]    │  [圖 4]   │         │
│  │ 風險預測   │ 行動呼籲  │         │
│  └───────────┴───────────┘         │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
ComicPanel.vue
├── ComicGrid.vue
│   └── ComicCell.vue（4-6 格）
└── ComicCaption.vue
4. 後端邏輯
4.1 API 端點
沿用 MVP P10 Email 預覽，擴充 comic 欄位。

4.2 請求/回應範例
GET /api/v1/app/email-preview：

json
{
  "success": true,
  "data": {
    "sections": {
      "comic": {
        "template": "daily_report_v1",
        "panels": [
          {
            "image": "reserve_down.svg",
            "caption": "儲備金降至 5 個月"
          },
          {
            "image": "insurance_gap.svg",
            "caption": "心血管缺口需注意"
          }
        ]
      }
    }
  }
}
4.3 資料庫變更
無需新增表。

4.4 環境變數
變數	說明
COMIC_TEMPLATE	daily_report_v1
COMIC_MAX_PANELS	6
5. 單元測試
python
# tests/unit/test_comic_generator.py
def test_generate_4_panels():
    result = generator.generate(user_id, "daily_report_v1")
    assert 4 <= len(result["panels"]) <= 6

def test_comic_covers_finance_and_insurance():
    result = generator.generate(user_id, "daily_report_v1")
    captions = [p["caption"] for p in result["panels"]]
    # 至少一格金融、一格保險
    assert any("儲備" in c or "淨值" in c for c in captions)
    assert any("保險" in c or "缺口" in c for c in captions)
6. 驗收標準
□ 漫畫 4-6 格
□ 涵蓋金融 + 保險
□ 固定圖庫
□ LLM 生成文字
□ 顯示於 Email
□ 單元測試 ≥ 80%
7. 交付物清單
（略）


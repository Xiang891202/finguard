Full Phase 8：保險保單擴充子分類
版本：v1.0
所屬：完整版
依賴 MVP Phase：MVP P8（保險保單）
預計工時：4 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P8：保單 CRUD 已存在

🔄 與 MVP 的差異
項目	MVP	完整版
分類	人身 / 財產	人身 / 財產
子分類	無	壽險 / 意外 / 疾病 / 汽車 / 住宅
對應部位	基礎	完整
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/insurance.py	修改	加入子分類
backend/app/services/insurance/policy_service.py	修改	擴充
backend/app/db/seeds/insurance_subcategories.py	新增	Seed
frontend/src/components/insurance/PolicyForm.vue	修改	加入子分類
backend/tests/unit/test_policy_subcategory.py	新增	測試
1. 目標
擴充保險保單子分類。

2. 前置條件
□ MVP P8 完成
3. 前端畫面
3.2 UI 草圖
PolicyForm（更新）：

text
┌─────────────────────────────────────┐
│  新增保單                            │
├─────────────────────────────────────┤
│  分類：[○人身 ○財產]                │
│                                     │
│  子分類（若選人身）：                │
│  [○壽險 ○意外 ○疾病 ○醫療]          │
│                                     │
│  子分類（若選財產）：                │
│  [○汽車 ○住宅 ○其他]                │
│                                     │
│  保單名稱：[__________]              │
│  保額：[__________]                  │
│  涵蓋部位：                          │
│  ├── ☑ 心臟                          │
│  ├── ☐ 大腦                          │
│  └── ...                             │
│                                     │
│  [儲存] [取消]                       │
└─────────────────────────────────────┘
3.3 Vue 元件結構
沿用 MVP P8，加入動態子分類。

4. 後端邏輯
4.1 API 端點
沿用 MVP P8，加入 subcategory 驗證。

4.2 請求/回應範例
POST /api/v1/app/insurance/policies：

json
{
  "category": "life",
  "subcategory": "disease",
  "policy_name": "XX 終身醫療險",
  "coverage_amount": 1000000
}
4.3 資料庫變更
無需變更（subcategory 欄位已存在）。

4.4 環境變數
無新增。

5. 單元測試
python
def test_valid_subcategories():
    assert service.validate_subcategory("life", "life") is True
    assert service.validate_subcategory("life", "accident") is True
    assert service.validate_subcategory("life", "car") is False

def test_property_subcategories():
    assert service.validate_subcategory("property", "car") is True
    assert service.validate_subcategory("property", "home") is True
6. 驗收標準
□ 子分類驗證正確
□ 動態下拉選單
□ 單元測試 ≥ 80%
7. 交付物清單
（略）


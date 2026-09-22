Full Phase 11：保險缺口精算
版本：v1.0
所屬：完整版
依賴 MVP Phase：MVP P11（基礎精算）
預計工時：7 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P11：Coverage Ratio 基礎計算已存在

🔄 與 MVP 的差異
項目	MVP	完整版
乘數	4 個	8 個
醫療費用	8 疾病	30+ 疾病
基因	8 點位	20+ 點位
精算維度	基礎	多維
年齡分段	4 段	8 段
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/services/insurance/coverage_calculator.py	修改	擴充
backend/app/db/seeds/medical_costs_extended.py	新增	擴充 Seed
backend/app/db/seeds/genetic_markers_extended.py	新增	擴充 Seed
backend/tests/unit/test_coverage_advanced.py	新增	測試
1. 目標
擴充精算模型，納入更多乘數與維度。

2. 前置條件
□ MVP P11 完成
3. 前端畫面
沿用 MVP P11，擴充詳情面板。

3.2 UI 草圖
PartDetailPanel（更新）：

text
┌────────────────────────────────┐
│  心臟 / 心血管                  │
├────────────────────────────────┤
│  覆蓋率：38% 🔴                 │
│                                │
│  計算細節：                     │
│  ├── 基礎：50 萬                │
│  ├── 年齡 55 歲：×1.5           │
│  ├── 性別 男：×1.3              │
│  ├── 家族病史：×1.5             │
│  ├── 基因（LDLR+）：×1.8        │
│  ├── 生活習慣（吸菸）：×1.2     │
│  ├── BMI（過重）：×1.1          │
│  └── 職業（高風險）：×1.0       │
│                                │
│  = 需求：263 萬                 │
└────────────────────────────────┘
4. 後端邏輯
4.1 API 端點
沿用 MVP P11。

4.2 請求/回應範例
GET /api/v1/app/insurance/gap：

json
{
  "success": true,
  "data": {
    "parts": [
      {
        "part_code": "heart",
        "required_coverage": 3159000,
        "calculation_detail": {
          "base_cost": 500000,
          "age_multiplier": 1.5,
          "gender_multiplier": 1.3,
          "family_history_multiplier": 1.5,
          "genetic_multiplier": 1.8,
          "lifestyle_multiplier": 1.2,
          "bmi_multiplier": 1.1,
          "occupation_multiplier": 1.0
        }
      }
    ]
  }
}
4.3 資料庫變更
擴充 user_health_profiles：

sql
ALTER TABLE user_health_profiles 
ADD COLUMN lifestyle JSONB,
ADD COLUMN bmi NUMERIC(4, 1),
ADD COLUMN occupation_risk VARCHAR(20);
4.4 環境變數
無新增。

5. 單元測試
python
def test_8_multipliers():
    result = calculator.calculate(
        base_cost=500000,
        age=55,
        gender="male",
        family_history=True,
        genetic_positive=True,
        lifestyle={"smoking": True},
        bmi=27.5,
        occupation="high_risk"
    )
    # 500000 × 1.5 × 1.3 × 1.5 × 1.8 × 1.2 × 1.1 × 1.0 = 3159000
    assert result["required_coverage"] == 3159000
6. 驗收標準
□ 8 個乘數正確
□ 30+ 疾病費用
□ 20+ 基因點位
□ 年齡分段 8 段
□ 單元測試 ≥ 80%
7. 交付物清單
（略）


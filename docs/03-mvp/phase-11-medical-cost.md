Phase 11：醫療費用 + 覆蓋率精算
版本：v1.0
所屬：MVP
依賴 Phase：P8, P9
預計工時：5 天

⚠️ 本 Phase 的 MVP/完整版約束
MVP：醫療費用人工 Seed（Full P19 才用爬蟲）

Coverage Ratio 精準計算

顯示保障缺口，不推薦商品

📂 前置檔案檢查
檔案路徑	來源
docs/02-reference/01-database-schema.md	第二批
docs/03-mvp/phase-08-insurance.md	第三批
docs/03-mvp/phase-09-forecast.md	第三批
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/insurance.py	修改	加入 gap 端點
backend/app/api/v1/admin_medical.py	新增	醫療費用管理
backend/app/services/insurance/coverage_calculator.py	新增	覆蓋率計算
backend/app/services/health/medical_cost_service.py	新增	醫療費用
backend/app/db/seeds/medical_costs.py	新增	Seed 醫療費用
backend/app/db/seeds/disease_risk_mapping.py	新增	Seed 風險映射
frontend/src/views/app/BodyMapView.vue	新增	人體圖譜（唯讀）
frontend/src/components/body-map/BodyMap.vue	新增	人體圖
frontend/src/components/body-map/BodyPart.vue	新增	部位
frontend/src/components/body-map/PartDetailPanel.vue	新增	部位詳情
frontend/src/components/insurance/CoverageRatio.vue	新增	覆蓋率
frontend/src/views/admin/MedicalCostsView.vue	新增	醫療費用管理
frontend/src/views/admin/GeneticMarkersView.vue	新增	基因點位管理
frontend/src/api/coverage.js	新增	API
frontend/src/api/bodyMap.js	新增	API
backend/tests/unit/test_coverage_calculator.py	新增	測試
backend/tests/integration/test_coverage_flow.py	新增	整合
1. 目標
建立醫療費用參考、精準覆蓋率計算、人體圖譜（唯讀）。

2. 前置條件
□ P8, P9 完成
□ 健康檔案已可填寫
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
BodyMapView	/app/body-map	人體圖譜（唯讀）
MedicalCostsView	/admin/medical-costs	醫療費用管理
GeneticMarkersView	/admin/genetic-markers	基因點位管理
3.2 UI 草圖
BodyMapView：

text
┌─────────────────────────────────────┐
│  🧬 人體圖譜                         │
├─────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐│
│  │              │  │ 心臟 / 心血管 ││
│  │   [人體圖]    │  │              ││
│  │              │  │ 覆蓋率：38%  ││
│  │    ● 心臟     │  │ 🔴 嚴重缺口  ││
│  │              │  │              ││
│  │              │  │ 現有：100 萬  ││
│  │              │  │ 需求：263 萬  ││
│  │              │  │              ││
│  │              │  │ 醫療費用參考：││
│  │              │  │ 15-30 萬      ││
│  │              │  │              ││
│  │              │  │ 乘數：        ││
│  │              │  │ 年齡 1.5×    ││
│  │              │  │ 性別 1.3×    ││
│  │              │  │ 家族 1.5×    ││
│  │              │  │ 基因 1.8×    ││
│  └──────────────┘  └──────────────┘│
│                                     │
│  🟢 2 | 🟡 3 | 🔴 3                  │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
BodyMapView.vue
├── BodyMap.vue
│   ├── BodyPart.vue（8 個）
│   └── SVG 底圖
└── PartDetailPanel.vue
    ├── CoverageRatio.vue
    └── CalculationDetail.vue

MedicalCostsView.vue（管理員）
├── MedicalCostList.vue
└── MedicalCostForm.vue

GeneticMarkersView.vue（管理員）
├── GeneticMarkerList.vue
└── GeneticMarkerForm.vue
元件職責：

元件	職責	Props	Emits
BodyMapView	頁面	-	-
BodyMap	人體圖	parts: Array	part-click
BodyPart	單一部位	part: Object, state: String	click
PartDetailPanel	詳情	part: Object, coverage: Object	-
CoverageRatio	覆蓋率	ratio: Number	-
3.4 樣式規範
人體圖：SVG 三色高亮

動畫：點擊部位 200ms 過場

顏色：綠 #10B981 / 黃 #F59E0B / 紅 #EF4444

3.5 響應式設計
裝置	佈局
電腦	左右佈局
平板	上下佈局
手機	上下佈局，詳情底部彈窗
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/app/insurance/gap	缺口查詢（含精算）
GET	/api/v1/app/insurance/body-map	部位清單
GET	/api/v1/admin/medical-costs	醫療費用列表
POST	/api/v1/admin/medical-costs	新增
PUT	/api/v1/admin/medical-costs/{id}	更新
DELETE	/api/v1/admin/medical-costs/{id}	刪除
GET	/api/v1/admin/genetic-markers	基因點位列表
POST	/api/v1/admin/genetic-markers	新增
4.2 請求/回應範例
GET /api/v1/app/insurance/gap：

json
{
  "success": true,
  "data": {
    "snapshot_date": "2026-09-21",
    "parts": [
      {
        "part_code": "heart",
        "part_name": "心臟 / 心血管",
        "existing_coverage": 1000000,
        "required_coverage": 2632500,
        "coverage_ratio": 0.38,
        "state": "red",
        "calculation_detail": {
          "base_cost": 500000,
          "age_multiplier": 1.5,
          "gender_multiplier": 1.3,
          "family_history_multiplier": 1.5,
          "genetic_multiplier": 1.8
        }
      }
    ],
    "summary": {
      "green_count": 2,
      "yellow_count": 3,
      "red_count": 3
    }
  }
}
4.3 資料庫變更
使用表：medical_cost_references, disease_risk_mapping, insurance_gap_snapshots

Seed 醫療費用（8 個疾病）與風險映射。

4.4 環境變數
無新增。

5. 單元測試
5.1 後端測試
python
# tests/unit/test_coverage_calculator.py
def test_coverage_basic():
    result = coverage_calc.calculate(
        base_cost=500000,
        age=55,
        gender="male",
        family_history=True,
        genetic_positive=True
    )
    # 500000 × 1.5 × 1.3 × 1.5 × 1.8 = 2632500
    assert result["required_coverage"] == 2632500

def test_coverage_no_multipliers():
    result = coverage_calc.calculate(
        base_cost=500000,
        age=25,
        gender="female",
        family_history=False,
        genetic_positive=False
    )
    # 只有基礎費用
    assert result["required_coverage"] == 500000

def test_coverage_state_green():
    result = coverage_calc.compute_state(
        existing=1000000,
        required=500000
    )
    assert result["state"] == "green"
    assert result["coverage_ratio"] == 2.0

def test_coverage_state_yellow():
    result = coverage_calc.compute_state(existing=700000, required=1000000)
    assert result["state"] == "yellow"

def test_coverage_state_red():
    result = coverage_calc.compute_state(existing=300000, required=1000000)
    assert result["state"] == "red"
5.2 前端測試
javascript
describe('CoverageRatio', () => {
  it('displays red state for low ratio', () => {
    const wrapper = mount(CoverageRatio, {
      props: { ratio: 0.38, state: 'red' }
    })
    expect(wrapper.find('.state-red').exists()).toBe(true)
  })
})

describe('BodyMap', () => {
  it('emits part-click on part click', async () => {
    const wrapper = mount(BodyMap, {
      props: { parts: [{ part_code: 'heart' }] }
    })
    await wrapper.find('[data-part="heart"]').trigger('click')
    expect(wrapper.emitted('part-click')[0]).toEqual(['heart'])
  })
})
5.3 整合測試
python
def test_coverage_flow(auth_client, test_user_with_health_profile, test_insurance_policies):
    response = auth_client.get("/api/v1/app/insurance/gap")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "parts" in data
    assert "summary" in data
    # 驗證心臟部位計算
    heart = next(p for p in data["parts"] if p["part_code"] == "heart")
    assert "coverage_ratio" in heart
    assert heart["state"] in ["green", "yellow", "red"]
6. 驗收標準
□ 醫療費用 Seed 完成（≥ 8 疾病）
□ 疾病風險映射 Seed 完成
□ Coverage Ratio 計算正確
□ 年齡、性別、家族病史、基因乘數正確
□ 人體圖譜可點擊
□ 三色狀態正確
□ 響應式設計
□ 不顯示具體商品推薦
□ 管理員可管理醫療費用
□ 管理員可管理基因點位
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
類型	檔案	狀態
後端	coverage_calculator.py, medical_cost_service.py	✅
後端	Seeds: medical_costs, disease_risk_mapping	✅
前端	BodyMapView, BodyMap, BodyPart, PartDetailPanel	✅
前端	CoverageRatio, MedicalCostsView, GeneticMarkersView	✅
測試	test_coverage_calculator.py, test_coverage_flow.py	✅
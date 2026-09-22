Full Phase 5：人體剖面圖
版本：v1.0
所屬：完整版
依賴 MVP Phase：MVP P8（保險保單 CRUD）
預計工時：7 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P8：body_part_mapping 表已建立

依賴 MVP P11：Coverage Ratio 已可計算

🔄 與 MVP 的差異
項目	MVP	完整版
人體圖譜	無	SVG 互動
三色狀態	API 回傳	互動顯示
點擊部位	❌	✅
響應式	❌	電腦 / 平板 / 手機
管理員擴充	❌	✅
📦 本 Phase 產出檔案
檔案路徑	動作	說明
backend/app/api/v1/body_map.py	修改	加入互動 API
backend/app/services/insurance/body_map_service.py	修改	擴充
frontend/src/views/app/BodyMapView.vue	修改	互動版本
frontend/src/components/body-map/BodyMap.vue	修改	SVG 互動
frontend/src/components/body-map/BodyPart.vue	修改	動畫
frontend/src/components/body-map/PartDetailPanel.vue	修改	側欄
frontend/src/composables/useBodyMapInteraction.js	新增	互動邏輯
frontend/src/assets/svg/human-body.svg	新增	SVG 底圖
backend/tests/unit/test_body_map_service.py	新增	測試
1. 目標
建立互動式人體剖面圖，支援三色狀態與點擊互動。

2. 前置條件
□ MVP P8, P11 完成
□ SVG 底圖已準備
3. 前端畫面
3.1 頁面清單
頁面	路由
BodyMapView	/app/body-map
3.2 UI 草圖
text
┌─────────────────────────────────────┐
│  🧬 人體剖面圖                       │
├─────────────────────────────────────┤
│  ┌────────────┐ ┌────────────────┐  │
│  │            │ │ 心臟 / 心血管   │  │
│  │  [人體圖]   │ │                │  │
│  │  左：外觀   │ │ 覆蓋率：38%    │  │
│  │  右：內部   │ │ 🔴 嚴重缺口    │  │
│  │            │ │                │  │
│  │   ●心臟     │ │ 現有：100 萬   │  │
│  │   ●大腦     │ │ 需求：263 萬   │  │
│  │            │ │                │  │
│  │            │ │ 醫療費用參考：  │  │
│  │            │ │ 15-30 萬       │  │
│  └────────────┘ └────────────────┘  │
│                                     │
│  🟢 2 | 🟡 3 | 🔴 3                  │
└─────────────────────────────────────┘
3.3 Vue 元件結構
text
BodyMapView.vue
├── BodyMap.vue
│   ├── SvgBase.vue（左：外觀）
│   ├── SvgInternal.vue（右：內部）
│   └── BodyPart.vue（8 個，可點擊）
└── PartDetailPanel.vue
    ├── CoverageRatio.vue
    └── CalculationDetail.vue
元件職責：

元件	職責	Props	Emits
BodyMap	人體圖	parts: Array, coverageMap: Object	part-click
BodyPart	單一部位	part: Object, state: String, selected: Boolean	click
PartDetailPanel	詳情	part: Object, coverage: Object	-
狀態管理：

類型	檔案	用途
Composable	composables/useBodyMapInteraction.js	選取、動畫
3.4 樣式規範
動畫：

點擊：選中部位 glow 300ms

其他部位：opacity 0.3，300ms

顏色：

🟢 #10B981

🟡 #F59E0B

🔴 #EF4444

3.5 響應式設計
裝置	佈局
電腦	左右佈局，圖 60% / 面板 40%
平板	上下佈局，圖 60% / 面板 40%
手機	上下佈局，面板底部彈窗
4. 後端邏輯
4.1 API 端點
方法	路徑	說明
GET	/api/v1/app/insurance/body-map	部位清單（含 ui_config）
GET	/api/v1/app/insurance/gap	缺口（含 coverage_ratio）
4.2 請求/回應範例
GET /api/v1/app/insurance/body-map：

json
{
  "success": true,
  "data": {
    "parts": [
      {
        "part_code": "heart",
        "part_name": "心臟 / 心血管",
        "category": "internal",
        "ui_config": {
          "svg_id": "part-heart",
          "view": "internal",
          "path": "M120,100 ..."
        },
        "state": "red",
        "coverage_ratio": 0.38
      }
    ]
  }
}
4.3 資料庫變更
擴充 body_part_mapping.ui_config：

sql
UPDATE body_part_mapping SET ui_config = jsonb_set(
    ui_config, '{view}', '"internal"'::jsonb
) WHERE category = 'internal';
4.4 環境變數
無新增。

5. 單元測試
5.1 後端測試
python
# tests/unit/test_body_map_service.py
def test_get_body_map_with_state():
    result = service.get_map(user_id)
    heart = next(p for p in result["parts"] if p["part_code"] == "heart")
    assert "state" in heart
    assert heart["state"] in ["green", "yellow", "red"]
5.2 前端測試
javascript
describe('BodyMap', () => {
  it('emits part-click on heart click', async () => {
    const wrapper = mount(BodyMap, {
      props: { parts: [{ part_code: 'heart' }] }
    })
    await wrapper.find('[data-part="heart"]').trigger('click')
    expect(wrapper.emitted('part-click')[0]).toEqual(['heart'])
  })

  it('dims other parts when one selected', async () => {
    const wrapper = mount(BodyMap, {
      props: { parts: [{ part_code: 'heart' }, { part_code: 'brain' }] }
    })
    await wrapper.find('[data-part="heart"]').trigger('click')
    expect(wrapper.find('[data-part="brain"]').classes()).toContain('dimmed')
  })
})
5.3 整合測試
python
def test_body_map_flow(auth_client, test_user_with_policies):
    response = auth_client.get("/api/v1/app/insurance/body-map")
    assert response.status_code == 200
    parts = response.json()["data"]["parts"]
    assert len(parts) == 8
    for part in parts:
        assert "ui_config" in part
        assert "state" in part
6. 驗收標準
□ SVG 人體圖正確顯示
□ 左右半身（外觀 / 內部）
□ 三色狀態正確
□ 點擊部位高亮
□ 其他部位變暗
□ 側欄顯示詳情
□ 響應式（3 裝置）
□ 觸控區域 ≥ 44px
□ 單元測試 ≥ 80%
□ 整合測試通過
7. 交付物清單
（略）
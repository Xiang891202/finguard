📄 文件 A：每日工作流程
版本：v1.0
適用範圍：實作階段每日工作節奏

markdown
# 每日工作流程（Daily Workflow）

**版本**：v1.0
**最後更新**：2026-09-22

---

## 1. 為什麼需要每日工作流程？

實作 32 個 Phase（165 天）需要**穩定的節奏**。本文件定義：

- ✅ 每天該做什麼
- ✅ 每個時段分配多少時間
- ✅ 如何避免「做到一半卡住」
- ✅ 如何確保進度可控

---

## 2. 每日三時段制（建議）
┌─────────────────────────────────────────────────────────────┐
│ 🌅 早上（09:00-12:00）3 小時 │
│ ├── 09:00-09:15 檢視昨日進度 │
│ ├── 09:15-09:30 確認今日任務 │
│ ├── 09:30-11:30 深度實作（無干擾） │
│ └── 11:30-12:00 撰寫單元測試 │
└─────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│ ☀️ 下午（13:00-18:00）5 小時 │
│ ├── 13:00-15:00 繼續實作 │
│ ├── 15:00-15:30 休息 + 複習文件 │
│ ├── 15:30-17:00 整合測試 │
│ └── 17:00-18:00 Git commit + 更新文件 │
└─────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│ 🌙 晚上（19:00-21:00）2 小時（彈性） │
│ ├── 19:00-20:00 Code Review（自我） │
│ ├── 20:00-20:30 修正問題 │
│ └── 20:30-21:00 明日規劃 │
└─────────────────────────────────────────────────────────────┘

text

**每日總工時**：8-10 小時（彈性調整）

---

## 3. 每日詳細流程

### 3.1 早上：啟動與深度實作

#### 09:00-09:15 檢視昨日進度

**動作**：
1. 打開 `git log --oneline -10` 查看昨日 commit
2. 檢視昨日未完成的任務
3. 確認是否有 failing test

**檢查清單**：
- [ ] 昨日 commit 是否已 push？
- [ ] 是否有未解決的 TODO？
- [ ] CI 是否綠燈？

#### 09:15-09:30 確認今日任務

**動作**：
1. 打開當前 Phase 規劃書
2. 對照「每日進度」表格
3. 列出今日 3 個主要任務

**範例**（Phase 3 Day 2）：
今日任務：

實作 EquityHandler.fetch_price()

實作 EquityHandler.calculate_volatility()

撰寫 EquityHandler 單元測試

text

#### 09:30-11:30 深度實作（無干擾）

**原則**：
- 關閉 Slack / Email 通知
- 手機靜音
- 番茄鐘 50 分鐘 + 休息 10 分鐘

**實作順序**：
先寫測試（TDD）
↓

實作最小可用版本
↓

測試通過
↓

重構
↓

再測試

text

**每日進度追蹤**：
```markdown
## Phase 3 Day 2 進度

- [x] EquityHandler.fetch_price() 實作
- [x] EquityHandler.calculate_volatility() 實作
- [ ] EquityHandler 單元測試（進行中）
- [ ] 整合測試（下午）
11:30-12:00 撰寫單元測試
動作：

為上午實作的程式碼寫測試

確保覆蓋率 ≥ 80%

執行 pytest tests/unit/

測試範例：

python
# tests/unit/handlers/test_equity_handler.py

def test_fetch_price_success():
    handler = EquityHandler({...})
    with patch("...get_stock_price", return_value=155.20):
        assert handler.fetch_price("2026-09-22") == 155.20

def test_fetch_price_fallback():
    handler = EquityHandler({...})
    with patch("...get_stock_price", 
               side_effect=[Exception(), 155.18]):
        assert handler.fetch_price("2026-09-22") == 155.18
3.2 下午：整合與收尾
13:00-15:00 繼續實作
動作：

完成上午未完的任務

實作下午規劃的任務

持續測試

注意事項：

若卡住 > 30 分鐘 → 記錄問題，跳過，繼續下一項

不要陷入「完美主義」

先求有，再求好

15:00-15:30 休息 + 複習文件
動作：

離開座位，走動 5-10 分鐘

複習當前 Phase 的規劃書

檢視是否有遺漏

複習清單：

□ Phase 目標是否達成？
□ 驗收標準是否清楚？
□ 是否有未預期的依賴？
15:30-17:00 整合測試
動作：

撰寫整合測試（API → Service → DB）

執行 pytest tests/integration/

修正問題

整合測試範例：

python
# tests/integration/test_holdings_crud.py

def test_holdings_crud_integration(auth_client, test_model, test_asset):
    # POST
    response = auth_client.post("/api/v1/app/holdings", json={...})
    assert response.status_code == 201
    
    # GET
    response = auth_client.get("/api/v1/app/holdings")
    assert len(response.json()["data"]) == 1
    
    # PUT
    holding_id = response.json()["data"][0]["id"]
    response = auth_client.put(f"/api/v1/app/holdings/{holding_id}", json={...})
    assert response.status_code == 200
    
    # DELETE
    response = auth_client.delete(f"/api/v1/app/holdings/{holding_id}")
    assert response.status_code == 200
17:00-18:00 Git commit + 更新文件
動作：

執行測試確保全部通過

Git add + commit

Push 到遠端

更新 Phase 進度文件

Commit 規範：

text
feat(holdings): 實作 EquityHandler

- 實作 fetch_price()
- 實作 calculate_volatility()
- 加入 fallback 機制
- 單元測試覆蓋率 85%

Closes: Phase-3-Day-2
更新 Phase 進度：

markdown
# Phase 3 進度（Day 2/4）

## Day 1 ✅
- [x] BaseAssetHandler 抽象類
- [x] 專案結構建立

## Day 2 ✅
- [x] EquityHandler.fetch_price()
- [x] EquityHandler.calculate_volatility()
- [x] 單元測試

## Day 3（明日）
- [ ] 持有部位 CRUD API

## Day 4
- [ ] 前端頁面整合
3.3 晚上：檢討與規劃（彈性）
19:00-20:00 Code Review（自我）
動作：

重新檢視今日 commit

檢查是否有：

未使用的 import

硬編碼的值

缺少的錯誤處理

違反 SRP 的程式碼

Code Review 清單：

□ 函式命名清楚？
□ 是否有重複邏輯？
□ 錯誤處理完整？
□ 註解是否必要？
□ 測試是否充分？
20:00-20:30 修正問題
動作：

修正 Code Review 發現的問題

重新執行測試

再次 commit

20:30-21:00 明日規劃
動作：

對照 Phase 規劃書

列出明日 3 個主要任務

準備好前置資料

明日規劃範本：

markdown
## 明日（Day 3）任務

1. 實作持有部位 CRUD API
   - POST /api/v1/app/holdings
   - GET /api/v1/app/holdings
   - PUT /api/v1/app/holdings/{id}
   - DELETE /api/v1/app/holdings/{id}

2. 撰寫單元測試
3. 撰寫整合測試

## 前置準備
- [ ] 確認 holdings 表結構
- [ ] 確認 API 請求格式
- [ ] 準備測試資料
4. 每週節奏
4.1 週一：啟動新 Phase
text
09:00-10:00  讀 Phase 規劃書
10:00-12:00  建立專案結構、確認依賴
13:00-18:00  開始實作
4.2 週二至週四：穩定實作
text
照每日三時段制進行
4.3 週五：Phase 驗收
text
09:00-12:00  完成剩餘任務
13:00-15:00  整合測試
15:00-16:00  驗收標準檢查
16:00-17:00  更新文件、Git commit
17:00-18:00  Phase 回顧
4.4 週末：彈性
text
- 補進度（若有落後）
- 學習新技術（若需要）
- 休息
5. 進度追蹤
5.1 每日追蹤表
建立 docs/progress/daily-log.md：

markdown
# 每日進度追蹤

## 2026-10-01（Day 1 / Phase 0）
- [x] 建立專案結構
- [x] 安裝套件
- [ ] 建立資料表（進行中）

**工時**：8 小時
**心情**：😊 順利
**問題**：無

## 2026-10-02（Day 2 / Phase 0）
...
5.2 每週追蹤表
建立 docs/progress/weekly-log.md：

markdown
# 每週進度追蹤

## Week 1（2026-10-01 ~ 2026-10-07）
**Phase**：P0（基礎建設）

- 完成日：2026-10-03（提前 0 天）
- 測試覆蓋率：85%
- 遇到問題：Docker 網路設定
- 解決方式：改用 host network
- 下週目標：P1（用戶認證 + 健康檔案）
6. 常見情境處理
6.1 卡關超過 30 分鐘
text
1. 記錄問題到 docs/issues/
2. 標記「需協助」
3. 跳過，繼續下一項任務
4. 晚上或隔天再處理
問題記錄範本：

markdown
# Issue-001：Docker 容器無法連線 PostgreSQL

**日期**：2026-10-01
**Phase**：P0 Day 2
**嚴重度**：高

**問題描述**：
執行 docker-compose up 後，FastAPI 無法連線 PostgreSQL

**已嘗試**：
1. 檢查環境變數 → 正確
2. 檢查網路 → 可能問題

**待嘗試**：
1. 改用 host network
2. 檢查防火牆設定
6.2 測試一直失敗
text
1. 先確認是「程式碼錯」還是「測試錯」
2. 若是程式碼錯 → 修程式碼
3. 若是測試錯 → 修測試
4. 若都不確定 → 加 log，觀察實際行為
6.3 進度落後
text
1. 分析落後原因
2. 若是「低估工時」→ 調整後續 Phase 預估
3. 若是「卡關」→ 尋求協助
4. 若是「分心」→ 檢討工作環境
5. 決定：加班趕進度 / 延後 Phase
6.4 想改架構
text
1. 停止當前 Phase
2. 評估影響範圍
3. 建立 Framework v1.6
4. 影響分析
5. 決定：繼續 / 重做 / 修改
6. 記錄在 Phase 規劃書
7. 每日檢查清單
7.1 早上啟動
□ 檢視昨日 commit
□ 確認今日 3 個任務
□ 環境正常（DB / Redis 連線）
7.2 中午檢查
□ 上午任務進度 50% 以上
□ 至少 1 個單元測試通過
7.3 下午收尾
□ 今日任務完成
□ 單元測試通過
□ 整合測試通過
□ Git commit
□ 更新 Phase 進度
7.4 晚上檢討
□ Code Review 完成
□ 明日規劃完成
□ 記錄卡關問題
8. 工具建議
用途	工具
任務追蹤	GitHub Issues / Notion
番茄鐘	Pomofocus / Forest
時間追蹤	Toggl / Clockify
筆記	Obsidian / Notion
Git GUI	GitKraken / SourceTree
API 測試	Postman / Insomnia / HTTPie
9. 健康提醒
項目	建議
睡眠	每日 7-8 小時
運動	每週 3 次（每次 30 分鐘）
眼睛	每 50 分鐘休息 10 分鐘
姿勢	每小時起身走動
飲食	定時用餐，不邊寫程式邊吃
10. 版本紀錄
版本	日期	變更
v1.0	2026-09-22	初版建立
文件結束
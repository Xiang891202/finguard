📄 文件 B：驗證清單

**版本**：v1.0
**適用範圍**：每個 Phase 的驗證檢查

---

```markdown
# 驗證清單（Verification Checklist）

**版本**：v1.0
**最後更新**：2026-09-22

---

## 1. 為什麼需要驗證清單？

每個 Phase 完成時，必須確認**所有面向都通過**。本文件定義：

- ✅ 每個 Phase 的通用檢查項
- ✅ 各 Phase 的特定檢查項
- ✅ 整體系統的驗證方式
- ✅ 問題發現時的處理流程

---

## 2. 通用驗證清單（每個 Phase 都適用）

### 2.1 程式碼品質

- [ ] 所有單元測試通過（`pytest tests/unit/`）
- [ ] 所有整合測試通過（`pytest tests/integration/`）
- [ ] 測試覆蓋率 ≥ 80%（`pytest --cov`）
- [ ] 無 lint 錯誤（`ruff check .` / `eslint .`）
- [ ] 無型別錯誤（`mypy .` / TypeScript）
- [ ] 無未使用的 import
- [ ] 無硬編碼的敏感資訊（密碼、API Key）

### 2.2 功能驗證

- [ ] 前端畫面可操作
- [ ] 後端 API 端點回應正確
- [ ] API 回應格式符合規格
- [ ] 錯誤處理正確（404、401、500）
- [ ] 資料庫變更已套用
- [ ] 環境變數已設定

### 2.3 測試驗證

- [ ] 成功情境測試通過
- [ ] 失敗情境測試通過
- [ ] 邊界情境測試通過
- [ ] Fallback 情境測試通過（若適用）
- [ ] 錯誤處理測試通過

### 2.4 安全驗證

- [ ] 認證機制正確（JWT / OTP）
- [ ] 授權檢查正確（管理員 / 用戶）
- [ ] 資料隔離正確（tenant_id + user_id）
- [ ] SQL Injection 防護（ORM 使用正確）
- [ ] XSS 防護（前端轉義）
- [ ] 敏感資料加密（基因、密碼）

### 2.5 文件驗證

- [ ] Phase 規劃書已更新
- [ ] API 規格已更新（若有變更）
- [ ] 資料庫 Schema 已更新（若有變更）
- [ ] 環境變數文件已更新
- [ ] 交付物清單已確認

### 2.6 Git 驗證

- [ ] 所有變更已 commit
- [ ] Commit message 清楚
- [ ] 已 push 到遠端
- [ ] CI 綠燈
- [ ] 無未追蹤的檔案（除 .gitignore）

---

## 3. 各 Phase 特定驗證清單

### Phase 0：基礎建設

- [ ] `docker-compose up` 可執行
- [ ] 36 張表建立完成
- [ ] `GET /health` 回應 200
- [ ] 前端可訪問（顯示版本）
- [ ] CI 可執行（lint + test）
- [ ] 資料庫遷移（Alembic）可執行

**驗證指令**：
```bash
docker-compose up -d
curl http://localhost:8000/health
# 應回應 {"status": "healthy", "version": "1.5.0"}
Phase 1：用戶認證 + 健康檔案
□ 用戶可用 Email + OTP 登入
□ 管理員可用 Email + 密碼登入
□ OTP 防濫用機制生效（60 秒、每日上限）
□ Refresh Token Rotation 生效
□ 新用戶登入後強制導向健康檔案
□ 健康檔案完成度計算正確（生日 40% + 性別 40% + 家族 10% + 基因 10%）
□ 基因資料加密存儲（Fernet）
□ 基因同意書獨立顯示
□ 舊用戶可跳過健康檔案
□ 響應式設計（3 裝置）
驗證指令：

bash
# 完整認證流程
curl -X POST /auth/otp/request -d '{"email": "test@example.com"}'
# 從 DB 取 OTP
curl -X POST /auth/otp/verify -d '{"email": "test@example.com", "otp": "123456"}'
Phase 2：財務模型 + 金庫
□ 模型 CRUD 完整
□ 金庫 CRUD 完整
□ 模型上限生效（一般用戶 2、管理員 10）
□ 軟刪除（is_archived）
□ 預設模型只能一個
□ 響應式設計
驗證指令：

bash
# 一般用戶測試上限
curl -X POST /app/models -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"name": "M1"}'
curl -X POST /app/models -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"name": "M2"}'
curl -X POST /app/models -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"name": "M3"}'
# 第三次應回 400 MODEL_LIMIT_EXCEEDED
Phase 3：持有部位（EquityHandler）
□ 持有部位 CRUD 完整
□ EquityHandler 實作完成
□ EquityHandler 單元測試通過
□ 資產下拉選擇可用
□ 損益計算正確
□ 響應式設計
驗證指令：

bash
curl -X POST /app/holdings -H "Authorization: Bearer $TOKEN" \
  -d '{"model_id": "...", "asset_definition_id": "...", 
       "quantity": 100, "average_cost": 150.50}'
Phase 4：負債
□ 負債 CRUD 完整
□ 剩餘金額不可超過總額
□ 響應式設計
Phase 5：外匯（ForexHandler）
□ ForexHandler 實作完成
□ ForexHandler 單元測試通過（含 fallback）
□ 外匯 Seed 資料建立
□ 可透過 HoldingsView 管理
Phase 6：貨幣基金
□ MoneyMarketHandler 實作完成
□ 固定低波動率正確
□ Seed 資料建立
Phase 7：爬蟲調度 + 三源驗證
□ 手動觸發爬蟲
□ 三源驗證 Level 1/2/3 正確
□ DATA_CONFLICT 觸發 Incident
□ STALE 標記正確
□ 管理員可查看歷史
□ 動態載入 Handler 正確
驗證指令：

bash
curl -X POST /app/crawler/trigger -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"asset_class": "equity"}'
Phase 8：保險保單 CRUD
□ 保單 CRUD 完整
□ 人身 / 財產分類正確
□ 子分類正確
□ Body Part Selector 可用
□ body_part_mapping Seed 完成（8 部位）
□ 響應式設計
Phase 9：蒙地卡羅 + 風險計算（v2.0）
□ 蒙地卡羅引擎實作
□ 3 個月與 6 個月預測
□ 破產機率計算正確
□ 儲備金跌破機率計算正確
□ 市場情緒數值化（sentiment_score）
□ 規則式解讀正確（v1.5）
□ 無 LLM 依賴（v1.5）
□ 圖表顯示正確
驗證指令：

bash
# 驗證無 LLM 依賴
grep -r "ollama\|llm" backend/app/services/forecast/
# 應該沒有結果
Phase 10：Email 報告 + 自癒（v2.0）
□ Email 6 區塊齊全
□ 保險缺口顯示 Coverage Ratio（非商品）
□ 市場情緒用規則式解讀（v1.5）
□ 無 LLM 依賴（v1.5）
□ 管理員可收到異常警報
□ Level 1 修復不通知
□ Level 2 記錄 Incident
□ Level 3 停止並通知
□ 通知頻率控制生效
驗證指令：

bash
curl /app/email-preview -H "Authorization: Bearer $TOKEN"
# 回應應包含 6 個 sections
Phase 11：醫療費用 + 覆蓋率精算
□ 醫療費用 Seed 完成（≥ 8 疾病）
□ 疾病風險映射 Seed 完成
□ Coverage Ratio 計算正確
□ 年齡、性別、家族病史、基因乘數正確
□ 人體圖譜可點擊
□ 三色狀態正確
□ 不顯示具體商品推薦
□ 管理員可管理醫療費用
□ 管理員可管理基因點位
驗證指令：

bash
curl /app/insurance/gap -H "Authorization: Bearer $TOKEN"
# 驗證 calculation_detail 欄位
4. 完整版各 Phase 驗證清單（摘要）
Full P1：多租戶架構
□ 多租戶隔離生效
□ 所有查詢帶 tenant_id
□ 管理員可跨租戶管理
□ 租戶註冊流程可用
□ 租戶方案限制生效
□ 隔離測試通過
Full P5.5：引擎版本管理（v1.5）
□ 5 大引擎版本管理可用
□ 版本生命週期正確
□ 同一引擎同時只有一個 active
□ 執行快照正確記錄
□ 追蹤樹可視覺化
□ 重算任務可執行
□ Redis Pub/Sub 快取失效生效（< 1 秒）
□ 圖形化編輯器可即時測試
□ 權限控制正確（僅管理員）
驗證指令：

bash
# 測試快取失效
curl -X POST /admin/engines/llm/versions/{id}/activate
# 應 < 1 秒後生效
Full P9：LLM Provider 抽象層（v2.0）
□ 5 個 Provider 實作完成
□ Provider 依方案路由
□ Provider 可切換（管理員 UI）
□ 成本追蹤正確
□ 整合引擎版本管理
□ 圖形化編輯器可用
□ Provider 離線時降級為 Template
□ 用戶可查看自己使用的 Provider
Full P15：指揮中心（v2.0）
□ 三級修復正確
□ Level 1 不通知
□ Level 2 記錄 Incident
□ Level 3 立即通知
□ 手動控制可用
□ 頻率控制生效
□ 引擎健康面板顯示 5 引擎（v1.5）
□ 引擎健康與版本管理一致（v1.5）
□ 可從指揮中心跳轉到追蹤樹（v1.5）
5. 整體系統驗證
5.1 MVP 完成時（E2E 測試）
□ 新用戶完整流程（註冊 → 健康檔案 → 建立模型 → 新增資產）
□ 爬蟲完整流程（觸發 → 三源驗證 → 更新價格）
□ 保險完整流程（建立保單 → 計算 Coverage Ratio）
□ 預測完整流程（蒙地卡羅 → Email 預覽）
□ 自癒完整流程（模擬異常 → 自動修復 → 通知）
5.2 完整版完成時
□ 多租戶註冊與隔離
□ 管理員動態新增資產
□ 自動排程爬蟲
□ 引擎版本管理完整運作
□ LLM Provider 切換
□ 保險商品爬蟲與生命週期
□ 精算模型升級
□ 完整三級自癒
□ 金流訂閱
5.3 效能驗證（Full P14）
□ API 平均回應 < 200ms
□ Redis 快取生效
□ 無 N+1 查詢
□ 索引優化完成
驗證指令：

bash
# 效能測試
pytest tests/performance/ --benchmark
6. 問題發現時的處理
6.1 問題分類
類型	處理方式
功能錯誤	立即修正
測試失敗	先修測試，再修程式碼
效能問題	記錄，延後處理（除嚴重）
安全問題	立即修正（優先）
文件缺失	記錄，Phase 完成前補
6.2 問題記錄範本
建立 docs/issues/issue-{number}.md：

markdown
# Issue-001：{標題}

**日期**：2026-10-01
**Phase**：P3
**嚴重度**：高 / 中 / 低
**狀態**：Open / In Progress / Resolved

## 問題描述
{詳細說明}

## 重現步驟
1. ...
2. ...

## 已嘗試
1. ...
2. ...

## 解決方式
{待補}

## 相關檔案
- backend/app/...
- frontend/src/...
7. Phase 完成簽核表
每個 Phase 完成時，填寫下表：

markdown
# Phase {N} 完成簽核表

**Phase**：P{N}
**名稱**：{名稱}
**完成日期**：2026-XX-XX
**實際工時**：X 天

## 驗證結果

### 通用驗證
- [x] 程式碼品質（全部通過）
- [x] 功能驗證（全部通過）
- [x] 測試驗證（覆蓋率 85%）
- [x] 安全驗證（全部通過）
- [x] 文件驗證（已更新）
- [x] Git 驗證（已 push）

### 特定驗證
- [x] {Phase 特定項目 1}
- [x] {Phase 特定項目 2}
- [x] ...

## 交付物

| 類型 | 檔案 | 狀態 |
| :--- | :--- | :---: |
| 後端 | ... | ✅ |
| 前端 | ... | ✅ |
| 測試 | ... | ✅ |

## 遇到問題

| 問題 | 解決方式 |
| :--- | :--- |
| Docker 網路 | 改用 host network |
| ... | ... |

## 下一個 Phase

- **Phase**：P{N+1}
- **名稱**：{名稱}
- **預計開始**：2026-XX-XX

## 簽核

- [ ] 自己確認
- [ ] 測試通過
- [ ] 文件完成
8. 自動化驗證腳本
建立 scripts/verify.sh：

bash
#!/bin/bash

echo "🔍 開始驗證..."

# 1. Lint
echo "📝 Lint..."
ruff check backend/ || exit 1
cd frontend && npm run lint || exit 1
cd ..

# 2. 型別檢查
echo "🔎 型別檢查..."
mypy backend/app/ || exit 1

# 3. 單元測試
echo "🧪 單元測試..."
cd backend && pytest tests/unit/ --cov --cov-fail-under=80 || exit 1
cd ..

# 4. 整合測試
echo "🔗 整合測試..."
cd backend && pytest tests/integration/ || exit 1
cd ..

# 5. 前端測試
echo "🎨 前端測試..."
cd frontend && npm run test:unit || exit 1
cd ..

echo "✅ 全部通過！"
使用方式：

bash
chmod +x scripts/verify.sh
./scripts/verify.sh
9. 每週進度回顧
9.1 週五回顧清單
□ 本週完成的 Phase
□ 實際工時 vs 預估工時
□ 遇到的問題
□ 學到的新知
□ 下週規劃
9.2 週回顧範本
markdown
# Week {N} 回顧

**日期**：2026-XX-XX ~ 2026-XX-XX
**Phase**：P{N}

## 完成事項
- [x] {任務 1}
- [x] {任務 2}

## 未完成事項
- [ ] {任務 3}（延後至下週）

## 工時統計
- 預估：X 天
- 實際：Y 天
- 差異：+/-Z

## 遇到的問題
1. {問題 1} → {解決方式}
2. {問題 2} → {解決方式}

## 學到的新知
- {新知 1}
- {新知 2}

## 下週規劃
- 開始 Phase P{N+1}
- 預計完成：{任務}

## 心情
😊 順利 / 😐 普通 / 😟 卡關
10. 版本紀錄
版本	日期	變更
v1.0	2026-09-22	初版建立
文件結束
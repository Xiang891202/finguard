# FinGuard（財安）

> 個人 / 家庭財務安全儀表板
> Personal & Family Financial Safety Dashboard

## 📖 專案簡介

一套結合「理財模型 × 保險保障 × 健康風險 × AI 預測」的個人財務風險管理系統。

- **短期目標**：個人與家人使用（MVP）
- **長期目標**：多租戶 SaaS（完整版）
- **設計原則**：個人優先、商業就緒、免費優先、插件化、15 年長期運作

## 📚 文件導航

所有規劃書位於 [`docs/`](./docs/)，請從 [`docs/README.md`](./docs/README.md) 開始閱讀。

| 批次 | 文件 | 說明 |
| :--- | :--- | :--- |
| 第一批 | [框架層](./docs/01-framework/) | 共用框架、操作手冊、Phase 模板 |
| 第二批 | [參考文件](./docs/02-reference/) | 資料庫 Schema、API 規格 |
| 第三批 | [MVP 規劃](./docs/03-mvp/) | MVP 功能規劃與各 Phase（12 個） |
| 第四批 | [完整版規劃](./docs/04-full/) | 完整版功能規劃與各 Phase（20 個） |
| 第五批 | [實作指南](./docs/05-implementation-guide/) | 實作順序、每日流程、驗證清單 |

## 🏗️ 技術棧

| 組件 | 選擇 |
| :--- | :--- |
| 主框架 | Node.js（完整版 BFF） |
| 核心業務 | Python FastAPI |
| 金流 | Java Spring Boot |
| 前端 | Vue 3 + Vite + Tailwind CSS |
| 資料庫 | PostgreSQL（MVP 與完整版一致） |
| 快取 / Queue | Redis / Upstash |
| AI 預測 | Python + NumPy（蒙地卡羅） |
| LLM Provider | Template / Groq / Gemini / OpenAI / Ollama（5 層抽象） |
| 安全掃描 | Strix（本地） |
| 部署 | Render（MVP）→ AWS / GCP（完整版） |

## 📊 專案規模

| 項目 | 數量 |
| :--- | :---: |
| 開發階段（Phase） | 32（MVP 12 + 完整版 20） |
| 資料表 | 36 |
| API 端點 | 106 |
| 預估工時 | 165 天 |
| 架構層級 | 7 層 |
| 程式語言 | 4（Vue / Node / Python / Java） |
| 引擎 | 5（爬蟲 / 正規化 / 驗證 / 比對 / 蒙地卡羅 / LLM） |

---

## 🛠️ 開發指令

### 📋 環境需求

| 工具 | 版本 | 用途 |
| :--- | :---: | :--- |
| Docker Desktop | 最新版 | 容器化環境 |
| Python | 3.11+ | 後端 |
| Node.js | 20+ | 前端 |
| Git | 最新版 | 版本控制 |

---

### 🐳 Docker 環境（第一步）

```powershell
# 啟動 PostgreSQL + Redis
docker compose up -d

# 查看容器狀態（應顯示 healthy）
docker compose ps

# 查看日誌
docker compose logs -f

# 停止容器
docker compose down

# 停止並清除資料
docker compose down -v
驗證容器運作：

powershell
# 測試 PostgreSQL
docker exec -it finguard-postgres psql -U finguard -d finguard -c "SELECT version();"

# 測試 Redis
docker exec -it finguard-redis redis-cli ping
# 預期回應：PONG

# 查詢 36 張表
docker exec -it finguard-postgres psql -U finguard -d finguard -P pager=off -c "\dt"

# 查詢表數量（應為 37 = 36 業務 + 1 alembic_version）
docker exec -it finguard-postgres psql -U finguard -d finguard -P pager=off -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';"
🔑 環境變數設定
產生密鑰（JWT + Encryption）
powershell
# 產生 JWT_SECRET（64 字元隨機字串）
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})

# 產生 ENCRYPTION_KEY（再跑一次，產生第二組）
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
建立後端 .env
powershell
cd backend
Copy-Item .env.example .env
notepad .env
填入剛才產生的兩組密鑰：

bash
JWT_SECRET=<貼上第一組>
ENCRYPTION_KEY=<貼上第二組>
建立前端 .env
powershell
cd frontend
Copy-Item .env.example .env
前端 .env 通常不需修改，預設值即可：

bash
VITE_ENV=development
VITE_API_URL=http://localhost:8000
VITE_ENABLE_DEVTOOLS=true
🐍 後端啟動（FastAPI）
首次設定
powershell
cd backend

# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境（每次開新視窗都要執行）
.\venv\Scripts\Activate.ps1

# 若執行政策錯誤，先執行一次
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# 升級 pip
python -m pip install --upgrade pip

# 安裝依賴
pip install -r requirements.txt
資料庫遷移
powershell
# 產生 migration（模型變更時執行）
alembic revision --autogenerate -m "描述變更內容"

# 執行 migration
alembic upgrade head

# 查看當前版本
alembic current

# 回退一個版本
alembic downgrade -1
啟動後端
powershell
# 開發模式（自動重載）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 預期輸出：
# INFO:     Uvicorn running on http://0.0.0.0:8000
# 🚀 FinGuard v1.5.0 啟動
# 環境：development
這個視窗保持開著，開新視窗執行其他指令。

🎨 前端啟動（Vue 3 + Vite）
首次設定
powershell
cd frontend

# 安裝依賴
npm install

# 若 npm install 很慢，使用淘寶鏡像
npm install --registry=https://registry.npmmirror.com
啟動前端
powershell
npm run dev

# 預期輸出：
# VITE v6.x.x  ready in 300 ms
# ➜  Local:   http://localhost:5173/
這個視窗保持開著。

其他前端指令
powershell
# 建置正式版
npm run build

# 預覽正式版
npm run preview

# Lint 檢查
npm run lint

# 單元測試
npm run test:unit
🌐 健康檢查（curl）
⚠️ PowerShell 提示：使用 curl.exe（真正的 curl），不要用 curl（PowerShell 別名）

powershell
# 後端健康檢查
curl.exe http://localhost:8000/health
# 預期：{"status":"healthy","version":"1.5.0","database":"connected","redis":"connected"}

# 後端 API 文件（瀏覽器打開）
# http://localhost:8000/docs

# 前端健康檢查
curl.exe http://localhost:5173
# 預期：HTML 內容

# 前端瀏覽器打開
# http://localhost:5173
🔄 完整啟動流程（一鍵複製）
開 3 個 PowerShell 視窗，依序執行：

視窗 1：Docker
powershell
cd C:\Users\Xiang\Desktop\finguard
docker compose up -d
docker compose ps
視窗 2：後端
powershell
cd C:\Users\Xiang\Desktop\finguard\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
視窗 3：前端
powershell
cd C:\Users\Xiang\Desktop\finguard\frontend
npm run dev
視窗 4：測試
powershell
curl.exe http://localhost:8000/health
curl.exe http://localhost:5173
🧪 測試指令
後端測試
powershell
cd backend
.\venv\Scripts\Activate.ps1

# 執行所有測試
pytest

# 執行單元測試
pytest tests/unit/

# 執行整合測試
pytest tests/integration/

# 顯示覆蓋率
pytest --cov=app --cov-report=term-missing

# 覆蓋率門檻（≥ 80%）
pytest --cov=app --cov-fail-under=80
前端測試
powershell
cd frontend

# 執行測試
npm run test:unit

# 監聽模式
npm run test:unit -- --watch
Lint 檢查
powershell
# 後端
cd backend
ruff check .
mypy app/

# 前端
cd frontend
npm run lint
📦 Git 指令
powershell
# 查看狀態
git status

# 加入所有變更
git add .

# 提交
git commit -m "feat(p0): 描述你的變更"

# 推送
git push

# 查看歷史
git log --oneline -10

# 查看遠端
git remote -v
Commit 訊息慣例：

前綴	用途
feat:	新功能
fix:	錯誤修正
docs:	文件更新
refactor:	重構
test:	測試
chore:	雜項（建置、設定）
🚨 常見問題排除
Docker 無法連線
powershell
# 錯誤：failed to connect to the docker API
# 解法：開啟 Docker Desktop，等待「Engine running」
Port 已被占用
powershell
# 查看占用 port 的程式
netstat -ano | findstr :5432
netstat -ano | findstr :8000
netstat -ano | findstr :5173
venv 無法啟動
powershell
# 錯誤：無法辨識 'Activate.ps1'
# 解法：
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
Alembic 錯誤
powershell
# 檢查 models 是否正確載入
python -c "from app import models; print(len(models.__all__))"
# 預期：36
前端 API 連線失敗
powershell
# 檢查 .env
Get-Content frontend\.env

# 確認後端有跑
curl.exe http://localhost:8000/health

# 修改 .env 後需重啟 npm run dev
📌 文件版本
目前版本：v1.5

最後更新：2026-09-23

版本紀錄：見 docs/README.md

✨ v1.5 核心亮點
引擎版本管理系統：5 大引擎獨立版本、可還原、可重算

LLM Provider 抽象層：免費為主、付費解鎖

Redis Pub/Sub 快取失效：設定變更即時生效（< 1 秒）

圖形化引擎編輯器：本地編輯 → 測試 → 提交 → 部署

健康檔案精算：納入年齡、性別、家族病史、基因

📈 開發進度
Phase	名稱	狀態
P0	基礎建設	✅ 完成
P1	用戶認證 + 健康檔案	⏳ 待開始
P2	財務模型 + 金庫	⏳
P3	持有部位（Equity）	⏳
P4	負債	⏳
P5	外匯（Forex）	⏳
P6	貨幣基金	⏳
P7	爬蟲調度 + 三源驗證	⏳
P8	保險保單 CRUD	⏳
P9	蒙地卡羅 + 風險計算	⏳
P10	Email 報告 + 自癒	⏳
P11	醫療費用 + 覆蓋率精算	⏳
🚫 重要限制
❌ 不提供投資建議

❌ 不提供操作做法

❌ 不推薦具體保險商品

✅ 僅提供「風險機率」與「水位狀態」

✅ 只呈現數據，不下結論

📄 授權
（待補）
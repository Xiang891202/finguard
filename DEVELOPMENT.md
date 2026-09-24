\# FinGuard 開發指南



> 本文件包含所有開發環境設定、啟動、測試、部署指令。

> 專案介紹請見 \[README.md](./README.md)。



\*\*目前版本\*\*：v1.5

\*\*最後更新\*\*：2026-09-24

\*\*已完成 Phase\*\*：P0、P1



\---



\## 📋 環境需求



| 工具 | 版本 | 用途 |

| :--- | :---: | :--- |

| Docker Desktop | 最新版 | PostgreSQL + Redis |

| Python | 3.11+ | 後端 |

| Node.js | 20+ | 前端 |

| Git | 最新版 | 版本控制 |



\---



\## 🐳 Docker 環境（第一步）



```powershell

cd C:\\Users\\Xiang\\Desktop\\finguard



\# 啟動 PostgreSQL + Redis

docker compose up -d



\# 查看容器狀態（應顯示 healthy）

docker compose ps



\# 查看日誌

docker compose logs -f



\# 停止容器（保留資料）

docker compose down



\# 停止並清除資料

docker compose down -v

```



\### 驗證容器



```powershell

\# 測試 PostgreSQL

docker exec -it finguard-postgres psql -U finguard -d finguard -c "SELECT version();"



\# 測試 Redis

docker exec -it finguard-redis redis-cli ping

\# 預期：PONG



\# 查詢 36 張表

docker exec -it finguard-postgres psql -U finguard -d finguard -P pager=off -c "\\dt"



\# 表數量（應為 37 = 36 業務 + 1 alembic\_version）

docker exec -it finguard-postgres psql -U finguard -d finguard -P pager=off `

&#x20; -c "SELECT COUNT(\*) FROM information\_schema.tables WHERE table\_schema='public';"

```



\---



\## 🔑 環境變數設定



\### 產生密鑰



```powershell

\# 產生 JWT\_SECRET

python -c "import secrets; print(secrets.token\_hex(32))"



\# 產生 OTP\_PEPPER（再跑一次，得到第二組）

python -c "import secrets; print(secrets.token\_hex(32))"



\# 產生 Fernet key（ENCRYPTION\_KEY）

python -c "from cryptography.fernet import Fernet; print(Fernet.generate\_key().decode())"

```



\### 建立後端 `.env`



```powershell

cd backend

Copy-Item .env.example .env

notepad .env

```



填入：



```dotenv

\# 環境

ENV=development

DEBUG=True



\# 資料庫 / Redis

DATABASE\_URL=postgresql://finguard:dev\_password\_change\_me@localhost:5432/finguard

REDIS\_URL=redis://localhost:6379



\# JWT

JWT\_SECRET=<剛才產生的第一組 hex>

JWT\_ALGORITHM=HS256

JWT\_ISSUER=finguard

JWT\_ACCESS\_EXPIRY=900

JWT\_REFRESH\_EXPIRY=604800



\# OTP

OTP\_EXPIRY\_SECONDS=300

OTP\_MAX\_ATTEMPTS=3

OTP\_RESEND\_INTERVAL=60

OTP\_DAILY\_LIMIT=10

OTP\_PEPPER=<剛才產生的第二組 hex>



\# IP 限流

IP\_RATE\_PER\_MINUTE=5

IP\_RATE\_PER\_DAY=50



\# 加密（Fernet）

ENCRYPTION\_KEY=<剛才產生的 Fernet key>



\# SMTP（本機可留空，dev\_code 會顯示於前端）

SMTP\_HOST=smtp.gmail.com

SMTP\_PORT=587

SMTP\_USER=your-email@gmail.com

SMTP\_PASSWORD=your-app-password

SMTP\_FROM=FinGuard <your-email@gmail.com>

```



\### 建立前端 `.env`



```powershell

cd frontend

Copy-Item .env.example .env

```



預設即可：



```dotenv

VITE\_API\_URL=http://localhost:8000

VITE\_ENABLE\_DEVTOOLS=true

```



\---



\## 🐍 後端啟動（FastAPI）



\### 首次設定



```powershell

cd backend



\# 建立虛擬環境

python -m venv venv



\# 啟動 venv（每次開新視窗都要執行）

.\\venv\\Scripts\\Activate.ps1



\# 若執行政策錯誤：

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned



\# 升級 pip

python -m pip install --upgrade pip



\# 安裝依賴

pip install -r requirements.txt

```



\### 資料庫遷移



```powershell

\# 產生 migration（模型變更時）

alembic revision --autogenerate -m "描述變更內容"



\# 執行 migration

alembic upgrade head



\# 查看當前版本

alembic current



\# 查看 head

alembic heads



\# 回退一個版本

alembic downgrade -1

```



\### 建立管理員帳號



```powershell

\# 首次建立

python scripts/create\_admin.py --email admin@finguard.local --password "你的強密碼"



\# 更新密碼（同指令，會覆蓋）

python scripts/create\_admin.py --email admin@finguard.local --password "新密碼"

```



\### 啟動後端



```powershell

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```



預期輸出：



```

INFO:     Uvicorn running on http://0.0.0.0:8000

\[START] FinGuard v1.5.0 啟動

環境：development

```



\---



\## 🎨 前端啟動（Vue 3 + Vite）



\### 首次設定



```powershell

cd frontend



\# 安裝依賴

npm install

```



\### 啟動前端



```powershell

npm run dev

```



預期輸出：



```

VITE v6.x.x  ready in 300 ms

➜  Local:   http://localhost:5173/

```



\### 其他前端指令



```powershell

npm run build          # 建置正式版

npm run preview        # 預覽正式版

npm run lint           # ESLint 檢查

npm run test:unit      # Vitest 監聽模式

npm run test:unit -- --run   # Vitest 單次執行

npm run test:e2e       # Playwright E2E

npm run test:e2e:ui    # Playwright 互動模式

```



\---



\## 🌐 健康檢查



⚠️ PowerShell 中請使用 `curl.exe`（真正的 curl），不要用 `curl`（PowerShell 別名）。



```powershell

\# 後端健康檢查

curl.exe http://localhost:8000/health

\# 預期：{"status":"healthy","version":"1.5.0","database":"connected","redis":"connected"}



\# 後端 API 文件（瀏覽器）

\# http://localhost:8000/docs



\# 前端（瀏覽器）

\# http://localhost:5173

```



\---



\## 🔄 完整啟動流程（一鍵複製）



開 3 個 PowerShell 視窗：



\### 視窗 1：Docker



```powershell

cd C:\\Users\\Xiang\\Desktop\\finguard

docker compose up -d

docker compose ps

```



\### 視窗 2：後端



```powershell

cd C:\\Users\\Xiang\\Desktop\\finguard\\backend

.\\venv\\Scripts\\Activate.ps1

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```



\### 視窗 3：前端



```powershell

cd C:\\Users\\Xiang\\Desktop\\finguard\\frontend

npm run dev

```



\---



\## 🧪 測試指令



\### 後端（pytest）



```powershell

cd backend

.\\venv\\Scripts\\Activate.ps1



\# 全部測試

python -m pytest



\# 單元測試

python -m pytest tests\\unit\\



\# 整合測試

python -m pytest tests\\integration\\



\# 顯示覆蓋率

python -m pytest --cov=app --cov-report=term-missing



\# 覆蓋率門檻（≥ 80%）

python -m pytest --cov=app --cov-fail-under=80



\# 某個檔案

python -m pytest tests\\test\_auth\_otp.py -v

```



\### 前端（Vitest）



```powershell

cd frontend



\# 單次執行

npm run test:unit -- --run



\# 監聽模式

npm run test:unit

```



\### E2E（Playwright）



```powershell

cd frontend



\# 全部 E2E（會自動啟動前後端）

npm run test:e2e



\# 互動 UI 模式

npm run test:e2e:ui



\# 跑單一檔案

npx playwright test e2e/auth.spec.js

```



⚠️ \*\*前置條件\*\*：跑 E2E 前請確認本機 `uvicorn` 已關閉（讓 Playwright 自己啟動並套用 TESTING 環境變數）。



\### Lint



```powershell

\# 後端

cd backend

ruff check .

mypy app/



\# 前端

cd frontend

npm run lint

```



\---



\## 📦 Git 指令



```powershell

git status                # 查看狀態

git add -A                # 加入所有變更

git commit -m "訊息"      # 提交

git push                  # 推送

git log --oneline -10     # 查看歷史

git remote -v             # 查看遠端

```



\### Commit 訊息慣例



| 前綴 | 用途 |

| :--- | :--- |

| `feat:` | 新功能 |

| `fix:` | 錯誤修正 |

| `docs:` | 文件更新 |

| `refactor:` | 重構 |

| `test:` | 測試 |

| `chore:` | 雜項（建置、設定） |



\---



\## 🚨 常見問題排除



\### Docker 無法連線



```

錯誤：failed to connect to the docker API

解法：開啟 Docker Desktop，等待「Engine running」

```



\### Port 已被占用



```powershell

\# 查看占用 port 的程式

netstat -ano | findstr :5432

netstat -ano | findstr :8000

netstat -ano | findstr :5173



\# 找 PID 並關閉

Get-NetTCPConnection -LocalPort 8000 -State Listen | Select-Object OwningProcess

Stop-Process -Id <PID> -Force

```



\### venv 無法啟動



```

錯誤：無法辨識 'Activate.ps1'

解法：Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

```



\### Alembic 錯誤



```powershell

\# 檢查 models 是否正確載入

python -c "from app import models; print(len(models.\_\_all\_\_))"

\# 預期：36

```



\### 前端 API 連線失敗



```powershell

\# 檢查 .env

Get-Content frontend\\.env



\# 確認後端有跑

curl.exe http://localhost:8000/health



\# 修改 .env 後需重啟 npm run dev

```



\### PowerShell 中文亂碼



在 `$PROFILE` 加入：



```powershell

chcp 65001 | Out-Null

$OutputEncoding = \[System.Text.Encoding]::UTF8

\[Console]::OutputEncoding = \[System.Text.Encoding]::UTF8

```



\### Playwright 首次安裝



```powershell

cd frontend

npm install -D @playwright/test

npx playwright install chromium

```



\### E2E 失敗：`IP rate limit` 或 `Dev code 未顯示`



確認 `uvicorn` 已關閉（讓 Playwright 用自己啟動的後端套用 `TESTING=true`）。



```powershell

Test-NetConnection localhost -Port 8000

\# 預期：TcpTestSucceeded : False

```



\---



\## 📁 專案結構速查



```

finguard/

├── backend/

│   ├── app/

│   │   ├── api/v1/          # 路由（auth / admin\_auth / health\_profile / genetic）

│   │   ├── core/            # config / security / encryption / exceptions

│   │   ├── db/              # session（sync + async）

│   │   ├── models/          # 36 個 ORM 模型

│   │   ├── schemas/         # Pydantic DTO

│   │   ├── services/        # 商業邏輯

│   │   └── main.py

│   ├── alembic/versions/    # 資料庫遷移

│   ├── scripts/

│   │   ├── create\_admin.py  # 建立管理員 CLI

│   │   └── manual/          # 手動 SQL 工具（開發用）

│   └── tests/

│       ├── unit/

│       └── integration/

├── frontend/

│   ├── src/

│   │   ├── api/             # axios 模組

│   │   ├── components/

│   │   ├── composables/

│   │   ├── router/

│   │   ├── stores/          # Pinia

│   │   └── views/

│   ├── e2e/                 # Playwright

│   └── tests/               # Vitest

├── docs/                    # 規劃書

└── docker-compose.yml

```



\---



\## 🔗 相關文件



\- \[README.md](./README.md) — 專案介紹與進度

\- \[docs/](./docs/) — 完整規劃書

\- \[docs/01-framework/01-shared-framework.md](./docs/01-framework/01-shared-framework.md) — 共用框架

\- \[docs/02-reference/02-api-spec.md](./docs/02-reference/02-api-spec.md) — API 規格


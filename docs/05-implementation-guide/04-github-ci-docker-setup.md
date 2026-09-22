# GitHub + CI + Docker 設置指南

**版本**：v1.0
**最後更新**：2026-09-22
**適用範圍**：專案初始化階段

---

## 1. 設置順序
步驟 1：GitHub 連線
↓
步驟 2：CI 設置（GitHub Actions）
↓
步驟 3：Docker 設置
↓
步驟 4：.env.example 建立
↓
步驟 5：驗證

text

---

## 2. GitHub 連線

### 2.1 初始化

```powershell
cd C:\Users\Xiang\Desktop\finguard
git init
git add .
git commit -m "init: FinGuard 專案初始化"
git branch -M main
2.2 連接遠端
powershell
git remote add origin https://github.com/你的帳號/finguard.git
git push -u origin main
2.3 日常操作
powershell
# 查看狀態
git status

# 加入變更
git add .

# 提交
git commit -m "feat: 新增 XXX"

# 推送
git push
3. CI 設置
3.1 CI 觸發時機
Push 到 main 或 develop

Pull Request 到 main 或 develop

3.2 CI Jobs
Job	說明
docs-check	Markdown 格式檢查
backend-check	Python lint + test（P0 後啟用）
frontend-check	Node lint + test（P0 後啟用）
docker-check	Docker 建置測試
security-check	敏感檔案、漏洞掃描
ci-summary	總結結果
3.3 查看 CI 結果
前往 GitHub repo

點擊「Actions」標籤

查看最近執行的 workflow

4. Docker 設置
4.1 開發用指令
powershell
# 只啟動 DB + Redis
docker compose up -d

# 完整啟動
docker compose --profile full up -d

# 查看狀態
docker compose ps

# 查看日誌
docker compose logs -f backend

# 停止
docker compose down

# 停止並清除資料
docker compose down -v
4.2 連接資訊
服務	位址
PostgreSQL	localhost:5432
Redis	localhost:6379
Backend	localhost:8000
Frontend	localhost:5173
5. 環境變數
5.1 .env 檔案位置
檔案	進 Git？	說明
backend/.env	❌	真實設定
backend/.env.example	✅	範本
frontend/.env	❌	真實設定
frontend/.env.example	✅	範本
5.2 換電腦時
powershell
# 1. Clone 專案
git clone https://github.com/你的帳號/finguard.git

# 2. 複製 .env.example
Copy-Item backend\.env.example backend\.env
Copy-Item frontend\.env.example frontend\.env

# 3. 編輯 .env 填入真實值
notepad backend\.env
6. 驗證清單
□ git remote -v 顯示正確的 GitHub URL
□ git push 成功
□ GitHub Actions 顯示綠燈
□ docker compose up -d 成功
□ docker compose ps 顯示 postgres + redis 都是 healthy
□ .env 檔案不在 Git 中（git ls-files | grep .env 無結果）
7. 常見問題
Q1：git push 出現認證錯誤
A：使用 Personal Access Token（PAT）

GitHub → Settings → Developer settings → Personal access tokens

生成 token（勾選 repo 權限）

推送時密碼欄位填 token

Q2：docker compose up 失敗
A：檢查 Docker Desktop 是否啟動

powershell
docker --version
docker compose version
Q3：port 5432 已被占用
A：本機已有 PostgreSQL 在跑

powershell
# Windows 檢查
netstat -ano | findstr :5432
# 停止本機 PostgreSQL 服務，或改用其他 port
Q4：CI 執行失敗
A：點擊 GitHub Actions 中的失敗 job，查看錯誤訊息。

8. 版本紀錄
版本	日期	變更
v1.0	2026-09-22	初版建立
text

---

# 🚀 執行順序總結

## 步驟 1：建立所有檔案

```powershell
cd C:\Users\Xiang\Desktop\finguard

# CI
New-Item -ItemType Directory -Force -Path .github\workflows
New-Item -ItemType File -Force -Path .github\workflows\ci.yml

# Docker
New-Item -ItemType File -Force -Path docker-compose.yml

# .env.example
New-Item -ItemType Directory -Force -Path backend
New-Item -ItemType Directory -Force -Path frontend
New-Item -ItemType File -Force -Path backend\.env.example
New-Item -ItemType File -Force -Path frontend\.env.example

# Dockerfile（預留）
New-Item -ItemType File -Force -Path backend\Dockerfile
New-Item -ItemType File -Force -Path frontend\Dockerfile

# 文件
New-Item -ItemType File -Force -Path docs\05-implementation-guide\04-github-ci-docker-setup.md

Write-Host "✅ 所有檔案建立完成！" -ForegroundColor Green
步驟 2：貼入內容
依序將上面的內容貼入對應檔案。

步驟 3：GitHub 設定
powershell
# 初始化
git init
git add .
git commit -m "init: FinGuard 專案初始化"
git branch -M main

# 到 GitHub 建立 repo 後
git remote add origin https://github.com/你的帳號/finguard.git
git push -u origin main
步驟 4：測試 Docker
powershell
docker compose up -d
docker compose ps
應該看到 finguard-postgres 和 finguard-redis 都是 healthy。

步驟 5：驗證 CI
前往 GitHub repo

點擊「Actions」

應看到 CI workflow 執行中

等待完成，應顯示綠燈 ✅
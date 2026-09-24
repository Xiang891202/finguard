\# 手動 SQL 腳本



這些是\*\*開發階段的臨時工具\*\*，非正式流程的一部分。



\## 檔案說明



| 檔案 | 用途 | 使用時機 |

|---|---|---|

| `cleanup\_user.sql` | 刪除指定用戶的所有資料（CASCADE 清 health / genetic / tokens） | 測試新用戶流程前清乾淨 |

| `cleanup\_health.sql` | 只刪健康檔案與基因資料，保留 user 帳號 | 想重測健康檔案填寫流程 |

| `seed\_markers.sql` | 手動 seed 8 個基因點位 | ⚠️ 已被 Alembic migration 取代 |



\## 使用方式



```powershell

docker cp scripts\\manual\\cleanup\_user.sql finguard-postgres:/tmp/cleanup.sql

docker exec finguard-postgres psql -U finguard -d finguard -f /tmp/cleanup.sql


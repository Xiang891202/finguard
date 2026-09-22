📄 文件 5：API 完整規格
版本：v1.5
適用範圍：MVP 與完整版共用

0. 通用規範
0.1 Base URL
text
MVP：https://finguard-mvp.onrender.com/api/v1
完整版：https://api.finguard.com/api/v1
0.2 認證
用戶端：Authorization: Bearer {access_token}
管理員端：Authorization: Bearer {admin_access_token}

0.3 通用回應格式
成功：

json
{
  "success": true,
  "data": { },
  "meta": { "page": 1, "total": 100 }
}
失敗：

json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "錯誤訊息",
    "details": { }
  }
}
0.4 通用錯誤碼
HTTP	Code	說明
400	BAD_REQUEST	請求格式錯誤
401	UNAUTHORIZED	未認證
403	FORBIDDEN	無權限
404	NOT_FOUND	資源不存在
429	RATE_LIMITED	請求過於頻繁
500	INTERNAL_ERROR	伺服器錯誤
0.5 分頁參數
參數	預設	範圍
page	1	≥ 1
page_size	20	1-100
sort	created_at	欄位名
order	desc	asc / desc
1. 認證 API（/auth/*）
1.1 POST /auth/otp/request
請求：

json
{
  "email": "user@example.com"
}
回應：

json
{
  "success": true,
  "data": {
    "message": "驗證碼已寄出",
    "expires_in": 300
  }
}
錯誤：

Code	說明
AUTH_OTP_RATE_LIMITED	60 秒內重複請求
AUTH_OTP_DAILY_LIMIT	每日上限
USER_NOT_FOUND	用戶不存在
1.2 POST /auth/otp/verify
請求：

json
{
  "email": "user@example.com",
  "otp": "123456"
}
回應：

json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "Bearer",
    "expires_in": 900,
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "display_name": "使用者",
      "is_new_user": true,
      "health_profile_completed": false
    }
  }
}
1.3 POST /auth/refresh
請求：

json
{
  "refresh_token": "eyJ..."
}
回應：

json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "expires_in": 900
  }
}
1.4 POST /auth/logout
請求：

json
{
  "refresh_token": "eyJ..."
}
回應：

json
{
  "success": true,
  "data": { "message": "已登出" }
}
2. 管理員認證 API（/admin/auth/*）
2.1 POST /admin/auth/login
請求：

json
{
  "email": "admin@example.com",
  "password": "password123"
}
回應：

json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "expires_in": 900,
    "admin": {
      "id": "uuid",
      "email": "admin@example.com",
      "display_name": "管理員",
      "role": "admin"
    }
  }
}
2.2 POST /admin/auth/logout
（與 /auth/logout 相同）

3. 健康檔案 API（/app/health/*）
3.1 GET /app/health/profile
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "birth_date": "1985-06-15",
    "gender": "male",
    "family_history": {
      "cardiovascular": true,
      "diabetes": false,
      "cancer": true
    },
    "has_genetic_test": true,
    "consent_genetic": true,
    "consent_genetic_at": "2026-09-21T10:00:00Z",
    "completion_rate": 100.00
  }
}
3.2 POST /app/health/profile
請求：

json
{
  "birth_date": "1985-06-15",
  "gender": "male",
  "family_history": {
    "cardiovascular": true,
    "diabetes": false
  }
}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "completion_rate": 90.00,
    "message": "健康檔案已建立"
  }
}
3.3 PUT /app/health/profile
（同 POST）

3.4 POST /app/health/consent
請求：

json
{
  "consent": true
}
回應：

json
{
  "success": true,
  "data": {
    "consent_genetic": true,
    "consent_genetic_at": "2026-09-21T10:00:00Z"
  }
}
3.5 GET /app/health/genetic-markers
回應：

json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "marker_code": "BRCA1",
      "marker_name": "BRCA1 基因",
      "related_diseases": ["乳癌", "卵巢癌"],
      "related_body_parts": ["reproductive"]
    }
  ]
}
3.6 GET /app/health/genetic-tests
回應：

json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "marker_id": "uuid",
      "marker_code": "BRCA1",
      "result": "positive",
      "risk_level_computed": 3.0
    }
  ]
}
3.7 POST /app/health/genetic-tests
請求：

json
{
  "marker_id": "uuid",
  "result": "positive"
}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "marker_code": "BRCA1",
    "result": "positive",
    "risk_level_computed": 3.0
  }
}
3.8 DELETE /app/health/genetic-tests/{id}
回應：

json
{
  "success": true,
  "data": { "message": "已刪除" }
}
3.9 GET /app/health/completion
回應：

json
{
  "success": true,
  "data": {
    "completion_rate": 80.00,
    "missing_fields": ["genetic_test"],
    "precision_level": "medium"
  }
}
4. 財務模型 API（/app/models/*）
4.1 GET /app/models
回應：

json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "我的家庭財務",
      "base_currency": "TWD",
      "emergency_fund_months": 6,
      "is_default": true,
      "created_at": "2026-09-21T10:00:00Z"
    }
  ],
  "meta": { "page": 1, "total": 1 }
}
4.2 POST /app/models
請求：

json
{
  "name": "我的家庭財務",
  "base_currency": "TWD",
  "emergency_fund_months": 6
}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "我的家庭財務",
    "is_default": false
  }
}
錯誤：

Code	說明
MODEL_LIMIT_EXCEEDED	模型數量超過上限
4.3 PUT /app/models/{id}
4.4 DELETE /app/models/{id}
5. 金庫 API（/app/vaults/*）
5.1 GET /app/vaults
Query：?model_id=uuid

5.2 POST /app/vaults
請求：

json
{
  "model_id": "uuid",
  "name": "緊急預備金",
  "vault_type": "reserve",
  "currency": "TWD",
  "amount": 300000
}
5.3 PUT /app/vaults/{id}
5.4 DELETE /app/vaults/{id}
6. 持有部位 API（/app/holdings/*）
6.1 GET /app/holdings
Query：?model_id=uuid&asset_class=equity

回應：

json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "asset_definition": {
        "id": "uuid",
        "symbol": "0050.TW",
        "display_name": "元大台灣50",
        "asset_class": "equity"
      },
      "quantity": 100,
      "average_cost": 150.50,
      "current_price": 155.20,
      "current_value": 15520.00,
      "unrealized_gain": 470.00
    }
  ]
}
6.2 POST /app/holdings
請求：

json
{
  "model_id": "uuid",
  "asset_definition_id": "uuid",
  "quantity": 100,
  "average_cost": 150.50
}
6.3 PUT /app/holdings/{id}
6.4 DELETE /app/holdings/{id}
7. 負債 API（/app/liabilities/*）
7.1 GET /app/liabilities
7.2 POST /app/liabilities
請求：

json
{
  "model_id": "uuid",
  "name": "房貸",
  "liability_type": "mortgage",
  "total_amount": 10000000,
  "remaining_amount": 8000000,
  "interest_rate": 0.0185,
  "monthly_payment": 45000
}
7.3 PUT /app/liabilities/{id}
7.4 DELETE /app/liabilities/{id}
8. 爬蟲 API（/app/crawler/*）
8.1 POST /app/crawler/trigger
請求：

json
{
  "asset_class": "equity",
  "force": false
}
回應：

json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "status": "running",
    "assets_count": 5
  }
}
8.2 GET /app/crawler/status/{task_id}
回應：

json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "status": "completed",
    "assets_success": 5,
    "assets_failed": 0,
    "data_conflicts": 0,
    "completed_at": "2026-09-21T10:05:00Z"
  }
}
9. 預測 API（/app/forecast/*）
9.1 POST /app/forecast/run
請求：

json
{
  "model_id": "uuid",
  "horizon_months": 6,
  "simulation_count": 10000
}
回應：

json
{
  "success": true,
  "data": {
    "run_id": "uuid",
    "model_version": "v1.0.0",
    "horizon_months": 6,
    "results": {
      "bankruptcy_probability": 0.072,
      "reserve_breach_probability": 0.145,
      "volatility_level": "elevated"
    },
    "generated_at": "2026-09-21T10:00:00Z"
  }
}
9.2 GET /app/forecast/latest
Query：?model_id=uuid

10. 保險 API（/app/insurance/*）
10.1 GET /app/insurance/policies
Query：?category=life

10.2 POST /app/insurance/policies
請求：

json
{
  "model_id": "uuid",
  "category": "life",
  "subcategory": "disease",
  "policy_name": "終身醫療險",
  "insurer_name": "XX 人壽",
  "coverage_amount": 1000000,
  "annual_premium": 30000,
  "covered_body_parts": ["heart", "brain"]
}
10.3 PUT /app/insurance/policies/{id}
10.4 DELETE /app/insurance/policies/{id}
10.5 GET /app/insurance/gap
Query：?model_id=uuid

回應：

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
10.6 GET /app/insurance/body-map
回應：

json
{
  "success": true,
  "data": {
    "parts": [
      {
        "part_code": "brain",
        "part_name": "大腦 / 神經",
        "category": "internal",
        "ui_config": { "svg_id": "part-brain", "x": 100, "y": 50 }
      }
    ]
  }
}
11. Email 預覽 API（/app/email-preview/*）
11.1 GET /app/email-preview
回應：

json
{
  "success": true,
  "data": {
    "date": "2026-09-21",
    "sections": {
      "financial": { },
      "market_sentiment": {
        "score": 62,
        "state": "elevated",
        "explanation": "目前市場波動程度相對提高...",
        "provider": "template"
      },
      "forecast": { },
      "insurance_gap": { },
      "comic": { },
      "disclaimer": "..."
    }
  }
}
12. 管理員系統 API（/admin/*）
12.1 GET /admin/dashboard
回應：

json
{
  "success": true,
  "data": {
    "health": {
      "database": "green",
      "redis": "green",
      "external_api": "yellow"
    },
    "queues": {
      "crawl": 0,
      "forecast": 0,
      "email": 2
    },
    "incidents_today": 1
  }
}
12.2 GET /admin/users
Query：?status=active&page=1

12.3 GET /admin/asset-classes
（MVP 唯讀）

12.4 GET /admin/asset-definitions
（MVP 唯讀）

12.5 GET /admin/genetic-markers
12.6 POST /admin/genetic-markers
12.7 GET /admin/medical-costs
12.8 POST /admin/medical-costs
12.9 GET /admin/incidents
Query：?status=open&severity=critical

12.10 GET /admin/incidents/{id}
12.11 POST /admin/incidents/{id}/resolve
12.12 GET /admin/billing
（Full P18）

12.13 POST /admin/billing/toggle
（Full P18）

13. 引擎管理 API（/admin/engines/*）— v1.5 新增
13.1 GET /admin/engines
說明：取得 5 大引擎總覽

回應：

json
{
  "success": true,
  "data": [
    {
      "engine_type": "crawler",
      "name": "爬蟲引擎",
      "active_version": "v1.2",
      "version_count": 3,
      "last_execution": "2026-09-22T06:00:00Z",
      "status": "healthy"
    },
    {
      "engine_type": "llm",
      "name": "LLM 引擎",
      "active_version": "v1.3",
      "version_count": 3,
      "last_execution": "2026-09-22T08:00:00Z",
      "status": "healthy"
    }
  ]
}
13.2 GET /admin/engines/{type}/versions
Query：?status=active&page=1

回應：

json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "engine_type": "llm",
      "version": "v1.3",
      "status": "active",
      "description": "優化市場情緒解讀語氣",
      "created_at": "2026-09-20T10:00:00Z",
      "activated_at": "2026-09-20T11:00:00Z"
    },
    {
      "id": "uuid",
      "engine_type": "llm",
      "version": "v1.2",
      "status": "archived",
      "description": "初始版本",
      "created_at": "2026-09-01T10:00:00Z"
    }
  ]
}
13.3 GET /admin/engines/{type}/versions/{id}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "engine_type": "llm",
    "version": "v1.3",
    "config": {
      "model": "qwen2.5:7b",
      "temperature": 0.3,
      "max_tokens": 200,
      "system_prompt": "你是一位財務分析師...",
      "user_prompt_template": "市場情緒分數：{{ sentiment_score }}..."
    },
    "status": "active",
    "description": "優化市場情緒解讀語氣",
    "created_at": "2026-09-20T10:00:00Z"
  }
}
13.4 POST /admin/engines/{type}/versions
請求：

json
{
  "version": "v1.4",
  "config": {
    "model": "qwen2.5:7b",
    "temperature": 0.3,
    "max_tokens": 200,
    "system_prompt": "你是一位財務分析師...",
    "user_prompt_template": "市場情緒分數：{{ sentiment_score }}..."
  },
  "description": "優化市場情緒解讀語氣"
}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "version": "v1.4",
    "status": "draft"
  }
}
錯誤：

Code	說明
ENGINE_VERSION_EXISTS	版本號已存在
ENGINE_INVALID_CONFIG	設定格式錯誤
13.5 PUT /admin/engines/{type}/versions/{id}
說明：更新草稿或測試版（啟用中不可改）

13.6 POST /admin/engines/{type}/versions/{id}/test
說明：用測試輸入驗證版本

請求：

json
{
  "test_input": {
    "sentiment_score": 62,
    "state": "elevated",
    "volatility": 0.23,
    "drawdown": -0.08
  }
}
回應：

json
{
  "success": true,
  "data": {
    "output": "目前市場情緒分數為 62...",
    "latency_ms": 850,
    "tokens_input": 45,
    "tokens_output": 120,
    "status": "success"
  }
}
13.7 POST /admin/engines/{type}/versions/{id}/activate
說明：啟用版本（原 active 版本自動 archived）

回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "status": "active",
    "activated_at": "2026-09-22T10:00:00Z",
    "cache_invalidation_published": true
  }
}
13.8 POST /admin/engines/{type}/versions/{id}/archive
說明：封存版本

13.9 DELETE /admin/engines/{type}/versions/{id}
說明：刪除草稿（僅 draft 可刪）

13.10 GET /admin/engines/traces
Query：?engine_type=llm&status=success&date=2026-09-22

回應：

json
{
  "success": true,
  "data": [
    {
      "execution_snapshot_id": "uuid",
      "execution_date": "2026-09-22",
      "status": "success",
      "engines": {
        "crawler": "v1.2",
        "normalizer": "v1.0",
        "validator": "v1.1",
        "matcher": "v1.0",
        "monte_carlo": "v1.0.0",
        "llm": "v1.3"
      }
    }
  ]
}
13.11 GET /admin/engines/traces/{snapshot_id}
說明：取得完整追蹤樹

回應：

json
{
  "success": true,
  "data": {
    "execution_snapshot_id": "uuid",
    "execution_date": "2026-09-22",
    "root": {
      "engine_type": "crawler",
      "step_name": "daily_crawl",
      "status": "success",
      "duration_ms": 3200,
      "children": [
        {
          "engine_type": "crawler",
          "step_name": "fetch_twse",
          "status": "success",
          "duration_ms": 320,
          "input_data": { "symbol": "0050" },
          "output_data": { "price": 155.20 }
        },
        {
          "engine_type": "crawler",
          "step_name": "fetch_yfinance",
          "status": "success",
          "duration_ms": 1200,
          "output_data": { "price": 155.18 }
        }
      ]
    }
  }
}
13.12 POST /admin/engines/recompute
說明：建立重算任務

請求：

json
{
  "engine_type": "monte_carlo",
  "from_version_id": "uuid-v1.0.0",
  "to_version_id": "uuid-v1.1.0",
  "start_date": "2026-08-23",
  "end_date": "2026-09-22"
}
回應：

json
{
  "success": true,
  "data": {
    "job_id": "uuid",
    "status": "pending",
    "estimated_records": 30
  }
}
13.13 GET /admin/engines/recompute/{job_id}
回應：

json
{
  "success": true,
  "data": {
    "id": "uuid",
    "engine_type": "monte_carlo",
    "status": "completed",
    "affected_records": 30,
    "started_at": "2026-09-22T10:00:00Z",
    "completed_at": "2026-09-22T10:05:00Z"
  }
}
13.14 GET /admin/engines/recompute
Query：?status=running

13.15 GET /admin/engines/llm-usage
Query：?provider=groq&date_from=2026-09-01&date_to=2026-09-22

回應：

json
{
  "success": true,
  "data": {
    "total_requests": 1500,
    "total_tokens_input": 67500,
    "total_tokens_output": 180000,
    "total_cost_usd": 0.00,
    "by_provider": {
      "template": { "requests": 1000, "cost_usd": 0.00 },
      "groq": { "requests": 450, "cost_usd": 0.00 },
      "ollama": { "requests": 50, "cost_usd": 0.00 }
    }
  }
}
14. LLM Provider API（/admin/llm/*）— v1.5 新增
14.1 GET /admin/llm/providers
說明：取得可用的 Provider 列表

回應：

json
{
  "success": true,
  "data": [
    {
      "provider": "template",
      "name": "模板",
      "status": "available",
      "config_required": false
    },
    {
      "provider": "groq",
      "name": "Groq",
      "status": "available",
      "config_required": true
    },
    {
      "provider": "gemini",
      "name": "Gemini",
      "status": "available",
      "config_required": true
    },
    {
      "provider": "openai",
      "name": "OpenAI",
      "status": "not_configured",
      "config_required": true
    },
    {
      "provider": "ollama",
      "name": "Ollama（自建）",
      "status": "offline",
      "config_required": true
    }
  ]
}
14.2 POST /admin/llm/providers/{provider}/test
說明：測試 Provider 連線

請求：

json
{
  "test_prompt": "請用一句話說明市場狀態"
}
回應：

json
{
  "success": true,
  "data": {
    "provider": "groq",
    "status": "healthy",
    "latency_ms": 420,
    "output": "目前市場波動程度相對提高。"
  }
}
14.3 PUT /admin/llm/providers/{provider}/config
說明：設定 Provider 金鑰

請求：

json
{
  "api_key": "gsk_..."
}
14.4 GET /admin/llm/routing
說明：查看方案與 Provider 對應

回應：

json
{
  "success": true,
  "data": {
    "routing": {
      "free": "template",
      "pro": "groq",
      "pro_plus": "gemini",
      "admin": "ollama"
    }
  }
}
14.5 PUT /admin/llm/routing
說明：修改路由

請求：

json
{
  "routing": {
    "free": "template",
    "pro": "groq",
    "pro_plus": "gemini",
    "admin": "ollama"
  }
}
15. 金流 API（/billing/*，Full P18）
15.1 POST /billing/checkout
請求：

json
{
  "plan": "pro",
  "auto_renew": true
}
回應：

json
{
  "success": true,
  "data": {
    "checkout_url": "https://checkout.stripe.com/...",
    "session_id": "cs_..."
  }
}
15.2 POST /billing/webhook
（Stripe Webhook）

15.3 GET /billing/subscription
15.4 GET /billing/invoices
15.5 POST /billing/cancel
15.6 POST /billing/refund
16. 健康檢查 API（/health/*）
16.1 GET /health
回應：

json
{
  "status": "healthy",
  "version": "1.5.0",
  "database": "connected",
  "redis": "connected",
  "timestamp": "2026-09-22T10:00:00Z"
}
16.2 GET /health/ready
16.3 GET /health/live
17. 錯誤碼總表（v1.5 更新）
前綴	類別	錯誤碼
AUTH_	認證	AUTH_INVALID_OTP, AUTH_OTP_EXPIRED, AUTH_OTP_RATE_LIMITED, AUTH_OTP_DAILY_LIMIT, AUTH_OTP_MAX_ATTEMPTS, AUTH_INVALID_CREDENTIALS
USER_	用戶	USER_NOT_FOUND, USER_INACTIVE, USER_DELETED
MODEL_	模型	MODEL_NOT_FOUND, MODEL_LIMIT_EXCEEDED, MODEL_INVALID_INPUT
CRAWL_	爬蟲	CRAWL_SOURCE_FAILED, CRAWL_DATA_CONFLICT, CRAWL_TIMEOUT
FORECAST_	預測	FORECAST_INSUFFICIENT_DATA, FORECAST_FAILED
INSURANCE_	保險	INSURANCE_POLICY_NOT_FOUND, INSURANCE_POLICY_EXPIRED
HEALTH_	健康	HEALTH_CONSENT_REQUIRED, HEALTH_PROFILE_NOT_FOUND, HEALTH_INVALID_BIRTH_DATE
ENGINE_	引擎管理	ENGINE_VERSION_NOT_FOUND, ENGINE_VERSION_EXISTS, ENGINE_INVALID_CONFIG, ENGINE_CANNOT_EDIT_ACTIVE, ENGINE_ACTIVATION_FAILED, ENGINE_RECOMPUTE_FAILED, ENGINE_CACHE_PUBLISH_FAILED
LLM_	LLM	LLM_PROVIDER_NOT_FOUND, LLM_PROVIDER_OFFLINE, LLM_RATE_LIMITED, LLM_INVALID_API_KEY, LLM_TIMEOUT
BILLING_	金流	BILLING_PAYMENT_FAILED, BILLING_SUBSCRIPTION_NOT_FOUND
SYSTEM_	系統	SYSTEM_SERVICE_UNAVAILABLE, SYSTEM_TIMEOUT
INCIDENT_	異常	INCIDENT_RECOVERY_FAILED
文件 5 結束
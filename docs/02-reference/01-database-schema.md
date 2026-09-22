📄 文件 4：資料庫完整 Schema
版本：v1.5
適用範圍：MVP 與完整版共用
資料庫：PostgreSQL

0. 通用規範
0.1 命名規則
類型	規則	範例
表名	snake_case、複數	users、financial_models
欄位名	snake_case	user_id、created_at
主鍵	id（UUID）	id CHAR(36)
外鍵	{表名單數}_id	user_id
索引	idx_{表名}_{欄位}	idx_users_email
唯一鍵	uniq_{表名}_{欄位}	uniq_users_email
0.2 通用欄位
所有表都必須包含：

欄位	類型	說明
id	CHAR(36)	主鍵（UUID）
created_at	TIMESTAMP	建立時間
updated_at	TIMESTAMP	更新時間
多租戶表額外包含：

欄位	類型	說明
tenant_id	CHAR(36)	租戶隔離
created_by	CHAR(36)	建立者
0.3 UUID 產生
sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- 預設值
id CHAR(36) DEFAULT uuid_generate_v4()::text
0.4 時間戳記自動更新
sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
1. 租戶與核心表（1-9）
1.1 tenants（租戶）
sql
CREATE TABLE tenants (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    plan VARCHAR(20) DEFAULT 'free',
    status VARCHAR(20) DEFAULT 'active',
    max_users INT DEFAULT 5,
    max_models INT DEFAULT 2,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tenants_slug ON tenants(slug);
CREATE INDEX idx_tenants_status ON tenants(status);
Seed 資料：

sql
INSERT INTO tenants (id, name, slug, plan, max_users, max_models)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    '預設租戶', 'default', 'free', 5, 10
);
1.2 users（一般用戶）— v1.5 修改
sql
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    tenant_id CHAR(36) NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    status VARCHAR(20) DEFAULT 'active',
    -- v1.5 新增欄位
    llm_provider VARCHAR(30) DEFAULT 'template',
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by CHAR(36),
    UNIQUE (tenant_id, email)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_tenant ON users(tenant_id);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_llm_provider ON users(llm_provider);
llm_provider 可能值：template / groq / gemini / openai / ollama

1.3 admin_users（管理員）
sql
CREATE TABLE admin_users (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'admin',
    status VARCHAR(20) DEFAULT 'active',
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_admin_users_email ON admin_users(email);
1.4 otp_tokens（OTP 驗證碼）
sql
CREATE TABLE otp_tokens (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    email VARCHAR(255) NOT NULL,
    otp_hash VARCHAR(255) NOT NULL,
    purpose VARCHAR(20) DEFAULT 'login',
    attempts INT DEFAULT 0,
    max_attempts INT DEFAULT 3,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_otp_tokens_email ON otp_tokens(email);
CREATE INDEX idx_otp_tokens_expires ON otp_tokens(expires_at);
CREATE INDEX idx_otp_tokens_used ON otp_tokens(used_at);
1.5 refresh_tokens（Refresh Token）
sql
CREATE TABLE refresh_tokens (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id CHAR(36) NOT NULL,
    user_type VARCHAR(20) NOT NULL,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    revoked_at TIMESTAMP,
    replaced_by CHAR(36),
    user_agent TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id, user_type);
CREATE INDEX idx_refresh_tokens_hash ON refresh_tokens(token_hash);
CREATE INDEX idx_refresh_tokens_expires ON refresh_tokens(expires_at);
1.6 financial_models（財務模型）
sql
CREATE TABLE financial_models (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    tenant_id CHAR(36) NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id CHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    base_currency VARCHAR(3) DEFAULT 'TWD',
    emergency_fund_months INT DEFAULT 6,
    is_default BOOLEAN DEFAULT FALSE,
    is_archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by CHAR(36)
);

CREATE INDEX idx_financial_models_user ON financial_models(user_id);
CREATE INDEX idx_financial_models_tenant ON financial_models(tenant_id);
CREATE INDEX idx_financial_models_default ON financial_models(user_id, is_default);
1.7 vaults（金庫）
sql
CREATE TABLE vaults (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    tenant_id CHAR(36) NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id CHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    model_id CHAR(36) NOT NULL REFERENCES financial_models(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    vault_type VARCHAR(20) NOT NULL,
    currency VARCHAR(3) DEFAULT 'TWD',
    amount NUMERIC(18, 2) DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by CHAR(36)
);

CREATE INDEX idx_vaults_model ON vaults(model_id);
CREATE INDEX idx_vaults_user ON vaults(user_id);
CREATE INDEX idx_vaults_type ON vaults(vault_type);
1.8 holdings（持有部位）
sql
CREATE TABLE holdings (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    tenant_id CHAR(36) NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id CHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    model_id CHAR(36) NOT NULL REFERENCES financial_models(id) ON DELETE CASCADE,
    asset_definition_id CHAR(36) NOT NULL REFERENCES asset_definitions(id),
    quantity NUMERIC(18, 6) NOT NULL,
    average_cost NUMERIC(18, 4),
    currency VARCHAR(3) DEFAULT 'TWD',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by CHAR(36)
);

CREATE INDEX idx_holdings_model ON holdings(model_id);
CREATE INDEX idx_holdings_user ON holdings(user_id);
CREATE INDEX idx_holdings_asset ON holdings(asset_definition_id);
1.9 liabilities（負債）
sql
CREATE TABLE liabilities (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    tenant_id CHAR(36) NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id CHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    model_id CHAR(36) NOT NULL REFERENCES financial_models(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    liability_type VARCHAR(20) NOT NULL,
    total_amount NUMERIC(18, 2) NOT NULL,
    remaining_amount NUMERIC(18, 2) NOT NULL,
    interest_rate NUMERIC(5, 4),
    monthly_payment NUMERIC(18, 2),
    start_date DATE,
    end_date DATE,
    currency VARCHAR(3) DEFAULT 'TWD',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by CHAR(36)
);

CREATE INDEX idx_liabilities_model ON liabilities(model_id);
CREATE INDEX idx_liabilities_user ON liabilities(user_id);
CREATE INDEX idx_liabilities_type ON liabilities(liability_type);
2. 資產插件表（10-11）
2.1 asset_classes（資產類別）
sql
CREATE TABLE asset_classes (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    handler_class VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_asset_classes_code ON asset_classes(code);
CREATE INDEX idx_asset_classes_active ON asset_classes(is_active);
Seed 資料：

sql
INSERT INTO asset_classes (code, name, handler_class, display_order) VALUES
('equity', '股票', 'EquityHandler', 1),
('forex', '外匯', 'ForexHandler', 2),
('money_market', '貨幣基金', 'MoneyMarketHandler', 3),
('bond', '債券', 'BondHandler', 4),
('metal', '貴金屬', 'MetalHandler', 5),
('crypto', '虛擬貨幣', 'CryptoHandler', 6);
2.2 asset_definitions（資產標的）
sql
CREATE TABLE asset_definitions (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    asset_class_id CHAR(36) NOT NULL REFERENCES asset_classes(id),
    symbol VARCHAR(50) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    currency VARCHAR(3) DEFAULT 'TWD',
    source_config JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (asset_class_id, symbol)
);

CREATE INDEX idx_asset_definitions_class ON asset_definitions(asset_class_id);
CREATE INDEX idx_asset_definitions_symbol ON asset_definitions(symbol);
CREATE INDEX idx_asset_definitions_active ON asset_definitions(is_active);
CREATE INDEX idx_asset_definitions_source ON asset_definitions USING GIN(source_config);
Seed 資料：

sql
INSERT INTO asset_definitions (asset_class_id, symbol, display_name, source_config)
SELECT (SELECT id FROM asset_classes WHERE code = 'equity'),
    '0050.TW', '元大台灣50',
    '{
        "primary": {"provider": "twse", "symbol": "0050"},
        "fallbacks": [
            {"provider": "yfinance", "ticker": "0050.TW"},
            {"provider": "cnyes", "symbol": "0050"}
        ],
        "validation": {"tolerance_pct": 0.5, "min_sources": 2},
        "update_frequency": "daily"
    }'::jsonb;

INSERT INTO asset_definitions (asset_class_id, symbol, display_name, source_config)
SELECT (SELECT id FROM asset_classes WHERE code = 'forex'),
    'USD/TWD', '美元兌台幣',
    '{
        "primary": {"provider": "cbc", "pair": "USD/TWD"},
        "fallbacks": [
            {"provider": "cnyes", "pair": "USDTWD"},
            {"provider": "yfinance", "ticker": "TWD=X"}
        ],
        "validation": {"tolerance_pct": 0.5, "min_sources": 2},
        "update_frequency": "daily"
    }'::jsonb;

INSERT INTO asset_definitions (asset_class_id, symbol, display_name, source_config)
SELECT (SELECT id FROM asset_classes WHERE code = 'money_market'),
    'TWD_MMF', '台幣貨幣基金',
    '{
        "primary": {"provider": "manual", "nav": 1.0},
        "validation": {"tolerance_pct": 0.1, "min_sources": 1},
        "update_frequency": "weekly"
    }'::jsonb;
3. 市場資料表（12-13）— v1.5 修改
3.1 market_prices（最新 canonical 價格）
sql
CREATE TABLE market_prices (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    asset_definition_id CHAR(36) NOT NULL REFERENCES asset_definitions(id) ON DELETE CASCADE,
    symbol VARCHAR(50) NOT NULL,
    price NUMERIC(18, 6) NOT NULL,
    currency VARCHAR(3) DEFAULT 'TWD',
    price_date DATE NOT NULL,
    source_status VARCHAR(20) DEFAULT 'VERIFIED',
    source_used VARCHAR(50),
    source_detail JSONB,
    validation_level VARCHAR(20),
    -- v1.5 新增
    execution_snapshot_id CHAR(36),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (asset_definition_id)
);

CREATE INDEX idx_market_prices_symbol ON market_prices(symbol);
CREATE INDEX idx_market_prices_status ON market_prices(source_status);
CREATE INDEX idx_market_prices_date ON market_prices(price_date);
CREATE INDEX idx_market_prices_snapshot ON market_prices(execution_snapshot_id);
3.2 market_snapshots（歷史快照）
sql
CREATE TABLE market_snapshots (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    asset_definition_id CHAR(36) NOT NULL REFERENCES asset_definitions(id) ON DELETE CASCADE,
    symbol VARCHAR(50) NOT NULL,
    snapshot_date DATE NOT NULL,
    open NUMERIC(18, 6),
    high NUMERIC(18, 6),
    low NUMERIC(18, 6),
    close NUMERIC(18, 6) NOT NULL,
    volume BIGINT,
    currency VARCHAR(3) DEFAULT 'TWD',
    source VARCHAR(50) NOT NULL,
    validation_status VARCHAR(20) DEFAULT 'LEVEL_1',
    -- v1.5 新增
    execution_snapshot_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (asset_definition_id, snapshot_date)
);

CREATE INDEX idx_market_snapshots_symbol ON market_snapshots(symbol);
CREATE INDEX idx_market_snapshots_date ON market_snapshots(snapshot_date);
CREATE INDEX idx_market_snapshots_asset_date ON market_snapshots(asset_definition_id, snapshot_date DESC);
CREATE INDEX idx_market_snapshots_snapshot ON market_snapshots(execution_snapshot_id);
4. 預測表（14-16）— v1.5 修改
4.1 forecast_runs（預測執行紀錄）
sql
CREATE TABLE forecast_runs (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id CHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    model_id CHAR(36) NOT NULL REFERENCES financial_models(id) ON DELETE CASCADE,
    model_version VARCHAR(20) NOT NULL,
    input_snapshot_id CHAR(36) NOT NULL REFERENCES forecast_inputs(id),
    simulation_count INT NOT NULL,
    horizon_months INT NOT NULL,
    status VARCHAR(20) DEFAULT 'completed',
    -- v1.5 新增
    execution_snapshot_id CHAR(36),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_forecast_runs_user ON forecast_runs(user_id);
CREATE INDEX idx_forecast_runs_model ON forecast_runs(model_id);
CREATE INDEX idx_forecast_runs_date ON forecast_runs(generated_at DESC);
CREATE INDEX idx_forecast_runs_snapshot ON forecast_runs(execution_snapshot_id);
4.2 forecast_results（預測結果）
sql
CREATE TABLE forecast_results (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    run_id CHAR(36) NOT NULL REFERENCES forecast_runs(id) ON DELETE CASCADE,
    metric VARCHAR(50) NOT NULL,
    value NUMERIC(10, 6) NOT NULL,
    confidence_interval_low NUMERIC(10, 6),
    confidence_interval_high NUMERIC(10, 6),
    -- v1.5 新增
    execution_snapshot_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_forecast_results_run ON forecast_results(run_id);
CREATE INDEX idx_forecast_results_metric ON forecast_results(metric);
CREATE INDEX idx_forecast_results_snapshot ON forecast_results(execution_snapshot_id);
4.3 forecast_inputs（預測輸入快照）
sql
CREATE TABLE forecast_inputs (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id CHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    user_snapshot JSONB NOT NULL,
    data_quality VARCHAR(20) DEFAULT 'GOOD',
    market_snapshot_refs JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_forecast_inputs_user ON forecast_inputs(user_id);
CREATE INDEX idx_forecast_inputs_date ON forecast_inputs(snapshot_date DESC);
5. 保險表（17-21）— v1.5 修改
5.1 insurance_policies（用戶保單）
sql
CREATE TABLE insurance_policies (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    tenant_id CHAR(36) NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id CHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    model_id CHAR(36) REFERENCES financial_models(id) ON DELETE SET NULL,
    category VARCHAR(20) NOT NULL,
    subcategory VARCHAR(30),
    policy_name VARCHAR(200) NOT NULL,
    insurer_name VARCHAR(100),
    policy_number VARCHAR(100),
    coverage_amount NUMERIC(18, 2) NOT NULL,
    annual_premium NUMERIC(18, 2),
    payment_period_years INT,
    start_date DATE,
    end_date DATE,
    covered_body_parts JSONB,
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by CHAR(36)
);

CREATE INDEX idx_insurance_policies_user ON insurance_policies(user_id);
CREATE INDEX idx_insurance_policies_model ON insurance_policies(model_id);
CREATE INDEX idx_insurance_policies_category ON insurance_policies(category, subcategory);
CREATE INDEX idx_insurance_policies_active ON insurance_policies(is_active);
5.2 insurance_products（保險商品）
sql
CREATE TABLE insurance_products (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    product_code VARCHAR(100) NOT NULL UNIQUE,
    product_name VARCHAR(200) NOT NULL,
    insurer_name VARCHAR(100) NOT NULL,
    category VARCHAR(20) NOT NULL,
    subcategory VARCHAR(30),
    coverage_type VARCHAR(50),
    covered_body_parts JSONB,
    coverage_amount NUMERIC(18, 2),
    annual_premium NUMERIC(18, 2),
    is_active BOOLEAN DEFAULT TRUE,
    listed_at DATE,
    delisted_at DATE,
    source VARCHAR(50),
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_insurance_products_code ON insurance_products(product_code);
CREATE INDEX idx_insurance_products_active ON insurance_products(is_active);
CREATE INDEX idx_insurance_products_category ON insurance_products(category, subcategory);
CREATE INDEX idx_insurance_products_parts ON insurance_products USING GIN(covered_body_parts);
5.3 insurance_products_history（商品生命週期）
sql
CREATE TABLE insurance_products_history (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    product_id CHAR(36) NOT NULL REFERENCES insurance_products(id) ON DELETE CASCADE,
    change_type VARCHAR(20) NOT NULL,
    change_detail JSONB,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50)
);

CREATE INDEX idx_insurance_products_history_product ON insurance_products_history(product_id);
CREATE INDEX idx_insurance_products_history_type ON insurance_products_history(change_type);
CREATE INDEX idx_insurance_products_history_date ON insurance_products_history(changed_at DESC);
5.4 body_part_mapping（人體部位映射）
sql
CREATE TABLE body_part_mapping (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    part_code VARCHAR(30) NOT NULL UNIQUE,
    part_name VARCHAR(100) NOT NULL,
    category VARCHAR(20) NOT NULL,
    description TEXT,
    related_diseases JSONB,
    required_coverage NUMERIC(18, 2),
    ui_config JSONB,
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_body_part_mapping_code ON body_part_mapping(part_code);
CREATE INDEX idx_body_part_mapping_active ON body_part_mapping(is_active);
Seed 資料：

sql
INSERT INTO body_part_mapping (part_code, part_name, category, related_diseases, required_coverage, ui_config, display_order) VALUES
('brain', '大腦 / 神經', 'internal', '["腦中風", "癲癇", "失智"]'::jsonb, 3000000,
 '{"svg_id": "part-brain", "x": 100, "y": 50, "layer": "internal"}'::jsonb, 1),
('heart', '心臟 / 心血管', 'internal', '["心肌梗塞", "心臟病"]'::jsonb, 2000000,
 '{"svg_id": "part-heart", "x": 120, "y": 100, "layer": "internal"}'::jsonb, 2),
('eyes', '雙眼 / 視力', 'external', '["白內障", "視網膜病變"]'::jsonb, 500000,
 '{"svg_id": "part-eyes", "x": 130, "y": 30, "layer": "external"}'::jsonb, 3),
('limbs', '四肢 / 骨骼', 'external', '["骨折", "截肢"]'::jsonb, 800000,
 '{"svg_id": "part-limbs", "x": 100, "y": 200, "layer": "external"}'::jsonb, 4),
('liver', '肝臟 / 消化', 'internal', '["肝炎", "肝硬化"]'::jsonb, 1500000,
 '{"svg_id": "part-liver", "x": 110, "y": 120, "layer": "internal"}'::jsonb, 5),
('lungs', '肺 / 呼吸', 'internal', '["肺癌", "氣喘"]'::jsonb, 2000000,
 '{"svg_id": "part-lungs", "x": 125, "y": 80, "layer": "internal"}'::jsonb, 6),
('skin', '皮膚 / 外觀', 'external', '["燒燙傷", "皮膚癌"]'::jsonb, 500000,
 '{"svg_id": "part-skin", "x": 100, "y": 150, "layer": "external"}'::jsonb, 7),
('reproductive', '生殖系統', 'internal', '["乳癌", "子宮頸癌"]'::jsonb, 2500000,
 '{"svg_id": "part-reproductive", "x": 110, "y": 160, "layer": "internal"}'::jsonb, 8);
5.5 insurance_gap_snapshots（保險缺口快照）— v1.5 修改
sql
CREATE TABLE insurance_gap_snapshots (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id CHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    part_code VARCHAR(30) NOT NULL REFERENCES body_part_mapping(part_code),
    existing_coverage NUMERIC(18, 2) DEFAULT 0,
    required_coverage NUMERIC(18, 2) NOT NULL,
    coverage_ratio NUMERIC(6, 4) NOT NULL,
    state VARCHAR(10) NOT NULL,
    calculation_detail JSONB,
    -- v1.5 新增
    execution_snapshot_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, snapshot_date, part_code)
);

CREATE INDEX idx_insurance_gap_user ON insurance_gap_snapshots(user_id);
CREATE INDEX idx_insurance_gap_date ON insurance_gap_snapshots(snapshot_date DESC);
CREATE INDEX idx_insurance_gap_state ON insurance_gap_snapshots(state);
CREATE INDEX idx_insurance_gap_snapshot ON insurance_gap_snapshots(execution_snapshot_id);
6. 審計與事件表（22-25）
6.1 email_logs（Email 發送紀錄）
sql
CREATE TABLE email_logs (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id CHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    email_type VARCHAR(50) NOT NULL,
    recipient VARCHAR(255) NOT NULL,
    subject VARCHAR(500),
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_email_logs_user ON email_logs(user_id);
CREATE INDEX idx_email_logs_type ON email_logs(email_type);
CREATE INDEX idx_email_logs_status ON email_logs(status);
CREATE INDEX idx_email_logs_sent ON email_logs(sent_at DESC);
6.2 incidents（系統異常）
sql
CREATE TABLE incidents (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    incident_number VARCHAR(20) NOT NULL UNIQUE,
    service_name VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    trigger_event VARCHAR(50) NOT NULL,
    diagnosis_report TEXT,
    possible_causes JSONB,
    auto_recovery_attempted BOOLEAN DEFAULT FALSE,
    auto_recovery_success BOOLEAN DEFAULT FALSE,
    recovery_action_taken VARCHAR(100),
    recovery_error TEXT,
    engineer_email_sent BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'open',
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

CREATE INDEX idx_incidents_number ON incidents(incident_number);
CREATE INDEX idx_incidents_service ON incidents(service_name);
CREATE INDEX idx_incidents_severity ON incidents(severity);
CREATE INDEX idx_incidents_status ON incidents(status);
CREATE INDEX idx_incidents_detected ON incidents(detected_at DESC);
6.3 subscriptions（訂閱，完整版才寫入）
sql
CREATE TABLE subscriptions (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    tenant_id CHAR(36) NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id CHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    stripe_customer_id VARCHAR(100),
    stripe_subscription_id VARCHAR(100),
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    trial_end TIMESTAMP,
    auto_renew BOOLEAN DEFAULT FALSE,
    failed_payment_count INT DEFAULT 0,
    grace_period_end TIMESTAMP,
    canceled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_subscriptions_tenant ON subscriptions(tenant_id);
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_subscriptions_stripe ON subscriptions(stripe_subscription_id);
6.4 audit_logs（操作審計）
sql
CREATE TABLE audit_logs (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id CHAR(36),
    user_type VARCHAR(20),
    tenant_id CHAR(36),
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id CHAR(36),
    changes JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user ON audit_logs(user_id, user_type);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at DESC);
7. 健康檔案表（26-30）
7.1 user_health_profiles（用戶健康檔案）
sql
CREATE TABLE user_health_profiles (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id CHAR(36) NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    birth_date DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    family_history JSONB,
    has_genetic_test BOOLEAN DEFAULT FALSE,
    consent_genetic BOOLEAN DEFAULT FALSE,
    consent_genetic_at TIMESTAMP,
    completion_rate NUMERIC(5, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_health_profiles_user ON user_health_profiles(user_id);
CREATE INDEX idx_health_profiles_consent ON user_health_profiles(consent_genetic);
7.2 genetic_markers（基因點位清單）
sql
CREATE TABLE genetic_markers (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    marker_code VARCHAR(50) NOT NULL UNIQUE,
    marker_name VARCHAR(100) NOT NULL,
    related_diseases JSONB NOT NULL,
    related_body_parts JSONB,
    risk_level_high NUMERIC(4, 2) DEFAULT 2.0,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_genetic_markers_code ON genetic_markers(marker_code);
CREATE INDEX idx_genetic_markers_active ON genetic_markers(is_active);
Seed 資料：

sql
INSERT INTO genetic_markers (marker_code, marker_name, related_diseases, related_body_parts, risk_level_high, display_order) VALUES
('BRCA1', 'BRCA1 基因', '["乳癌", "卵巢癌"]'::jsonb, '["reproductive"]'::jsonb, 3.0, 1),
('BRCA2', 'BRCA2 基因', '["乳癌", "卵巢癌", "胰臟癌"]'::jsonb, '["reproductive"]'::jsonb, 3.0, 2),
('APOE', 'APOE 基因', '["阿茲海默症"]'::jsonb, '["brain"]'::jsonb, 2.5, 3),
('LDLR', 'LDLR 基因', '["家族性高膽固醇", "心血管疾病"]'::jsonb, '["heart"]'::jsonb, 2.0, 4),
('TP53', 'TP53 基因', '["多種癌症"]'::jsonb, '["reproductive", "lungs"]'::jsonb, 3.0, 5),
('HFE', 'HFE 基因', '["血色素沉著症"]'::jsonb, '["liver"]'::jsonb, 2.0, 6),
('MTHFR', 'MTHFR 基因', '["血栓", "葉酸代謝異常"]'::jsonb, '["heart"]'::jsonb, 1.5, 7),
('ALDH2', 'ALDH2 基因', '["酒精代謝異常", "食道癌"]'::jsonb, '["liver"]'::jsonb, 1.8, 8),
('HLA-B*1502', 'HLA-B*1502', '["藥物過敏（卡馬西平）"]'::jsonb, '[]'::jsonb, 1.5, 9);
7.3 user_genetic_tests（用戶基因檢測結果）
sql
CREATE TABLE user_genetic_tests (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id CHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    marker_id CHAR(36) NOT NULL REFERENCES genetic_markers(id),
    result VARCHAR(20) NOT NULL,
    raw_data_encrypted TEXT,
    risk_level_computed NUMERIC(4, 2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, marker_id)
);

CREATE INDEX idx_user_genetic_tests_user ON user_genetic_tests(user_id);
CREATE INDEX idx_user_genetic_tests_marker ON user_genetic_tests(marker_id);
CREATE INDEX idx_user_genetic_tests_result ON user_genetic_tests(result);
7.4 medical_cost_references（醫療費用參考）
sql
CREATE TABLE medical_cost_references (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    disease_code VARCHAR(50) NOT NULL UNIQUE,
    disease_name VARCHAR(200) NOT NULL,
    related_body_part VARCHAR(30) REFERENCES body_part_mapping(part_code),
    cost_min NUMERIC(18, 2) NOT NULL,
    cost_max NUMERIC(18, 2) NOT NULL,
    cost_avg NUMERIC(18, 2),
    currency VARCHAR(3) DEFAULT 'TWD',
    source VARCHAR(100),
    effective_date DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_medical_costs_code ON medical_cost_references(disease_code);
CREATE INDEX idx_medical_costs_body_part ON medical_cost_references(related_body_part);
Seed 資料：

sql
INSERT INTO medical_cost_references (disease_code, disease_name, related_body_part, cost_min, cost_max, cost_avg, source) VALUES
('HEART_SURGERY', '心導管手術', 'heart', 150000, 300000, 225000, '人工 Seed'),
('CANCER_CHEMO', '癌症化療（完整療程）', 'reproductive', 500000, 2000000, 1250000, '人工 Seed'),
('STROKE_REHAB', '腦中風復健', 'brain', 300000, 1000000, 650000, '人工 Seed'),
('DIALYSIS_YEAR', '洗腎（年）', 'liver', 600000, 800000, 700000, '人工 Seed'),
('FRACTURE_SURGERY', '骨折手術', 'limbs', 50000, 150000, 100000, '人工 Seed'),
('CATARACT_SURGERY', '白內障手術', 'eyes', 30000, 80000, 55000, '人工 Seed'),
('LUNG_CANCER', '肺癌治療', 'lungs', 800000, 2500000, 1650000, '人工 Seed'),
('SKIN_BURN', '燒燙傷治療', 'skin', 100000, 500000, 300000, '人工 Seed');
7.5 disease_risk_mapping（疾病風險映射）
sql
CREATE TABLE disease_risk_mapping (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    body_part_code VARCHAR(30) NOT NULL REFERENCES body_part_mapping(part_code),
    disease_code VARCHAR(50) NOT NULL,
    age_risk_multiplier JSONB,
    gender_risk_multiplier JSONB,
    family_history_multiplier NUMERIC(4, 2) DEFAULT 1.5,
    genetic_multiplier NUMERIC(4, 2) DEFAULT 1.5,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_disease_risk_body_part ON disease_risk_mapping(body_part_code);
CREATE INDEX idx_disease_risk_disease ON disease_risk_mapping(disease_code);
Seed 資料：

sql
INSERT INTO disease_risk_mapping (body_part_code, disease_code, age_risk_multiplier, gender_risk_multiplier, family_history_multiplier, genetic_multiplier) VALUES
('heart', 'HEART_SURGERY',
 '{"0-30": 0.8, "31-50": 1.3, "51-65": 1.8, "66+": 2.5}'::jsonb,
 '{"male": 1.3, "female": 1.0}'::jsonb, 1.5, 1.8),
('brain', 'STROKE_REHAB',
 '{"0-30": 0.5, "31-50": 1.0, "51-65": 1.8, "66+": 2.5}'::jsonb,
 '{"male": 1.2, "female": 1.0}'::jsonb, 1.8, 2.5),
('reproductive', 'CANCER_CHEMO',
 '{"0-30": 0.8, "31-50": 1.2, "51-65": 1.5, "66+": 1.5}'::jsonb,
 '{"male": 0.9, "female": 1.3}'::jsonb, 2.0, 3.0);
8. 引擎管理表（31-36）— v1.5 新增
8.1 engine_versions（引擎版本總表）
sql
CREATE TABLE engine_versions (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    engine_type VARCHAR(30) NOT NULL,       -- crawler/normalizer/validator/matcher/monte_carlo/llm
    version VARCHAR(30) NOT NULL,            -- v1.2
    config JSONB NOT NULL,                   -- 完整設定
    status VARCHAR(20) DEFAULT 'draft',      -- draft/testing/active/archived
    description TEXT,
    created_by CHAR(36),
    activated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(engine_type, version)
);

CREATE INDEX idx_engine_versions_type ON engine_versions(engine_type);
CREATE INDEX idx_engine_versions_status ON engine_versions(status);
CREATE INDEX idx_engine_versions_active ON engine_versions(engine_type, status) 
    WHERE status = 'active';
Seed 資料（初始版本）：

sql
INSERT INTO engine_versions (engine_type, version, config, status, description) VALUES
('crawler', 'v1.0', '{"script_version": "v1.0"}'::jsonb, 'active', '初始爬蟲版本'),
('normalizer', 'v1.0', '{"rules": []}'::jsonb, 'active', '初始正規化版本'),
('validator', 'v1.0', '{"tolerance_pct": 0.5, "min_sources": 2}'::jsonb, 'active', '初始驗證版本'),
('matcher', 'v1.0', '{"logic": "user_holdings_only"}'::jsonb, 'active', '初始比對版本'),
('monte_carlo', 'v1.0.0', '{"simulation_count": 10000, "seed": 42}'::jsonb, 'active', '初始模型版本'),
('llm', 'v1.0', '{"provider": "template"}'::jsonb, 'active', '初始模板版本');
8.2 execution_snapshots（執行快照）
sql
CREATE TABLE execution_snapshots (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    execution_date DATE NOT NULL,
    crawler_version_id CHAR(36) REFERENCES engine_versions(id),
    normalizer_version_id CHAR(36) REFERENCES engine_versions(id),
    validator_version_id CHAR(36) REFERENCES engine_versions(id),
    matcher_version_id CHAR(36) REFERENCES engine_versions(id),
    monte_carlo_version_id CHAR(36) REFERENCES engine_versions(id),
    llm_version_id CHAR(36) REFERENCES engine_versions(id),
    status VARCHAR(20) DEFAULT 'pending',    -- pending/running/success/partial/failed
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_exec_snapshots_date ON execution_snapshots(execution_date DESC);
CREATE INDEX idx_exec_snapshots_status ON execution_snapshots(status);
8.3 engine_traces（引擎追蹤樹）
sql
CREATE TABLE engine_traces (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    execution_snapshot_id CHAR(36) REFERENCES execution_snapshots(id) ON DELETE CASCADE,
    engine_type VARCHAR(30) NOT NULL,
    parent_trace_id CHAR(36) REFERENCES engine_traces(id),
    step_name VARCHAR(100),
    input_data JSONB,
    output_data JSONB,
    status VARCHAR(20),                      -- success/failed/skipped
    duration_ms INT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_engine_traces_snapshot ON engine_traces(execution_snapshot_id);
CREATE INDEX idx_engine_traces_engine ON engine_traces(engine_type);
CREATE INDEX idx_engine_traces_status ON engine_traces(status);
CREATE INDEX idx_engine_traces_parent ON engine_traces(parent_trace_id);
CREATE INDEX idx_engine_traces_created ON engine_traces(created_at DESC);
8.4 recompute_jobs（重算任務）
sql
CREATE TABLE recompute_jobs (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    engine_type VARCHAR(30) NOT NULL,
    from_version_id CHAR(36) REFERENCES engine_versions(id),
    to_version_id CHAR(36) REFERENCES engine_versions(id),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'pending',    -- pending/running/completed/failed
    affected_records INT DEFAULT 0,
    error_message TEXT,
    created_by CHAR(36),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_recompute_jobs_status ON recompute_jobs(status);
CREATE INDEX idx_recompute_jobs_engine ON recompute_jobs(engine_type);
CREATE INDEX idx_recompute_jobs_created ON recompute_jobs(created_at DESC);
8.5 llm_usage_logs（LLM 使用紀錄）
sql
CREATE TABLE llm_usage_logs (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id CHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    provider VARCHAR(30) NOT NULL,           -- template/groq/gemini/openai/ollama
    request_type VARCHAR(50),                -- market_sentiment / insurance_gap
    tokens_input INT DEFAULT 0,
    tokens_output INT DEFAULT 0,
    cost_usd NUMERIC(10, 6) DEFAULT 0,
    latency_ms INT,
    status VARCHAR(20),                      -- success/failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_llm_usage_user ON llm_usage_logs(user_id);
CREATE INDEX idx_llm_usage_provider ON llm_usage_logs(provider);
CREATE INDEX idx_llm_usage_created ON llm_usage_logs(created_at DESC);
CREATE INDEX idx_llm_usage_type ON llm_usage_logs(request_type);
8.6 engine_cache_invalidations（快取失效紀錄）
sql
CREATE TABLE engine_cache_invalidations (
    id CHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    engine_type VARCHAR(30) NOT NULL,
    version_id CHAR(36) REFERENCES engine_versions(id),
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subscriber_count INT DEFAULT 0
);

CREATE INDEX idx_cache_inv_published ON engine_cache_invalidations(published_at DESC);
CREATE INDEX idx_cache_inv_engine ON engine_cache_invalidations(engine_type);
9. 索引總結（v1.5 更新）
表	索引數	用途
tenants	2	slug、status
users	4	email、tenant、status、llm_provider
admin_users	1	email
otp_tokens	3	email、expires、used
refresh_tokens	3	user、hash、expires
financial_models	3	user、tenant、default
vaults	3	model、user、type
holdings	3	model、user、asset
liabilities	3	model、user、type
asset_classes	2	code、active
asset_definitions	4	class、symbol、active、GIN
market_prices	4	symbol、status、date、snapshot
market_snapshots	4	symbol、date、asset+date、snapshot
forecast_runs	4	user、model、date、snapshot
forecast_results	3	run、metric、snapshot
forecast_inputs	2	user、date
insurance_policies	4	user、model、category、active
insurance_products	4	code、active、category、GIN
insurance_products_history	3	product、type、date
body_part_mapping	2	code、active
insurance_gap_snapshots	4	user、date、state、snapshot
email_logs	4	user、type、status、sent
incidents	5	number、service、severity、status、date
subscriptions	4	tenant、user、status、stripe
audit_logs	4	user、resource、action、date
user_health_profiles	2	user、consent
genetic_markers	2	code、active
user_genetic_tests	3	user、marker、result
medical_cost_references	2	code、body_part
disease_risk_mapping	2	body_part、disease
engine_versions（v1.5）	3	type、status、active
execution_snapshots（v1.5）	2	date、status
engine_traces（v1.5）	5	snapshot、engine、status、parent、created
recompute_jobs（v1.5）	3	status、engine、created
llm_usage_logs（v1.5）	4	user、provider、created、type
engine_cache_invalidations（v1.5）	2	published、engine
10. 外鍵關係圖（v1.5 新增部分）
text
engine_versions
├── execution_snapshots（crawler_version_id 等 6 個）
├── recompute_jobs（from_version_id, to_version_id）
└── engine_cache_invalidations（version_id）

execution_snapshots
├── engine_traces（execution_snapshot_id）
├── market_prices（execution_snapshot_id）
├── market_snapshots（execution_snapshot_id）
├── forecast_runs（execution_snapshot_id）
├── forecast_results（execution_snapshot_id）
└── insurance_gap_snapshots（execution_snapshot_id）

engine_traces
└── engine_traces（parent_trace_id，自我參考）

users
└── llm_usage_logs（user_id）
11. 資料保留政策實作
11.1 分級刪除邏輯
表	保留政策	實作方式
users	用戶請求刪除	軟刪除 + 30 天後硬刪除
user_health_profiles	用戶請求刪除	立即硬刪除
user_genetic_tests	用戶請求刪除	立即硬刪除
financial_models	用戶請求刪除	級聯刪除
insurance_policies	用戶請求刪除	級聯刪除
subscriptions	法定保留	不刪除
audit_logs	法定保留	不刪除
incidents	系統維運	保留 3 年
email_logs	系統維運	保留 1 年
engine_versions（v1.5）	系統維運	保留（用於追溯）
execution_snapshots（v1.5）	系統維運	保留 2 年
engine_traces（v1.5）	系統維運	保留 1 年
llm_usage_logs（v1.5）	成本追蹤	保留 1 年
11.2 清理任務（cleanup_worker）
python
def cleanup_expired_data():
    # 1. 刪除過期 OTP
    db.query(OtpToken).filter(
        OtpToken.expires_at < datetime.now() - timedelta(days=7)
    ).delete()
    
    # 2. 刪除撤銷的 Refresh Token
    db.query(RefreshToken).filter(
        RefreshToken.revoked_at < datetime.now() - timedelta(days=30)
    ).delete()
    
    # 3. 刪除 30 天前軟刪除的用戶
    db.query(User).filter(
        User.status == 'deleted',
        User.updated_at < datetime.now() - timedelta(days=30)
    ).delete()
    
    # 4. v1.5：清理舊的 engine_traces（> 1 年）
    db.query(EngineTrace).filter(
        EngineTrace.created_at < datetime.now() - timedelta(days=365)
    ).delete()
    
    # 5. v1.5：清理舊的 execution_snapshots（> 2 年）
    db.query(ExecutionSnapshot).filter(
        ExecutionSnapshot.created_at < datetime.now() - timedelta(days=730)
    ).delete()
文件 4 結束


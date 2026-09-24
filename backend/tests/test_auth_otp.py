"""Day 1 重構：OTP 請求 / 驗證 / 節流 / 錯誤碼。"""
import pytest


EMAIL = "user@example.com"


@pytest.fixture
def fixed_otp(monkeypatch):
    import app.services.otp_service as svc
    monkeypatch.setattr(svc, "generate_otp_code", lambda length=6: "123456")
    return "123456"


# ---- 1. 請求成功 ----
async def test_request_success(client, fixed_otp):
    r = await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    assert body["data"]["expires_in"] == 300
    assert body["data"]["dev_code"] == "123456"


# ---- 2. 60 秒節流 ----
async def test_request_throttled(client, fixed_otp):
    await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    r = await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    assert r.status_code == 429
    body = r.json()
    assert body["success"] is False
    assert body["error"]["code"] == "AUTH_OTP_RATE_LIMITED"


# ---- 3. 驗證成功 → 直接回 token ----
async def test_verify_returns_tokens(client, fixed_otp):
    await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    r = await client.post(
        "/api/v1/auth/otp/verify",
        json={"email": EMAIL, "otp": fixed_otp},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["success"] is True
    data = body["data"]
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "Bearer"
    assert data["user"]["email"] == EMAIL
    assert data["user"]["is_new_user"] is True


# ---- 4. 錯誤 OTP → AUTH_INVALID_OTP ----
async def test_verify_wrong_otp(client, fixed_otp):
    await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    r = await client.post(
        "/api/v1/auth/otp/verify",
        json={"email": EMAIL, "otp": "000000"},
    )
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "AUTH_INVALID_OTP"


# ---- 5. 超過 3 次嘗試 → AUTH_OTP_MAX_ATTEMPTS ----
async def test_verify_max_attempts(client, fixed_otp):
    await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    for _ in range(3):
        await client.post(
            "/api/v1/auth/otp/verify",
            json={"email": EMAIL, "otp": "000000"},
        )
    r = await client.post(
        "/api/v1/auth/otp/verify",
        json={"email": EMAIL, "otp": fixed_otp},
    )
    assert r.status_code == 429
    assert r.json()["error"]["code"] == "AUTH_OTP_MAX_ATTEMPTS"


# ---- 6. 未請求直接驗證 → AUTH_OTP_EXPIRED ----
async def test_verify_without_request(client):
    r = await client.post(
        "/api/v1/auth/otp/verify",
        json={"email": EMAIL, "otp": "123456"},
    )
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "AUTH_OTP_EXPIRED"


# ---- 7. Email 格式錯誤 ----
async def test_invalid_email(client):
    r = await client.post(
        "/api/v1/auth/otp/request", json={"email": "not-an-email"}
    )
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "VALIDATION_ERROR"


# ---- 8. Redis 只存 hash ----
async def test_redis_stores_hash_only(client, fixed_otp, fake_redis):
    await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    stored = await fake_redis.get(f"otp:code:{EMAIL}")
    assert stored is not None
    assert fixed_otp not in stored
    assert "$" in stored


# ---- 9. 每日上限（關節流） ----
async def test_daily_limit(client, fixed_otp, monkeypatch):
    from app.core.config import settings
    monkeypatch.setattr(settings, "OTP_RESEND_INTERVAL", 0)
    monkeypatch.setattr(settings, "IP_RATE_PER_MINUTE", 1000)
    monkeypatch.setattr(settings, "IP_RATE_PER_DAY", 100000)

    for i in range(settings.OTP_DAILY_LIMIT):
        r = await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
        assert r.status_code == 200, f"第 {i+1} 次失敗：{r.text}"

    r = await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    assert r.status_code == 429
    assert r.json()["error"]["code"] == "AUTH_OTP_DAILY_LIMIT"

# ---- 10. IP 限流 ----
async def test_ip_rate_limit(client, fixed_otp, monkeypatch):
    from app.core.config import settings
    monkeypatch.setattr(settings, "OTP_RESEND_INTERVAL", 0)
    monkeypatch.setattr(settings, "IP_RATE_PER_MINUTE", 3)

    # 前 3 次 200
    for _ in range(3):
        r = await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
        assert r.status_code == 200

    # 第 4 次被 IP 限流
    r = await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    assert r.status_code == 429
    assert r.json()["error"]["code"] == "AUTH_IP_RATE_LIMITED"
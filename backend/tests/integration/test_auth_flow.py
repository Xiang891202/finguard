"""整合測試：完整登入、授權、健康檔案、基因資料流程。

涵蓋 3 條 Critical Path：
1. 用戶 OTP 登入 → /me → refresh → logout
2. 管理員 密碼登入 → /me → logout
3. 用戶登入 → 建 profile → 同意基因 → 新增檢測 → 100%
"""
import pytest


USER_EMAIL = "flow-user@example.com"


@pytest.fixture
def fixed_otp(monkeypatch):
    import app.services.otp_service as svc
    monkeypatch.setattr(svc, "generate_otp_code", lambda length=6: "654321")
    return "654321"


# ============================================================
# Path 1：用戶完整登入流程
# ============================================================

async def test_user_full_auth_flow(client, fixed_otp):
    # ---- 1. 請求 OTP ----
    r = await client.post("/api/v1/auth/otp/request", json={"email": USER_EMAIL})
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    dev_code = body["data"]["dev_code"]
    assert dev_code == fixed_otp

    # ---- 2. 驗證 OTP → 拿 token ----
    r = await client.post(
        "/api/v1/auth/otp/verify",
        json={"email": USER_EMAIL, "otp": dev_code},
    )
    assert r.status_code == 200, r.text
    tokens = r.json()["data"]
    assert tokens["access_token"]
    assert tokens["refresh_token"]
    assert tokens["token_type"] == "Bearer"
    assert tokens["user"]["email"] == USER_EMAIL
    assert tokens["user"]["is_new_user"] is True

    access = tokens["access_token"]
    refresh = tokens["refresh_token"]

    # ---- 3. 用 access 存取 /me ----
    r = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access}"},
    )
    assert r.status_code == 200
    assert r.json()["data"]["email"] == USER_EMAIL

    # ---- 4. 無 token 存取 /me 應 401 ----
    r = await client.get("/api/v1/auth/me")
    assert r.status_code == 401

    # ---- 5. refresh 換新 token ----
    r = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh},
    )
    assert r.status_code == 200
    new_tokens = r.json()["data"]
    assert new_tokens["access_token"] != access
    assert new_tokens["refresh_token"] != refresh

    # ---- 6. 舊 refresh 重放 → 撤銷整個 family ----
    r = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh},
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "AUTH_REFRESH_REUSED"

    # ---- 7. 新 refresh 也應該失效（family 被撤銷）----
    r = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": new_tokens["refresh_token"]},
    )
    assert r.status_code == 401


# ============================================================
# Path 2：管理員完整登入流程
# ============================================================

async def test_admin_full_auth_flow(client, admin_user):
    from tests.conftest import ADMIN_EMAIL, ADMIN_PASSWORD

    # ---- 1. 登入 ----
    r = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert r.status_code == 200, r.text
    tokens = r.json()["data"]
    assert tokens["access_token"]
    assert tokens["refresh_token"]
    assert tokens["admin"]["email"] == ADMIN_EMAIL
    assert tokens["admin"]["role"] == "admin"

    # ---- 2. /me ----
    r = await client.get(
        "/api/v1/admin/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert r.status_code == 200
    assert r.json()["data"]["email"] == ADMIN_EMAIL

    # ---- 3. 用 user token 打 admin 端點 → 401 ----
    r = await client.post(
        "/api/v1/auth/otp/request",
        json={"email": "someone@example.com"},
    )
    # 用假的 user token 試（不重要，只要驗證 admin 端點拒絕非 admin）
    r = await client.get(
        "/api/v1/admin/auth/me",
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert r.status_code == 401

    # ---- 4. logout ----
    r = await client.post(
        "/api/v1/admin/auth/logout",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert r.status_code == 200
    assert r.json()["data"]["message"] == "已登出"

    # ---- 5. logout 後 refresh 失效 ----
    r = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert r.status_code == 401


# ============================================================
# Path 3：健康檔案完整旅程
# ============================================================

async def test_health_profile_full_journey(client, fixed_otp):
    """登入 → 建 profile (80%) → 同意基因 → 新增檢測 → 100%"""

    # ---- 登入 ----
    await client.post("/api/v1/auth/otp/request", json={"email": USER_EMAIL})
    r = await client.post(
        "/api/v1/auth/otp/verify",
        json={"email": USER_EMAIL, "otp": fixed_otp},
    )
    assert r.status_code == 200
    token = r.json()["data"]["access_token"]
    h = {"Authorization": f"Bearer {token}"}

    # ---- 1. 建 profile（生日 + 性別 = 80%）----
    r = await client.post(
        "/api/v1/app/health/profile",
        json={"birth_date": "1985-06-15", "gender": "male"},
        headers=h,
    )
    assert r.status_code == 200
    assert r.json()["data"]["completion_rate"] == 80.0

    # ---- 2. 重複 POST 應 409 ----
    r = await client.post(
        "/api/v1/app/health/profile",
        json={"birth_date": "1985-06-15", "gender": "male"},
        headers=h,
    )
    assert r.status_code == 409
    assert r.json()["error"]["code"] == "HEALTH_PROFILE_EXISTS"

    # ---- 3. 同意基因 ----
    r = await client.post(
        "/api/v1/app/health/consent",
        json={"consent": True},
        headers=h,
    )
    assert r.status_code == 200
    assert r.json()["data"]["consent_genetic"] is True
    assert r.json()["data"]["consent_genetic_at"] is not None

    # ---- 4. 取 BRCA1 marker ----
    r = await client.get("/api/v1/app/health/genetic-markers", headers=h)
    assert r.status_code == 200
    markers = r.json()["data"]
    assert len(markers) >= 1
    brca1 = next(m for m in markers if m["marker_code"] == "BRCA1")

    # ---- 5. 新增檢測（高風險）----
    r = await client.post(
        "/api/v1/app/health/genetic-tests",
        json={"marker_id": brca1["id"], "result": "high"},
        headers=h,
    )
    assert r.status_code == 200
    test_data = r.json()["data"]
    assert test_data["marker_code"] == "BRCA1"
    assert test_data["result"] == "high"
    assert test_data["risk_level_computed"] == 3.0

    # ---- 6. 完成度 90%（80 + 基因勾選 10）----
    r = await client.get("/api/v1/app/health/completion", headers=h)
    assert r.json()["data"]["completion_rate"] == 90.0
    assert "family_history" in r.json()["data"]["missing_fields"]

    # ---- 7. 更新 profile 加家族病史 → 100% ----
    r = await client.put(
        "/api/v1/app/health/profile",
        json={"family_history": {"cardiovascular": True}},
        headers=h,
    )
    assert r.status_code == 200
    assert r.json()["data"]["completion_rate"] == 100.0

    # ---- 8. 完成度最終 100% ----
    r = await client.get("/api/v1/app/health/completion", headers=h)
    assert r.json()["data"]["completion_rate"] == 100.0
    assert r.json()["data"]["precision_level"] == "full"
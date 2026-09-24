"""Day 2 重構：Refresh / Logout / Me。"""
import pytest


EMAIL = "user@example.com"


@pytest.fixture
def fixed_otp(monkeypatch):
    import app.services.otp_service as svc
    monkeypatch.setattr(svc, "generate_otp_code", lambda length=6: "123456")
    return "123456"


async def _login(client, fixed_otp):
    await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    r = await client.post(
        "/api/v1/auth/otp/verify",
        json={"email": EMAIL, "otp": fixed_otp},
    )
    assert r.status_code == 200, r.text
    return r.json()["data"]


# ---- 1. /me ----
async def test_me(client, fixed_otp):
    data = await _login(client, fixed_otp)
    r = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {data['access_token']}"},
    )
    assert r.status_code == 200
    assert r.json()["data"]["email"] == EMAIL


# ---- 2. /me 無 token ----
async def test_me_no_token(client):
    r = await client.get("/api/v1/auth/me")
    assert r.status_code == 401


# ---- 3. refresh 成功 ----
async def test_refresh(client, fixed_otp):
    data = await _login(client, fixed_otp)
    r = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": data["refresh_token"]},
    )
    assert r.status_code == 200
    new = r.json()["data"]
    assert new["refresh_token"] != data["refresh_token"]


# ---- 4. 重放舊 refresh → 全撤銷 ----
async def test_refresh_reuse_revokes(client, fixed_otp):
    data = await _login(client, fixed_otp)
    old = data["refresh_token"]

    r1 = await client.post("/api/v1/auth/refresh", json={"refresh_token": old})
    assert r1.status_code == 200
    new = r1.json()["data"]["refresh_token"]

    # 重放舊的
    r2 = await client.post("/api/v1/auth/refresh", json={"refresh_token": old})
    assert r2.status_code == 401
    assert r2.json()["error"]["code"] == "AUTH_REFRESH_REUSED"

    # 新的也應該失效
    r3 = await client.post("/api/v1/auth/refresh", json={"refresh_token": new})
    assert r3.status_code == 401


# ---- 5. logout 後 refresh 失效 ----
async def test_logout_revokes(client, fixed_otp):
    data = await _login(client, fixed_otp)
    r = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": data["refresh_token"]},
    )
    assert r.status_code == 200
    assert r.json()["data"]["message"] == "已登出"

    r = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": data["refresh_token"]},
    )
    assert r.status_code == 401


# ---- 6. 用 access token 去 refresh → 401 ----
async def test_refresh_with_access(client, fixed_otp):
    data = await _login(client, fixed_otp)
    r = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": data["access_token"]},
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "AUTH_TOKEN_INVALID"
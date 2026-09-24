"""Phase 1 Day 3：管理員登入。"""
import pytest

from tests.conftest import ADMIN_EMAIL, ADMIN_PASSWORD


async def test_admin_login_success(client, admin_user):
    r = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["success"] is True
    d = body["data"]
    assert d["access_token"]
    assert d["refresh_token"]
    assert d["token_type"] == "Bearer"
    assert d["admin"]["email"] == ADMIN_EMAIL
    assert d["admin"]["role"] == "admin"


async def test_admin_login_wrong_password(client, admin_user):
    r = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": ADMIN_EMAIL, "password": "wrongpassword"},
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "AUTH_INVALID_CREDENTIALS"


async def test_admin_login_unknown_email(client):
    r = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": "ghost@test.local", "password": "whatever123"},
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "AUTH_INVALID_CREDENTIALS"


async def test_admin_me(client, admin_user):
    r = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    token = r.json()["data"]["access_token"]

    r = await client.get(
        "/api/v1/admin/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.json()["data"]["email"] == ADMIN_EMAIL


async def test_admin_me_no_token(client):
    r = await client.get("/api/v1/admin/auth/me")
    assert r.status_code == 401


async def test_user_token_rejected_by_admin_endpoint(client, admin_user):
    """一般用戶的 access token 不能打 admin 端點。"""
    from tests.test_auth_token import _login as user_login
    from tests.test_auth_token import EMAIL as USER_EMAIL

    # 用 user 流程登入
    r = await client.post("/api/v1/auth/otp/request", json={"email": USER_EMAIL})
    assert r.status_code == 200
    dev_code = r.json()["data"]["dev_code"]
    r = await client.post(
        "/api/v1/auth/otp/verify",
        json={"email": USER_EMAIL, "otp": dev_code},
    )
    user_token = r.json()["data"]["access_token"]

    r = await client.get(
        "/api/v1/admin/auth/me",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "AUTH_TOKEN_INVALID"


async def test_admin_logout_revokes(client, admin_user):
    r = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    refresh = r.json()["data"]["refresh_token"]

    r = await client.post(
        "/api/v1/admin/auth/logout",
        json={"refresh_token": refresh},
    )
    assert r.status_code == 200
    assert r.json()["data"]["message"] == "已登出"

    # 撤銷後不能再 refresh
    r = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh},
    )
    assert r.status_code == 401


async def test_admin_login_lockout(client, admin_user):
    """連續 5 次錯密碼 → 鎖定。"""
    for _ in range(5):
        r = await client.post(
            "/api/v1/admin/auth/login",
            json={"email": ADMIN_EMAIL, "password": "wrongwrong"},
        )
        assert r.status_code == 401

    # 第 6 次正確密碼也被鎖
    r = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert r.status_code == 401
    assert "鎖定" in r.json()["error"]["message"]
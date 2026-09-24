"""Phase 1 Day 5：基因資料（同意 + 加密 + CRUD）。"""
import pytest
from cryptography.fernet import Fernet


EMAIL = "user@example.com"


@pytest.fixture
def fixed_otp(monkeypatch):
    import app.services.otp_service as svc
    monkeypatch.setattr(svc, "generate_otp_code", lambda length=6: "123456")
    return "123456"


@pytest.fixture(autouse=True)
def _fernet(monkeypatch):
    """測試用 Fernet key（不依賴 .env）。"""
    from app.core.config import settings
    monkeypatch.setattr(settings, "ENCRYPTION_KEY", Fernet.generate_key().decode())


async def _token(client, fixed_otp):
    await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    r = await client.post(
        "/api/v1/auth/otp/verify",
        json={"email": EMAIL, "otp": fixed_otp},
    )
    return r.json()["data"]["access_token"]


def _h(t: str) -> dict:
    return {"Authorization": f"Bearer {t}"}


async def _setup_profile_and_token(client, fixed_otp):
    token = await _token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/profile",
        json={"birth_date": "1985-06-15", "gender": "male"},
        headers=_h(token),
    )
    return token


async def _get_marker_id(client, token, code="BRCA1"):
    r = await client.get("/api/v1/app/health/genetic-markers", headers=_h(token))
    for m in r.json()["data"]:
        if m["marker_code"] == code:
            return m["id"]
    raise AssertionError(f"marker {code} not found")


# ---------- 同意 ----------

async def test_consent_requires_profile(client, fixed_otp):
    token = await _token(client, fixed_otp)
    r = await client.post(
        "/api/v1/app/health/consent",
        json={"consent": True},
        headers=_h(token),
    )
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "HEALTH_PROFILE_NOT_FOUND"


async def test_consent_success(client, fixed_otp):
    token = await _setup_profile_and_token(client, fixed_otp)
    r = await client.post(
        "/api/v1/app/health/consent",
        json={"consent": True},
        headers=_h(token),
    )
    assert r.status_code == 200
    assert r.json()["data"]["consent_genetic"] is True
    assert r.json()["data"]["consent_genetic_at"] is not None


async def test_consent_revoke(client, fixed_otp):
    token = await _setup_profile_and_token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/consent",
        json={"consent": True}, headers=_h(token),
    )
    r = await client.post(
        "/api/v1/app/health/consent",
        json={"consent": False}, headers=_h(token),
    )
    assert r.status_code == 200
    assert r.json()["data"]["consent_genetic"] is False
    assert r.json()["data"]["consent_genetic_at"] is None


# ---------- 點位清單 ----------

async def test_list_markers(client, fixed_otp):
    token = await _setup_profile_and_token(client, fixed_otp)
    r = await client.get("/api/v1/app/health/genetic-markers", headers=_h(token))
    assert r.status_code == 200
    codes = [m["marker_code"] for m in r.json()["data"]]
    assert "BRCA1" in codes
    assert "APOE" in codes


async def test_list_markers_requires_auth(client):
    r = await client.get("/api/v1/app/health/genetic-markers")
    assert r.status_code == 401


# ---------- 新增檢測：同意檢查 ----------

async def test_add_without_consent_403(client, fixed_otp):
    token = await _setup_profile_and_token(client, fixed_otp)
    marker_id = await _get_marker_id(client, token)
    r = await client.post(
        "/api/v1/app/health/genetic-tests",
        json={"marker_id": marker_id, "result": "high"},
        headers=_h(token),
    )
    assert r.status_code == 403
    assert r.json()["error"]["code"] == "HEALTH_CONSENT_REQUIRED"


# ---------- 新增檢測：成功 + 加密 ----------

async def test_add_success_and_encrypt(client, fixed_otp, db):
    token = await _setup_profile_and_token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/consent",
        json={"consent": True}, headers=_h(token),
    )
    marker_id = await _get_marker_id(client, token)

    plaintext = "ATCG-ATCG-SECRET"
    r = await client.post(
        "/api/v1/app/health/genetic-tests",
        json={
            "marker_id": marker_id,
            "result": "high",
            "raw_data": plaintext,
            "notes": "初次檢測",
        },
        headers=_h(token),
    )
    assert r.status_code == 200, r.text
    d = r.json()["data"]
    assert d["marker_code"] == "BRCA1"
    assert d["result"] == "high"
    assert d["risk_level_computed"] == 3.0
    assert d["has_raw_data"] is True

    # 驗證 DB 裡是密文
    from sqlalchemy import select
    from app.models.health import UserGeneticTest
    q = await db.execute(select(UserGeneticTest).where(UserGeneticTest.marker_id == marker_id))
    row = q.scalar_one()
    assert row.raw_data_encrypted is not None
    assert plaintext not in row.raw_data_encrypted
    from app.core.encryption import decrypt
    assert decrypt(row.raw_data_encrypted) == plaintext


# ---------- 完成度連動 ----------

async def test_add_test_updates_completion(client, fixed_otp):
    token = await _setup_profile_and_token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/consent",
        json={"consent": True}, headers=_h(token),
    )
    marker_id = await _get_marker_id(client, token)

    await client.post(
        "/api/v1/app/health/genetic-tests",
        json={"marker_id": marker_id, "result": "high"},
        headers=_h(token),
    )
    r = await client.get("/api/v1/app/health/completion", headers=_h(token))
    assert r.json()["data"]["completion_rate"] == 90.0


# ---------- 重複 ----------

async def test_add_duplicate_marker(client, fixed_otp):
    token = await _setup_profile_and_token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/consent",
        json={"consent": True}, headers=_h(token),
    )
    marker_id = await _get_marker_id(client, token)

    await client.post(
        "/api/v1/app/health/genetic-tests",
        json={"marker_id": marker_id, "result": "high"},
        headers=_h(token),
    )
    r = await client.post(
        "/api/v1/app/health/genetic-tests",
        json={"marker_id": marker_id, "result": "low"},
        headers=_h(token),
    )
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "HEALTH_INVALID_INPUT"


# ---------- 列表 ----------

async def test_list_tests(client, fixed_otp):
    token = await _setup_profile_and_token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/consent",
        json={"consent": True}, headers=_h(token),
    )
    mid1 = await _get_marker_id(client, token, "BRCA1")
    mid2 = await _get_marker_id(client, token, "APOE")

    await client.post(
        "/api/v1/app/health/genetic-tests",
        json={"marker_id": mid1, "result": "high"}, headers=_h(token),
    )
    await client.post(
        "/api/v1/app/health/genetic-tests",
        json={"marker_id": mid2, "result": "medium"}, headers=_h(token),
    )

    r = await client.get("/api/v1/app/health/genetic-tests", headers=_h(token))
    assert r.status_code == 200
    assert len(r.json()["data"]) == 2


# ---------- 刪除 ----------

async def test_delete_test_and_completion(client, fixed_otp):
    token = await _setup_profile_and_token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/consent",
        json={"consent": True}, headers=_h(token),
    )
    mid = await _get_marker_id(client, token)
    r = await client.post(
        "/api/v1/app/health/genetic-tests",
        json={"marker_id": mid, "result": "high"}, headers=_h(token),
    )
    tid = r.json()["data"]["id"]

    r = await client.delete(
        f"/api/v1/app/health/genetic-tests/{tid}", headers=_h(token),
    )
    assert r.status_code == 200
    assert r.json()["data"]["message"] == "已刪除"

    r = await client.get("/api/v1/app/health/completion", headers=_h(token))
    assert r.json()["data"]["completion_rate"] == 80.0

    r = await client.get("/api/v1/app/health/genetic-tests", headers=_h(token))
    assert r.json()["data"] == []


async def test_delete_other_users_test(client, fixed_otp, db):
    """A 用戶不能刪 B 用戶的檢測。"""
    token_a = await _setup_profile_and_token(client, fixed_otp)
    await client.post("/api/v1/app/health/consent",
                      json={"consent": True}, headers=_h(token_a))
    mid = await _get_marker_id(client, token_a)
    r = await client.post(
        "/api/v1/app/health/genetic-tests",
        json={"marker_id": mid, "result": "high"}, headers=_h(token_a),
    )
    tid = r.json()["data"]["id"]

    await client.post("/api/v1/auth/otp/request", json={"email": "b@example.com"})
    r = await client.post(
        "/api/v1/auth/otp/verify",
        json={"email": "b@example.com", "otp": "123456"},
    )
    token_b = r.json()["data"]["access_token"]

    r = await client.delete(
        f"/api/v1/app/health/genetic-tests/{tid}", headers=_h(token_b),
    )
    assert r.status_code == 404


# ---------- 驗證 ----------

async def test_invalid_result(client, fixed_otp):
    token = await _setup_profile_and_token(client, fixed_otp)
    await client.post("/api/v1/app/health/consent",
                      json={"consent": True}, headers=_h(token))
    mid = await _get_marker_id(client, token)
    r = await client.post(
        "/api/v1/app/health/genetic-tests",
        json={"marker_id": mid, "result": "maybe"},
        headers=_h(token),
    )
    assert r.status_code == 422


async def test_marker_not_found(client, fixed_otp):
    token = await _setup_profile_and_token(client, fixed_otp)
    await client.post("/api/v1/app/health/consent",
                      json={"consent": True}, headers=_h(token))
    r = await client.post(
        "/api/v1/app/health/genetic-tests",
        json={"marker_id": "00000000-0000-0000-0000-000000000000", "result": "high"},
        headers=_h(token),
    )
    assert r.status_code == 404
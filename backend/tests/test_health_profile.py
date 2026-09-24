"""Phase 1 Day 4：健康檔案 CRUD。"""
import pytest


EMAIL = "user@example.com"


@pytest.fixture
def fixed_otp(monkeypatch):
    import app.services.otp_service as svc
    monkeypatch.setattr(svc, "generate_otp_code", lambda length=6: "123456")
    return "123456"


async def _token(client, fixed_otp):
    await client.post("/api/v1/auth/otp/request", json={"email": EMAIL})
    r = await client.post(
        "/api/v1/auth/otp/verify",
        json={"email": EMAIL, "otp": fixed_otp},
    )
    return r.json()["data"]["access_token"]


def _h(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ---------- 建立 ----------

async def test_create_minimum_80(client, fixed_otp):
    token = await _token(client, fixed_otp)
    r = await client.post(
        "/api/v1/app/health/profile",
        json={"birth_date": "1985-06-15", "gender": "male"},
        headers=_h(token),
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["success"] is True
    assert body["data"]["completion_rate"] == 80.0
    assert body["data"]["message"] == "健康檔案已建立"


async def test_create_with_family_90(client, fixed_otp):
    token = await _token(client, fixed_otp)
    r = await client.post(
        "/api/v1/app/health/profile",
        json={
            "birth_date": "1985-06-15",
            "gender": "male",
            "family_history": {"cardiovascular": True, "diabetes": False},
        },
        headers=_h(token),
    )
    assert r.status_code == 200
    assert r.json()["data"]["completion_rate"] == 90.0


async def test_create_full_100(client, fixed_otp):
    token = await _token(client, fixed_otp)
    r = await client.post(
        "/api/v1/app/health/profile",
        json={
            "birth_date": "1985-06-15",
            "gender": "female",
            "family_history": {"cardiovascular": True},
            "has_genetic_test": True,
        },
        headers=_h(token),
    )
    assert r.status_code == 200
    assert r.json()["data"]["completion_rate"] == 100.0


async def test_create_duplicate_409(client, fixed_otp):
    token = await _token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/profile",
        json={"birth_date": "1985-06-15", "gender": "male"},
        headers=_h(token),
    )
    r = await client.post(
        "/api/v1/app/health/profile",
        json={"birth_date": "1985-06-15", "gender": "male"},
        headers=_h(token),
    )
    assert r.status_code == 409
    assert r.json()["error"]["code"] == "HEALTH_PROFILE_EXISTS"


# ---------- 查詢 ----------

async def test_get(client, fixed_otp):
    token = await _token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/profile",
        json={"birth_date": "1985-06-15", "gender": "male"},
        headers=_h(token),
    )
    r = await client.get("/api/v1/app/health/profile", headers=_h(token))
    assert r.status_code == 200
    assert r.json()["data"]["birth_date"] == "1985-06-15"
    assert r.json()["data"]["gender"] == "male"


async def test_get_not_found(client, fixed_otp):
    token = await _token(client, fixed_otp)
    r = await client.get("/api/v1/app/health/profile", headers=_h(token))
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "HEALTH_PROFILE_NOT_FOUND"


# ---------- 更新 ----------

async def test_update(client, fixed_otp):
    token = await _token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/profile",
        json={"birth_date": "1985-06-15", "gender": "male"},
        headers=_h(token),
    )
    r = await client.put(
        "/api/v1/app/health/profile",
        json={"family_history": {"cancer": True}, "has_genetic_test": True},
        headers=_h(token),
    )
    assert r.status_code == 200
    assert r.json()["data"]["completion_rate"] == 100.0
    assert r.json()["data"]["message"] == "健康檔案已更新"


async def test_update_partial(client, fixed_otp):
    """只改 gender，其他保留。"""
    token = await _token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/profile",
        json={
            "birth_date": "1985-06-15",
            "gender": "male",
            "family_history": {"x": True},
        },
        headers=_h(token),
    )
    r = await client.put(
        "/api/v1/app/health/profile",
        json={"gender": "female"},
        headers=_h(token),
    )
    assert r.status_code == 200
    d = r.json()["data"]
    assert d["gender"] == "female"
    assert d["birth_date"] == "1985-06-15"
    assert d["family_history"] == {"x": True}    # 沒被清掉
    assert d["completion_rate"] == 90.0


async def test_update_not_found(client, fixed_otp):
    token = await _token(client, fixed_otp)
    r = await client.put(
        "/api/v1/app/health/profile",
        json={"family_history": {"x": True}},
        headers=_h(token),
    )
    assert r.status_code == 404


# ---------- 完成度 ----------

async def test_completion_80(client, fixed_otp):
    token = await _token(client, fixed_otp)
    await client.post(
        "/api/v1/app/health/profile",
        json={"birth_date": "1985-06-15", "gender": "male"},
        headers=_h(token),
    )
    r = await client.get("/api/v1/app/health/completion", headers=_h(token))
    assert r.status_code == 200
    d = r.json()["data"]
    assert d["completion_rate"] == 80.0
    assert d["precision_level"] == "medium"
    assert "family_history" in d["missing_fields"]


async def test_completion_no_profile(client, fixed_otp):
    token = await _token(client, fixed_otp)
    r = await client.get("/api/v1/app/health/completion", headers=_h(token))
    assert r.status_code == 200
    assert r.json()["data"]["completion_rate"] == 0.0
    assert r.json()["data"]["precision_level"] == "none"


# ---------- 驗證 ----------

async def test_invalid_gender(client, fixed_otp):
    token = await _token(client, fixed_otp)
    r = await client.post(
        "/api/v1/app/health/profile",
        json={"birth_date": "1985-06-15", "gender": "unknown"},
        headers=_h(token),
    )
    assert r.status_code == 422


async def test_future_birth_date(client, fixed_otp):
    token = await _token(client, fixed_otp)
    r = await client.post(
        "/api/v1/app/health/profile",
        json={"birth_date": "2100-01-01", "gender": "male"},
        headers=_h(token),
    )
    assert r.status_code == 422


async def test_no_token(client):
    r = await client.get("/api/v1/app/health/profile")
    assert r.status_code == 401
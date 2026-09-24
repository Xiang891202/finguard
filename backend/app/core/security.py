"""安全工具：OTP hash + JWT 編碼 / 解碼。"""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.core.config import settings


# ==================== OTP ====================

def generate_otp_code(length: int = 6) -> str:
    """產生純數字 OTP（允許前導零）。"""
    return f"{secrets.randbelow(10 ** length):0{length}d}"


def hash_otp(code: str, pepper: str, salt: str | None = None) -> str:
    """HMAC-SHA256(pepper, salt + code) → 'salt$digest'。"""
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hmac.new(
        pepper.encode("utf-8"),
        (salt + code).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{salt}${digest}"


def verify_otp_hash(code: str, stored: str, pepper: str) -> bool:
    """常數時間比對。"""
    try:
        salt, _ = stored.split("$", 1)
    except ValueError:
        return False
    candidate = hash_otp(code, pepper, salt)
    return hmac.compare_digest(candidate, stored)


def sha256_hex(s: str) -> str:
    """用於 refresh token 的 hash 儲存。"""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ==================== JWT ====================

def make_jti() -> str:
    return secrets.token_urlsafe(16)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def encode_access_token(sub: str, user_type: str = "user") -> tuple[str, str, datetime]:
    """回傳 (token, jti, expires_at)。"""
    jti = make_jti()
    now = _now()
    exp = now + timedelta(seconds=settings.JWT_ACCESS_EXPIRY)
    payload = {
        "sub": sub,
        "jti": jti,
        "type": "access",
        "user_type": user_type,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "iss": settings.JWT_ISSUER,
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, jti, exp


def encode_refresh_token(
    sub: str, family_id: str, user_type: str = "user"
) -> tuple[str, str, datetime]:
    """回傳 (token, jti, expires_at)。"""
    jti = make_jti()
    now = _now()
    exp = now + timedelta(seconds=settings.JWT_REFRESH_EXPIRY)
    payload = {
        "sub": sub,
        "jti": jti,
        "type": "refresh",
        "family": family_id,
        "user_type": user_type,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "iss": settings.JWT_ISSUER,
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, jti, exp


def decode_token(token: str) -> dict[str, Any]:
    """解碼並驗證。失敗丟 jose.JWTError。"""
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
        issuer=settings.JWT_ISSUER,
    )


# ==================== Password (bcrypt) ====================

import bcrypt


def hash_password(password: str) -> str:
    """bcrypt 雜湊密碼（cost=12）。"""
    # bcrypt 上限 72 bytes，超過需截斷
    pw_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pw_bytes, bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """常數時間比對 bcrypt 雜湊。"""
    try:
        pw_bytes = password.encode("utf-8")[:72]
        return bcrypt.checkpw(pw_bytes, hashed.encode("utf-8"))
    except Exception:
        return False
"""FastAPI 共用依賴。"""
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthTokenInvalid, AuthTokenRevoked
from app.core.redis import get_redis
from app.core.security import decode_token
from app.db.session import get_async_db
from app.services.token_service import TokenService


_bearer = HTTPBearer(auto_error=False)


async def _decode_and_check(
    credentials: HTTPAuthorizationCredentials | None,
    redis: Redis,
    db: AsyncSession,
    expected_type: str,
) -> dict:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthTokenInvalid("缺少 Bearer token")

    try:
        payload = decode_token(credentials.credentials)
    except Exception:
        raise AuthTokenInvalid("Token 無效或已過期")

    if payload.get("type") != "access":
        raise AuthTokenInvalid("不是 access token")

    user_type = payload.get("user_type", "user")
    if user_type != expected_type:
        raise AuthTokenInvalid("Token 類型不符")

    svc = TokenService(redis, db)
    if await svc.is_access_revoked(payload["jti"]):
        raise AuthTokenRevoked("Token 已撤銷")

    return payload


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_async_db),
) -> str:
    payload = await _decode_and_check(credentials, redis, db, "user")
    return payload["sub"]


async def get_current_admin_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_async_db),
) -> str:
    payload = await _decode_and_check(credentials, redis, db, "admin")
    return payload["sub"]
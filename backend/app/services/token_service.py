"""JWT 簽發、Refresh Rotation、Revoke（支援 user / admin）。"""
import secrets
from datetime import datetime, timezone

from redis.asyncio import Redis
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    AuthRefreshReused,
    AuthTokenInvalid,
    AuthTokenRevoked,
)
from app.core.logging import logger
from app.core.security import (
    decode_token,
    encode_access_token,
    encode_refresh_token,
    sha256_hex,
)
from app.models.user import AdminUser, RefreshToken, User


def _naive_utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class TokenService:
    def __init__(self, redis: Redis, db: AsyncSession) -> None:
        self.redis = redis
        self.db = db

    # ---------- keys ----------
    @staticmethod
    def _k_denylist(jti: str) -> str:
        return f"jwt:denylist:{jti}"

    # ==================== 用戶 ====================

    async def _get_or_create_user(self, email: str) -> tuple[User, bool]:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user:
            return user, False

        user = User(
            email=email,
            display_name=email.split("@")[0],
            role="user",
            status="active",
            tenant_id="00000000-0000-0000-0000-000000000001",
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user, True

    async def issue_for_email(
        self,
        email: str,
        *,
        user_agent: str | None = None,
        ip: str | None = None,
    ) -> dict:
        user, is_new = await self._get_or_create_user(email)
        user.last_login_at = _naive_utcnow()
        await self.db.commit()

        family_id = secrets.token_urlsafe(16)
        pair = await self._issue_pair(user.id, "user", family_id, user_agent, ip)
        pair["user"] = {
            "id": user.id,
            "email": user.email,
            "display_name": user.display_name,
            "is_new_user": is_new,
            "health_profile_completed": False,   # Day 4 補
        }
        return pair

    # ==================== 管理員 ====================

    async def issue_for_admin(
        self,
        admin: AdminUser,
        *,
        user_agent: str | None = None,
        ip: str | None = None,
    ) -> dict:
        family_id = secrets.token_urlsafe(16)
        pair = await self._issue_pair(admin.id, "admin", family_id, user_agent, ip)
        pair["admin"] = {
            "id": admin.id,
            "email": admin.email,
            "display_name": admin.display_name,
            "role": admin.role,
        }
        return pair

    # ==================== 共用 ====================

    async def _issue_pair(
        self,
        user_id: str,
        user_type: str,
        family_id: str,
        user_agent: str | None,
        ip: str | None,
    ) -> dict:
        access_token, _, _ = encode_access_token(user_id, user_type)
        refresh_token, _, refresh_exp = encode_refresh_token(
            user_id, family_id, user_type
        )

        row = RefreshToken(
            user_id=user_id,
            user_type=user_type,
            token_hash=sha256_hex(refresh_token),
            expires_at=refresh_exp.replace(tzinfo=None),
            user_agent=user_agent,
            ip_address=ip,
        )
        self.db.add(row)
        await self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": settings.JWT_ACCESS_EXPIRY,
        }

    async def refresh(
        self,
        refresh_token: str,
        *,
        user_agent: str | None = None,
        ip: str | None = None,
    ) -> dict:
        try:
            payload = decode_token(refresh_token)
        except Exception as e:
            raise AuthTokenInvalid("Refresh token 無效或已過期") from e

        if payload.get("type") != "refresh":
            raise AuthTokenInvalid("不是 refresh token")

        user_id = payload["sub"]
        user_type = payload.get("user_type", "user")
        family_id = payload.get("family") or secrets.token_urlsafe(16)
        token_hash = sha256_hex(refresh_token)

        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        row = result.scalar_one_or_none()

        if row is None or row.revoked_at is not None:
            await self._revoke_all_tokens(user_id)
            logger.warning("🚨 Refresh token 重放 user=%s type=%s", user_id, user_type)
            raise AuthRefreshReused("偵測到 token 重放，所有 session 已撤銷")

        if row.expires_at < _naive_utcnow():
            raise AuthTokenRevoked("Refresh token 已過期")

        # 檢查實體存在
        if user_type == "admin":
            entity = await self.db.get(AdminUser, user_id)
        else:
            entity = await self.db.get(User, user_id)
        if entity is None:
            raise AuthTokenInvalid("帳號不存在")

        row.revoked_at = _naive_utcnow()
        await self.db.commit()

        return await self._issue_pair(
            user_id, user_type, family_id,
            user_agent or row.user_agent, ip or row.ip_address,
        )

    async def revoke(self, refresh_token: str) -> None:
        try:
            payload = decode_token(refresh_token)
        except Exception:
            return

        if payload.get("type") != "refresh":
            return

        token_hash = sha256_hex(refresh_token)
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        row = result.scalar_one_or_none()
        if row and row.revoked_at is None:
            row.revoked_at = _naive_utcnow()
            await self.db.commit()

        await self._revoke_all_tokens(payload["sub"])

    async def _revoke_all_tokens(self, user_id: str) -> None:
        await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))
            .values(revoked_at=_naive_utcnow())
        )
        await self.db.commit()

    # ---------- Access 黑名單 ----------
    async def revoke_access(self, access_token: str) -> None:
        try:
            payload = decode_token(access_token)
        except Exception:
            return
        if payload.get("type") != "access":
            return
        jti = payload.get("jti")
        exp = payload.get("exp")
        if not jti or not exp:
            return
        ttl = max(int(exp - datetime.now(timezone.utc).timestamp()), 1)
        await self.redis.setex(self._k_denylist(jti), ttl, "1")

    async def is_access_revoked(self, jti: str) -> bool:
        return bool(await self.redis.exists(self._k_denylist(jti)))
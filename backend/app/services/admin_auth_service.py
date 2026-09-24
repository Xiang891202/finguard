"""管理員認證：bcrypt 密碼驗證 + 失敗鎖定。"""
from datetime import datetime, timezone

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthInvalidCredentials, AuthTokenRevoked
from app.core.logging import logger
from app.core.security import verify_password
from app.models.user import AdminUser


_FAIL_PREFIX = "admin:login_fail"
_LOCK_SECONDS = 900     # 15 分鐘
_MAX_FAILS = 5


def _naive_utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class AdminAuthService:
    def __init__(self, redis: Redis, db: AsyncSession) -> None:
        self.redis = redis
        self.db = db

    def _fail_key(self, email: str) -> str:
        return f"{_FAIL_PREFIX}:{email}"

    async def _check_lock(self, email: str) -> None:
        key = self._fail_key(email)
        n = await self.redis.get(key)
        if n and int(n) >= _MAX_FAILS:
            ttl = await self.redis.ttl(key)
            raise AuthTokenRevoked(
                f"帳號暫時鎖定，請於 {max(ttl, 1)} 秒後再試"
            )

    async def _record_fail(self, email: str) -> None:
        key = self._fail_key(email)
        n = await self.redis.incr(key)
        if n == 1:
            await self.redis.expire(key, _LOCK_SECONDS)

    async def _clear_fail(self, email: str) -> None:
        await self.redis.delete(self._fail_key(email))

    async def login(self, email: str, password: str) -> AdminUser:
        await self._check_lock(email)

        result = await self.db.execute(
            select(AdminUser).where(AdminUser.email == email)
        )
        admin = result.scalar_one_or_none()

        # 常數時間防列舉：沒找到也跑一次 verify
        dummy_hash = "$2b$12$" + "x" * 53
        hashed = admin.password_hash if admin else dummy_hash
        ok = verify_password(password, hashed)

        if not admin or not ok or admin.status != "active":
            await self._record_fail(email)
            logger.warning("管理員登入失敗 email=%s", email)
            raise AuthInvalidCredentials("Email 或密碼錯誤")

        await self._clear_fail(email)
        admin.last_login_at = _naive_utcnow()
        await self.db.commit()
        logger.info("管理員登入成功 email=%s", email)
        return admin

    async def get_by_id(self, admin_id: str) -> AdminUser | None:
        return await self.db.get(AdminUser, admin_id)
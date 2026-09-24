"""OTP 服務：Redis 主儲存 + DB 審計。"""
from datetime import datetime, timedelta, timezone

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    AuthInvalidOTP,
    AuthIPRateLimited,
    AuthOTPDailyLimit,
    AuthOTPExpired,
    AuthOTPMaxAttempts,
    AuthOTPRateLimited,
)
from app.core.logging import logger
from app.core.security import generate_otp_code, hash_otp, verify_otp_hash

# 依你的 ORM 模型實際路徑調整
from app.models.user import OtpToken


class OTPService:
    def __init__(self, redis: Redis, db: AsyncSession) -> None:
        self.redis = redis
        self.db = db

    # ---------- keys ----------
    @staticmethod
    def _k_code(email: str) -> str:
        return f"otp:code:{email}"

    @staticmethod
    def _k_throttle(email: str) -> str:
        return f"otp:throttle:{email}"

    @staticmethod
    def _k_daily(email: str) -> str:
        d = datetime.now(timezone.utc).strftime("%Y%m%d")
        return f"otp:daily:{d}:{email}"

    @staticmethod
    def _k_attempts(email: str) -> str:
        return f"otp:attempts:{email}"

    # ---------- IP rate ----------
    async def _check_ip(self, ip: str | None) -> None:
        if not ip:
            return
        now = datetime.now(timezone.utc)

        m_key = f"otp:ip:m:{ip}:{now.strftime('%Y%m%d%H%M')}"
        c = await self.redis.incr(m_key)
        if c == 1:
            await self.redis.expire(m_key, 60)
        if c > settings.IP_RATE_PER_MINUTE:
            raise AuthIPRateLimited("IP 請求過於頻繁，請稍後再試")

        d_key = f"otp:ip:d:{ip}:{now.strftime('%Y%m%d')}"
        c = await self.redis.incr(d_key)
        if c == 1:
            await self.redis.expire(d_key, 86400)
        if c > settings.IP_RATE_PER_DAY:
            raise AuthIPRateLimited("IP 已達每日上限")

    # ---------- request ----------
    async def request_otp(
        self, email: str, *, ip: str | None = None
    ) -> dict:
        # 1) IP 限流
        await self._check_ip(ip)

        # 2) 60 秒節流
        throttle_key = self._k_throttle(email)
        ttl = await self.redis.ttl(throttle_key)
        if ttl and ttl > 0:
            raise AuthOTPRateLimited(f"請於 {ttl} 秒後再試")

        # 3) 每日上限（先 incr 再判斷）
        daily_key = self._k_daily(email)
        c = await self.redis.incr(daily_key)
        if c == 1:
            await self.redis.expire(daily_key, 86400)
        if c > settings.OTP_DAILY_LIMIT:
            raise AuthOTPDailyLimit(f"已達每日上限（{settings.OTP_DAILY_LIMIT} 次）")

        # 4) 產碼 + hash
        code = generate_otp_code()
        hashed = hash_otp(code, settings.OTP_PEPPER)

        # 5) 存 Redis（主儲存）
        await self.redis.setex(
            self._k_code(email), settings.OTP_EXPIRY_SECONDS, hashed
        )
        await self.redis.delete(self._k_attempts(email))

        # 6) 設節流
        if settings.OTP_RESEND_INTERVAL > 0:
            await self.redis.setex(throttle_key, settings.OTP_RESEND_INTERVAL, "1")

        # 7) DB 審計
        db_row = OtpToken(
            email=email,
            otp_hash=hashed,
            purpose="login",
            max_attempts=settings.OTP_MAX_ATTEMPTS,
            expires_at=datetime.now(timezone.utc).replace(tzinfo=None)
            + timedelta(seconds=settings.OTP_EXPIRY_SECONDS),
            ip_address=ip,
        )
        self.db.add(db_row)
        await self.db.commit()

        # 8) 開發階段：log（不在此處寄信，改由 API 層丟背景任務）
        if settings.DEBUG:
            logger.warning("[OTP-DEV] email=%s code=%s", email, code)

        return (
            {
                "message": "驗證碼已寄出",
                "expires_in": settings.OTP_EXPIRY_SECONDS,
                "dev_code": code if settings.DEBUG else None,
            },
            code,   # 回傳明文 code 給 API 層丟背景任務
        )

    # ---------- verify ----------
    async def verify_otp(self, email: str, code: str) -> None:
        """驗證成功即銷毀 OTP。失敗拋對應例外。"""
        code_key = self._k_code(email)
        stored = await self.redis.get(code_key)
        if not stored:
            raise AuthOTPExpired("驗證碼不存在或已過期，請重新申請")

        # 嘗試次數 +1
        attempts_key = self._k_attempts(email)
        n = await self.redis.incr(attempts_key)
        if n == 1:
            await self.redis.expire(attempts_key, settings.OTP_EXPIRY_SECONDS)

        if n > settings.OTP_MAX_ATTEMPTS:
            await self.redis.delete(code_key)
            raise AuthOTPMaxAttempts("嘗試次數過多，請重新申請驗證碼")

        if not verify_otp_hash(code, stored, settings.OTP_PEPPER):
            raise AuthInvalidOTP("驗證碼錯誤")

        # 成功：一次性刪除
        await self.redis.delete(code_key)
        await self.redis.delete(attempts_key)

        # DB：標記為 used（審計）
        result = await self.db.execute(
            select(OtpToken)
            .where(OtpToken.email == email, OtpToken.used_at.is_(None))
            .order_by(OtpToken.created_at.desc())
            .limit(1)
        )
        row = result.scalar_one_or_none()
        if row:
            row.used_at = datetime.now(timezone.utc).replace(tzinfo=None)
            await self.db.commit()
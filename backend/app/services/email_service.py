"""Email 服務（OTP 寄送）。"""
from email.message import EmailMessage

import aiosmtplib

from app.core.config import settings
from app.core.logging import logger


_OTP_TEMPLATE = """您好，

您的 FinGuard 驗證碼是：

    {code}

此驗證碼 5 分鐘內有效，請勿分享給任何人。

若您並未請求此驗證碼，請忽略此郵件，您的帳號不會被登入。

--
FinGuard 財安 · 個人財務安全儀表板
"""


class EmailService:
    @staticmethod
    async def send_otp(email: str, code: str) -> bool:
        """寄送 OTP 驗證碼。回傳是否成功。"""
        if settings.TESTING:
            logger.debug("[TEST] 跳過寄信 email=%s code=%s", email, code)
            return False

        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            logger.warning("SMTP 未設定，無法寄送 OTP 至 %s", email)
            return False

        msg = EmailMessage()
        msg["From"] = settings.SMTP_FROM
        msg["To"] = email
        msg["Subject"] = f"[FinGuard] 您的驗證碼：{code}"
        msg.set_content(_OTP_TEMPLATE.format(code=code))

        try:
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=True,
                timeout=15,
            )
            logger.info("OTP 郵件已寄出至 %s", email)
            return True
        except Exception as e:
            logger.exception("OTP 郵件寄送失敗：%s", e)
            return False
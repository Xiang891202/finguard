"""Auth 相關 Pydantic schema。"""
import re
from pydantic import BaseModel, Field, field_validator

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _norm_email(v: str) -> str:
    v = v.strip().lower()
    if not _EMAIL_RE.match(v):
        raise ValueError("email 格式錯誤")
    return v


# ===== OTP =====

class OTPRequestIn(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)

    _v = field_validator("email")(classmethod(lambda cls, v: _norm_email(v)))


class OTPRequestData(BaseModel):
    message: str = "驗證碼已寄出"
    expires_in: int
    dev_code: str | None = None   # 僅 DEBUG 模式


class OTPVerifyIn(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    otp: str = Field(..., min_length=4, max_length=10)

    _v = field_validator("email")(classmethod(lambda cls, v: _norm_email(v)))


# ===== Token / User =====

class UserOut(BaseModel):
    id: str
    email: str
    display_name: str | None = None
    is_new_user: bool = False
    health_profile_completed: bool = False


class TokenPairData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: UserOut | None = None


class RefreshIn(BaseModel):
    refresh_token: str = Field(..., min_length=10)


class LogoutIn(BaseModel):
    refresh_token: str = Field(..., min_length=10)


# ===== /me =====

class MeData(BaseModel):
    id: str
    email: str
    display_name: str | None = None
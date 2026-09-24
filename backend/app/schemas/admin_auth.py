"""管理員認證 schema。"""
import re
from pydantic import BaseModel, Field, field_validator

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _norm_email(v: str) -> str:
    v = v.strip().lower()
    if not _EMAIL_RE.match(v):
        raise ValueError("email 格式錯誤")
    return v


class AdminLoginIn(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=6, max_length=72)

    _v = field_validator("email")(classmethod(lambda cls, v: _norm_email(v)))


class AdminOut(BaseModel):
    id: str
    email: str
    display_name: str | None = None
    role: str


class AdminTokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    admin: AdminOut


class AdminLogoutIn(BaseModel):
    refresh_token: str = Field(..., min_length=10)


class AdminMeOut(BaseModel):
    id: str
    email: str
    display_name: str | None = None
    role: str
"""Fernet 對稱式加密。用於基因原始資料（規劃書 10.3）。"""
from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings
from app.core.exceptions import ApiException


class EncryptionError(ApiException):
    status_code = 500
    code = "SYSTEM_ENCRYPTION_FAILED"


def _fernet() -> Fernet:
    key = settings.ENCRYPTION_KEY
    if not key or key.startswith("change-this"):
        raise EncryptionError("ENCRYPTION_KEY 未正確設定")
    try:
        return Fernet(key.encode() if isinstance(key, str) else key)
    except Exception as e:
        raise EncryptionError("ENCRYPTION_KEY 格式錯誤（需 44 字元 base64）") from e


def encrypt(plaintext: str) -> str:
    """明文 → Fernet token（str）。"""
    return _fernet().encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt(token: str) -> str:
    """Fernet token → 明文。"""
    try:
        return _fernet().decrypt(token.encode("utf-8")).decode("utf-8")
    except InvalidToken as e:
        raise EncryptionError("解密失敗") from e
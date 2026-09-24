"""統一例外體系。所有業務錯誤都帶 code + message + status_code。"""
from typing import Any


class ApiException(Exception):
    """業務例外基底。"""
    status_code: int = 400
    code: str = "BAD_REQUEST"

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.code = code or self.code
        self.details = details or {}
        super().__init__(message)


# ========== AUTH 系列（對齊規劃書 6.4 / API 規格 17）==========

class AuthError(ApiException):
    status_code = 401
    code = "AUTH_ERROR"


class AuthInvalidOTP(AuthError):
    status_code = 400
    code = "AUTH_INVALID_OTP"


class AuthOTPExpired(AuthError):
    status_code = 400
    code = "AUTH_OTP_EXPIRED"


class AuthOTPRateLimited(AuthError):
    status_code = 429
    code = "AUTH_OTP_RATE_LIMITED"


class AuthOTPDailyLimit(AuthError):
    status_code = 429
    code = "AUTH_OTP_DAILY_LIMIT"


class AuthOTPMaxAttempts(AuthError):
    status_code = 429
    code = "AUTH_OTP_MAX_ATTEMPTS"


class AuthIPRateLimited(AuthError):
    status_code = 429
    code = "AUTH_IP_RATE_LIMITED"


class AuthInvalidIdentifier(ApiException):
    status_code = 422
    code = "AUTH_INVALID_IDENTIFIER"


class AuthTokenInvalid(AuthError):
    code = "AUTH_TOKEN_INVALID"


class AuthTokenRevoked(AuthError):
    code = "AUTH_TOKEN_REVOKED"


class AuthRefreshReused(AuthError):
    code = "AUTH_REFRESH_REUSED"


class AuthVerificationRequired(AuthError):
    code = "AUTH_VERIFICATION_REQUIRED"


class AuthInvalidCredentials(AuthError):
    code = "AUTH_INVALID_CREDENTIALS"


# ========== 通用 ==========

class NotFound(ApiException):
    status_code = 404
    code = "NOT_FOUND"


class BadRequest(ApiException):
    status_code = 400
    code = "BAD_REQUEST"

# ========== HEALTH 系列 ==========

class HealthProfileExists(ApiException):
    status_code = 409
    code = "HEALTH_PROFILE_EXISTS"


class HealthProfileNotFound(ApiException):
    status_code = 404
    code = "HEALTH_PROFILE_NOT_FOUND"


class HealthInvalidInput(ApiException):
    status_code = 422
    code = "HEALTH_INVALID_INPUT"


class HealthConsentRequired(ApiException):
    status_code = 403
    code = "HEALTH_CONSENT_REQUIRED"

class AuthEmailSendFailed(ApiException):
    status_code = 503
    code = "AUTH_EMAIL_SEND_FAILED"
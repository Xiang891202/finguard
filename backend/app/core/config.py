from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # 環境
    ENV: str = "development"
    DEBUG: bool = True

    # 資料庫
    DATABASE_URL: str = "postgresql://finguard:dev_password_change_me@localhost:5432/finguard"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # === OTP（對齊規劃書 6.6）===
    OTP_EXPIRY_SECONDS: int = 300      # 5 分鐘
    OTP_MAX_ATTEMPTS: int = 3          # 嘗試次數
    OTP_RESEND_INTERVAL: int = 60      # 60 秒節流
    OTP_DAILY_LIMIT: int = 10          # 每日上限
    OTP_PEPPER: str = "dev-pepper-change-in-prod"

    # === IP 限流（對齊規劃書 6.6）===
    IP_RATE_PER_MINUTE: int = 5
    IP_RATE_PER_DAY: int = 50

    # === JWT ===
    JWT_SECRET: str = "change-this-to-a-random-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_ISSUER: str = "finguard"
    JWT_ACCESS_EXPIRY: int = 900       # 15 分鐘
    JWT_REFRESH_EXPIRY: int = 604800   # 7 天

    # 加密
    ENCRYPTION_KEY: str = "change-this-to-a-random-key"

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@finguard.local"

    # LLM
    LLM_DEFAULT_PROVIDER: str = "template"
    OLLAMA_HOST: str = "http://localhost:11434"

    # 應用
    APP_NAME: str = "FinGuard"
    APP_VERSION: str = "1.5.0"

    # 測試
    TESTING: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
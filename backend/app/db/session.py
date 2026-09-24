"""資料庫 session 管理。

- Sync engine：給 Alembic migration、同步腳本使用
- Async engine：給 FastAPI 請求使用
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# ==================== Sync（Alembic / 腳本用）====================

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Sync session。Alembic 或純同步腳本用。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== Async（FastAPI 用）====================

def _to_async_url(url: str) -> str:
    """把 sync URL 轉成 async URL。"""
    if url.startswith("postgresql+psycopg2://"):
        return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


async_engine = create_async_engine(
    _to_async_url(settings.DATABASE_URL),
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,   # 避免 commit 後物件失效
    class_=AsyncSession,
)


async def get_async_db():
    """Async session。FastAPI 依賴用。"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
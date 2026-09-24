"""pytest fixtures。"""
import pytest_asyncio
import fakeredis.aioredis
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.core.redis import get_redis
from app.db.base import Base
from app.db.session import get_async_db
from app.main import app


TEST_DB_URL = (
    "postgresql+asyncpg://finguard:dev_password_change_me@localhost:5432/finguard_test"
)

DEFAULT_TENANT_ID = "00000000-0000-0000-0000-000000000001"


def _make_engine():
    return create_async_engine(
        TEST_DB_URL, echo=False, future=True, poolclass=NullPool
    )


async def _seed(session: AsyncSession) -> None:
    """每個測試建表後，種入預設租戶 + 基因點位。"""
    from app.models.tenant import Tenant
    from app.models.health import GeneticMarker

    session.add(
        Tenant(
            id=DEFAULT_TENANT_ID,
            name="預設租戶",
            slug="default",
            plan="free",
            status="active",
            max_users=5,
            max_models=10,
        )
    )

    session.add_all([
        GeneticMarker(
            marker_code="BRCA1", marker_name="BRCA1 基因",
            related_diseases=["乳癌", "卵巢癌"],
            related_body_parts=["reproductive"],
            risk_level_high=3.0, display_order=1,
        ),
        GeneticMarker(
            marker_code="APOE", marker_name="APOE 基因",
            related_diseases=["阿茲海默症"],
            related_body_parts=["brain"],
            risk_level_high=2.5, display_order=2,
        ),
        GeneticMarker(
            marker_code="LDLR", marker_name="LDLR 基因",
            related_diseases=["家族性高膽固醇"],
            related_body_parts=["heart"],
            risk_level_high=2.0, display_order=3,
        ),
    ])
    await session.commit()


@pytest_asyncio.fixture
async def db():
    import app.models  # noqa: F401  確保所有模型被 import

    engine = _make_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with SessionLocal() as session:
        await _seed(session)
        yield session

    # 清空所有表
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())

    await engine.dispose()


@pytest_asyncio.fixture
async def fake_redis():
    r = fakeredis.aioredis.FakeRedis(decode_responses=True)
    try:
        yield r
    finally:
        await r.flushall()
        await r.aclose()


@pytest_asyncio.fixture
async def client(fake_redis, db):
    app.dependency_overrides[get_redis] = lambda: fake_redis
    app.dependency_overrides[get_async_db] = lambda: db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


import pytest


@pytest_asyncio.fixture
async def admin_user(db):
    """測試用管理員。"""
    from app.core.security import hash_password
    from app.models.user import AdminUser

    admin = AdminUser(
        email="admin@test.local",
        password_hash=hash_password("testpassword123"),
        display_name="Test Admin",
        role="admin",
        status="active",
    )
    db.add(admin)
    await db.commit()
    await db.refresh(admin)
    return admin

@pytest.fixture(autouse=True)
def _disable_smtp(monkeypatch):
    """測試時不寄真信（清空 SMTP 設定，EmailService 會自動跳過）。"""
    from app.core.config import settings
    monkeypatch.setattr(settings, "SMTP_USER", "")
    monkeypatch.setattr(settings, "SMTP_PASSWORD", "")


ADMIN_EMAIL = "admin@test.local"
ADMIN_PASSWORD = "testpassword123"
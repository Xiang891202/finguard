"""管理員認證 API。路徑 /api/v1/admin/auth/*"""
from fastapi import APIRouter, Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_admin_id
from app.core.exceptions import NotFound
from app.core.redis import get_redis
from app.core.responses import ok
from app.db.session import get_async_db
from app.schemas.admin_auth import (
    AdminLoginIn,
    AdminLogoutIn,
    AdminMeOut,
)
from app.services.admin_auth_service import AdminAuthService
from app.services.token_service import TokenService


router = APIRouter(prefix="/api/v1/admin/auth", tags=["admin-auth"])


def _client_ip(request: Request) -> str | None:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else None


def _user_agent(request: Request) -> str | None:
    return request.headers.get("user-agent")


@router.post("/login")
async def admin_login(
    payload: AdminLoginIn,
    request: Request,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_async_db),
):
    svc = AdminAuthService(redis, db)
    admin = await svc.login(payload.email, payload.password)

    token_svc = TokenService(redis, db)
    data = await token_svc.issue_for_admin(
        admin,
        user_agent=_user_agent(request),
        ip=_client_ip(request),
    )
    return ok(data)


@router.post("/logout")
async def admin_logout(
    payload: AdminLogoutIn,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_async_db),
):
    svc = TokenService(redis, db)
    await svc.revoke(payload.refresh_token)
    return ok({"message": "已登出"})


@router.get("/me")
async def admin_me(
    admin_id: str = Depends(get_current_admin_id),
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_async_db),
):
    svc = AdminAuthService(redis, db)
    admin = await svc.get_by_id(admin_id)
    if admin is None:
        raise NotFound("管理員不存在")
    return ok(AdminMeOut(
        id=admin.id,
        email=admin.email,
        display_name=admin.display_name,
        role=admin.role,
    ).model_dump())
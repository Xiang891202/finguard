"""Auth API 路由。對齊規劃書 v1.5 / API 規格 1.x。"""
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user_id
from app.core.redis import get_redis
from app.core.responses import ok
from app.core.exceptions import NotFound
from app.db.session import get_async_db
from app.models.user import User
from app.schemas.auth import (
    LogoutIn,
    MeData,
    OTPRequestIn,
    OTPVerifyIn,
    RefreshIn,
)
from app.services.otp_service import OTPService
from app.services.token_service import TokenService


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def _client_ip(request: Request) -> str | None:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else None


def _user_agent(request: Request) -> str | None:
    return request.headers.get("user-agent")


@router.post("/otp/request")
async def request_otp(
    payload: OTPRequestIn,
    request: Request,
    background_tasks: BackgroundTasks,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_async_db),
):
    svc = OTPService(redis, db)
    data, code = await svc.request_otp(payload.email, ip=_client_ip(request))

    # 背景寄信（async 函式，BackgroundTasks 會用 event loop 執行）
    from app.services.email_service import EmailService
    background_tasks.add_task(EmailService.send_otp, payload.email, code)

    return ok(data)


@router.post("/otp/verify")
async def verify_otp(
    payload: OTPVerifyIn,
    request: Request,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_async_db),
):
    otp_svc = OTPService(redis, db)
    await otp_svc.verify_otp(payload.email, payload.otp)

    token_svc = TokenService(redis, db)
    data = await token_svc.issue_for_email(
        payload.email,
        user_agent=_user_agent(request),
        ip=_client_ip(request),
    )
    return ok(data)


@router.post("/refresh")
async def refresh(
    payload: RefreshIn,
    request: Request,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_async_db),
):
    svc = TokenService(redis, db)
    data = await svc.refresh(
        payload.refresh_token,
        user_agent=_user_agent(request),
        ip=_client_ip(request),
    )
    return ok(data)


@router.post("/logout")
async def logout(
    payload: LogoutIn,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_async_db),
):
    svc = TokenService(redis, db)
    await svc.revoke(payload.refresh_token)
    return ok({"message": "已登出"})


@router.get("/me")
async def me(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise NotFound("用戶不存在")
    return ok(
        MeData(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
        ).model_dump()
    )
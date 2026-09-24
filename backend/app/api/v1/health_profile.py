"""健康檔案 API。前綴 /api/v1/app/health"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user_id
from app.core.exceptions import HealthProfileExists, HealthProfileNotFound
from app.core.responses import ok
from app.db.session import get_async_db
from app.schemas.health import (
    HealthProfileCreateIn,
    HealthProfileUpdateIn,
)
from app.services.health_profile_service import HealthProfileService


router = APIRouter(prefix="/api/v1/app/health", tags=["health-profile"])


@router.post("/profile")
async def create_profile(
    payload: HealthProfileCreateIn,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    svc = HealthProfileService(db)
    existing = await svc.get(user_id)
    if existing is not None:
        raise HealthProfileExists("健康檔案已存在，請改用 PUT 更新")

    profile = await svc.upsert(user_id, payload.model_dump())
    return ok(svc.serialize(profile, message="健康檔案已建立"))


@router.put("/profile")
async def update_profile(
    payload: HealthProfileUpdateIn,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    svc = HealthProfileService(db)
    existing = await svc.get(user_id)
    if existing is None:
        raise HealthProfileNotFound("健康檔案尚未建立，請先 POST")

    data = payload.model_dump(exclude_unset=True, exclude_none=True)
    profile = await svc.upsert(user_id, data)
    return ok(svc.serialize(profile, message="健康檔案已更新"))


@router.get("/profile")
async def get_profile(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    svc = HealthProfileService(db)
    profile = await svc.get(user_id)
    if profile is None:
        raise HealthProfileNotFound("健康檔案尚未建立")
    return ok(svc.serialize(profile))


@router.get("/completion")
async def get_completion(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    svc = HealthProfileService(db)
    profile = await svc.get(user_id)
    if profile is None:
        return ok({
            "completion_rate": 0.0,
            "missing_fields": ["profile"],
            "precision_level": "none",
        })

    rate, missing = svc.calculate_completion(
        profile.birth_date,
        profile.gender,
        profile.family_history,
        bool(profile.has_genetic_test),
    )
    return ok({
        "completion_rate": rate,
        "missing_fields": missing,
        "precision_level": svc.precision_level(rate),
    })
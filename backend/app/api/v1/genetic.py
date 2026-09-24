"""基因資料 API。前綴 /api/v1/app/health"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user_id
from app.core.responses import ok
from app.db.session import get_async_db
from app.schemas.health import ConsentIn, GeneticTestCreateIn
from app.services.genetic_service import GeneticService


router = APIRouter(prefix="/api/v1/app/health", tags=["health-genetic"])


@router.post("/consent")
async def set_consent(
    payload: ConsentIn,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    svc = GeneticService(db)
    profile = await svc.set_consent(user_id, payload.consent)
    return ok({
        "consent_genetic": bool(profile.consent_genetic),
        "consent_genetic_at": (
            profile.consent_genetic_at.isoformat()
            if profile.consent_genetic_at else None
        ),
    })


@router.get("/genetic-markers")
async def list_markers(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    svc = GeneticService(db)
    markers = await svc.list_markers()
    return ok([svc.serialize_marker(m) for m in markers])


@router.get("/genetic-tests")
async def list_tests(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    svc = GeneticService(db)
    rows = await svc.list_tests(user_id)
    return ok([svc.serialize_test(t, m) for t, m in rows])


@router.post("/genetic-tests")
async def add_test(
    payload: GeneticTestCreateIn,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    svc = GeneticService(db)
    test, marker = await svc.add_test(
        user_id, payload.marker_id, payload.result,
        payload.raw_data, payload.notes,
    )
    return ok(svc.serialize_test(test, marker))


@router.delete("/genetic-tests/{test_id}")
async def delete_test(
    test_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    svc = GeneticService(db)
    await svc.delete_test(user_id, test_id)
    return ok({"message": "已刪除"})
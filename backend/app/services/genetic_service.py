"""基因資料服務：同意、檢測結果、加密儲存、完成度連動。"""
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.encryption import encrypt
from app.core.exceptions import (
    HealthConsentRequired,
    HealthInvalidInput,
    HealthProfileNotFound,
    NotFound,
)
from app.models.health import GeneticMarker, UserGeneticTest, UserHealthProfile
from app.services.health_profile_service import HealthProfileService


def _naive_utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class GeneticService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ---------- 同意 ----------
    async def set_consent(self, user_id: str, consent: bool) -> UserHealthProfile:
        result = await self.db.execute(
            select(UserHealthProfile).where(UserHealthProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        if profile is None:
            raise HealthProfileNotFound("請先建立健康檔案")

        profile.consent_genetic = consent
        profile.consent_genetic_at = _naive_utcnow() if consent else None
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    # ---------- 點位清單 ----------
    async def list_markers(self) -> list[GeneticMarker]:
        result = await self.db.execute(
            select(GeneticMarker)
            .where(GeneticMarker.is_active.is_(True))
            .order_by(GeneticMarker.display_order)
        )
        return list(result.scalars().all())

    # ---------- 我的檢測 ----------
    async def list_tests(
        self, user_id: str
    ) -> list[tuple[UserGeneticTest, GeneticMarker]]:
        result = await self.db.execute(
            select(UserGeneticTest, GeneticMarker)
            .join(GeneticMarker, UserGeneticTest.marker_id == GeneticMarker.id)
            .where(UserGeneticTest.user_id == user_id)
            .order_by(UserGeneticTest.created_at.desc())
        )
        return list(result.all())

    async def add_test(
        self,
        user_id: str,
        marker_id: str,
        result: str,
        raw_data: str | None,
        notes: str | None,
    ) -> tuple[UserGeneticTest, GeneticMarker]:
        profile = await self._require_profile(user_id)
        if not profile.consent_genetic:
            raise HealthConsentRequired("請先同意基因資料處理條款")

        marker = await self.db.get(GeneticMarker, marker_id)
        if marker is None or not marker.is_active:
            raise NotFound("基因點位不存在或已停用")

        dup = await self.db.execute(
            select(UserGeneticTest).where(
                UserGeneticTest.user_id == user_id,
                UserGeneticTest.marker_id == marker_id,
            )
        )
        if dup.scalar_one_or_none() is not None:
            raise HealthInvalidInput("此基因點位已有檢測結果")

         # 風險等級計算
        risk: float | None = None
        high = float(marker.risk_level_high or 2.0)
        if result == "high":
            risk = high
        elif result == "medium":
            risk = round(high * 0.66, 2)
        elif result == "low":
            risk = 1.0

        test = UserGeneticTest(
            user_id=user_id,
            marker_id=marker_id,
            result=result,
            raw_data_encrypted=encrypt(raw_data) if raw_data else None,
            risk_level_computed=risk,
            notes=notes,
        )
        self.db.add(test)

        # 自動開啟 has_genetic_test + 完成度
        profile.has_genetic_test = True
        rate, _ = HealthProfileService.calculate_completion(
            profile.birth_date, profile.gender,
            profile.family_history, True,
        )
        profile.completion_rate = rate

        await self.db.commit()
        await self.db.refresh(test)
        return test, marker

    async def delete_test(self, user_id: str, test_id: str) -> None:
        result = await self.db.execute(
            select(UserGeneticTest).where(
                UserGeneticTest.id == test_id,
                UserGeneticTest.user_id == user_id,
            )
        )
        test = result.scalar_one_or_none()
        if test is None:
            raise NotFound("檢測紀錄不存在")

        await self.db.delete(test)
        await self.db.flush()

        # 若無其他檢測 → 關閉 has_genetic_test + 重算完成度
        still = await self.db.execute(
            select(UserGeneticTest).where(UserGeneticTest.user_id == user_id)
        )
        has_any = still.scalars().first() is not None

        profile = await self._require_profile(user_id)
        profile.has_genetic_test = has_any
        rate, _ = HealthProfileService.calculate_completion(
            profile.birth_date, profile.gender,
            profile.family_history, has_any,
        )
        profile.completion_rate = rate

        await self.db.commit()

    # ---------- helpers ----------
    async def _require_profile(self, user_id: str) -> UserHealthProfile:
        result = await self.db.execute(
            select(UserHealthProfile).where(UserHealthProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        if profile is None:
            raise HealthProfileNotFound("請先建立健康檔案")
        return profile

    # ---------- 序列化 ----------
    @staticmethod
    def serialize_marker(m: GeneticMarker) -> dict:
        return {
            "id": m.id,
            "marker_code": m.marker_code,
            "marker_name": m.marker_name,
            "related_diseases": m.related_diseases or [],
            "related_body_parts": m.related_body_parts or [],
        }

    @staticmethod
    def serialize_test(t: UserGeneticTest, m: GeneticMarker) -> dict:
        return {
            "id": t.id,
            "marker_id": t.marker_id,
            "marker_code": m.marker_code,
            "marker_name": m.marker_name,
            "result": t.result,
            "risk_level_computed": (
                float(t.risk_level_computed) if t.risk_level_computed is not None else None
            ),
            "has_raw_data": bool(t.raw_data_encrypted),
            "notes": t.notes,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        }
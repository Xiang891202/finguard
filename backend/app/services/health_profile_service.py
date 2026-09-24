"""健康檔案商業邏輯。完成度依規劃書 14.3：
    生日 40% + 性別 40% + 家族病史 10% + 基因檢測 10%
"""
from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.health import UserHealthProfile


def _naive_utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class HealthProfileService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ---------- 完成度計算 ----------
    @staticmethod
    def calculate_completion(
        birth_date: date | None,
        gender: str | None,
        family_history: dict | None,
        has_genetic_test: bool,
    ) -> tuple[float, list[str]]:
        score = 0.0
        missing: list[str] = []

        if birth_date:
            score += 40.0
        else:
            missing.append("birth_date")

        if gender:
            score += 40.0
        else:
            missing.append("gender")

        if family_history and len(family_history) > 0:
            score += 10.0
        else:
            missing.append("family_history")

        if has_genetic_test:
            score += 10.0

        return round(score, 2), missing

    @staticmethod
    def precision_level(rate: float) -> str:
        if rate >= 100:
            return "full"
        if rate >= 90:
            return "high"
        if rate >= 80:
            return "medium"
        if rate > 0:
            return "low"
        return "none"

    # ---------- CRUD ----------
    async def get(self, user_id: str) -> UserHealthProfile | None:
        result = await self.db.execute(
            select(UserHealthProfile).where(UserHealthProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def upsert(self, user_id: str, data: dict) -> UserHealthProfile:
        profile = await self.get(user_id)
        is_new = profile is None

        if is_new:
            profile = UserHealthProfile(user_id=user_id, **data)
            self.db.add(profile)
        else:
            for k, v in data.items():
                setattr(profile, k, v)

        # 處理 consent_genetic 時間戳
        consent = data.get("consent_genetic")
        if consent is True and not profile.consent_genetic_at:
            profile.consent_genetic_at = _naive_utcnow()
        elif consent is False:
            profile.consent_genetic_at = None

        # 重算完成度
        rate, _ = self.calculate_completion(
            profile.birth_date,
            profile.gender,
            profile.family_history,
            bool(profile.has_genetic_test),
        )
        profile.completion_rate = rate

        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    # ---------- 序列化 ----------
    @staticmethod
    def serialize(
        profile: UserHealthProfile, message: str | None = None
    ) -> dict:
        data = {
            "id": profile.id,
            "user_id": profile.user_id,
            "birth_date": profile.birth_date.isoformat() if profile.birth_date else None,
            "gender": profile.gender,
            "family_history": profile.family_history,
            "has_genetic_test": bool(profile.has_genetic_test),
            "consent_genetic": bool(profile.consent_genetic),
            "consent_genetic_at": (
                profile.consent_genetic_at.isoformat()
                if profile.consent_genetic_at
                else None
            ),
            "completion_rate": float(profile.completion_rate or 0),
            "created_at": profile.created_at.isoformat() if profile.created_at else None,
            "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
        }
        if message:
            data["message"] = message
        return data
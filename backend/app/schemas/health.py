"""健康檔案 schema。"""
from datetime import date
from typing import Any

from pydantic import BaseModel, Field, field_validator


VALID_GENDERS = {"male", "female", "other"}


def _validate_birth_date(v: date) -> date:
    today = date.today()
    if v > today:
        raise ValueError("生日不可為未來日期")
    if v.year < 1900:
        raise ValueError("生日年份過早")
    return v


def _validate_gender(v: str) -> str:
    v = v.strip().lower()
    if v not in VALID_GENDERS:
        raise ValueError(f"性別必須是 {sorted(VALID_GENDERS)}")
    return v


class HealthProfileCreateIn(BaseModel):
    birth_date: date
    gender: str = Field(..., min_length=1, max_length=10)
    family_history: dict[str, Any] | None = None
    has_genetic_test: bool = False
    consent_genetic: bool = False      # ← 新增

    _bd = field_validator("birth_date")(classmethod(lambda cls, v: _validate_birth_date(v)))
    _gd = field_validator("gender")(classmethod(lambda cls, v: _validate_gender(v)))


class HealthProfileUpdateIn(BaseModel):
    birth_date: date | None = None
    gender: str | None = None
    family_history: dict[str, Any] | None = None
    has_genetic_test: bool | None = None
    consent_genetic: bool | None = None    # ← 新增

    @field_validator("birth_date")
    @classmethod
    def _bd(cls, v: date | None) -> date | None:
        return _validate_birth_date(v) if v is not None else None

    @field_validator("gender")
    @classmethod
    def _gd(cls, v: str | None) -> str | None:
        return _validate_gender(v) if v is not None else None


class CompletionOut(BaseModel):
    completion_rate: float
    missing_fields: list[str]
    precision_level: str


# ===== Day 5: 基因 =====

class ConsentIn(BaseModel):
    consent: bool


class ConsentOut(BaseModel):
    consent_genetic: bool
    consent_genetic_at: str | None = None


class GeneticMarkerOut(BaseModel):
    id: str
    marker_code: str
    marker_name: str
    related_diseases: list[str]
    related_body_parts: list[str] = []


class GeneticTestCreateIn(BaseModel):
    marker_id: str = Field(..., min_length=1, max_length=36)
    result: str = Field(..., min_length=1, max_length=20)
    raw_data: str | None = None   # 明文；service 會加密
    notes: str | None = None

    @field_validator("result")
    @classmethod
    def _v_result(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in {"high", "medium", "low"}:
            raise ValueError("result 必須是 high / medium / low")
        return v


class GeneticTestOut(BaseModel):
    id: str
    marker_id: str
    marker_code: str
    marker_name: str
    result: str
    risk_level_computed: float | None = None
    has_raw_data: bool
    notes: str | None = None
    created_at: str | None = None
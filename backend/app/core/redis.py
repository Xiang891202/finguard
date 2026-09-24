"""非同步 Redis 連線池（singleton）。"""
from __future__ import annotations

import redis.asyncio as aioredis

from app.core.config import settings

_redis: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    """FastAPI Depends 用；回傳共用連線池。"""
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            health_check_interval=30,
        )
    return _redis


async def close_redis() -> None:
    """應用關閉時呼叫。"""
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None
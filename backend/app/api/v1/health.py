from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
import redis
from app.core.config import settings
from app.db.session import get_db

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """完整健康檢查"""
    result = {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "database": "unknown",
        "redis": "unknown"
    }

    # 檢查資料庫
    try:
        db.execute(text("SELECT 1"))
        result["database"] = "connected"
    except Exception as e:
        result["database"] = f"error: {str(e)}"
        result["status"] = "unhealthy"

    # 檢查 Redis
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        result["redis"] = "connected"
    except Exception as e:
        result["redis"] = f"error: {str(e)}"

    return result

@router.get("/health/ready")
async def readiness():
    """就緒檢查（K8s readiness）"""
    return {"status": "ready"}

@router.get("/health/live")
async def liveness():
    """存活檢查（K8s liveness）"""
    return {"status": "alive"}
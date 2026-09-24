from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import ApiException
from app.core.logging import setup_logging, logger
from app.core.redis import close_redis
from app.core.responses import fail
from app.api.v1 import health
from app.api.v1 import auth as auth_router
from app.api.v1 import admin_auth as admin_auth_router
from app.api.v1 import health_profile as health_profile_router
from app.api.v1 import genetic as genetic_router

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 例外處理器：全部包成 {success, error} =====
@app.exception_handler(ApiException)
async def api_exception_handler(request: Request, exc: ApiException):
    return JSONResponse(
        status_code=exc.status_code,
        content=fail(exc.code, exc.message, exc.details or None),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Pydantic 的 ctx 可能含 ValueError 物件，需清洗成可 JSON 序列化的型別
    cleaned = []
    for err in exc.errors():
        e = dict(err)
        if "ctx" in e and isinstance(e["ctx"], dict):
            e["ctx"] = {
                k: v if isinstance(v, (str, int, float, bool, type(None)))
                else str(v)
                for k, v in e["ctx"].items()
            }
        cleaned.append(e)

    return JSONResponse(
        status_code=422,
        content=fail("VALIDATION_ERROR", "請求格式錯誤", {"errors": cleaned}),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("未處理例外：%s", exc)
    return JSONResponse(
        status_code=500,
        content=fail("SYSTEM_SERVICE_UNAVAILABLE", "伺服器暫時無法處理請求"),
    )


# 路由
app.include_router(health.router, tags=["health"])
app.include_router(auth_router.router)
app.include_router(admin_auth_router.router)
app.include_router(health_profile_router.router)
app.include_router(genetic_router.router)


@app.on_event("startup")
async def startup():
    logger.info(f"[START] {settings.APP_NAME} v{settings.APP_VERSION} 啟動")
    logger.info(f"環境：{settings.ENV}")


@app.on_event("shutdown")
async def shutdown():
    logger.info("[STOP] 關閉中...")
    await close_redis()
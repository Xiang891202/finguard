from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.api.v1 import health

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(health.router, tags=["health"])

@app.on_event("startup")
async def startup():
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 啟動")
    logger.info(f"環境：{settings.ENV}")

@app.on_event("shutdown")
async def shutdown():
    logger.info("👋 關閉中...")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db
from routers import auth, mood, love, diary, voice, tarot, payment
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    init_db()
    print("🌙 TaroMeet API 启动成功!")
    yield
    # Shutdown
    print("👋 TaroMeet API 关闭")


app = FastAPI(
    title=settings.APP_NAME,
    description="TaroMeet - AI 情感陪伴助手 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(mood.router)
app.include_router(love.router)
app.include_router(diary.router)
app.include_router(voice.router)
app.include_router(tarot.router)
app.include_router(payment.router)


@app.get("/")
async def root():
    return {
        "message": "欢迎使用 TaroMeet API 🌙",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}

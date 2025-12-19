from pydantic_settings import BaseSettings
from functools import lru_cache
import os

# Supabase PostgreSQL connection - using session pooler
# From Supabase dashboard: aws-1-ap-south-1.pooler.supabase.com
SUPABASE_DB_URL = "postgresql://postgres.jxregeqaytbcwtrmlweg:55886767%2BaB@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"

class Settings(BaseSettings):
    APP_NAME: str = "TaroMeet API"
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "taromeet-super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    OLLAMA_BASE_URL: str = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = "qwen2:0.5b"
    
    # Database - Use Supabase by default, can override with env var
    DATABASE_URL: str = os.environ.get("DATABASE_URL", SUPABASE_DB_URL)
    
    # Free tier limits
    FREE_CHAT_LIMIT: int = 5
    FREE_VOICE_MINUTES: int = 2
    FREE_TAROT_LIMIT: int = 1
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()


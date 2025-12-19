from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "TaroMeet API"
    SECRET_KEY: str = "taromeet-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2:0.5b"
    DATABASE_URL: str = "sqlite:///./taromeet.db"
    
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

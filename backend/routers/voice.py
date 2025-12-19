from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models import User
from routers.auth import get_current_user, check_and_reset_daily_limits
from services.ollama_service import ollama_service
from config import settings

router = APIRouter(prefix="/voice", tags=["语音陪伴"])


class VoiceTextRequest(BaseModel):
    message: str


class VoiceResponse(BaseModel):
    response_text: str
    # audio_url: Optional[str] = None  # For future TTS integration


@router.post("/chat", response_model=VoiceResponse)
async def voice_chat(
    request: VoiceTextRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Text-based companion chat (voice transcription handled on frontend)"""
    check_and_reset_daily_limits(current_user, db)
    
    # Check usage limits for free users
    if not current_user.is_premium:
        if current_user.daily_chat_count >= settings.FREE_CHAT_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="今日免费次数已用完，请升级会员解锁更多次数"
            )
        current_user.daily_chat_count += 1
        db.commit()
    
    # Get AI response
    response_text = await ollama_service.voice_companion(request.message)
    
    return VoiceResponse(response_text=response_text)

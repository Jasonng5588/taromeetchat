from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import get_db
from models import User
from routers.auth import get_current_user, check_and_reset_daily_limits
from services.ollama_service import ollama_service
from config import settings

router = APIRouter(prefix="/love", tags=["恋爱教练"])


class LoveRequest(BaseModel):
    chat_content: str


class LoveResponse(BaseModel):
    analysis: str
    suggestions: List[str]
    tips: str
    affection_score: int


@router.post("/analyze", response_model=LoveResponse)
async def analyze_love_chat(
    request: LoveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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
    
    # Get AI analysis
    ai_result = await ollama_service.analyze_love_chat(request.chat_content)
    
    return LoveResponse(
        analysis=ai_result.get("analysis", ""),
        suggestions=ai_result.get("suggestions", []),
        tips=ai_result.get("tips", ""),
        affection_score=ai_result.get("affection_score", 50)
    )

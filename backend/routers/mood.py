from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List

from database import get_db
from models import User, MoodEntry
from routers.auth import get_current_user, check_and_reset_daily_limits
from services.ollama_service import ollama_service
from config import settings

router = APIRouter(prefix="/mood", tags=["心情分析"])


class MoodRequest(BaseModel):
    mood_text: str


class MoodResponse(BaseModel):
    id: int
    mood_text: str
    encouragement: str
    suggestion: str
    emoji: str
    mood_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/analyze", response_model=MoodResponse)
async def analyze_mood(
    request: MoodRequest,
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
    ai_result = await ollama_service.analyze_mood(request.mood_text)
    
    # Save to database
    mood_entry = MoodEntry(
        user_id=current_user.id,
        mood_text=request.mood_text,
        mood_score=ai_result.get("mood_score", 0),
        ai_response=ai_result.get("encouragement", ""),
        emoji=ai_result.get("emoji", "💖")
    )
    db.add(mood_entry)
    db.commit()
    db.refresh(mood_entry)
    
    return MoodResponse(
        id=mood_entry.id,
        mood_text=mood_entry.mood_text,
        encouragement=ai_result.get("encouragement", ""),
        suggestion=ai_result.get("suggestion", ""),
        emoji=ai_result.get("emoji", "💖"),
        mood_score=ai_result.get("mood_score", 0),
        created_at=mood_entry.created_at
    )


@router.get("/history", response_model=List[MoodResponse])
async def get_mood_history(
    limit: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Free users can only see 7 days
    if not current_user.is_premium:
        limit = min(limit, 7)
    
    entries = db.query(MoodEntry).filter(
        MoodEntry.user_id == current_user.id
    ).order_by(MoodEntry.created_at.desc()).limit(limit).all()
    
    return [
        MoodResponse(
            id=e.id,
            mood_text=e.mood_text,
            encouragement=e.ai_response or "",
            suggestion="",
            emoji=e.emoji or "💖",
            mood_score=e.mood_score or 0,
            created_at=e.created_at
        )
        for e in entries
    ]

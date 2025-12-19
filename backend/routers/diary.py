from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List

from database import get_db
from models import User, DiaryEntry
from routers.auth import get_current_user, check_and_reset_daily_limits
from services.ollama_service import ollama_service
from config import settings

router = APIRouter(prefix="/diary", tags=["自我反省日记"])


class DiaryRequest(BaseModel):
    content: str


class DiaryResponse(BaseModel):
    id: int
    content: str
    reflection: str
    growth_insight: str
    tomorrow_suggestion: str
    growth_score: int
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/reflect", response_model=DiaryResponse)
async def reflect_diary(
    request: DiaryRequest,
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
    ai_result = await ollama_service.reflect_diary(request.content)
    
    # Save to database
    diary_entry = DiaryEntry(
        user_id=current_user.id,
        content=request.content,
        ai_analysis=ai_result.get("reflection", ""),
        growth_score=ai_result.get("growth_score", 0)
    )
    db.add(diary_entry)
    db.commit()
    db.refresh(diary_entry)
    
    return DiaryResponse(
        id=diary_entry.id,
        content=diary_entry.content,
        reflection=ai_result.get("reflection", ""),
        growth_insight=ai_result.get("growth_insight", ""),
        tomorrow_suggestion=ai_result.get("tomorrow_suggestion", ""),
        growth_score=ai_result.get("growth_score", 70),
        created_at=diary_entry.created_at
    )


@router.get("/history", response_model=List[DiaryResponse])
async def get_diary_history(
    limit: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Free users can only see 7 days
    if not current_user.is_premium:
        limit = min(limit, 7)
    
    entries = db.query(DiaryEntry).filter(
        DiaryEntry.user_id == current_user.id
    ).order_by(DiaryEntry.created_at.desc()).limit(limit).all()
    
    return [
        DiaryResponse(
            id=e.id,
            content=e.content,
            reflection=e.ai_analysis or "",
            growth_insight="",
            tomorrow_suggestion="",
            growth_score=int(e.growth_score or 70),
            created_at=e.created_at
        )
        for e in entries
    ]

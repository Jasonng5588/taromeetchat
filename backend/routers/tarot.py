from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import json
import random

from database import get_db
from models import User, TarotReading
from routers.auth import get_current_user, check_and_reset_daily_limits
from services.ollama_service import ollama_service
from config import settings

router = APIRouter(prefix="/tarot", tags=["塔罗牌占卜"])

# Load tarot cards data
TAROT_CARDS = []
try:
    with open("data/tarot_cards.json", "r", encoding="utf-8") as f:
        TAROT_CARDS = json.load(f)
except:
    TAROT_CARDS = [
        {"name": "The Fool", "meaning": "新的开始"},
        {"name": "The Magician", "meaning": "创造力"},
        {"name": "The Lovers", "meaning": "爱情"},
        {"name": "The Star", "meaning": "希望"},
        {"name": "The Sun", "meaning": "成功"},
        {"name": "The World", "meaning": "圆满"},
    ]


class TarotRequest(BaseModel):
    question: Optional[str] = None
    num_cards: int = 3


class TarotCard(BaseModel):
    name: str
    meaning: str
    image: str


class TarotResponse(BaseModel):
    id: int
    question: Optional[str]
    cards: List[TarotCard]
    interpretation: str
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/draw", response_model=TarotResponse)
async def draw_tarot(
    request: TarotRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_and_reset_daily_limits(current_user, db)
    
    # Check usage limits for free users
    if not current_user.is_premium:
        if current_user.daily_tarot_count >= settings.FREE_TAROT_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="今日免费次数已用完，请升级会员解锁更多次数"
            )
        current_user.daily_tarot_count += 1
        db.commit()
    
    # Draw random cards
    num_cards = min(request.num_cards, 5)
    drawn_cards = random.sample(TAROT_CARDS, num_cards)
    
    card_names = [card["name"] for card in drawn_cards]
    
    # Get AI interpretation
    interpretation = await ollama_service.interpret_tarot(
        cards=card_names,
        question=request.question or ""
    )
    
    # Save to database
    reading = TarotReading(
        user_id=current_user.id,
        question=request.question,
        cards=json.dumps(card_names),
        interpretation=interpretation
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    
    return TarotResponse(
        id=reading.id,
        question=request.question,
        cards=[
            TarotCard(
                name=card["name"],
                meaning=card["meaning"],
                image=card.get("image", "default")
            )
            for card in drawn_cards
        ],
        interpretation=interpretation,
        created_at=reading.created_at
    )


@router.get("/history", response_model=List[TarotResponse])
async def get_tarot_history(
    limit: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_premium:
        limit = min(limit, 7)
    
    readings = db.query(TarotReading).filter(
        TarotReading.user_id == current_user.id
    ).order_by(TarotReading.created_at.desc()).limit(limit).all()
    
    result = []
    for r in readings:
        card_names = json.loads(r.cards) if r.cards else []
        cards = []
        for name in card_names:
            card_data = next((c for c in TAROT_CARDS if c["name"] == name), None)
            if card_data:
                cards.append(TarotCard(
                    name=card_data["name"],
                    meaning=card_data["meaning"],
                    image=card_data.get("image", "default")
                ))
        
        result.append(TarotResponse(
            id=r.id,
            question=r.question,
            cards=cards,
            interpretation=r.interpretation or "",
            created_at=r.created_at
        ))
    
    return result


@router.get("/cards")
async def get_all_cards():
    """Get all available tarot cards"""
    return TAROT_CARDS

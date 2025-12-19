from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_premium = Column(Boolean, default=False)
    premium_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Usage tracking
    daily_chat_count = Column(Integer, default=0)
    daily_voice_seconds = Column(Integer, default=0)
    daily_tarot_count = Column(Integer, default=0)
    last_usage_reset = Column(DateTime, default=datetime.utcnow)
    
    moods = relationship("MoodEntry", back_populates="user")
    diaries = relationship("DiaryEntry", back_populates="user")
    tarot_readings = relationship("TarotReading", back_populates="user")
    payments = relationship("PaymentReceipt", back_populates="user")


class MoodEntry(Base):
    __tablename__ = "mood_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mood_text = Column(Text, nullable=False)
    mood_score = Column(Float, nullable=True)  # -1 to 1
    ai_response = Column(Text, nullable=True)
    emoji = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="moods")


class DiaryEntry(Base):
    __tablename__ = "diary_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    ai_analysis = Column(Text, nullable=True)
    growth_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="diaries")


class TarotReading(Base):
    __tablename__ = "tarot_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question = Column(Text, nullable=True)
    cards = Column(String(255), nullable=False)  # JSON string of card names
    interpretation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="tarot_readings")


class PaymentReceipt(Base):
    __tablename__ = "payment_receipts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    receipt_image = Column(Text, nullable=True)  # Base64 partial reference
    status = Column(String(20), default="pending")  # pending, approved, rejected
    ai_analysis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="payments")


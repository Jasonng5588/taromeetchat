"""
Database configuration for Vercel serverless functions
Uses Supabase PostgreSQL
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Supabase PostgreSQL connection
DATABASE_URL = "postgresql://postgres.jxregeqaytbcwtrmlweg:55886767%2BaB@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User Model
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
    last_usage_reset = Column(DateTime, nullable=True)

# Payment Receipt Model
class PaymentReceipt(Base):
    __tablename__ = "payment_receipts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    receipt_image = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    ai_analysis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

# Initialize tables on import
try:
    init_db()
except Exception as e:
    print(f"DB init error: {e}")

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
import base64

from database import get_db
from models import User, PaymentReceipt
from routers.auth import get_current_user
from services.receipt_ai import verify_receipt_with_ai

router = APIRouter(prefix="/payment", tags=["支付"])

# Bank account details
BANK_DETAILS = {
    "bank": "Maybank",
    "account": "004058673007",
    "name": "Ng Jya Shen",
    "amount": 19.90
}


class BankDetailsResponse(BaseModel):
    bank: str
    account: str
    name: str
    amount: float


class VerifyReceiptResponse(BaseModel):
    success: bool
    message: str
    is_premium: bool
    verification_details: Optional[dict] = None


@router.get("/bank-details", response_model=BankDetailsResponse)
async def get_bank_details():
    """Get bank transfer details for payment"""
    return BankDetailsResponse(**BANK_DETAILS)


@router.post("/verify-receipt", response_model=VerifyReceiptResponse)
async def verify_receipt(
    receipt: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload receipt image for AI verification.
    AI will check: amount, account number, recipient name, status.
    Auto-upgrades to premium if all checks pass.
    """
    # Read image data
    image_data = await receipt.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    # AI verification
    verification_result = await verify_receipt_with_ai(
        image_base64=image_base64,
        expected_amount=BANK_DETAILS["amount"],
        expected_account=BANK_DETAILS["account"],
        expected_name=BANK_DETAILS["name"]
    )
    
    # Save payment record
    payment_record = PaymentReceipt(
        user_id=current_user.id,
        amount=BANK_DETAILS["amount"],
        receipt_image=image_base64[:500],  # Store partial for reference
        status="approved" if verification_result["verified"] else "rejected",
        ai_analysis=str(verification_result),
        created_at=datetime.utcnow()
    )
    db.add(payment_record)
    
    if verification_result["verified"]:
        # Upgrade user to premium
        current_user.is_premium = True
        current_user.premium_until = datetime.utcnow() + timedelta(days=30)
        db.commit()
        db.refresh(current_user)
        
        return VerifyReceiptResponse(
            success=True,
            message="验证成功！您已升级为 Premium 会员 🎉",
            is_premium=True,
            verification_details=verification_result
        )
    else:
        db.commit()
        return VerifyReceiptResponse(
            success=False,
            message=f"验证失败: {verification_result.get('reason', '收据信息不符')}",
            is_premium=False,
            verification_details=verification_result
        )


@router.get("/status")
async def get_payment_status(
    current_user: User = Depends(get_current_user)
):
    """Check user's premium status"""
    return {
        "is_premium": current_user.is_premium,
        "premium_until": current_user.premium_until.isoformat() if current_user.premium_until else None
    }

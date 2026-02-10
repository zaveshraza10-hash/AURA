from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db, Transaction, User
from models.fraud_detection import FraudDetector
import random

router = APIRouter()
fraud_detector = FraudDetector()

@router.post("/withdraw")
async def withdraw(user_id: str, amount: float, method: str = "face", db: Session = Depends(get_db)):
    # Check fraud
    fraud_check = fraud_detector.detect({
        "amount": amount,
        "transaction_count": random.randint(1, 10)
    })
    
    if fraud_check["is_fraud"]:
        raise HTTPException(status_code=403, detail="Transaction flagged as potential fraud")
    
    # Check balance
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    # Update balance
    user.balance -= amount
    
    # Record transaction
    transaction = Transaction(
        user_id=user_id,
        type="withdrawal",
        amount=amount,
        method=method
    )
    db.add(transaction)
    db.commit()
    
    return {
        "status": "success",
        "new_balance": user.balance,
        "fraud_check": fraud_check
    }

@router.post("/deposit")
async def deposit(user_id: str, amount: float, method: str = "qr", db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update balance
    user.balance += amount
    
    # Record transaction
    transaction = Transaction(
        user_id=user_id,
        type="deposit",
        amount=amount,
        method=method
    )
    db.add(transaction)
    db.commit()
    
    return {
        "status": "success",
        "new_balance": user.balance,
        "message": f"₹{amount} deposited successfully"
    }

@router.get("/balance/{user_id}")
async def get_balance(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user_id,
        "balance": user.balance,
        "credit_score": user.credit_score
    }
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import shutil
import os
from datetime import datetime

# Import our simple face auth
from models.face_recognition import face_auth
from utils.qr_generator import generate_qr_base64

app = FastAPI(title="AURA ATM API", version="1.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary directory for uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to AURA ATM API", "status": "active"}

@app.post("/auth/face-login")
async def face_login(file: UploadFile = File(...)):
    """Face login endpoint"""
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, f"face_{datetime.now().timestamp()}.jpg")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Verify face (mock)
        user_id = face_auth.verify_face(file_path)
        
        if user_id:
            user_info = face_auth.get_user_info(user_id)
            return {
                "status": "success",
                "user_id": user_id,
                "user_info": user_info,
                "message": "Face authentication successful"
            }
        else:
            return {
                "status": "error",
                "message": "Face not recognized"
            }
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/auth/qr/{user_id}")
async def get_qr_code(user_id: str):
    """Generate QR code for user"""
    try:
        qr_data = generate_qr_base64(user_id)
        return {
            "status": "success",
            "qr_code": qr_data,
            "message": "QR code generated"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/users/{user_id}/balance")
async def get_balance(user_id: str):
    """Get user balance"""
    user_info = face_auth.get_user_info(user_id)
    if user_info:
        return {
            "status": "success",
            "balance": user_info.get("balance", 0),
            "currency": "INR"
        }
    return {"status": "error", "message": "User not found"}

@app.post("/transactions/withdraw")
async def withdraw_amount(
    user_id: str = Form(...),
    amount: float = Form(...)
):
    """Withdraw money"""
    user_info = face_auth.get_user_info(user_id)
    if not user_info:
        return {"status": "error", "message": "User not found"}
    
    balance = user_info.get("balance", 0)
    if amount > balance:
        return {"status": "error", "message": "Insufficient balance"}
    
    # Mock transaction
    new_balance = balance - amount
    user_info["balance"] = new_balance
    
    return {
        "status": "success",
        "message": f"₹{amount} withdrawn successfully",
        "new_balance": new_balance,
        "transaction_id": f"TXN{datetime.now().timestamp()}"
    }

@app.post("/loan/check-eligibility")
async def check_loan_eligibility(
    user_id: str = Form(...),
    loan_amount: float = Form(50000),
    duration_months: int = Form(12)
):
    """Check loan eligibility"""
    user_info = face_auth.get_user_info(user_id)
    if not user_info:
        return {"status": "error", "message": "User not found"}
    
    # Mock AI loan prediction
    balance = user_info.get("balance", 0)
    
    # Simple eligibility logic
    eligible = balance > 10000
    probability = min(0.3 + (balance / 100000), 0.95)
    
    if eligible:
        interest_rate = 10.5 + (5 * (1 - probability))
        emi = loan_amount * (interest_rate/100/12) * (1 + (interest_rate/100/12))**duration_months
        emi = emi / ((1 + (interest_rate/100/12))**duration_months - 1)
        
        # Generate repayment schedule
        schedule = []
        remaining = loan_amount
        for month in range(1, duration_months + 1):
            interest = remaining * (interest_rate/100/12)
            principal = emi - interest
            remaining -= principal
            schedule.append({
                "month": month,
                "emi": round(emi, 2),
                "principal": round(principal, 2),
                "interest": round(interest, 2),
                "remaining": round(remaining, 2)
            })
        
        return {
            "status": "success",
            "eligible": True,
            "probability": round(probability, 2),
            "interest_rate": round(interest_rate, 2),
            "monthly_emi": round(emi, 2),
            "repayment_schedule": schedule,
            "message": "Congratulations! You are eligible for the loan."
        }
    else:
        return {
            "status": "success",
            "eligible": False,
            "probability": round(probability, 2),
            "message": "Currently not eligible. Try increasing your account balance."
        }

if __name__ == "__main__":
    print("Starting AURA ATM Server...")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
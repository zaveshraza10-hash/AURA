from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes import auth, transactions, loan

app = FastAPI(title="AURA ATM Backend", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(loan.router, prefix="/loan", tags=["Loan"])

@app.get("/")
def home():
    return {"message": "Welcome to AURA ATM API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
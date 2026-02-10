from fastapi import APIRouter
from models.loan_eligibility import LoanPredictor

router = APIRouter()
loan_predictor = LoanPredictor()

@router.post("/check-eligibility")
async def check_eligibility(data: dict):
    result = loan_predictor.predict(data)
    
    # Generate repayment schedule
    if result['eligible']:
        amount = result['suggested_limit']
        rate = result['interest_rate'] / 100 / 12
        months = 12
        emi = amount * rate * (1 + rate)**months / ((1 + rate)**months - 1)
        schedule = []
        balance = amount
        for month in range(1, months + 1):
            interest = balance * rate
            principal = emi - interest
            balance -= principal
            schedule.append({
                "month": month,
                "emi": round(emi, 2),
                "principal": round(principal, 2),
                "interest": round(interest, 2),
                "balance": round(balance, 2)
            })
        result['repayment_schedule'] = schedule
    
    return result
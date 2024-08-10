from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.utils.jwt import get_current_user
from app.finance_class import FinanceData
from datetime import datetime
from app.utils.models import User
from enum import Enum

router = APIRouter()



@router.get('/transactions')
async def get_transactions(
    start_date: str = '12-31-1969',
    end_date: str = '12-31-2099',
    exclude_income: bool = False,
    exclude_expenses: bool = False,
    current_user: User = Depends(get_current_user)
):
    transactions = FinanceData.get_transactions(
        start_date, end_date, user_id=current_user.id, exclude_income=exclude_income, exclude_expenses=exclude_expenses
    )
    return transactions
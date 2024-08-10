from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.utils.jwt import get_current_user
from app.finance_class import FinanceData
from datetime import datetime
from app.utils.models import User
from enum import Enum




router = APIRouter()


class Category(str, Enum):
    expense = 'Expense'
    income = 'Income'

@router.post('/add')
async def add_entry(
    date: str = datetime.now().strftime('%m-%d-%Y'),
    amount: float = None,
    category: Category = Category.expense,
    description: str = None,
    current_user: User = Depends(get_current_user)
):
    if not amount:
        raise HTTPException(status_code=400, detail="Amount is required.")
    FinanceData.add_entry(current_user.id, date, amount, category.value, description)
    return {"message": "Entry added successfully"}
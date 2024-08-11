from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.utils.jwt import get_current_user
from sqlalchemy.orm import Session
from app.finance_class import FinanceData
from datetime import datetime
from app.utils.models import Finance
from app.utils.models import User
from enum import Enum
from app.utils.database import get_db




router = APIRouter()


class Category(str, Enum):
    expense = 'Expense'
    income = 'Income'


@router.post('/add')
def add_entry(
    date: str = datetime.now().strftime('%m-%d-%Y'),
    amount: float = None,
    category: Category = Category.expense,
    description: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not amount:
        raise HTTPException(status_code=400, detail="Amount is required.")
    
    try:
        finance_entry = Finance(
            user_id=current_user.id,
            date=datetime.strptime(date, '%m-%d-%Y'),
            amount=amount,
            category=category.value,
            description=description
        )
        db.add(finance_entry)
        db.commit()
        db.refresh(finance_entry)
        return {"message": "Entry added successfully", "id": finance_entry.user_id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while adding the entry")
from fastapi import HTTPException, Depends, APIRouter
from app.utils.jwt import get_current_user
from app.finance_class import FinanceData
from app.utils.models import User
from app.utils.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/transactions')
async def get_transactions(
    start_date: str = '12-31-1969',
    end_date: str = '12-31-2099',
    exclude_income: bool = False,
    exclude_expenses: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        transactions = FinanceData.get_transactions(
            db, start_date, end_date, user_id=current_user.id, exclude_income=exclude_income, exclude_expenses=exclude_expenses
        )
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

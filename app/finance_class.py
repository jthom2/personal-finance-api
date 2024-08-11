import os
from datetime import datetime
import pandas as pd
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.utils.models import Finance

DATABASE_URL = os.getenv('DATABASE_URL')

class FinanceData:
    TABLE_NAME = 'finance_data'
    DATE_FORMAT = '%m-%d-%Y'

    @classmethod
    def get_transactions(cls, db: Session, start_date: str, end_date: str, user_id: int, exclude_income: bool = False, exclude_expenses: bool = False):
        try:
            start_date_obj = datetime.strptime(start_date, cls.DATE_FORMAT).date()
            end_date_obj = datetime.strptime(end_date, cls.DATE_FORMAT).date()

            # Use the Finance model in the query
            query = db.query(Finance).filter(
                and_(
                    Finance.date >= start_date_obj,
                    Finance.date <= end_date_obj,
                    Finance.user_id == user_id
                )
            )

            # Apply additional filters based on the flags
            if exclude_income:
                query = query.filter(Finance.category != 'Income')
            if exclude_expenses:
                query = query.filter(Finance.category != 'Expense')

            # Execute the query and fetch the results
            results = query.all()

            # Convert the results to a DataFrame for easy manipulation
            df = pd.DataFrame([{
                'date': r.date,
                'amount': r.amount,
                'category': r.category,
                'description': r.description
            } for r in results])

            # Ensure the 'date' column is in the correct format
            df['date'] = pd.to_datetime(df['date'], format=cls.DATE_FORMAT)

            # Return the results as a list of dictionaries
            return df.to_dict(orient='records')
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))
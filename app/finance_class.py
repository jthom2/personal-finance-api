import os
import io
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import psycopg2
from psycopg2 import sql

DATABASE_URL = os.getenv('DATABASE_URL')

class FinanceData:
    TABLE_NAME = 'finance_data'
    DATE_FORMAT = '%m-%d-%Y'

    @classmethod
    def connect_db(cls):
        return psycopg2.connect(DATABASE_URL)

    @classmethod
    def add_entry(cls, user_id, date, amount, category, description):
        conn = cls.connect_db()
        cur = conn.cursor()
        try:
            cur.execute(
                sql.SQL("""
                    INSERT INTO finance_data (user_id, date, amount, category, description)
                    VALUES (%s, %s, %s, %s, %s)
                """),
                [user_id, date, amount, category, description]
            )
            conn.commit()
        finally:
            cur.close()
            conn.close()


    @classmethod
    def get_transactions(cls, start_date, end_date, user_id, exclude_income=False, exclude_expenses=False):
        conn = cls.connect_db()
        cur = conn.cursor()
        try:
            query = sql.SQL("""
                SELECT date, amount, category, description 
                FROM {table} 
                WHERE date >= %s AND date <= %s AND user_id = %s
            """)
            conditions = [start_date, end_date, user_id]

            if exclude_income:
                query += sql.SQL(" AND category != 'Income'")
            if exclude_expenses:
                query += sql.SQL(" AND category != 'Expense'")

            cur.execute(query.format(table=sql.Identifier(cls.TABLE_NAME)), conditions)
            rows = cur.fetchall()

            df = pd.DataFrame(rows, columns=['date', 'amount', 'category', 'description'])
            df['date'] = pd.to_datetime(df['date'], format=cls.DATE_FORMAT)

            return df.to_dict(orient='records')
        except Exception as e:
            print(f'Error: Unable to retrieve transactions from database: {e}')
        finally:
            cur.close()
            conn.close()
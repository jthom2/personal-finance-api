import os
import psycopg2

DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS finance_data (
            user_id INTEGER REFERENCES users(id),
            date DATE,
            amount NUMERIC,
            category TEXT,
            description TEXT
            )
    """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE,
            username TEXT UNIQUE,
            hashed_password TEXT
            )""")

conn.commit()


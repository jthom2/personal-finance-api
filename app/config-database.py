import os
import psycopg2
from sqlalchemy.orm import registry

mapper_registry = registry()
mapper_registry.configure()


DATABASE_URL = os.getenv('DATABASE_URL')


conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE,
            username TEXT UNIQUE,
            hashed_password TEXT
            )
    """)


cur.execute("""
            CREATE TABLE IF NOT EXISTS finance_data (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            date DATE,
            amount NUMERIC,
            category TEXT,
            description TEXT
            )
    """)

conn.commit()


cur.close()
conn.close()


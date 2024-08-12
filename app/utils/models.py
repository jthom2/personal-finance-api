from sqlalchemy import Column, String, Integer, Date, Numeric, Text, ForeignKey
from app.utils.database import Base



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Finance(Base):
    __tablename__ = 'finance_data'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    amount = Column(Numeric)
    category = Column(Text)
    description = Column(Text)


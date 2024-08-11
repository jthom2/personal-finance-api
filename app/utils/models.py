from sqlalchemy import Column, Integer, String, ForeignKey, Date
from app.utils.database import Base
from datetime import datetime, date



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# class Finance(Base):
#     __tablename__ = "finance_data"
#     user_id = Column(Integer, ForeignKey("users.id"))
#     date = Column(Date, default=datetime.today())
#     amount = Column(Integer)
#     category = Column(String)
#     description = Column(String)


from sqlalchemy import Column, Integer, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Finance(Base):
    __tablename__ = 'finance_data'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    amount = Column(Numeric)
    category = Column(Text)
    description = Column(Text)


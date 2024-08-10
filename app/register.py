import re
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from fastapi import Depends, APIRouter, HTTPException, status, Request
from app.utils.pwd import hash_password
from app.utils.models import User
from app.utils.database import get_db
from app.security.ip_validator import is_vpn_ip

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator("email")
    def validate_email(cls, v):
        if "+" in v:
            raise ValueError("Email addresses with aliases are not allowed")
        return v

    @validator("username")
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("Username must only contain alphanumeric characters")
        if len(v) < 3 or len(v) > 15:
            raise ValueError("Username must be between 3 and 15 characters long")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search("[a-zA-Z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search("[0-9]", v):
            raise ValueError("Password must contain at least one numeral")
        if len(v) > 100:
            raise ValueError("Password length is too long")
        return v


@router.post("/register")
def register(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    # Waiting for api key validation
    # user_ip = request.client.host
    # if is_vpn_ip(user_ip):
    #     raise HTTPException(status_code=400, detail="VPN usage is not allowed")
    try:
        existing_user = db.query(User).filter(User.username == user.username).first()
        existing_email = db.query(User).filter(User.email == user.email).first()

        if existing_user or existing_email:
            # Generic error message
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or Email already in use",
            )

        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"username": db_user.username}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

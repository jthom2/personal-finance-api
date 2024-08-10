from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter
from app.utils.database import get_db
from app.utils.models import User
from app.utils.jwt import create_access_token
from app.utils.pwd import verify_password
from pydantic import BaseModel, EmailStr, constr, validator

router = APIRouter()


from pydantic import constr

class LoginRequest(BaseModel):
    email: EmailStr 
    password: constr(strip_whitespace=True, min_length=1, max_length=100) # type: ignore

    @validator('email', pre=True)
    def normalize_email(cls, v):
        return v.strip().lower() if isinstance(v, str) else v


@router.post("/token")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == login_request.email).first()
    if not db_user or not verify_password(login_request.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

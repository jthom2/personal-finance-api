import os
import jwt
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from dotenv import load_dotenv
from app.utils.models import User
from app.utils.database import get_db


load_dotenv()

JWT_SECRET_KEY = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

bearer_scheme = HTTPBearer()


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, JWT_SECRET_KEY, algorithm='HS256')
    return encoded_jwt


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if credentials:
        return credentials.credentials
    else:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


def get_payload_sub(token: str = Depends(get_bearer_token)):
    """
    Get's the email from the token.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        return email
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


def get_current_user(
    db: Session = Depends(get_db), email: str = Depends(get_payload_sub)
):
    """
    Get's user's information from the database using the email from the token.
    """
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

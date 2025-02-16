# ALL dependices
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer           # OAuth2
from passlib.context import CryptContext
from jose import JWTError, jwt
# from pydantic import BaseModel
from dotenv import load_dotenv
import os
from .database import SessionLocal

load_dotenv()

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
oauth2_brearer_dependency = Annotated[str, Depends(oauth2_bearer)]

async def get_current_user(token: oauth2_brearer_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user credentials",
        # headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise credentials_exception

user_dependency = Annotated[dict, Depends(get_current_user)]
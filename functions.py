from db_connection import DbConnection
from sqlalchemy import select
from sqlite_database import User
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
import os
from models import TokenData
import logging
from typing import Optional


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username:str):
  Session = DbConnection().get_session()
  with Session:
    user = select(User).where(User.username==username)
  return Session.scalar(user)


def authenticate_user(username: str, password: str):
  user = get_user(username)
  if not user:
      return False
  if not verify_password(password, user.password):
      return False
  return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
      expire = datetime.now(timezone.utc) + expires_delta
  else:
      expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def get_token_from_request(request: Request) -> Optional[str]:
  token = request.headers.get("Authorization")
  if token and token.startswith("Bearer "):
      return token[7:]  
  return None


async def get_current_user(token: Annotated[Optional[str], Depends(get_token_from_request)]):
  if token:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except InvalidTokenError:
        return None
    user = get_user(username=token_data.username)
    if user is None:
        return None
    return user
  return None


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
  if current_user:
    if current_user.disabled:
      raise HTTPException(status_code=400, detail="Inactive user")
  return current_user


def validate_session(request: Request) -> bool:
  session_access_token = request.session.get("access_token")
  if not session_access_token:
    logging.info("No Authorization and access_token in session, redirecting to login")
    return False
  return session_access_token


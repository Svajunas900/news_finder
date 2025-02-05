from fastapi import FastAPI, Depends, HTTPException, status
from scraper import get_headlines
from models import News, User, Token
from sqlite_database import User as db_User
from datetime import datetime, timedelta
from functions import get_current_active_user, authenticate_user, create_access_token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm


ACCESS_TOKEN_EXPIRE_MINUTES = 30
app = FastAPI()


@app.get("/")
def home():
  return "Hello world"


@app.post("/news")
def news(news: News):
  headlines = get_headlines(news.number_of_news)
  return {"Headlines": headlines,
          "Date": datetime.now()}


@app.post("/token")
async def login_for_access_token(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
  user = authenticate_user(form_data.username, form_data.password)
  if not user:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Incorrect username or password",
          headers={"WWW-Authenticate": "Bearer"},
      )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
      data={"sub": user.username}, expires_delta=access_token_expires
  )
  return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[db_User, Depends(get_current_active_user)],
):
    return current_user
from fastapi import FastAPI, Depends, HTTPException, status, Request
from scraper import get_headlines
from models import News, User, Token
from sqlite_database import Logs, User as db_User
from datetime import datetime, timedelta
from functions import get_current_active_user, authenticate_user, create_access_token, get_current_user
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import requests
from db_connection import DbConnection


ACCESS_TOKEN_EXPIRE_MINUTES = 30
app = FastAPI()


@app.get("/")
def home(request: Request):
  login_data = {
    "username": "Svajunas",
    "password": "koncius"
  }
  login_response = requests.post("http://localhost:8000/token", data=login_data)
  token = login_response.json().get("access_token")
  client_ip = request.client.host
  return {"token": token, 
          "ip_adress": client_ip}


@app.post("/news")
def news(news: News):
  headlines = get_headlines(news.number_of_news)
  return {"Headlines": headlines,
          "Date": datetime.now()}


@app.post("/token")
async def login_for_access_token(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
  db = DbConnection()
  Session = db.get_session()
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
  today = datetime.now()
  date = datetime(today.year, today.month, today.day)
  time = str(datetime.time(datetime.now()))
  with Session as session: 
    log = Logs(user_id=user.id, time=time, date=date)
    session.add(log)
    session.commit()
  return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[db_User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/protected")
def read_protected_data(current_user: Annotated[str, Depends(get_current_active_user)]):
    return {"message": f"Hello {current_user}, you are logged in and can access this protected route!"}

from fastapi import FastAPI, Depends, HTTPException, status, Request
from scraper import get_headlines
from models import News, User, Token
from sqlite_database import Logs, UserRequests, User as db_User
from datetime import datetime, timedelta
from functions import get_current_active_user, authenticate_user, create_access_token, get_current_user, validate_session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import requests
from db_connection import DbConnection
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os 
from fastapi.responses import RedirectResponse
import jwt
from request_validation import not_authenticated_request_check


load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
SUPER_SECRET_KEY = os.getenv("SUPER_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SUPER_SECRET_KEY)


@app.get("/")
def home(request: Request):
  login_data = {
    "username": "Svajunas",
    "password": "koncius"
  }
  login_response = requests.post("http://localhost:8000/token", data=login_data)
  token = login_response.json().get("access_token")
 
  request.session["access_token"] = token
  return RedirectResponse("protected")


@app.post("/news")
def news(
   news: News, 
   request: Request,
   logged_in: Annotated[bool, Depends(validate_session)]):
  # headlines = get_headlines(news.number_of_news)
  client_ip = request.client.host
  db = DbConnection()
  Session = db.get_session()
  today = datetime.now()
  date = datetime(today.year, today.month, today.day)
  time = str(datetime.time(datetime.now()))
  if logged_in:
    token = request.session["access_token"]
    payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    with Session as session:
      request = UserRequests(user_id=payload.user_id, request="Get_Headlines", time=time, date=date, ip_adress=client_ip, header_number=news.number_of_news)
      session.add(request)
      session.commit()
  else:
    if news.number_of_news > 5:
       return "You have to be authenticated"
    check = not_authenticated_request_check(client_ip, news.number_of_news)
    if check:
      with Session as session:
        request = UserRequests(user_id=1, request="Get_Headlines", time=time, date=date, ip_adress=client_ip, header_number=news.number_of_news)
        session.add(request)
        session.commit()
    else:
       return "Error"
    
  return {"Headlines": "headlines",
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
      data={"sub": user.username, "id": user.id}, expires_delta=access_token_expires
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
def read_protected_data(
   request: Request,
   logged_in: Annotated[str, Depends(validate_session)]
   ):
    if logged_in: 
      token = request.session["access_token"]
      payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
      return {"message": f"Hello {payload}, you are logged in and can access this protected route!"}
    else:
      return "None"


@app.get("/logout")
async def logout(request: Request, response: RedirectResponse):
    request.session.clear()
    response.delete_cookie(key="Authorization")
    return RedirectResponse('')

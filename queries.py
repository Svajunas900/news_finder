from sqlalchemy import select
from db_connection import DbConnection
from functions import get_password_hash
from sqlite_database import User, UserRequests

db = DbConnection()
Session = db.get_session()
with Session as session:
  user = User(id=2, username="Svajunas", password=get_password_hash("koncius"), disabled=False, payable=False)
  session.add(user)
  session.commit()


db = DbConnection()
Session = db.get_session()
with Session as session:
  users = select(UserRequests)
for user in Session.scalars(users):
  print(user.id, user.time, user.date, user.header_number, user.user_id)
# from sqlalchemy import select
# from db_connection import DbConnection
# from functions import get_password_hash
# from sqlite_database import User, Logs

# db = DbConnection()
# Session = db.get_session()
# with Session as session:
#   user = User(id=1, username="Svajunas", password=get_password_hash("koncius"), disabled=False)
#   session.add(user)
#   session.commit()


# db = DbConnection()
# Session = db.get_session()
# with Session as session:
#   users = select(Logs)
# for user in Session.scalars(users):
#   print(user.user_id, user.date, user.time)
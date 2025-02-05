# db = DbConnection()
# Session = db.get_session()
# with Session as session:
#   user = User(id=4, username="Titas", password=get_password_hash("koncius"), disabled=False)
#   session.add(user)
#   session.commit()


# db = DbConnection()
# Session = db.get_session()
# with Session as session:
#   users = select(User)
# for user in Session.scalars(users):
#   print(user.username, user.password)
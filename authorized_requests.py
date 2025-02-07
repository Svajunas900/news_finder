from sqlalchemy import select
from db_connection import DbConnection
from sqlite_database import User, UserRequests
from datetime import datetime, timedelta

def authenticated_request_check(user_id, header_number):
  db = DbConnection()
  Session = db.get_session()
  with Session as session:
    select_user = select(User).where(User.id==user_id)
  user = Session.scalar(select_user)
  if user.payable:
    return True
  else:
    print("Isn't payable")
    return check_requests(user.id, header_number)
      

def check_requests(user_id, header_number):
  db = DbConnection()
  Session = db.get_session()
  with Session as session:
    user_requests = select(UserRequests).where(UserRequests.user_id==user_id).order_by(UserRequests.date, UserRequests.time)
  headers = header_number
  today = datetime.today().date()
  user_request = Session.scalar(user_requests)
  if user_request:
    for request in Session.scalars(user_requests):
      request_date = request.date.date()
      if check_if_ten_days_passed(request):
        print("10 days passed")
        print("Your free trial has ended")
        return False
      if today == request_date:
        print("Same day")
        headers += request.header_number
        if headers >= 20:
          print("Over 20 headers today")
          return False
    print("Success Headers")
  else: 
    return True


def check_if_ten_days_passed(request):
  present_date = datetime.today()
 
  last_request_date = request.date
  last_request_date_plus_two = last_request_date + timedelta(days=10)

  if last_request_date_plus_two < present_date:
    print("Ten days pasted")
    return True
  else:
    print(f"You still have {last_request_date_plus_two - present_date} days until your free trial ends")
    return False
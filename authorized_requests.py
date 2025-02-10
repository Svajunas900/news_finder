from celery_folder.sqlite_database import User, UserRequests
from celery_folder.my_db_connection import DbConnection
from sqlalchemy import select, func
from datetime import datetime, timedelta

def authenticated_request_check(user_id, header_number):
  db = DbConnection()
  session = db.get_session()
  with session:
    select_user = select(User).where(User.id==user_id)
  user = session.scalar(select_user)
  if user.payable:
    return True
  else:
    print("Isn't payable")
    return check_requests(user.id, header_number)
      

def check_requests(user_id, header_number):
  db = DbConnection()
  session = db.get_session()
  today = datetime.today().date()
  with session:
    user_requests = select(UserRequests).where(UserRequests.user_id==user_id).order_by(UserRequests.date, UserRequests.time)
  with session:
    todays_requests = select(UserRequests).where(func.date(UserRequests.date)==today, UserRequests.user_id==user_id)
  headers = header_number
  user_request = session.scalar(user_requests)
  if user_request:
    for request in session.scalars(user_requests):
      if check_if_ten_days_passed(request):
        print("10 days passed")
        print("Your free trial has ended")
        return False
    print("Success Headers")
    for request in session.scalars(todays_requests):
      print("Same day")
      headers += request.header_number
      if headers > 20:
        print("Over 20 headers today")
        return False
  else: 
    return True
  print("Request Successfull")
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
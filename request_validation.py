from sqlite_database import UserRequests
from sqlalchemy import select
from db_connection import DbConnection
from datetime import timedelta, datetime, time, date


def not_authenticated_request_check(ip_adress, num_of_headers):
  db = DbConnection()
  Session = db.get_session()
  with Session as session:
    user_requests = select(UserRequests).where(ip_adress==ip_adress).order_by(UserRequests.date.desc(), UserRequests.time.desc())
  request = Session.scalars(user_requests).fetchmany(5)
  headers_count = num_of_headers
  for number in range(len(request)):
    user_request = request[number]
    passed = check_if_two_days_passed(user_request)
    if not passed:
      headers_count += user_request.header_number
      if headers_count >= 5:
        return False
      else:
        continue
    else:
      continue
  return True


def check_if_two_days_passed(request):
  present_date = datetime.today()
 
  last_request_date = request.date
  last_request_date_plus_two = last_request_date + timedelta(days=2)

  if last_request_date_plus_two < present_date:
    print("Two days pasted")
    return True
  else:
    print(f"You need to wait for {last_request_date_plus_two - present_date}")
    return False
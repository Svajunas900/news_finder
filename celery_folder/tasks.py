from celery_app import app
from selenium.webdriver import Chrome, Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from celery_folder.my_db_connection import DbConnection
from sqlalchemy import select, func, insert
from sqlite_database import NewsFlow
from datetime import datetime, time


def get_headlines():
  remote_url = "http://selenium_scraper:4444/wd/hub"
  options = Options()
  options.add_argument("--headless")
  options.add_argument("--disable-gpu") 
  options.add_argument("--no-sandbox")  
  driver = Remote(
    command_executor=remote_url,
    options=options
  ) 
  headline_list = []
  url = "https://edition.cnn.com/"

  driver.get(url)

  headlines = driver.find_elements(by=By.CLASS_NAME, value="container__headline-text")
  for num in range(len(headlines)):
    headline_list.append(headlines[num].text)
  
  driver.quit()
  return headline_list


@app.task
def compare_headlines():
  headlines = get_headlines()
  db = DbConnection()
  session = db.get_session()
  today = datetime.today().date()
  result = []
  with session:
    todays_headlines = select(NewsFlow).where(func.date(NewsFlow.date)==today)
  for headline in session.scalars(todays_headlines):
    result.append(headline.header_news)
  for headline in headlines:
    if headline not in result:
      with session:
        news = insert(NewsFlow).values(date=datetime.today(), time=str(datetime.now().time()), header_news=headline)
      session.execute(news)
      session.commit()
  return "Success"



from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def get_headlines(number_of_headlines):
  driver = Chrome()
  headline_list = []
  url = "https://edition.cnn.com/"

  driver.get(url)

  headlines = driver.find_elements(by=By.CLASS_NAME, value="container__headline-text")
  for num in range(number_of_headlines):
    headline_list.append(headlines[num].text)
  
  driver.quit()
  return headline_list


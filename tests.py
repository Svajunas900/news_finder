import requests
import pytest
import requests_mock
from dotenv import load_dotenv
import os


load_dotenv()

USERNAME_TESTING = os.getenv("USERNAME_TESTING")
PASSWORD_TESTING = os.getenv("PASSWORD_TESTING")


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m


def test_login_in(mock_requests):
  data = {"username": USERNAME_TESTING,
          "password": PASSWORD_TESTING}
  mock_requests.get('/', json=data)
  result = requests.get("thtp://localhost:8000/").text
  mocked_result = {"username": USERNAME_TESTING, "password": PASSWORD_TESTING}
  assert type(f"{mocked_result}") == type(result)




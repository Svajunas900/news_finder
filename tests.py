import requests
import pytest
import requests_mock


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m

def test_login_in(mock_requests):
  data = {"username": "Svajunas",
          "password": "koncius"}
  mock_requests.get(f'/', json=data)
  assert '{"username": "Svajunas", "password": "koncius"}' == requests.get("thtp://localhost:8000/").text




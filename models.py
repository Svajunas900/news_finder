from pydantic import BaseModel


class News(BaseModel):
  number_of_news: int


class User(BaseModel):
  username: str
  password: str 
  disabled: bool | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
from sqlalchemy import DateTime, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 
from datetime import datetime
from db_connection import DbConnection
from sqlalchemy import select


class Base(DeclarativeBase):
  pass


class NewsFlow(Base):
  __tablename__ = "news_flow"

  id: Mapped[int] = mapped_column(primary_key=True)
  date: Mapped[datetime] = mapped_column(DateTime())
  time: Mapped[str] = mapped_column(String())
  header_news: Mapped[str] = mapped_column(String(200))


class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(String())
  password: Mapped[str] = mapped_column(String())
  disabled: Mapped[bool] = mapped_column(Boolean())


DbConnection().create_all_models(Base)



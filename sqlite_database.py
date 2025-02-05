from sqlalchemy import DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 
from datetime import datetime
from db_connection import DbConnection


class Base(DeclarativeBase):
  pass


class NewsFlow(Base):
  __tablename__ = "news_flow"

  id: Mapped[int] = mapped_column(primary_key=True)
  date: Mapped[datetime] = mapped_column(DateTime())
  time: Mapped[str] = mapped_column(String())
  header_news: Mapped[str] = mapped_column(String(200))


class Logs(Base):
  __tablename__ = "user_loggin_logs"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  time: Mapped[str] = mapped_column(String())
  date: Mapped[datetime] = mapped_column(DateTime())



class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(String())
  password: Mapped[str] = mapped_column(String())
  disabled: Mapped[bool] = mapped_column(Boolean())
  payable: Mapped[bool] = mapped_column(Boolean())


class UserRequests(Base):
  __tablename__ = "user_requests"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  request: Mapped[str] = mapped_column(String())
  time: Mapped[str] = mapped_column(String())
  date: Mapped[datetime] = mapped_column(DateTime())
  ip_adress: Mapped[str] = mapped_column(String())

DbConnection().create_all_models(Base)



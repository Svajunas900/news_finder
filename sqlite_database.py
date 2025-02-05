from sqlalchemy import create_engine, DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 
from datetime import datetime


engine = create_engine("sqlite:///news_flow_db.db")


class Base(DeclarativeBase):
  pass


class NewsFlow(Base):
  __tablename__ = "news_flow"

  id: Mapped[int] = mapped_column(primary_key=True)
  date: Mapped[datetime] = mapped_column(DateTime())
  time: Mapped[str] = mapped_column(String())
  header_news: Mapped[str] = mapped_column(String(200))


Base.metadata.create_all(engine)


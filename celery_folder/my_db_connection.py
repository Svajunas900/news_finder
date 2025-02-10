from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine


class MetaConnection(type):
  _instance = {}
  
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instance:
      instance = super().__call__(*args, **kwargs)  
      cls._instance[cls] = instance
    return cls._instance[cls]


class DbConnection(metaclass=MetaConnection):
  def __init__(self):
    self._engine = create_engine("sqlite:///news_flow_db.db", echo=True)
    self._Session = sessionmaker(bind=self._engine)
    
  def get_session(self):
    return self._Session()

  def create_all_models(self, base):
    base.metadata.create_all(self._engine)


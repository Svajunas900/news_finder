class MetaConnection(type):
  _instance = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instance:
      instance = super().__call__(cls, *args, **kwargs)  
      cls._instance[cls] = instance
    return cls._instance[cls]


class DbConnection(MetaConnection):
  pass
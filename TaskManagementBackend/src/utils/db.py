from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from src.utils.settings import settings


#! configuration of db:

Base = declarative_base()

Engine = create_engine(url = settings.DB_CONNECTION )

LocalSession = sessionmaker( bind = Engine )

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()
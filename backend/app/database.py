from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.settings import SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

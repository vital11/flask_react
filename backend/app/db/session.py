from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import BaseConfig


engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

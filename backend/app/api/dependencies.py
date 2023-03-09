from flask_sqlalchemy import SQLAlchemy

from app.db.session import engine, SessionLocal


db = SQLAlchemy()

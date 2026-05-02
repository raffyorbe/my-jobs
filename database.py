import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL) # Connects to PostgreSQL, SQLite specific connect_args={"check_same_thread": False} was removed

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) # Talks to DB

Base = declarative_base() # Defines models (tables)
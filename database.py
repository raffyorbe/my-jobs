from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./jobs.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # Connects to SQLite

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) # Talks to DB

Base = declarative_base() # Defines models (tables)
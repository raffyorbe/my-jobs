from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://my_jobs_db_user:skC1huhCOVqzN4rfBxQT7WlRgJFGiF3Y@dpg-d77fr2s50q8c73cq3r1g-a.virginia-postgres.render.com/my_jobs_db"

engine = create_engine(DATABASE_URL) # Connects to PostgreSQL, SQLite specific connect_args={"check_same_thread": False} was removed

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) # Talks to DB

Base = declarative_base() # Defines models (tables)
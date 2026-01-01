from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import asyncio

Base = declarative_base()

# Database engine and session
engine = create_engine('sqlite:///app.db', echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# For async compatibility
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

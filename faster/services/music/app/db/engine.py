from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base, engine, SessionLocal

# Create database if it doesn't exist
def create_database():
    try:
        engine.connect()
        print("Database connected successfully")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def init_db():
    """Initialize the database with tables."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized with tables")

# Create the database if it doesn't exist
create_database()

# Initialize tables
init_db()

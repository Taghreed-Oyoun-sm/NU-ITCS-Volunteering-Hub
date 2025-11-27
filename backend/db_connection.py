from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./students.db"

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

DATABASE_URL = "sqlite:///./app.db"  # <-- This creates a local SQLite file called app.db

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

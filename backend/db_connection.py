# backend/db_connection.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables (optional, if you want)
from dotenv import load_dotenv
load_dotenv()

# ---------------------------
# DATABASE URL
# ---------------------------

# You can set DATABASE_URL in .env, otherwise fallback to local MySQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:Aw2p2df23_dz!io@localhost:3306/NU_Volunteering_Hub_DB"
)

# Detect if SSL is required
if "ssl=true" in DATABASE_URL.lower():
    # Remove ?ssl=true from URL
    DATABASE_URL = DATABASE_URL.replace("?ssl=true", "")
    connect_args = {"ssl": {}}  # default SSL
else:
    connect_args = {}

# ---------------------------
# ENGINE & SESSION
# ---------------------------
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args=connect_args  # empty dict for SSL if needed, {} works for local too
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------------
# BASE for models
# ---------------------------
Base = declarative_base()

# ---------------------------
# Dependency for FastAPI
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This file handles the database connection setup for our NU Volunteering Hub backend.
# We use SQLAlchemy to connect to a local MySQL database for now.
# SessionLocal will be used throughout the app to interact with the database.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# Connected database remotely
# DATABASE_URL = "mysql+pymysql://root:vwaXJwvZmgotPxHQeEOoDvqXuyCuZcyy@shortline.proxy.rlwy.net:18490/railway?ssl=true"

# DATABASE_URL = "mysql+pymysql://root:Aw2p2df23_dz!io@localhost:3306/nu_volunteering_hub"

DATABASE_URL = "sqlite+pysqlite:///:memory:"

# Create engine with pool_pre_ping to avoid stale connections
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a configured "SessionLocal" class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # This file handles the database connection setup for our NU Volunteering Hub backend.
# # We use SQLAlchemy to connect to a local MySQL database for now.
# # SessionLocal will be used throughout the app to interact with the database.

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# Base = declarative_base()

# # Connected database remotely
# # DATABASE_URL = "mysql+pymysql://root:vwaXJwvZmgotPxHQeEOoDvqXuyCuZcyy@shortline.proxy.rlwy.net:18490/railway?ssl=true"

# DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_j2mv56sRNJpCBTmRwBv@nuvolunteerinhub-d01fecf-nu-volunteering-hub-7144.e.aivencloud.com:19987/defaultdb?ssl_md5_config=true"


# # Create engine with pool_pre_ping to avoid stale connections
# engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# # Create a configured "SessionLocal" class for database sessions
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




# # If you get an "SSL connection error", update your engine line like this:
# # Add this dictionary to tell the driver to use SSL
# # engine = create_engine(
# #     DATABASE_URL, 
# #     connect_args={"ssl": {"ssl_mode": "REQUIRED"}}, 
# #     pool_pre_ping=True
# # )




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. REMOVE the ?ssl_md5_config=true from the string
DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_j2mv56sRNJpCBTmRwBv@nuvolunteerinhub-d01fecf-nu-volunteering-hub-7144.e.aivencloud.com:19987/defaultdb"

# 2. Pass SSL through connect_args instead
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ssl_mode": "REQUIRED"
        }
    },
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
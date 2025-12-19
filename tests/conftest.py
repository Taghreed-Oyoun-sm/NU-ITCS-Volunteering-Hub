import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db_connection import Base

@pytest.fixture(scope="function")
def db_session():
    """
    Creates a fresh in-memory SQLite database for every single test.
    This ensures that data from Test A never leaks into Test B.
    """
    # 1. Setup the engine (SQLite in-memory is perfect for CI/CD)
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    
    # 2. Create a session factory
    TestingSessionLocal = sessionmaker(bind=engine)
    
    # 3. Create the tables (Post, Comment, Student) based on your models
    Base.metadata.create_all(bind=engine)
    
    # 4. Give the session to the test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # 5. Cleanup after the test is done
        db.close()
        Base.metadata.drop_all(bind=engine)
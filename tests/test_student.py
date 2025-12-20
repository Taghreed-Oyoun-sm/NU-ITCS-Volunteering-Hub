import pytest
from sqlalchemy.orm import Session
from backend.students.db_operations import create_user, get_user_by_email
from backend.students.dtos import UserCreate, Track, Year
from backend.students.password_handling import verify_password

# 1. Test successful student registration
def test_create_user_success(db_session: Session):
    user_data = UserCreate(
        student_id=2021001,
        name="Ahmed Ali",
        email="ahmed@example.com",
        year=Year.Junior,
        track=Track.CS,
        cgpa=3.8,
        research_skills=True,
        strength_areas=["Python", "Data Science"],
        password="securepassword123"
    )
    
    db_user = create_user(db=db_session, user_in=user_data)

    assert db_user.email == "ahmed@example.com"
    # Verify strength_areas converted from list to comma-separated string
    assert db_user.strength_areas == "Python,Data Science"
    # Verify password was hashed and is not plain text
    assert db_user.hashed_password != "securepassword123"
    assert verify_password("securepassword123", db_user.hashed_password) is True

# 2. Test prevention of duplicate emails
def test_create_user_duplicate_email(db_session: Session):
    user_data = UserCreate(
        student_id=1, name="User1", email="duplicate@test.com", 
        year=Year.Freshman, track=Track.AI, cgpa=3.0, password="password"
    )
    # Create the first user
    create_user(db_session, user_data)
    
    # Attempt to create a second user with the same email
    with pytest.raises(ValueError) as excinfo:
        create_user(db_session, user_data)
    assert "Email already registered" in str(excinfo.value)

# 3. Test retrieving a user by email
def test_get_user_by_email(db_session: Session):
    email = "search@test.com"
    user_data = UserCreate(
        student_id=2, name="Search Test", email=email, 
        year=Year.Senior, track=Track.BMD, cgpa=3.5, password="password"
    )
    create_user(db_session, user_data)
    
    found_user = get_user_by_email(db_session, email)
    assert found_user is not None
    assert found_user.name == "Search Test"
import pytest
from sqlalchemy.orm import Session
from backend.students.db_operations import create_user, get_user_by_email
from backend.students.dtos import UserCreate, Track, Year
from backend.students.password_handling import verify_password

def test_create_user_full_flow(db_session: Session):
    # Matches UserCreate DTO and backend join logic
    user_data = UserCreate(
        student_id=2024001,
        name="Test Student",
        email="test@nu.edu.eg",
        year=Year.Junior,
        track=Track.CS,
        cgpa=3.5,
        password="securepassword123",
        strength_areas=["Python", "SQL"]
    )
    
    user = create_user(db_session, user_data)
    
    assert user.email == "test@nu.edu.eg"
    assert user.strength_areas == "Python,SQL" # Matches backend join logic
    assert verify_password("securepassword123", user.hashed_password)

def test_duplicate_email_error(db_session: Session):
    user_data = UserCreate(
        student_id=1, name="U1", email="same@nu.edu.eg", 
        year=Year.Freshman, track=Track.AI, cgpa=3.0, password="pass"
    )
    create_user(db_session, user_data)
    
    # Matches the 'raise ValueError' in your backend
    with pytest.raises(ValueError, match="Email already registered"):
        create_user(db_session, user_data)

def test_get_user_by_email(db_session: Session):
    # Verifies the retrieval logic
    user_data = UserCreate(
        student_id=2, name="U2", email="find@nu.edu.eg", 
        year=Year.Senior, track=Track.BMD, cgpa=3.2, password="pass"
    )
    create_user(db_session, user_data)
    
    found = get_user_by_email(db_session, "find@nu.edu.eg")
    assert found is not None
    assert found.name == "U2"
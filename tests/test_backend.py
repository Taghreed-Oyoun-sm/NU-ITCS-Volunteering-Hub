import pytest
from sqlalchemy.orm import Session
from backend.students.db_operations import create_user, get_user_by_email
from backend.students.dtos import UserCreate
from backend.students.student_model import Year, Track
from backend.posts.db_operations import create_post
from backend.posts.dtos import PostCreate

def test_create_and_get_student(db_session: Session):
    user_input = UserCreate(
        student_id=1,
        name="Alice",
        email="alice@example.com",
        password="password123",
        year=Year.Freshman, # Fix: Use Enum, not "First"
        track=Track.CS,
        role="student",
        cgpa=3.8,
        research_skills=True,
        jta_skills=False
    )
    create_user(db_session, user_input)
    user = get_user_by_email(db_session, "alice@example.com")
    assert user is not None
    assert user.name == "Alice"

def test_create_post_integration(db_session: Session):
    # Setup: Post needs a student to exist first
    user_input = UserCreate(
        student_id=2, name="Bob", email="bob@example.com", password="password123",
        year=Year.Sophomore, track=Track.AI, role="student", cgpa=3.5
    )
    create_user(db_session, user_input)
    
    post_data = PostCreate(title="Test Post", content="Post Content", tags=["tag1"])
    # Fix: Pass student_id as the 3rd argument as per your backend
    post = create_post(db_session, post_data, student_id=2)
    assert post.post_id is not None
import pytest
from sqlalchemy.orm import Session
from backend.students.db_operations import create_user, get_user_by_email
from backend.students.dtos import UserCreate
from backend.students.student_model import Student, Year, Track
from backend.posts.db_operations import create_post, create_comment
from backend.posts.dtos import PostCreate
from backend.reports.db_operations import report_target
from backend.reports.report_model import TargetType

def test_create_and_get_student(db_session: Session):
    user_input = UserCreate(
        student_id=1,
        name="Alice",
        email="alice@example.com",
        password="password123",
        year=Year.Freshman, # Changed from "First"
        track=Track.CS,      # Changed from "CS" (ensuring enum usage)
        role="student",
        cgpa=3.8,
        research_skills=True,
        jta_skills=False
    )
    create_user(db_session, user_input)
    user = get_user_by_email(db_session, "alice@example.com")
    assert user is not None
    assert user.name == "Alice"

def test_create_post(db_session: Session):
    # Create student first
    user_input = UserCreate(
        student_id=2,
        name="Bob",
        email="bob@example.com",
        password="password123",
        year=Year.Sophomore, # Changed from "Second"
        track=Track.AI,       # Changed from "IT"
        role="student",
        cgpa=3.5,
        research_skills=False,
        jta_skills=True
    )
    create_user(db_session, user_input)
    
    post_data = PostCreate(title="Test Post", content="Post Content", tags=["tag1"])
    post = create_post(db_session, post_data, student_id=2)
    assert post.post_id is not None
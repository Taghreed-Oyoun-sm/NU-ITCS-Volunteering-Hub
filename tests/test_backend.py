# tests/test_backend.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.students.db_operations import create_user
from backend.students.student_model import Base as StudentBase
from backend.posts.db_operations import create_post, create_comment
from backend.posts.post_model import Base as PostBase
from backend.students.dtos import UserCreate
from backend.posts.dtos import PostCreate, CommentCreate
from backend.reports.db_operations import report_target
from backend.reports.report_model import TargetType

# -------------------- FIXTURE -------------------- #
@pytest.fixture(scope="function")
def db_session():
    # Create an SQLite DB for testing
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    TestingSessionLocal = sessionmaker(bind=engine)
    
    # Create all tables
    StudentBase.metadata.create_all(bind=engine)
    PostBase.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# -------------------- STUDENT TESTS -------------------- #
def test_create_and_get_student(db_session: Session):
    user_input = UserCreate(
        student_id=1,
        name="Alice",
        email="alice@nu.edu.eg",
        password="password123",
        year="Freshman",
        track="CS",
        role="student",
        cgpa=3.8,
        research_skills=True,
        jta_skills=False
    )
    student = create_user(db_session, user_input)
    assert student.name == "Alice"
    assert student.email == "alice@nu.edu.eg"

# -------------------- POST TESTS -------------------- #
def test_create_post(db_session: Session):
    # First create a student
    user_input = UserCreate(
        student_id=2,
        name="Bob",
        email="bob@nu.edu.eg",
        password="password123",
        year="Sophomore",
        track="AI",
        role="student",
        cgpa=3.5,
        research_skills=False,
        jta_skills=True
    )
    student = create_user(db_session, user_input)

    post_input = PostCreate(student_id=student.student_id, title="Hello World", content="This is my first post")
    post = create_post(db_session, post_input)
    assert post.content == "This is my first post"
    assert post.student_id == student.student_id

# -------------------- COMMENT TESTS -------------------- #
def test_create_comment(db_session: Session):
    # Create a student and post first
    user_input = UserCreate(
        student_id=3,
        name="Charlie",
        email="charlie@example.com",
        password="password123",
        year="Third",
        track="IS",
        role="student",
        cgpa=3.6,
        research_skills=True,
        jta_skills=True
    )
    student = create_user(db_session, user_input)
    post_input = PostCreate(student_id=student.student_id, title="Post for comment", content="Content here")
    post = create_post(db_session, post_input)

    comment_input = CommentCreate(
        student_id=student.student_id,
        post_id=post.id,
        parent_id=None,
        content="This is a comment"
    )
    comment = create_comment(db_session, comment_input)
    assert comment.content == "This is a comment"
    assert comment.post_id == post.id

# -------------------- REPORT TESTS -------------------- #
def test_report_post_and_comment(db_session: Session):
    # Create student, post, and comment
    user_input = UserCreate(
        student_id=4,
        name="David",
        email="david@example.com",
        password="password123",
        year="Fourth",
        track="IT",
        role="student",
        cgpa=3.7,
        research_skills=False,
        jta_skills=True
    )
    student = create_user(db_session, user_input)

    post_input = PostCreate(student_id=student.student_id, title="Reportable post", content="Some content")
    post = create_post(db_session, post_input)

    comment_input = CommentCreate(
        student_id=student.student_id,
        post_id=post.id,
        parent_id=None,
        content="Reportable comment"
    )
    comment = create_comment(db_session, comment_input)

    # Report post
    result_post = report_target(db_session, reporter_id=student.student_id,
                                target_id=post.id, target_type=TargetType.Post)
    assert result_post["status"] in ["reported", "deleted", "already_reported"]

    # Report comment
    result_comment = report_target(db_session, reporter_id=student.student_id,
                                   target_id=comment.id, target_type=TargetType.Comment)
    assert result_comment["status"] in ["reported", "deleted", "already_reported"]

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import backend operations
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
    
    # Create all tables required for the tests
    StudentBase.metadata.create_all(bind=engine)
    PostBase.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# -------------------- STUDENT TESTS -------------------- #
def test_create_and_get_student(db_session: Session):
    # FIX: Use strings directly to avoid the ImportError
    user_input = UserCreate(
        student_id=1,
        name="Alice",
        email="alice@nu.edu.eg",
        password="password123",
        year="Freshman",  # Standard string value
        track="CS",        # Standard string value
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
    # 1. Setup: Create the student first
    user_input = UserCreate(
        student_id=2, name="Bob", email="bob@nu.edu.eg", password="password123",
        year="Sophomore", track="AI", role="student", cgpa=3.5
    )
    student = create_user(db_session, user_input)

    # 2. Act: Create the post
    post_input = PostCreate(title="Hello World", content="This is my first post", tags=["General"])
    
    # FIX: In your backend, student_id is a separate argument
    post = create_post(db_session, post_input, student_id=student.student_id)
    
    assert post.content == "This is my first post"
    assert post.student_id == student.student_id

# -------------------- COMMENT TESTS -------------------- #
def test_create_comment(db_session: Session):
    # 1. Setup
    user_input = UserCreate(
        student_id=3, name="Charlie", email="c@example.com", password="p123",
        year="Sophomore", track="AI", role="student", cgpa=3.6
    )
    student = create_user(db_session, user_input)
    post_data = PostCreate(title="Post", content="Content", tags=["Discussion"])
    post = create_post(db_session, post_data, student_id=student.student_id)

    # 2. Act: Create a comment
    # FIX: Matches the exact backend signature
    comment = create_comment(
        db=db_session,
        content="This is a comment",
        student_id=student.student_id,
        post_id=post.post_id
    )
    
    assert comment.content == "This is a comment"
    assert comment.post_id == post.post_id

# -------------------- REPORT TESTS -------------------- #
def test_report_post_and_comment(db_session: Session):
    # 1. Setup
    user_input = UserCreate(
        student_id=4, name="David", email="d@example.com", password="p123",
        year="Freshman", track="CS", role="student", cgpa=3.7
    )
    student = create_user(db_session, user_input)
    post_data = PostCreate(title="Reportable", content="Content", tags=["Alert"])
    post = create_post(db_session, post_data, student_id=student.student_id)

    # 2. Act: Report
    # FIX: Uses Student_Question to match backend target types
    result = report_target(
        db=db_session, 
        reporter_id=student.student_id,
        target_id=post.post_id, 
        target_type=TargetType.Student_Question
    )
    
    assert result["status"] in ["reported", "deleted", "already_reported"]
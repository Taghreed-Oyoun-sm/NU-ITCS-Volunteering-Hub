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
    # Use string values for year and track to match backend expectations
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
    # 1. Setup: Post creation depends on an existing student
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

    # 2. Act: Create the post using the student_id
    post_input = PostCreate(title="Hello World", content="This is my first post", tags=["General"])
    
    # In your backend, student_id is passed as a separate argument to create_post
    post = create_post(db_session, post_input, student_id=student.student_id)
    
    assert post.content == "This is my first post"
    assert post.student_id == student.student_id

# -------------------- COMMENT TESTS -------------------- #
def test_create_comment(db_session: Session):
    # 1. Setup: Create student and post first
    user_input = UserCreate(
        student_id=3,
        name="Charlie",
        email="charlie@example.com",
        password="password123",
        year="Sophomore",
        track="AI",
        role="student",
        cgpa=3.6
    )
    student = create_user(db_session, user_input)
    post_input = PostCreate(title="Post for comment", content="Content here", tags=["Discussion"])
    post = create_post(db_session, post_input, student_id=student.student_id)

    # 2. Act: Create a comment
    # Use the specific field names expected by your create_comment function
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
    # 1. Setup: Create student and post
    user_input = UserCreate(
        student_id=4,
        name="David",
        email="david@example.com",
        password="password123",
        year="Freshman",
        track="CS",
        role="student",
        cgpa=3.7
    )
    student = create_user(db_session, user_input)
    post_input = PostCreate(title="Reportable post", content="Some content", tags=["Alert"])
    post = create_post(db_session, post_input, student_id=student.student_id)

    # 2. Act: Report the post
    result_post = report_target(
        db=db_session, 
        reporter_id=student.student_id,
        target_id=post.post_id, 
        target_type=TargetType.Student_Question
    )
    
    assert result_post["status"] in ["reported", "deleted", "already_reported"]